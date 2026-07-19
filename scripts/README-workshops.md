# AWS Workshop import

This site keeps AWS Workshop Studio content under `/aws-workshops/` while leaving the Hugo Stack blog layout unchanged.

## Source and output

- Source repositories: `/data/openclaw/AWS/workshop/aws-workshops/<name>/`
- Hugo content: `content/aws-workshops/<slug>/`
- Public assets and downloads: `static/aws-workshops/<slug>/assets/`
- Shared layout/style: `layouts/aws-workshops/`, `layouts/partials/aws-workshops/`, `layouts/shortcodes/`, `static/aws-workshops/workshop.css`

## Re-import

Run on `openclaw-dev-node`:

```bash
cd /data/code/hugo-stack-site
python3 scripts/import_aws_workshops.py
hugo --destination /tmp/hugo-workshops-check \
  --baseURL https://robinsujob.github.io/ \
  --cleanDestinationDir --minify
```

The importer:

1. preserves section hierarchy and ordering;
2. converts `/static/...` paths to workshop-scoped assets;
3. converts Workshop Studio alerts, tabs, expandable blocks, and `:assetUrl` values;
4. fixes case-only asset path mismatches and a missing ZIP extension when a unique local match exists;
5. emits browser download links as root-relative `/aws-workshops/...` paths;
6. emits URLs inside `wget`, `curl`, and JSON code examples through the `workshop-asset-url` shortcode, so Hugo derives the domain from the active `baseURL`;
7. fails when a referenced local asset cannot be resolved.

## Portable asset URLs

Do not hard-code `robinsujob.github.io` in workshop content. Browser links use root-relative paths. Command-line and JSON examples use:

```text
{{< workshop-asset-url path="/aws-workshops/<slug>/assets/<file>" >}}
```

The shortcode expands to an absolute URL at build time, which keeps local preview, GitHub Pages, and a future custom domain consistent.

## Download verification

`scripts/workshop-downloads.json` records each generated local download URL, byte size, and SHA-256 checksum. All ZIP archives are tested with Python `zipfile`, and release verification should fetch every manifest URL from a local production build before publishing.

## Known external replacement

`glb-ue-pixel-g4dn` referenced the Workshop Studio-only object `513.46_grid_64bit_aws_swl.exe`, but that file is absent from the source repository. The imported page links to the official AWS NVIDIA driver installation documentation instead of publishing a broken URL.

## Publishing rule

Do not commit, push, or deploy these workshops unless Robin explicitly asks to submit or publish them.
