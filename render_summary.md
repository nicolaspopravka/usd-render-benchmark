# USD Render Benchmark

| Scene \ Renderer | Cycles |
|---|---|
| McUsd | Success<br>2:42.05<br>757512KB |
| chess_set | Success<br>0:04.88<br>577816KB |
| entry | Failure<br>37:02.63<br>9466112KB |
## System Specs
RunPod Secure NVIDIA RTX PRO 4000 Blackwell, 580.159.04, 24467 MiB; Rocky Linux 9.8 (Blue Onyx); Linux 6.8.0-111-generic; Cycles 5.2.0 + OpenUSD 26.05 empty-material fix (ghcr.io/nicolaspopravka/usd-render-benchmark-cycles@sha256:01e83c16329522f430af67b3d5aa5d108f1c6c8d3f41868937b6d06957aa7c89); EGL headless wrapper
