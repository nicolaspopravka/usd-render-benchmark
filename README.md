# ASWF CY2026 / Hydra Render Benchmark

This branch records a partial Storm and Cycles
benchmark using the ASWF CY2026 environment and OpenUSD 26.03.
It is not a complete CY2026 rerun of the original benchmark.

![ASWF CY2026: Storm and Cycles across four benchmark scenes](render_sheet.jpg)

## Run configuration

- Renderers: Storm, Cycles 5.3.0 dev
- OpenUSD: 26.03
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:2beabfef0d378ba0064c5a623401aef707674d2ac992f2ea1bc7856886c9e43f`
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 595.91.07
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/`](renderers/). Complete logs are under [`logs/`](logs/).
