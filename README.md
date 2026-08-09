# ASWF CY2025 / MoonRay Render Benchmark

This branch records a partial MoonRay 2026.29.1 run using the ASWF CY2025
environment and OpenUSD 25.05.01. It is not a complete CY2025 rerun of the
original benchmark.

![ASWF CY2025 / MoonRay compared with ASWF CY2025 / MoonRay Patched](render_sheet.jpg)

## Run configuration

- Renderers: MoonRay 2026.29.1
- OpenUSD: 25.05.01
- Container: `ghcr.io/nicolaspopravka/openmoonray-hydra@sha256:75945fa61e05ee39c46d9f82c6e2add7759ac242568f5a51127d76170e1661fc`
- GPU: NVIDIA RTX 2000 Ada Generation, 16 GB
- Driver: NVIDIA 570.172.08
- OS: Rocky Linux 8.10

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Moonray/`](renderers/Moonray/). Complete logs are under [`logs/`](logs/).
