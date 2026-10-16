# ASWF CY2025 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2025
environment and OpenUSD 25.05.01. It is not a complete CY2025 rerun of the original benchmark.

![Yard 2024 / Storm compared with ASWF CY2025 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 25.05.01
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:adaca41a38a486b5876f3f7b11e25dcde100c7ede3f5e86b9fa85f0f80011415`
- GPU: NVIDIA RTX PRO 4500 Blackwell, 32 GB
- Driver: NVIDIA 580.126.20
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete logs are under [`logs/`](logs/).
