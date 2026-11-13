# ASWF CY2026 / Hydra Render Benchmark

This branch records a partial Storm and Cycles
benchmark using the ASWF CY2026 environment and OpenUSD 26.03.
It is not a complete CY2026 rerun of the original benchmark.

![ASWF CY2026: Storm and Cycles across four benchmark scenes](render_sheet.jpg)

## Run configuration

- Renderers: Storm, Cycles 5.4.0 dev
- OpenUSD: 26.03
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:4c515bf0aa8f07490d8879bc709389eaba0fb85b78167da09918a445b2a9ba2d`
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 595.91.07
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/`](renderers/). Complete logs are under [`logs/`](logs/).
