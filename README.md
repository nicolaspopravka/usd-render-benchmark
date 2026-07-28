# ASWF CY2025 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2025
environment and OpenUSD 25.05.01. It is not a complete CY2025 rerun of the original benchmark.

![Yard 2024 / Storm compared with ASWF CY2025 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 25.05.01
- Container: `aswf/ci-vfxall:2025`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.159.04
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete logs are under [`logs/`](logs/).
