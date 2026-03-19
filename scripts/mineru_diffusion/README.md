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
