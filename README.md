# ASWF CY2024 / Cycles Render Benchmark

This branch records a partial Cycles 4.2.0 run using the ASWF CY2024
environment and OpenUSD 24.05. It is not a complete CY2024 rerun of the
original benchmark.

![Yard 2024 / Cycles compared with ASWF CY2024 / Cycles](render_sheet.jpg)

## Run configuration

- Renderers: Cycles 4.2.0
- OpenUSD: 24.05
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-cycles:cycles-4.2.0-openusd-24.05-cy2024-split@sha256:de9f9d89bda4ddfb2ae7c63ea6231b58a1de13eae44756d4d84e688586f07c00`
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 570.172.08
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Cycles/`](renderers/Cycles/). Complete logs are under [`logs/`](logs/).
