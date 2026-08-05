# ASWF CY2025 / Cycles Render Benchmark

This branch records a partial Cycles 5.0.0 run using the ASWF CY2025
environment and OpenUSD 25.08. It is not a complete CY2025 rerun of the
original benchmark.

![Yard 2024 / Cycles compared with ASWF CY2025 / Cycles](render_sheet.jpg)

## Run configuration

- Renderers: Cycles 5.0.0
- OpenUSD: 25.08
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark-cycles:cycles-5.0.0-openusd-25.08-cy2025-split@sha256:880723e5754e1a3794531410ea6e4d3a17dfee3b989d4deda19dda142c5e3a22`
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 570.172.08
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Cycles/`](renderers/Cycles/). Complete logs are under [`logs/`](logs/).
