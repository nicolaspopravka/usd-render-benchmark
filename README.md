# USD Render Benchmark

This fork extends the original
[Yard renderer benchmark](https://github.com/TheYardVFX/usd-render-benchmark)
into a public results ledger for OpenUSD delivery paths, Hydra render
delegates, and VFX Platform stacks.

It records images, process outcomes, timings, memory, logs, and the build stack
used. Partial runs and regressions remain useful results when their logs and
outputs are preserved.

This is an independent community project. It is not ASWF or OpenUSD
certification, and it is not a renderer performance ranking.

> [!NOTE]
> **Results snapshot — 2026-09-29; build status updated 2026-10-02**
>
> - **New annual runs:** CY2023, CY2024 and CY2025 each run GL/Storm, MoonRay
>   and Cycles against one OpenUSD installation in one runnable image. Each
>   snapshot retains eight images across three scenes; equivalent coverage
>   across CY2023–CY2027 remains unfinished.
> - **Published:** 15/15 OpenUSD delivery-path results; five annual Cycles
>   results covering CY2023-CY2027 with patched CY2026/CY2027 follow-ups,
>   including a four-scene patched CY2027 run; the MoonRay CY2025 result
>   with focused texture and shading follow-ups; and five annual Embree
>   results covering CY2023–CY2027 on ASWF prebuilt stacks, plus two
>   CY2027 variants demonstrating the AO-disabled and scene-lit paths. The
>   refreshed CY2027 image also has an updated three-scene Storm result.
> - **Run model demo:** [`demo/run1`](https://github.com/nicolaspopravka/usd-render-benchmark/tree/demo/run1)
>   mounts a one-render Storm/Teapot branch into a published image on
>   a GitHub-hosted runner. This demonstrates the branch/image split.
> - **September refresh:** released ASWF images repair the tested OSL/OIIO
>   plugin loading and CY2027 Storm/MaterialX failures. Findings from earlier
>   VFX Platform years and focused open questions remain. The new annual runs extend this
>   coverage; missing renders and material limitations remain documented.
> - **Waiting upstream:** a tagged Cycles release with the merged Hydra fixes,
>   hdMoonray integration, and OpenUSD Ptex review.
> - **Not scheduled:** modern commercial-delegate coverage.

**Published** means a run branch contains the recorded outputs; it does not
mean the result was clean. **Waiting release** has an upstream change but no
tagged benchmark stack yet. **Waiting upstream** is blocked on an external
tracker or review. **Paused** needs a scope, cost, or build review decision.
**Not scheduled** has no current plan.

## Run branches and stack images

A benchmark result has two separate inputs:

- A run branch contains the harness, scene selection, Rez package definitions,
  and the output directories that preserve the result.
- A runnable image contains the OpenUSD and renderer environment used to
  execute that branch.

Image composition and publishing live in
[`usd-render-benchmark-stack`](https://github.com/nicolaspopravka/usd-render-benchmark-stack).
The caller mounts the run branch and selects that directory as the container's
working directory, so `render_script.sh` executes without being copied into
the image. Logs and renders remain in the mounted checkout; summary generation
is a separate runner step.

The [`demo/run1`](https://github.com/nicolaspopravka/usd-render-benchmark/tree/demo/run1)
branch is the first published example of this model. Stack workflow
[run 34144139279](https://github.com/nicolaspopravka/usd-render-benchmark-stack/actions/runs/34144139279)
mounted the branch into the CY2027 runnable image and completed a Storm
Teapot render on a headless GitHub runner.

## ASWF environments by year

The aim is a runnable Hydra benchmark environment for each VFX Platform year
from CY2023 through CY2027. Each environment uses the OpenUSD installation
supplied by its ASWF base, with the additional Hydra delegates built against it.
The project packages that environment in a runnable image; the result branch
supplies the benchmark configuration and retains its outputs.

### Published runs

| Run | OpenUSD | Hydra delegates | Images retained |
| --- | --- | --- | --- |
| [CY2023](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2023) | 23.08 | GL, MoonRay 2026.29.1, Cycles 4.0.2 | 8 across McUsd, OpenChessSet and ALab |
| [CY2024](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2024) | 24.08 | GL, MoonRay 2026.29.1, Cycles 4.3.0 | 8 across McUsd, OpenChessSet and ALab |
| [CY2025](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2025) | 25.05.01 | Storm, MoonRay 2026.29.1, Cycles 4.5.0 | 8 across McUsd, OpenChessSet and ALab |

Each run README includes a render sheet, configuration and links to its
summary, images and logs. Shared Docker instructions are in the [running guide](docs/RUNNING.md).
Success means exit 0; nonzero exits are failures. Image presence and appearance
are recorded separately. These three
snapshots have no Moana Island Scene images; Cycles/ALab is also absent.

CY2025 now uses the September 29 image with upstream default GPU support,
including MoonRay XPU and Cycles OptiX, plus OSL support. NanoVDB,
OpenImageDenoise and the precompiled dependency bundle remain disabled because
of the available dependencies; the exceptions are listed in the [running guide](docs/RUNNING.md#limitations).
The annual benchmark leaves device selection unchanged. Its results are not
an all-GPU benchmark.

The published CY2023 and CY2024 results retain their recorded image digests.
The [Python discovery fix](https://github.com/nicolaspopravka/usd-render-benchmark/issues/53)
is now integrated into the stack build script through
[PR #14](https://github.com/nicolaspopravka/usd-render-benchmark-stack/pull/14).
The tested default bases still have separate
[OSL/LLVM runtime](https://github.com/nicolaspopravka/usd-render-benchmark/issues/54)
and [older-Cycles/OpenVDB compatibility](https://github.com/nicolaspopravka/usd-render-benchmark/issues/56)
problems. The build script supports disabling those Cycles features explicitly;
ASWF's delayed-loading default is being discussed in
[#488](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/488).
Full builds and benchmark renders with refreshed bases are deferred until new
upstream images are released. These build updates do not change the published
results or establish restored OSL or volume support.

### Remaining environment coverage

| Environment | GL/Storm | MoonRay | Cycles |
| --- | --- | --- | --- |
| CY2023–CY2025 | Included in the annual runs | Included in the annual runs | Included in the annual runs |
| CY2026–CY2027 | Published separately | Tested build blocked by OpenUSD API changes and other integration failures ([#48](https://github.com/nicolaspopravka/usd-render-benchmark/issues/48)) | Tested released-tag builds blocked by Hydra API or dependency-target conflicts ([#50](https://github.com/nicolaspopravka/usd-render-benchmark/issues/50)) |

Earlier CY2026/CY2027 Cycles results exist on different images, including patched
follow-ups; they remain linked below. They do not establish equivalent delegate
coverage in the annual runnable environments. Build fixes and small validation
renders likewise need a released environment and scene runs before extending
this table.

Embree remains useful as an example delegate and has its own historical results.
It is not included in these three annual runs. Its Embree 3/4 packaging mismatch
on the older OpenUSD versions is recorded in
[#47](https://github.com/nicolaspopravka/usd-render-benchmark/issues/47).

## OpenUSD delivery paths

Each linked label reports successful process exits out of three scenes,
followed by the observed OpenChessSet appearance. `Textured`, `black`, and
`fallback` describe that image, not the other two scenes.

Most links below point to runs published in July and August. The CY2027
prebuilt Storm result was rerun after the September ASWF image refresh.

| Cycle / renderer | Pixar `build_usd.py` | ASWF `build_usd.sh` | ASWF prebuilt `ci-vfxall` |
| --- | --- | --- | --- |
| CY2023 · GL | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd_pixar/cy2023-gl-only) | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd/cy2023-gl-only) | [3/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2023-gl-only) |
| CY2024 · GL | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd_pixar/cy2024-gl-only) | [2/3 black](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd/cy2024-gl-only) | [1/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2024-gl-only) |
| CY2025 · Storm | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd_pixar/cy2025-storm-only) | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd/cy2025-storm-only) | [1/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2025-storm-only) |
| CY2026 · Storm | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd_pixar/cy2026-storm-only) | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd/cy2026-storm-only) | [0/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2026-storm-only) |
| CY2027 · Storm | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd_pixar/cy2027-storm-only) | [3/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/build_usd/cy2027-storm-only) | [3/3 textured — refreshed image](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2027-storm-only) |

## Delegate coverage

The earlier results below remain available alongside the new annual runs.
Their OpenUSD versions, delegate versions and images may differ; use each
result README when comparing them.

| Delegate | Published results | Current state |
| --- | --- | --- |
| Cycles | **Annual environments:** [CY2023–CY2025](#aswf-environments-by-year). **Earlier published partial:** [CY2023](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2023-cycles-only) · [CY2024](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2024-cycles-only) · [CY2025](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2025-cycles-only) · [CY2026](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2026-cycles-only) · [CY2027](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2027-cycles-only) — two of four scenes produce images on each released stack. | **Follow-up:** the patched [CY2026 run](https://github.com/nicolaspopravka/usd-render-benchmark/tree/test/cy2026-cycles-only) adds an OpenChessSet image after the merged empty-material fix. The patched [CY2027 run](https://github.com/nicolaspopravka/usd-render-benchmark/tree/test/cy2027-cycles-only) completes all four renderer processes, including Moana after deferred geometry deletion; its images retain material, texture, and exposure limitations. The changes are under review in Cycles [PR #78](https://projects.blender.org/blender/cycles/pulls/78), with UDIM discovery tracked separately in [#77](https://projects.blender.org/blender/cycles/issues/77). OptiX-enabled [CY2026](https://github.com/nicolaspopravka/aswf-docker/actions/runs/32348492265) and [CY2027](https://github.com/nicolaspopravka/aswf-docker/actions/runs/32348492179) images are built, but GPU rendering is not yet established. |
| MoonRay | **Annual environments:** [CY2023–CY2025](#aswf-environments-by-year). **Earlier published partial:** [CY2025 — three benchmark images, zero clean exits; Moana not run](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2025-moonray-only) · [tiled-texture and smooth-ALab follow-up](https://github.com/nicolaspopravka/usd-render-benchmark/tree/test/cy2025-moonray-only) | **Follow-up:** MaterialX BSDF support remains limited ([#24](https://github.com/nicolaspopravka/usd-render-benchmark/issues/24)); refinement-zero smoothing and missing light-link handling are in hdMoonray [#11](https://github.com/OpenMoonRay/hdMoonray/pull/11) and [#12](https://github.com/OpenMoonRay/hdMoonray/pull/12). An [XPU-capable image](https://github.com/nicolaspopravka/aswf-docker/commit/e49bf97aecc71b12ef7bb3eff7841b3acbf0b2b5) exists, but automatic mode used the vector path for these scenes; that historical run does not establish XPU use. The newer [CY2025 environment](#aswf-environments-by-year) includes GPU support and separate device probes. |
| Embree | **Published partial:** [CY2023](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2023-embree-only) · [CY2024](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2024-embree-only) · [CY2025](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2025-embree-only) · [CY2026](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2026-embree-only) · [CY2027](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2027-embree-only) — four scenes per stack using ASWF bases plus the documented Embree builds (3.2.2 / 4.3.3); CY2027 renders after the move to OpenUSD 26.08. | **Findings:** [GH #37](https://github.com/nicolaspopravka/usd-render-benchmark/issues/37) CY2027 infeasibility was lifted by OpenUSD 26.08; [GH #38](https://github.com/nicolaspopravka/usd-render-benchmark/issues/38) CY2026 texture-read failure; [GH #39](https://github.com/nicolaspopravka/usd-render-benchmark/issues/39) black ALab entry — root cause confirmed (AO collapse in enclosed interiors) and closed, with two CY2027 variants published; [GH #40](https://github.com/nicolaspopravka/usd-render-benchmark/issues/40) adapter warnings; [GH #41](https://github.com/nicolaspopravka/usd-render-benchmark/issues/41) dome-light texture. |

Modern Karma, RenderMan, and Arnold coverage is **not scheduled**. The
[original Yard baseline](https://github.com/TheYardVFX/usd-render-benchmark)
remains the historical mixed-result reference.

## Findings and upstream follow-up

| State | Finding | Public record |
| --- | --- | --- |
| **Published finding** | Material support is limited across delegates. Cycles does not support MaterialX material networks and supports only a subset of `UsdPreviewSurface`, falling back to its default surface when no supported network is available. MoonRay 2026.29.1 does not support the MaterialX BSDF nodes used by OpenChessSet. | [Cycles #21](https://github.com/nicolaspopravka/usd-render-benchmark/issues/21) · [Cycles #25](https://github.com/nicolaspopravka/usd-render-benchmark/issues/25) · [MoonRay #24](https://github.com/nicolaspopravka/usd-render-benchmark/issues/24) |
| **Published finding** | The July–August ASWF CI snapshots did not provide the same working Storm/MaterialX result as OpenUSD built with Pixar's `build_usd.py`. OpenChessSet rendered textured with the Pixar build, while the corresponding ASWF Conan-based stacks produced fallback or black results with MaterialX errors. | [OpenUSD results](#openusd-delivery-paths) · [ASWF issues #454](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/454) and [#455](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/455) |
| **Published finding** | Lighting is not consistent across delegates. The same scene can render with very different exposure and light contribution, so these are stack results rather than look-matched comparisons. | [delegate results](#delegate-coverage) · [Yard baseline](https://github.com/TheYardVFX/usd-render-benchmark) |
| **Published finding** | Exit status and image appearance must be read separately. In the annual runs, all eight retained CY2023 renders exit 0; four of eight CY2024 renders fail; CY2025 retains eight images, four from processes that exited nonzero. The ninth attempt, Cycles/ALab, failed without an image; its log is excluded from the current published snapshot. MoonRay empty-token diagnostics also appear on CY2023. Material limitations remain visible across all three years. | [OpenUSD results](#openusd-delivery-paths) · [delegate results](#delegate-coverage) |
| **Waiting release** | The Cycles empty-material fix is merged; comparable CY2026/CY2027 reruns wait for a tagged release containing it. | [Cycles #75](https://projects.blender.org/blender/cycles/pulls/75) · [patched CY2026](https://github.com/nicolaspopravka/usd-render-benchmark/tree/test/cy2026-cycles-only) · [patched CY2027](https://github.com/nicolaspopravka/usd-render-benchmark/tree/test/cy2027-cycles-only) |
| **Waiting upstream** | Cycles Hydra diagnostics, AOV reporting, unresolved asset paths, and deferred geometry deletion are under review. UDIM tile discovery remains separate. | Cycles [PR #78](https://projects.blender.org/blender/cycles/pulls/78) · [issue #77](https://projects.blender.org/blender/cycles/issues/77) · [patched CY2027 run](https://github.com/nicolaspopravka/usd-render-benchmark/tree/test/cy2027-cycles-only) |
| **Waiting upstream** | MoonRay refinement-zero smoothing and missing light-link handling are awaiting upstream integration. | hdMoonray [#11](https://github.com/OpenMoonRay/hdMoonray/pull/11) and [#12](https://github.com/OpenMoonRay/hdMoonray/pull/12) are open |
| **Released improvement** | In the refreshed ASWF images, the tested OSL and OIIO discovery plugins load without `LD_PRELOAD`. The benchmark finding and the ASWF tracking issue are closed. | [Fork issue #3](https://github.com/nicolaspopravka/usd-render-benchmark/issues/3) · [aswf-docker #450](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/450) |
| **Released improvement** | Refreshed CY2027 prebuilt Storm renders OpenChessSet with its textured materials on OpenUSD 26.08 / MaterialX 1.39.5, without preload or a MaterialX search-path override. Grey results from earlier VFX Platform years remain tracked separately. | [Refreshed CY2027 result](https://github.com/nicolaspopravka/usd-render-benchmark/tree/aswf/cy2027-storm-only) · [Fork issue #10](https://github.com/nicolaspopravka/usd-render-benchmark/issues/10) · [aswf-docker #454](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/454) |
| **Released improvement** | The refreshed CY2027 ASWF `build_usd.sh` path was reported fixed by its maintainer. The benchmark did not independently rerun that build method. | [Fork issue #2](https://github.com/nicolaspopravka/usd-render-benchmark/issues/2) · [aswf-docker #455](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/455) |
| **Waiting upstream** | Storm fails in the Ptex mipmap-loader path on two Moana Island subtrees. | OpenUSD [#4168](https://github.com/PixarAnimationStudios/OpenUSD/issues/4168) and [#4169](https://github.com/PixarAnimationStudios/OpenUSD/issues/4169) are open; crash-prevention [PR #4176](https://github.com/PixarAnimationStudios/OpenUSD/pull/4176) is under review |

Additional run-level findings are tracked in the
[benchmark issues](https://github.com/nicolaspopravka/usd-render-benchmark/issues).

The MoonRay client remaining alive after its Arras worker exits is tracked in
[#51](https://github.com/nicolaspopravka/usd-render-benchmark/issues/51) and
[OpenMoonRay #309](https://github.com/OpenMoonRay/openmoonray/issues/309).
The proposed fix in [hdMoonray draft PR #19](https://github.com/OpenMoonRay/hdMoonray/pull/19)
passed a full build and a test that killed the worker during rendering: the
client reported the failure and exited two seconds later. That is failure-handling
evidence, not a successful render or validation of reconnecting and repeated
failures. The patch is not included in the published reference results.

## Community coordination

Use the
[Ideas discussion](https://github.com/nicolaspopravka/usd-render-benchmark/discussions/18)
to suggest delegate/version combinations, available hardware and drivers,
licensed-renderer interest, scenes, upstream relevance, and priorities.
Failures are valid results, and ASWF reference, Pixar control, and delegate
diagnostic runs remain separate.

Community benchmark attempts are welcome through
[the Moana Island Scene / MoonRay discussion](https://github.com/nicolaspopravka/usd-render-benchmark/discussions/55).
The initial request is the Moana Island Scene with MoonRay on the new CY2025 image; its
[dedicated recipe](https://github.com/nicolaspopravka/usd-render-benchmark/blob/aswf/cy2025/docs/MOANA_MOONRAY.md)
runs that combination separately and records a bounded attempt. Coordinate
before starting, and share failures as well as images. Contributed results are
reviewed with their hardware, configuration, attribution and sharing terms
before being published as separate snapshots. Asset downloads remain with the
original providers. External code submissions remain deferred pending the
repository's contribution terms.

## Running the benchmark

Start with the [software demo](docs/RUNNING.md#software-demo) to render one
Teapot scene without an NVIDIA GPU. The same guide covers
[annual NVIDIA runs](docs/RUNNING.md#annual-nvidia-benchmark) and optional
render-sheet generation. Annual instructions have not had a complete
fresh-asset NVIDIA replay; published results are not a guarantee of exact replay.

## Reading the results

The default branch is the landing page and supplies the small
[`tools/system_specs.py`](tools/system_specs.py) and
[`tools/generate_render_sheet.py`](tools/generate_render_sheet.py) helpers. Result links point to
maintained run branches so published updates are visible. Each run
README describes its current results, with `render_summary.md`, `logs/`, and
`renderers/` preserving the recorded outputs. Exact commit links identify
specific historical evidence.

A result README is a starting point, not a guarantee of exact replay. Unknown
or historically unrecorded inputs remain limitations rather than being
inferred.
