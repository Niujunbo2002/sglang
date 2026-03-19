# `scripts/mineru_diffusion` 目录整理

本文档整理了 `/Users/niujunbo/niujunbo/sglang/scripts/mineru_diffusion` 目录下的全部内容，包含目录用途、文件说明以及各文件的完整内容。

## 目录概览

目录路径：

```text
/Users/niujunbo/niujunbo/sglang/scripts/mineru_diffusion
```

目录下共 4 个文件：

```text
README.md
run_server.sh
run_infer.sh
mineru_request.py
```

## 整体用途

这个目录主要用于本地启动一个 `sglang` 服务，并发送一条带图片的测试请求，验证 `MinerU-Diffusion-0315-patched` 模型是否可以正常完成 OCR / Text Recognition 推理。

流程大致如下：

1. 运行 `run_server.sh` 启动本地服务，监听 `127.0.0.1:31002`。
2. 运行 `run_infer.sh`。
3. `run_infer.sh` 会调用 `mineru_request.py`。
4. `mineru_request.py` 读取本地图片，转成 base64，向 `/v1/chat/completions` 发请求。
5. 脚本最终只打印 `choices[0].message.content`。

## 文件说明

### 1. `README.md`

作用：

- 提供快速启动说明。
- 指明服务启动脚本和推理脚本的调用方式。
- 说明推理请求发往的地址、读取的图片路径，以及输出内容。

完整内容：

````md
# MinerU Diffusion Quick Start

## Start server

```bash
bash /mnt/shared-storage-user/mineru2-shared/niujunbo/niujunbo_dev/sglang/scripts/mineru_diffusion/run_server.sh
```

Wait until you see:

```text
Uvicorn running on http://127.0.0.1:31002
```

## Run inference

```bash
bash /mnt/shared-storage-user/mineru2-shared/niujunbo/niujunbo_dev/sglang/scripts/mineru_diffusion/run_infer.sh
```

This script:
- sends the request to `http://127.0.0.1:31002/v1/chat/completions`
- disables proxy in Python
- reads `/mnt/shared-storage-user/mineru2-shared/niujunbo/sglang/image.png`
- prints only `choices[0].message.content`

## Files

- `run_server.sh`: start sglang server
- `mineru_request.py`: send one local test request
- `run_infer.sh`: run `mineru_request.py`
````

### 2. `run_server.sh`

作用：

- 以后台方式启动 `sglang serve`。
- 指定模型路径、端口、Tensor Parallel 大小以及若干推理选项。
- 将日志输出到 `sglang.log`。

关键配置：

- `CUDA_VISIBLE_DEVICES=0`
- `--host 127.0.0.1`
- `--port 31002`
- `--model-path /mnt/shared-storage-user/mineru2-shared/niujunbo/sglang/local_models/MinerU-Diffusion-0315-patched`
- `--dllm-algorithm LowConfidence`
- `--disable-cuda-graph`
- `--attention-backend triton`
- `--sampling-backend pytorch`

完整内容：

```bash
#!/usr/bin/env bash

nohup env PYTHONPATH=python CUDA_VISIBLE_DEVICES=0 \
sglang serve \
  --model-path /mnt/shared-storage-user/mineru2-shared/niujunbo/sglang/local_models/MinerU-Diffusion-0315-patched \
  --host 127.0.0.1 \
  --port 31002 \
  --tp-size 1 \
  --dllm-algorithm LowConfidence \
  --disable-cuda-graph \
  --attention-backend triton \
  --sampling-backend pytorch \
> sglang.log 2>&1 &
```

### 3. `run_infer.sh`

作用：

- 用一条 bash 命令直接执行 `mineru_request.py`。

特点：

- 当前脚本中写死了 Python 文件的绝对路径。

完整内容：

```bash
#!/usr/bin/env bash
python /mnt/shared-storage-user/mineru2-shared/niujunbo/niujunbo_dev/sglang/scripts/mineru_diffusion/mineru_request.py
```

### 4. `mineru_request.py`

作用：

- 构造一个 OpenAI 兼容格式的请求。
- 读取本地 PNG 图片并编码为 base64。
- 调用本地 `sglang` 的 `/v1/chat/completions` 接口。
- 输出模型返回的文本识别结果。

实现细节：

- 使用 `urllib.request`，没有依赖 `requests`。
- 通过 `ProxyHandler({})` 禁用代理。
- `base_url` 为 `http://127.0.0.1:31002/v1/chat/completions`。
- `model` 填写的是本地模型绝对路径。
- 图片路径为 `/mnt/shared-storage-user/mineru2-shared/niujunbo/sglang/image.png`。
- prompt 文本为 `Text Recognition:`。
- `max_tokens` 设置为 `128`。

完整内容：

```python
#!/usr/bin/env python3
import base64
import json
import pathlib
import urllib.request

urllib.request.install_opener(
    urllib.request.build_opener(urllib.request.ProxyHandler({}))
)

base_url = "http://127.0.0.1:31002/v1/chat/completions"
model = "/mnt/shared-storage-user/mineru2-shared/niujunbo/sglang/local_models/MinerU-Diffusion-0315-patched"
img_path = pathlib.Path("/mnt/shared-storage-user/mineru2-shared/niujunbo/sglang/image.png")
img_b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")

payload = {
    "model": model,
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Text Recognition:"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
            ],
        }
    ],
    "max_tokens": 128,
}

req = urllib.request.Request(
    base_url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
)

resp = json.loads(urllib.request.urlopen(req, timeout=180).read().decode("utf-8"))
content = resp["choices"][0]["message"]["content"]
print(content)
```

## 依赖关系

几个文件之间的关系如下：

- `README.md`：提供操作说明。
- `run_server.sh`：启动服务。
- `run_infer.sh`：调用 `mineru_request.py`。
- `mineru_request.py`：向 `run_server.sh` 启动的服务发送推理请求。

## 当前目录内容的特点

- 路径基本都写成了绝对路径，迁移到其他机器时需要改路径。
- 启动和推理流程比较直接，适合做单次本地验证。
- 请求是图片 OCR 场景，不是纯文本对话场景。
- 输出只保留最终识别文本，便于快速验证结果。

## 建议

如果后续要继续维护这个目录，可以考虑：

1. 把绝对路径改成相对路径或环境变量。
2. 在 `run_server.sh` 里补充启动成功后的提示。
3. 在 `mineru_request.py` 里增加异常处理和状态码检查。
4. 支持通过命令行参数传入图片路径，而不是写死 `image.png`。
