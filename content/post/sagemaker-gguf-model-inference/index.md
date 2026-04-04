---
slug: "sagemaker-gguf-model-inference"
title: "Deploy GGUF Models on Amazon SageMaker with llama.cpp"
date: 2025-02-12
description: "Step-by-step guide to deploying quantized GGUF models on SageMaker using llama.cpp."
image: images/architecture.jpg
categories:
  - AWS
  - AI/ML
tags:
  - sagemaker
  - gguf
  - llama.cpp
  - llm
---
With the rapid development of artificial intelligence, LLM models have demonstrated powerful capabilities in natural language processing, machine translation, and intelligent assistants. These models are typically developed using frameworks like PyTorch, with pre-trained results stored in specific binary formats such as PyTorch's .pt files. However, as model sizes continue to grow, traditional file formats face challenges in storage, transmission, and loading — large file sizes, slow loading speeds, and poor cross-platform compatibility.

To address these challenges, [GGUF](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md) (GPT-Generated Unified Format) was created. GGUF is a binary file format designed specifically for LLM models, proposed by Georgi Gerganov, the founder of the llama.cpp open-source project. It aims to improve the storage and exchange efficiency of large models through optimized data structures, compact binary encoding, and memory mapping. GGUF format is now widely used in deploying and sharing various large models, especially popular in open-source communities like Hugging Face.

Its core features enable developers to manage and use LLM models more efficiently while reducing resource consumption and improving performance. Through conversion tools, original model pre-training results can be easily converted to GGUF format for a more efficient experience.

In this article, you will learn how to deploy LLM models in GGUF file format using Amazon SageMaker AI real-time inference endpoints.

## Amazon SageMaker AI Model Deployment Options

