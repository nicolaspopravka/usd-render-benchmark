# ASWF CY2023 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2023
environment and OpenUSD 23.08. It is not a complete CY2023 rerun of the original benchmark.

![Yard 2024 / Storm compared with ASWF CY2023 / Storm](render_sheet.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 23.08
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:1d4bb2bf9332f21a0a825e676ef573d00e57ae51446ebb70747da9ac8056c76c`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.159.04
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/GL/`](renderers/GL/). Complete logs are under [`logs/`](logs/).
