# ASWF CY2024 / Hydra Render Benchmark

This branch records a partial Storm, MoonRay and Cycles
benchmark using the ASWF CY2024 environment and OpenUSD 24.08.
It is not a complete CY2024 rerun of the original benchmark.

![ASWF CY2024: Storm, MoonRay and Cycles across four benchmark scenes](render_sheet.jpg)

## Run configuration

- Renderers: Storm, MoonRay 2026.29.1, Cycles 4.3.0
- OpenUSD: 24.08
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:512d18ca12cc2a55140ce3efb5fd873c40d944ad8562c32f4f71f60695b85dc5`
- GPU: NVIDIA RTX PRO 4500 Blackwell, 32 GB
- Driver: NVIDIA 580.178.04
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/`](renderers/). Complete logs are under [`logs/`](logs/).
