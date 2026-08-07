# ASWF CY2024 / GL Render Benchmark

This branch records a partial GL run using the ASWF CY2024
environment and OpenUSD 24.08. It is not a complete CY2024 rerun of the original benchmark.

![ASWF CY2024 / GL compared with ASWF USD 24.08 / GL](render_sheet.jpg)

## Run configuration

- Renderer: Hydra GL
- USD: OpenUSD 24.08, ASWF [build script](https://github.com/AcademySoftwareFoundation/aswf-docker/blob/2c8484137a2f056a0abfd504dd5ad166240ab47e/scripts/vfx/build_usd.sh).
- Container: `ghcr.io/nicolaspopravka/openusd-build-paths:aswf-cy2024-d6b710a0b02eea4cd3f06d19387c0d1d71f937c4@sha256:e3a37cb3edb9ce6b7ba8ed01102410f963036588cc411eb46416202669632987`
- GPU: NVIDIA RTX PRO 4000 Blackwell, 24 GB
- Driver: NVIDIA 580.167.08
- OS: Rocky Linux 8.10

Stock `usdrecord` creates a GL context via Qt/PySide, which requires a display
server. [`tools/usdrecord_egl.py`](tools/usdrecord_egl.py) replaces this with
direct EGL initialization via ctypes, enabling headless GPU-accelerated
rendering. The Rez USD package (`packages/usd/24.08/package.py`) redirects the
`usdrecord` command to this wrapper via `alias("usdrecord", ...)`.

## Results

The results are in [`render_summary.md`](render_summary.md).

Moana Island is intentionally skipped by `render_script.sh` because this
configuration previously segfaulted.

Rendered images are under [`renderers/GL/`](renderers/GL/). Complete
logs are under [`logs/`](logs/).
