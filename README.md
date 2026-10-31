# USD Render Benchmark — `demo/run1`

This branch records one Storm render of Teapot using a mounted benchmark
checkout and a reusable container image. It demonstrates the benchmark's
mount-run model with software rendering.

![Storm / Teapot](renderers/Storm/Teapot.jpg)

## Run configuration

- Renderers: Storm
- OpenUSD: 26.03
- Container: `ghcr.io/nicolaspopravka/usd-render-benchmark:2026@sha256:4990be69cc2daf4ddff9178346ff9fc2c1f823524d90823922d022a77d04da94`
- GPU: None (software rendering)
- Driver: Mesa 23.1.4-4.el8_10
- OS: Rocky Linux 8

## Results

The results are in [`render_summary.md`](render_summary.md). Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete logs are under [`logs/`](logs/).
