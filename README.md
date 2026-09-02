# ASWF CY2027 / Storm Render Benchmark

This branch records a partial Storm run using the ASWF CY2027
environment and OpenUSD 26.08. It is not a complete CY2027 rerun of the original benchmark.

![Yard 2024 / GL compared with ASWF CY2027 / Storm](render_sheet.jpg)

## Run configuration

- Renderer: Hydra Storm
- Container: `aswf/ci-vfxall:2027-clang22.1@sha256:475f153a2e60598ba536d97e95e95caac74925524662d67cc4248901c06594d0`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.159.04
- OS: Rocky Linux 9.8

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/26.08/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/Storm/`](renderers/Storm/). Complete
logs are under [`logs/`](logs/).
