# USD Render Benchmark

| Scene \ Renderer | Cycles |
|---|---|
| McUsd | Success<br>2:35.51<br>757000KB |
| chess_set | Success<br>0:11.25<br>578280KB |
| entry | Failure<br>36:14.22<br>9405568KB |
## System Specs
RunPod Secure NVIDIA RTX PRO 4000 Blackwell, 580.159.04, 24467 MiB; Rocky Linux 8.10 (Green Obsidian); Linux 6.8.0-124-generic; Cycles 5.2.0 + OpenUSD 26.03 empty-material fix (ghcr.io/nicolaspopravka/usd-render-benchmark-cycles@sha256:bad67a76cbfa5e342ee06049864555b8280630258a446a1db6d8f6fcba7c8d50); EGL headless wrapper