[Amazon SageMaker AI](https://aws.amazon.com/cn/sagemaker-ai/) is a fully managed service that brings together a broad set of tools to enable high-performance, low-cost machine learning (ML) for any use case. With SageMaker AI, you can build, train, and deploy ML models at scale using notebooks, debuggers, profilers, pipelines, MLOps, and more. It supports built-in algorithms and pre-built Docker images for common ML frameworks (TensorFlow, PyTorch, ONNX, XGBoost), and provides specialized Deep Learning Containers (DLC), libraries, and tools for model parallelism and Large Model Inference (LMI).

If the pre-built Docker images don't meet your needs, you can build your own Docker container (BYOC – Bring Your Own Container) for inference. To be compatible with SageMaker AI, your container must:

- Have a web server listening on port 8080.
- Accept POST requests to /invocations and /ping endpoints. Requests must return within 60 seconds with a maximum size of 6 MB.

To deploy and run GGUF models in SageMaker AI, you need to build a custom Docker container. This approach integrates the llama.cpp project to run GGUF models for effective deployment and inference on the SageMaker AI platform.

## llama.cpp and GGUF

[llama.cpp](https://github.com/ggerganov/llama.cpp) is a C/C++ LLM inference project designed for local or cloud-based LLM inference with minimal setup and optimal performance across various hardware. Key advantages include:

- Pure C/C++ implementation with no dependencies
- First-class support for Apple silicon, optimized via ARM NEON, Accelerate, and Metal frameworks
- AVX, AVX2, AVX512, and AMX support for x86 architectures
- Multiple quantization options (from 5-bit to 8-bit) for faster inference and lower memory usage
- Multiple GPU backend support including NVIDIA (CUDA), AMD (HIP), and Moore Threads MTT (MUSA)
- CPU+GPU hybrid inference, enabling partial acceleration for models larger than VRAM capacity

To run in llama.cpp, models must be stored in GGUF format. You can run GGUF models through llama.cpp containers, leveraging its full capabilities. When running GGUF models in SageMaker, combining them with llama.cpp maximizes its efficient inference capabilities and multi-hardware architecture support.

## Hosting GGUF Models in SageMaker AI Using BYOC

The following section details how to combine GGUF with llama.cpp using Amazon SageMaker AI. We'll demonstrate how to build a dedicated GGUF Docker container for SageMaker AI and apply it to model inference.

Using the [Bring Your Own Container (BYOC)](https://docs.aws.amazon.com/sagemaker/latest/dg/adapt-inference-container.html) approach, Amazon SageMaker AI provides great flexibility. Regardless of programming language, runtime, framework, or dependencies, you can integrate virtually any model and code into the SageMaker AI ecosystem.

This article uses [Amazon SageMaker AI Notebook](https://aws.amazon.com/sagemaker-ai/notebooks/) to build and deploy the GGUF model runtime framework. The solution architecture is shown below.

![Solution Architecture](images/practice-running-gguf-format-model-inference-using-sagemaker-ai1.jpg)

The main steps are:

- From HuggingFace, download a GGUF model and upload it to S3. This blog uses Llama 3 8B GGUF as an example.
- Prepare the key BYOC files in the Notebook: Dockerfile, main.py, requirements.txt, serve, server.sh.
- Create a custom Docker image and push it to Amazon ECR.
- Create an Amazon SageMaker Model in the Notebook and deploy it to an inference endpoint.
- During endpoint startup, download the GGUF model from S3 to the specified location in the container.
- Test the endpoint by invoking inference with the SageMaker SDK.

### 1. Create Amazon SageMaker AI Notebook

You can create a SageMaker AI Notebook instance in the AWS console, selecting an appropriate instance type and storage. Note that disk space of 30GB or more is recommended, primarily for container building and model storage.

When selecting or creating an IAM role, ensure the role has permissions to push images to Amazon ECR.

If the permissions are missing, add the following inline policy:

![Notebook Creation](images/practice-running-gguf-format-model-inference-using-sagemaker-ai2.jpg)

![IAM Permissions](images/practice-running-gguf-format-model-inference-using-sagemaker-ai3.jpg)

```json
{
  "Effect": "Allow",
  "Action": [
    "ecr:CompleteLayerUpload",
    "ecr:UploadLayerPart",
    "ecr:InitiateLayerUpload",
    "ecr:BatchCheckLayerAvailability",
    "ecr:PutImage",
    "ecr:BatchGetImage"
  ],
  "Resource": "arn:aws:ecr:*:*:*"
}
```

### 2. Build BYOC Code

The complete code is available in the [aws-samples repository](https://github.com/aws-samples/deploy-gguf-model-to-sagemaker). This article covers key code explanations only.

To run GGUF models in SageMaker, prepare the code with the following file structure:

```
workspace
|-- Dockerfile
|-- main.py
|-- requirements.txt
|-- serve
|-- server.sh
```

The runtime trigger logic and HTTP requests are shown below.

![Runtime Logic](images/practice-running-gguf-format-model-inference-using-sagemaker-ai4.png)

#### 2.1 Dockerfile

The Dockerfile defines a container environment based on the llama.cpp CUDA version, designed specifically for running GGUF models on SageMaker.

```dockerfile
FROM ghcr.io/ggerganov/llama.cpp:full-cuda

ENV PYTHONUNBUFFERED=1
ENV MODELPATH=/app/llm_model.bin
ENV PATH=$PATH:/app
ENV BUCKET=""
ENV BUCKET_KEY=""

WORKDIR /app

RUN apt-get update && apt-get install -y \
    unzip \
    libcurl4-openssl-dev \
    python3 \
    python3-pip \
    python3-dev \
    git \
    psmisc \
    pciutils

COPY requirements.txt ./requirements.txt
COPY main.py /app/
COPY serve /app/
COPY server.sh /app/

RUN chmod u+x serve
RUN chmod u+x server.sh
RUN pip3 install -r requirements.txt
RUN export PATH=/app:$PATH

ENTRYPOINT ["/bin/bash"]
EXPOSE 8080
```

When building the Dockerfile, pay attention to these key environment variables:

- **MODELPATH**: Specifies the model filename used at startup.
- **BUCKET** and **BUCKET_KEY**: Define the Amazon S3 bucket name and object key for the model file.

#### 2.2 main.py

This file implements an HTTP API server for interacting with llama.cpp. Key modifications for SageMaker deployment include:

- Port configuration: main.py defaults to port 8080, connecting to llama.cpp on port 8081
- Route changes: /v1/completions changed to /invocations, added /ping health check
- Model loading: Added update_model function for automatic S3 model download

```python
def update_model(bucket, key):
    try:
        s3 = boto3.client('s3')
        s3.download_file(bucket, key, os.environ.get('MODELPATH'))
        subprocess.run(["/app/server.sh", os.environ.get('MODELPATH')])
        return True
    except Exception as e:
        print(str(traceback.format_exc()))
        return False

@app.route('/ping', methods=['GET'])
def ping():
    return Response(status=200)

@app.route("/invocations", methods=['POST'])
def completion():
    ...
    if (is_present(body, "configure")):
        res = update_model(body["configure"]["bucket"], body["configure"]["key"])
        return Response(status=200) if (res) else Response(status=500)
    ...
```

#### 2.3 SageMaker Inference Entry Point: serve File

SageMaker inference nodes execute `docker run image serve` by default when starting containers.

```bash
#!/bin/sh
echo "serve"
uvicorn 'main:asgi_app' --host 0.0.0.0 --port 8080 --workers 8
```

#### 2.4 llama.cpp Startup Script: server.sh

server.sh starts the llama.cpp service. See the [llama.cpp documentation](https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md) for available runtime parameters.

```bash
#!/bin/sh
echo "server.sh"
echo "args: $1"
echo "GPU Layer: $GPU_LAYERS"

if lspci | grep -i nvidia &> /dev/null; then
    echo "NVIDIA GPU is available."
    NGL="$GPU_LAYERS"
    CPU_PER_SLOT=1
else
    echo "No NVIDIA GPU found."
    NGL=0
    CPU_PER_SLOT=4
fi

killall llama-server
/app/llama-server -m "$1" -c 2048 -t $(nproc --all) \
    --host 0.0.0.0 --port 8081 -cb \
    -np $(($(nproc --all) / $CPU_PER_SLOT)) -ngl $NGL &
```

### 3. Model Deployment and Testing

During model deployment, specify the ECR image, instance type, and corresponding environment variables.

```python
container_uri = f"{ECR_REPOSITORY_URI}:{IMAGE_TAG}"
instance_type = "ml.g5.2xlarge"
endpoint_name = sagemaker.utils.name_from_base("llama-cpp-gguf-byoc")

model = sagemaker.Model(
    image_uri=container_uri,
    role=iam_role,
    name=endpoint_name,
    env={
        "MODELPATH": f"/app/{MODEL_NAME}",
        "BUCKET": S3_BUCKET_NAME,
        "BUCKET_KEY": MODEL_NAME,
        "GPU_LAYERS": "32",
    }
)

model.deploy(
    instance_type=instance_type,
    initial_instance_count=1,
    endpoint_name=endpoint_name,
)
```

During inference, you can pass parameters to get model output. Standard invocation:

```python
def invoke_sagemaker_endpoint(endpoint_name, llama_args):
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        Body=json.dumps(llama_args),
        ContentType='application/json',
    )
    response_body = json.loads(response['Body'].read().decode())
    return response_body

llama_args = {
    "prompt": "What are the most popular tourist attractions in Beijing?",
    "max_tokens": 512,
    "temperature": 3,
    "repeat_penalty": 10,
    "frequency_penalty": 1.1,
    "top_p": 1,
}
inference = invoke_sagemaker_endpoint(endpoint_name, llama_args)
print(inference['choices'][0]['text'])
```

Streaming output:

```python
def invoke_sagemaker_streaming_endpoint(endpoint_name, llama_args):
    response = sagemaker_runtime.invoke_endpoint_with_response_stream(
        EndpointName=endpoint_name,
        Body=json.dumps(llama_args),
        ContentType='application/json',
    )
    event_stream = response['Body']
    for line in event_stream:
        itm = line['PayloadPart']['Bytes'][6:]
        try:
            res = json.loads(itm, strict=False)
            print(res["choices"][0]["text"], end='')
        except:
            pass

llama_args = {
    "prompt": "What are the most popular tourist attractions in Beijing?",
    "max_tokens": 512,
    "temperature": 3,
    "repeat_penalty": 10,
    "frequency_penalty": 1.1,
    "top_p": 1,
    "stream": True
}
invoke_sagemaker_streaming_endpoint(endpoint_name, llama_args)
```

You can pass S3 bucket name and object key to the SageMaker AI inference instance for dynamic model replacement at runtime:

```python
payload = {
    "configure": {
        "bucket": S3_BUCKET_NAME,
        "key": MODEL_NAME
    }
}
response = sagemaker_runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType='application/json',
    Body=json.dumps(payload)
)
print(f"response: {response}")
```

The inference results after deployment are shown below.

![Inference Results](images/practice-running-gguf-format-model-inference-using-sagemaker-ai5.jpg)

After testing, if you no longer need the inference endpoint, delete the Endpoint resources to avoid unnecessary charges.

## Summary

This article demonstrated how to deploy GGUF format models on Amazon SageMaker AI inference endpoints using the Bring Your Own Container (BYOC) approach via SageMaker AI Notebook. After successful deployment, you can seamlessly integrate the model with other AWS services and embed it into your applications to build feature-rich AI applications.

## References

1. [GGUF Specification](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md)
2. [llama.cpp](https://github.com/ggerganov/llama.cpp)
3. [Amazon SageMaker](https://aws.amazon.com/cn/sagemaker/)
4. [Adapting Your Own Inference Container](https://docs.aws.amazon.com/sagemaker/latest/dg/adapt-inference-container.html)
5. [SageMaker BYOC Examples](https://sagemaker-examples.readthedocs.io/en/latest/advanced_functionality/scikit_bring_your_own/scikit_bring_your_own.html)
6. [llama.cpp API Example](https://github.com/ggerganov/llama.cpp/blob/gguf-python/examples/server/api_like_OAI.py)
7. [GenAI LLM CPU SageMaker](https://github.com/aws-samples/genai-llm-cpu-sagemaker/tree/main/docker)
8. [Community AWS Article](https://community.aws/content/2eazHYzSfcY9flCGKsuGjpwqq1B)

---

> Original post: [Practice Running GGUF Format Model Inference Using SageMaker AI](https://aws.amazon.com/cn/blogs/china/practice-running-gguf-format-model-inference-using-sagemaker-ai/)
>
> GitHub repo: [aws-samples/deploy-gguf-model-to-sagemaker](https://github.com/aws-samples/deploy-gguf-model-to-sagemaker)
