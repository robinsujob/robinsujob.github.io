#!/usr/bin/env python3
"""Import AWS Workshop Studio repositories into the Hugo workshop section."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import unicodedata
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

SOURCE_ROOT = Path('/data/openclaw/AWS/workshop/workshops')
REPO_ROOT = Path('/data/code/hugo-stack-site')
CONTENT_ROOT = REPO_ROOT / 'content/aws-workshops'
STATIC_ROOT = REPO_ROOT / 'static/aws-workshops'

WORKSHOPS = [
    {
        'source': 'wordpress-glb',
        'slug': 'wordpress-glb',
        'home_order': 1,
        'home_title': '在两层架构中部署 WordPress和RDS',
        'short': 'WordPress + Amazon RDS',
        'summary': '从零创建 VPC、EC2、弹性 IP 和 Amazon RDS for MySQL，部署 WordPress，并完成数据库安全加固及多可用区故障转移实验。',
    },
    {
        'source': 'single-ip-with-multi-instance',
        'slug': 'single-ip-with-multi-instance',
        'home_order': 9,
        'home_title': '电商运营 - 单IP多人运维环境部署',
        'short': '单 IP 多实例运维',
        'summary': '通过 CloudFormation、NAT Gateway 和 Systems Manager，为多台 Windows EC2 建立共享固定出口 IP 的安全运维环境。',
    },
    {
        'source': 'glbsaas-boost',
        'slug': 'glbsaas-boost',
        'home_order': 8,
        'home_title': 'SaaS Boost入门指南',
        'short': 'AWS SaaS Boost',
        'summary': '安装和配置 AWS SaaS Boost，构建示例容器应用，完成服务配置、租户入驻、访问验证与资源清理。',
    },
    {
        'source': 'glb-ue-pixel-g4dn',
        'slug': 'glb-ue-pixel-g4dn',
        'home_order': 7,
        'home_title': 'Unreal Engine虚幻引擎在G4dn上的容器化部署实践',
        'short': 'Unreal Engine on G4dn',
        'summary': '在 Windows 与 Linux EC2 G4dn 实例上安装 Unreal Engine，并通过容器、STUN/TURN 和 Pixel Streaming 部署实时应用。',
    },
    {
        'source': 'glb-sam-lwa',
        'slug': 'glb-sam-lwa',
        'home_order': 10,
        'home_title': 'Serverless应用开发与快速适配',
        'short': 'AWS SAM + Lambda Web Adapter',
        'summary': '从 AWS SAM CLI 入门到本地测试与部署，并将 Spring Boot、Flask 应用迁移到 AWS Lambda。',
    },
    {
        'source': 'glb-aigc-sagemaker-web',
        'slug': 'glb-aigc-sagemaker-web',
        'home_order': 5,
        'home_title': '端到端体验AIGC-从SageMaker到Web应用',
        'short': 'AIGC：SageMaker 到 Web',
        'summary': '使用 SageMaker Notebook 运行 Stable Diffusion，并在 Cloud9 构建可调用模型的 Flask Web 应用。',
    },
    {
        'source': 'glb-aigc-ami-workshop',
        'slug': 'glb-aigc-ami-workshop',
        'home_order': 6,
        'home_title': 'AIGC Stable Diffusion一键式方案',
        'short': 'Stable Diffusion + ControlNet',
        'summary': '通过 AWS Marketplace AMI 部署 Stable Diffusion，完成艺术二维码、OpenPose、艺术字和拜年图创作。',
    },
    {
        'source': 'glb-ai-solution-kit',
        'slug': 'glb-ai-solution-kit',
        'home_order': 2,
        'home_title': '动手训练营 - AI Solution Kit',
        'short': 'AWS AI Solution Kit',
        'summary': '部署 AI Solution Kit，并通过 API 体验多语种 OCR、自定义模板 OCR、物体识别和自然语言理解。',
    },
    {
        'source': 'amazon-eks-global',
        'slug': 'amazon-eks-global',
        'home_order': 3,
        'home_title': '动手训练营 – Amazon EKS',
        'short': 'Amazon EKS',
        'summary': '配置堡垒机与权限，部署 Amazon EKS 集群和托管节点组，并运行、扩展微服务应用。',
    },
]


def slugify(value: str) -> str:
    value = unicodedata.normalize('NFKC', value).strip().lower()
    value = re.sub(r'[\s._]+', '-', value)
    value = re.sub(r'[^\w\-\u4e00-\u9fff]+', '-', value)
    return re.sub(r'-+', '-', value).strip('-') or 'page'


def split_doc(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    match = re.match(r'^---\n(.*?)\n---\n?(.*)$', text, re.S)
    if not match:
        raise ValueError(f'Missing YAML front matter: {path}')
    raw, body = match.groups()
    title_match = re.search(r'^title\s*:\s*["\']?(.*?)["\']?\s*$', raw, re.M)
    weight_match = re.search(r'^weight\s*:\s*(-?\d+)', raw, re.M)
    return {
        'title': title_match.group(1) if title_match else path.stem,
        'weight': int(weight_match.group(1)) if weight_match else 9999,
    }, body.strip() + '\n'


def source_key(md: Path, content_dir: Path) -> PurePosixPath:
    rel = md.relative_to(content_dir)
    if rel.name.startswith('index.') or rel.name == 'index.md':
        return PurePosixPath(rel.parent.as_posix())
    return PurePosixPath(rel.with_suffix('').as_posix())


def target_key(key: PurePosixPath) -> PurePosixPath:
    if str(key) == '.':
        return PurePosixPath('.')
    return PurePosixPath(*(slugify(part) for part in key.parts))


def fuzzy_path(value: PurePosixPath) -> str:
    return '/'.join(re.sub(r'[^a-z0-9\u4e00-\u9fff]', '', part.lower()) for part in value.parts)


def parse_attrs(raw: str) -> dict[str, str]:
    return {key: value for key, value in re.findall(r'(\w+)\s*=\s*"([^"]*)"', raw or '')}


def shortcode_quote(value: str) -> str:
    return value.replace('\\', '\\\\').replace('"', '\\"')


def transform_directives(body: str) -> str:
    output: list[str] = []
    stack: list[tuple[int, str]] = []
    for line in body.splitlines():
        stripped = line.strip()
        alert_body = re.match(r'^::alert\[(.*)\](?:\{(.*)\})?$', stripped)
        alert_header = re.match(r'^::alert\{(.*)\}$', stripped)
        if alert_body:
            attrs = parse_attrs(alert_body.group(2) or '')
            title = attrs.get('header', '')
            kind = attrs.get('type', 'info')
            title_arg = f' title="{shortcode_quote(title)}"' if title else ''
            output.extend(['', f'{{{{% workshop-alert type="{kind}"{title_arg} %}}}}', alert_body.group(1), '{{% /workshop-alert %}}', ''])
            continue
        if alert_header:
            attrs = parse_attrs(alert_header.group(1))
            title = attrs.get('header', '')
            kind = attrs.get('type', 'info')
            output.extend(['', f'{{{{% workshop-alert type="{kind}" %}}}}', title, '{{% /workshop-alert %}}', ''])
            continue

        opening = re.match(r'^(?P<marks>:{3,})(?P<name>tabs|tab|expand)\{?(?P<attrs>.*)\}?$', stripped)
        if opening:
            marks = len(opening.group('marks'))
            name = opening.group('name')
            attrs = parse_attrs(opening.group('attrs'))
            if name == 'tabs':
                output.extend(['', '{{% workshop-tabs %}}', ''])
            elif name == 'tab':
                label = attrs.get('label', attrs.get('id', '选项'))
                output.extend(['', f'{{{{% workshop-tab title="{shortcode_quote(label)}" %}}}}', ''])
            else:
                title = attrs.get('header', '展开查看')
                is_open = str(attrs.get('defaultExpanded', 'false')).lower()
                output.extend(['', f'{{{{% workshop-expand title="{shortcode_quote(title)}" open="{is_open}" %}}}}', ''])
            stack.append((marks, name))
            continue

        closing = re.match(r'^(:{3,})$', stripped)
        if closing and stack:
            marks = len(closing.group(1))
            index = next((i for i in range(len(stack) - 1, -1, -1) if stack[i][0] == marks), len(stack) - 1)
            _, name = stack.pop(index)
            shortcode = {'tabs': 'workshop-tabs', 'tab': 'workshop-tab', 'expand': 'workshop-expand'}[name]
            output.extend(['', f'{{{{% /{shortcode} %}}}}', ''])
            continue
        output.append(line)
    while stack:
        _, name = stack.pop()
        shortcode = {'tabs': 'workshop-tabs', 'tab': 'workshop-tab', 'expand': 'workshop-expand'}[name]
        output.extend(['', f'{{{{% /{shortcode} %}}}}'])
    return '\n'.join(output).strip() + '\n'


def copy_static(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    for src in sorted(source.rglob('*')):
        rel = src.relative_to(source)
        if any(part.startswith('.') or part in {'__MACOSX'} for part in rel.parts):
            continue
        dst = target / rel
        if src.is_dir():
            dst.mkdir(parents=True, exist_ok=True)
        elif src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def import_workshop(config: dict[str, str], workshop_weight: int) -> dict[str, object]:
    source = SOURCE_ROOT / config['source']
    content_dir = source / 'content'
    static_dir = source / 'static'
    target_content = CONTENT_ROOT / config['slug']
    target_static = STATIC_ROOT / config['slug'] / 'assets'
    if not content_dir.is_dir() or not static_dir.is_dir():
        raise FileNotFoundError(source)

    if target_content.exists():
        shutil.rmtree(target_content)
    copy_static(static_dir, target_static)

    markdown = sorted(content_dir.rglob('*.md'))
    docs: dict[Path, dict[str, object]] = {}
    source_to_target: dict[PurePosixPath, PurePosixPath] = {}
    source_to_permalink: dict[PurePosixPath, str] = {}
    for md in markdown:
        meta, body = split_doc(md)
        key = source_key(md, content_dir)
        target = target_key(key)
        docs[md] = {'meta': meta, 'body': body, 'source_key': key, 'target_key': target}
        source_to_target[key] = target
        suffix = '' if str(target) == '.' else f'{target.as_posix()}/'
        source_to_permalink[key] = f'/aws-workshops/{config["slug"]}/{suffix}'

    fuzzy = {fuzzy_path(key): key for key in source_to_target}
    asset_files = [p for p in target_static.rglob('*') if p.is_file()]
    asset_exact = {p.relative_to(target_static).as_posix(): p for p in asset_files}
    asset_lower = {key.lower(): key for key in asset_exact}
    referenced_assets: set[str] = set()
    external_replacements: set[str] = set()

    def resolve_asset(raw_path: str, source_s3: bool = False) -> str:
        path = unquote(raw_path).lstrip('/')
        actual = path if path in asset_exact else asset_lower.get(path.lower())
        if not actual:
            stem_matches = [key for key in asset_exact if str(PurePosixPath(key).with_suffix('')) == str(PurePosixPath(path).with_suffix(''))]
            if len(stem_matches) == 1:
                actual = stem_matches[0]
        if actual:
            referenced_assets.add(actual)
            return f'/aws-workshops/{config["slug"]}/assets/{actual}'
        if source_s3 and path == '513.46_grid_64bit_aws_swl.exe':
            replacement = 'https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/install-nvidia-driver.html'
            external_replacements.add(replacement)
            return replacement
        raise FileNotFoundError(f'{config["slug"]}: missing referenced asset {raw_path}')

    def rewrite_asset_url(match: re.Match[str]) -> str:
        attrs = parse_attrs(match.group(1))
        return resolve_asset(attrs.get('path', ''), attrs.get('source') == 's3')

    def rewrite_static(match: re.Match[str]) -> str:
        raw = match.group('path')
        return resolve_asset(raw)

    def resolve_page_link(destination: str, current_md: Path) -> str:
        if destination.startswith(('http://', 'https://', 'mailto:', '#', 'tel:', 'javascript:')):
            return destination
        if destination.startswith('/aws-workshops/'):
            return destination
        path_and_query, sep, fragment = destination.partition('#')
        query = ''
        if '?' in path_and_query:
            path_only, query = path_and_query.split('?', 1)
            query = '?' + query
        else:
            path_only = path_and_query
        if not path_only:
            return destination
        if path_only.startswith('/'):
            candidate = PurePosixPath(path_only.lstrip('/'))
        else:
            current_key = source_key(current_md, content_dir)
            # Resolve from the page URL directory. A source task1.md becomes /task1/, so ../task2 targets its sibling.
            base = current_key
            candidate = PurePosixPath(base, path_only)
        parts: list[str] = []
        for part in candidate.parts:
            if part == '..' and parts:
                parts.pop()
            elif part not in {'.', ''}:
                parts.append(part)
        candidate = PurePosixPath(*parts)
        if candidate.suffix == '.md':
            candidate = candidate.with_suffix('')
        key = candidate if candidate in source_to_permalink else fuzzy.get(fuzzy_path(candidate))
        if not key:
            basename_matches = [item for item in source_to_permalink if fuzzy_path(PurePosixPath(item.name)) == fuzzy_path(PurePosixPath(candidate.name))]
            if len(basename_matches) == 1:
                key = basename_matches[0]
        if not key:
            return destination
        clean_fragment = fragment.rstrip('.')
        return source_to_permalink[key] + query + (f'#{clean_fragment}' if sep and clean_fragment else '')

    def rewrite_markdown_link(match: re.Match[str], current_md: Path) -> str:
        label, destination = match.group(1), match.group(2)
        return f'[{label}]({resolve_page_link(destination, current_md)})'

    siblings: dict[PurePosixPath, list[Path]] = {}
    for md, doc in docs.items():
        key = doc['target_key']
        parent = key.parent if str(key) != '.' else PurePosixPath('.')
        siblings.setdefault(parent, []).append(md)
    unique_weights: dict[Path, int] = {}
    for pages in siblings.values():
        for index, md in enumerate(sorted(pages, key=lambda p: (docs[p]['meta']['weight'], str(docs[p]['source_key']).lower()))):
            unique_weights[md] = index + 1

    warnings: list[str] = []
    for md, doc in docs.items():
        source_key_value: PurePosixPath = doc['source_key']
        target: PurePosixPath = doc['target_key']
        body: str = doc['body']
        body = re.sub(r':assetUrl\{([^}]*)\}', rewrite_asset_url, body)
        body = re.sub(r'(?P<prefix>(?:\.\./)+|/)static/(?P<path>[^\s)"<>]+)', rewrite_static, body)
        body = re.sub(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)', lambda m: rewrite_markdown_link(m, md), body)
        body = transform_directives(body)

        if str(target) == '.':
            output = target_content / '_index.md'
            # Root title must remain identical to source content/index.zh.md.
            title = str(doc['meta']['title'])
            weight = int(config['home_order'])
            extra = {
                'shortTitle': config['short'],
                'homeTitle': config['home_title'],
                'summary': config['summary'],
                'workshopRoot': True,
            }
        else:
            has_descendants = any(other != source_key_value and source_key_value in other.parents for other in source_to_target)
            output_dir = target_content.joinpath(*target.parts)
            output = output_dir / ('_index.md' if has_descendants else 'index.md')
            title = str(doc['meta']['title'])
            weight = unique_weights[md]
            extra = {}
        output.parent.mkdir(parents=True, exist_ok=True)
        front = ['---', f'title: {json.dumps(title, ensure_ascii=False)}', f'weight: {weight}', 'type: workshops']
        for key, value in extra.items():
            encoded = str(value).lower() if isinstance(value, bool) else json.dumps(value, ensure_ascii=False)
            front.append(f'{key}: {encoded}')
        front.extend(['---', ''])
        rendered = '\n'.join(front) + body
        temporary = output.with_name(f'.{output.name}.tmp')
        temporary.write_text(rendered, encoding='utf-8')
        temporary.replace(output)

    remaining_asset_vars = sum(path.read_text().count(':assetUrl') for path in target_content.rglob('*.md'))
    if remaining_asset_vars:
        raise RuntimeError(f'{config["slug"]}: unconverted assetUrl values: {remaining_asset_vars}')
    downloads = []
    for relative in sorted(referenced_assets):
        path = asset_exact[relative]
        data = path.read_bytes()
        site_path = f'/aws-workshops/{config["slug"]}/assets/{relative}'
        downloads.append({
            'url': site_path,
            'site_path': site_path,
            'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
        })
    return {
        'slug': config['slug'],
        'pages': len(markdown),
        'assets': len(asset_files),
        'bytes': sum(path.stat().st_size for path in asset_files),
        'downloads': downloads,
        'external_replacements': sorted(external_replacements),
        'warnings': warnings,
    }


def main() -> None:
    results = []
    for index, workshop in enumerate(WORKSHOPS, start=2):
        result = import_workshop(workshop, index)
        results.append(result)
        print(f"{result['slug']}: pages={result['pages']} assets={result['assets']} size={result['bytes']/1024/1024:.2f} MiB")
    manifest = {
        'generated_from': 'content/aws-workshops',
        'local_downloads': [item for result in results for item in result['downloads']],
        'external_replacements': sorted({item for result in results for item in result['external_replacements']}),
    }
    manifest_path = REPO_ROOT / 'scripts/workshop-downloads.json'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Imported {len(results)} workshops, {sum(r['pages'] for r in results)} pages, {sum(r['assets'] for r in results)} assets")
    print(f"Download manifest: {len(manifest['local_downloads'])} local files, {len(manifest['external_replacements'])} external replacements")


if __name__ == '__main__':
    main()
