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