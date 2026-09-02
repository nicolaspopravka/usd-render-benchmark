# ASWF CY2026 / Embree Render Benchmark

This branch records a partial Embree 4.3.3 run using the ASWF CY2026
environment and OpenUSD 26.03. It is not a complete CY2026 rerun of the original benchmark.

![Yard 2024 / Embree compared with ASWF CY2026 / Embree](render_sheet.jpg)

## Run configuration

- Renderers: Embree 4.3.3
- OpenUSD: 26.03
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-embree:cy2026@sha256:0ae591b17823286575689af9f1c33efefffde9dc0602e553c655575914bc4593`
- GPU: NVIDIA L4, 24 GB
- Driver: NVIDIA 550.127.05
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Embree/`](renderers/Embree/). Complete logs are under [`logs/`](logs/).
