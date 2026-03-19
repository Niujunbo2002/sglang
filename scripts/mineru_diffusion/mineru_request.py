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
