# ASWF CY2027 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2027
environment and OpenUSD 26.05. It is not a complete CY2027 rerun of the original benchmark.

![Yard 2024 / Storm compared with ASWF CY2027 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 26.05
- Container: `aswf/ci-vfxall:2027`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 9.8

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete logs are under [`logs/`](logs/).
