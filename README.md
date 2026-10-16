# ASWF CY2024 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2024
environment and OpenUSD 24.08. It is not a complete CY2024 rerun of the original benchmark.

![Yard 2024 / Storm compared with ASWF CY2024 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 24.08
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:82a1f775c6914289271d125fec3db6e5f9154357826347be634468ae69456d92`
- GPU: NVIDIA RTX PRO 4500 Blackwell, 32 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/GL/`](renderers/GL/). Complete logs are under [`logs/`](logs/).
