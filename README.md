# ASWF CY2025 / Hydra Render Benchmark

This branch records a partial Storm, MoonRay and Cycles
benchmark using the ASWF CY2025 environment and OpenUSD 25.05.01.
It is not a complete CY2025 rerun of the original benchmark.

![ASWF CY2025: Storm, MoonRay and Cycles across four benchmark scenes](render_sheet.jpg)

## Run configuration

- Renderers: Storm, MoonRay 2026.29.1, Cycles 4.5.0
- OpenUSD: 25.05.01
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark:2025.3@sha256:dc85819610d10b5d335a0c01e5bf80184ae42c9d07133f8c7be8ecce92e09032`
- GPU: NVIDIA GeForce RTX 4090, 24 GB
- Driver: NVIDIA 580.126.20
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/`](renderers/). Complete logs are under [`logs/`](logs/).
