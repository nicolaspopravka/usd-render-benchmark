# ASWF CY2023 / Hydra Render Benchmark

This branch records a partial Storm, MoonRay and Cycles
benchmark using the ASWF CY2023 environment and OpenUSD 23.08.
It is not a complete CY2023 rerun of the original benchmark.

![ASWF CY2023: Storm, MoonRay and Cycles across four benchmark scenes](render_sheet.jpg)

## Run configuration

- Renderers: Storm, MoonRay 2026.29.1, Cycles 4.0.2
- OpenUSD: 23.08
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:fdbf13c0007a0f5e623071a123f4af67d57632ba1ed6db46436790cee771f415`
- GPU: NVIDIA RTX PRO 4500 Blackwell, 32 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/`](renderers/). Complete logs are under [`logs/`](logs/).
