# USD Render Benchmark

This fork extends the original [Yard renderer benchmark](https://github.com/TheYardVFX/usd-render-benchmark)
into a public evidence ledger for modern OpenUSD, Hydra delegates, and VFX
Platform stacks.

The benchmark compares images, timings, memory, and failures from the same USD
scenes. This fork also records how OpenUSD was delivered, which renderer and
graphics runtime were used, and which dependency closure produced the result.
An OpenUSD version alone does not identify a working stack.

**Status — 2026-08-04:** all 15 GL/Storm delivery-path runs are published.
Cycles CY2026 validation is in progress; MoonRay XPU work is paused pending a
reviewed build boundary and NVIDIA runtime validation.

## GL / Storm delivery paths

Every linked entry is published evidence. The symbol describes the observed
result, not whether the run is complete.

| OpenUSD delivery path | CY2023 | CY2024 | CY2025 | CY2026 | candidate CY2027 |
| --- | --- | --- | --- | --- | --- |
| Pixar `build_usd.py` | ✅ [GL](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd_pixar/cy2023-gl-only) | ⚠️ [GL](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd_pixar/cy2024-gl-only) | ⚠️ [Storm](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd_pixar/cy2025-storm-only) | ✅ [Storm](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd_pixar/cy2026-storm-only) | ✅ [Storm](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd_pixar/cy2027-storm-only) |
| ASWF `build_usd.sh` | ✅ [GL](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd/cy2023-gl-only) | ⚠️ [GL](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd/cy2024-gl-only) | ⚠️ [Storm](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd/cy2025-storm-only) | ✅ [Storm](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd/cy2026-storm-only) | ⚠️ [Storm](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd/cy2027-storm-only) |
| Prebuilt `aswf/ci-vfxall` | ⚠️ [GL](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2023-gl-only) | ⚠️ [GL](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2024-gl-only) | ⚠️ [Storm](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2025-storm-only) | ⚠️ [Storm](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2026-storm-only) | ⚠️ [Storm](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2027-storm-only) |

✅ expected result · ⚠️ published finding

## Open-source delegates

| Delegate | Published evidence | Current state |
| --- | --- | --- |
| Cycles | ✅ [CY2024 candidate](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2024-cycles-only) · ✅ [CY2025 candidate](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2025-cycles-only) | 🔄 [CY2026 validation](https://github.com/nicolaspopravka/aswf-docker/tree/codex/delegates/cycles-5.2-ghcr) in progress; later-stack coverage follows that result |
| MoonRay | ⚠️ [CY2025 CPU](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2025-moonray-only) | ⏸️ [XPU candidate](https://github.com/nicolaspopravka/aswf-docker/tree/codex/moonray-hydra-v2026-29-1) paused pending build review and NVIDIA validation |

The MoonRay CPU images are coherent, but stock `usdrecord` exits nonzero after
rendering. That post-render failure remains part of the published result.

## Commercial delegates

| Delegate | Existing evidence | Modern stack coverage |
| --- | --- | --- |
| Karma | ✅ [Yard baseline](https://github.com/TheYardVFX/usd-render-benchmark) | — not scheduled |
| RenderMan | ✅ [Yard baseline](https://github.com/TheYardVFX/usd-render-benchmark) | — not scheduled |
| Arnold | ✅ [Yard baseline](https://github.com/TheYardVFX/usd-render-benchmark) | — not scheduled |

## Open findings and follow-up

| Area | Public record | State |
| --- | --- | --- |
| ASWF OSL plugin loading | [aswf-docker #450](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/450) | Open |
| Prebuilt CY2027 MaterialX resources | [aswf-docker #454](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/454) · [PR #453](https://github.com/AcademySoftwareFoundation/aswf-docker/pull/453) | Issue open; fix merged |
| ASWF-built CY2027 MaterialX shaders | [aswf-docker #455](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/455) | Open |
| Storm/Moana Ptex allocation failures | [OpenUSD #4168](https://github.com/PixarAnimationStudios/OpenUSD/issues/4168) · [#4169](https://github.com/PixarAnimationStudios/OpenUSD/issues/4169) · [diagnostic branch](https://github.com/nicolaspopravka/USD/tree/hdst-ptex-buffer-size-overflow) | Issues open; diagnostic patch available |

## Reading and reproducing results

Each result branch is a self-contained evidence snapshot: its README identifies
the stack and scope, `render_summary.md` summarizes outcomes, `logs/` preserves
diagnostics and resource measurements, and `renderers/` contains the produced
images. Follow that branch's README when reproducing a result; package paths
and graphics-runtime requirements are lane-specific.
