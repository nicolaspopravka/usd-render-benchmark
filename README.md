# ASWF CY2027 / Hydra Render Benchmark

This branch records a partial Storm and Cycles
benchmark using the ASWF CY2027 environment and OpenUSD 26.08.
It is not a complete CY2027 rerun of the original benchmark.

![ASWF CY2027: Storm and Cycles across four benchmark scenes](render_sheet.jpg)

## Run configuration

- Renderers: Storm, Cycles 5.3.0 dev
- OpenUSD: 26.08
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark@sha256:6548091513540c5afb0c3281f5c2b22ee8f790efc4016993c93ba8726b491986`
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 595.91.07
- OS: Rocky Linux 9.8

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/`](renderers/). Complete logs are under [`logs/`](logs/).
