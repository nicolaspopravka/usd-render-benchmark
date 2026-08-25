# USD Render Benchmark

| Scene \ Renderer | Cycles |
|---|---|
| McUsd | Success<br>0:26.42<br>744004KB |
| chess_set | Success<br>0:04.07<br>518408KB |
| entry | Success<br>6:20.08<br>6471044KB |
| island | Success<br>16:17.66<br>107102092KB |
## System Specs
RunPod Secure NVIDIA RTX PRO 6000 Blackwell Server Edition, 595.91.07, 97887 MiB; Rocky Linux 9.8 (Blue Onyx); Linux 6.8.0-138-generic; CPU render (`CYCLES_DEVICE` unset); Cycles `1319002982e09970cb50f727e3f299cea78de229` plus `08ad1ac15`, `e80c514f8`, `d8ff91e73`, `471d90155`, and `7a3639efe`; OpenUSD `2095fafafd033fa23386d7ec6d58c7cc33974518`; ghcr.io/nicolaspopravka/usd-render-benchmark-cycles@sha256:4b4a2023fdb69816afaee1a2dd526dade7577b30d76e42e206926bdf93374afa; EGL headless wrapper
