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
> **Snapshot — 2026-08-25**
>
> - **Published:** 15/15 OpenUSD delivery-path results; five annual Cycles
>   results covering CY2023-CY2027 with patched CY2026/CY2027 follow-ups,
>   including a four-scene patched CY2027 run; and the MoonRay CY2025 result
>   with focused texture and shading follow-ups.
> - **Waiting upstream:** ASWF image/package findings, a tagged Cycles release
>   with the merged Hydra fixes, hdMoonray integration, and OpenUSD Ptex
>   review.
> - **Not scheduled:** modern commercial-delegate coverage.

**Published** means a pinned snapshot of the run's outputs exists; it does not
mean the result was clean. **Waiting release** has an upstream change but no
tagged benchmark stack yet. **Waiting upstream** is blocked on an external
tracker or review. **Paused** needs a scope, cost, or build review decision.
**Not scheduled** has no current plan.

## OpenUSD delivery paths

Each linked label reports successful process exits out of three scenes,
followed by the observed OpenChessSet appearance. `Textured`, `black`, and
`fallback` describe that image, not the other two scenes.

| Cycle / renderer | Pixar `build_usd.py` | ASWF `build_usd.sh` | ASWF prebuilt `ci-vfxall` |
| --- | --- | --- | --- |
| CY2023 · GL | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/c9c991a999f8b9c2e9bb5337cc2272fa27d824aa) | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/c5d06b7bbc17f752c090ddb39a71e402e1c46131) | [3/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/bb72885fc55ff8c746eb222f6869056a3add4a97) |
| CY2024 · GL | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/23402807430abc928e880bd13c24c0c09e52ebc3) | [2/3 black](https://github.com/nicolaspopravka/usd-render-benchmark/tree/46729937133729068f279e464784959667f09ab9) | [1/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/8daa2eeee2d9e2d969dc26472e5dfef4cf0fbe98) |
| CY2025 · Storm | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/20254fd1c5d17150de936d5716cbae2f144cc767) | [2/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/b162dd7ec760db2d73ca6f34e382b727c070e6be) | [1/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/cc22a590d380bfdeb1d74859824df0304ddb29bf) |
| CY2026 · Storm | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/b0ae01b750e713d61b9bfa1218b53fa4b9bdfef6) | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/48e351a2bee476b4bdcd7e23028ca47579325e54) | [0/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/7c5cb01a9837815e29cda594d623a014d0d12ea2) |
| Candidate CY2027 · Storm | [3/3 textured](https://github.com/nicolaspopravka/usd-render-benchmark/tree/35492323fb2648c69c0c560ce12512376d1bd59a) | [3/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/8a94d2e9e417af8dfaa1881d031aa308be3bed57) | [0/3 fallback](https://github.com/nicolaspopravka/usd-render-benchmark/tree/6b43bffc0ae3fd6cc2fc4008100d756ce05aecea) |

## Delegate coverage

| Delegate | Published results | Current state |
| --- | --- | --- |
| Cycles | **Published partial:** [CY2023](https://github.com/nicolaspopravka/usd-render-benchmark/tree/f6d2b5ec8c13add663a0e95219c1c9d81328de29) · [CY2024](https://github.com/nicolaspopravka/usd-render-benchmark/tree/fbb3ea60e0f8ed691c1002354097741302f9ba93) · [CY2025](https://github.com/nicolaspopravka/usd-render-benchmark/tree/fc634112bd3212071f983080c781d3dc122c2b34) · [CY2026](https://github.com/nicolaspopravka/usd-render-benchmark/tree/d3ed81b39eeed6b86bb1c5c74f5176c22ea27d2b) · [CY2027](https://github.com/nicolaspopravka/usd-render-benchmark/tree/c13b502a7cf3f5669ecc7392937d26640532494c) — two of four scenes produce images on each released stack. | **Follow-up:** patched [CY2026](https://github.com/nicolaspopravka/usd-render-benchmark/tree/b0d7bbfb5dbf85d4b3d5d89f82258eaf4ec68dd8) and [CY2027](https://github.com/nicolaspopravka/usd-render-benchmark/tree/da46aa746886dbfd730bf526486b30d3d2d92035) runs add OpenChessSet images after the merged empty-material fix. A newer patched [CY2027 four-scene run](https://github.com/nicolaspopravka/usd-render-benchmark/tree/e5c43595fc22d876a2790d68ec104eb9abbfac10) completes all four renderer processes, including Moana after deferred geometry deletion; its images retain material, texture, and exposure limitations. The changes are under review in Cycles [PR #78](https://projects.blender.org/blender/cycles/pulls/78), with UDIM discovery tracked separately in [#77](https://projects.blender.org/blender/cycles/issues/77). OptiX-enabled [CY2026](https://github.com/nicolaspopravka/aswf-docker/actions/runs/32348492265) and [CY2027](https://github.com/nicolaspopravka/aswf-docker/actions/runs/32348492179) images are built, but GPU rendering is not yet established. |
| MoonRay | **Published partial:** [CY2025 — three benchmark images, zero clean exits; Moana not run](https://github.com/nicolaspopravka/usd-render-benchmark/tree/f04463d97dedb644d1a81cb63d7d9b871188f980) · [tiled-texture and smooth-ALab follow-up](https://github.com/nicolaspopravka/usd-render-benchmark/tree/e0ec0768ddcd81140d80a3a4850c84a572936ee2) | **Follow-up:** MaterialX BSDF support remains limited ([#24](https://github.com/nicolaspopravka/usd-render-benchmark/issues/24)); refinement-zero smoothing and missing light-link handling are in hdMoonray [#11](https://github.com/OpenMoonRay/hdMoonray/pull/11) and [#12](https://github.com/OpenMoonRay/hdMoonray/pull/12). An [XPU-capable image](https://github.com/nicolaspopravka/aswf-docker/commit/e49bf97aecc71b12ef7bb3eff7841b3acbf0b2b5) exists, but automatic mode used the vector path for these scenes; no XPU benchmark result is claimed. |

Modern Karma, RenderMan, and Arnold coverage is **not scheduled**. The
[original Yard baseline](https://github.com/TheYardVFX/usd-render-benchmark)
remains the historical mixed-result reference.

## Findings and upstream follow-up

| State | Finding | Public record |
| --- | --- | --- |
| **Published finding** | Material support is limited across delegates. Cycles does not support MaterialX material networks and supports only a subset of `UsdPreviewSurface`, falling back to its default surface when no supported network is available. MoonRay 2026.29.1 does not support the MaterialX BSDF nodes used by OpenChessSet. | [Cycles #21](https://github.com/nicolaspopravka/usd-render-benchmark/issues/21) · [Cycles #25](https://github.com/nicolaspopravka/usd-render-benchmark/issues/25) · [MoonRay #24](https://github.com/nicolaspopravka/usd-render-benchmark/issues/24) |
| **Published finding** | The tested ASWF CI images do not provide the same working Storm/MaterialX stack as OpenUSD built with Pixar's `build_usd.py`. OpenChessSet renders textured with the Pixar build, while the corresponding ASWF Conan-based stacks produce fallback or black results with MaterialX errors. | [OpenUSD results](#openusd-delivery-paths) · [ASWF issues #454](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/454) and [#455](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/455) |
| **Published finding** | Lighting is not consistent across delegates. The same scene can render with very different exposure and light contribution, so these are stack results rather than look-matched comparisons. | [delegate results](#delegate-coverage) · [Yard baseline](https://github.com/TheYardVFX/usd-render-benchmark) |
| **Published finding** | Exit status does not describe the rendered result on its own. Some runs exit successfully with black or fallback output; others return nonzero after writing a coherent image. | [OpenUSD results](#openusd-delivery-paths) · [delegate results](#delegate-coverage) |
| **Waiting release** | The Cycles empty-material fix is merged; comparable CY2026/CY2027 reruns wait for a tagged release containing it. | [Cycles #75](https://projects.blender.org/blender/cycles/pulls/75) · [patched CY2026](https://github.com/nicolaspopravka/usd-render-benchmark/tree/b0d7bbfb5dbf85d4b3d5d89f82258eaf4ec68dd8) · [patched CY2027](https://github.com/nicolaspopravka/usd-render-benchmark/tree/da46aa746886dbfd730bf526486b30d3d2d92035) |
| **Waiting upstream** | Cycles Hydra diagnostics, AOV reporting, unresolved asset paths, and deferred geometry deletion are under review. UDIM tile discovery remains separate. | Cycles [PR #78](https://projects.blender.org/blender/cycles/pulls/78) · [issue #77](https://projects.blender.org/blender/cycles/issues/77) · [patched CY2027 run](https://github.com/nicolaspopravka/usd-render-benchmark/tree/e5c43595fc22d876a2790d68ec104eb9abbfac10) |
| **Waiting upstream** | MoonRay refinement-zero smoothing and missing light-link handling are awaiting upstream integration. | hdMoonray [#11](https://github.com/OpenMoonRay/hdMoonray/pull/11) and [#12](https://github.com/OpenMoonRay/hdMoonray/pull/12) are open |
| **Waiting upstream** | The ASWF OSL discovery plugin fails to load without `LD_PRELOAD`. | [Fork issue #3](https://github.com/nicolaspopravka/usd-render-benchmark/issues/3) · [aswf-docker #450](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/450) is open |
| **Waiting upstream** | Prebuilt CY2027 MaterialX resources resolve incorrectly and OpenChessSet uses fallback materials. | [Fork issue #10](https://github.com/nicolaspopravka/usd-render-benchmark/issues/10) · [aswf-docker #454](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/454) is open. Related workaround-removal [PR #453](https://github.com/AcademySoftwareFoundation/aswf-docker/pull/453) merged; it is not the fix for #454. |
| **Waiting upstream** | The ASWF-built CY2027 run reaches MaterialX GLSL compilation but fails on `AIRY_FRESNEL_ITERATIONS`. | [Fork issue #2](https://github.com/nicolaspopravka/usd-render-benchmark/issues/2) · [aswf-docker #455](https://github.com/AcademySoftwareFoundation/aswf-docker/issues/455) is open |
| **Waiting upstream** | Storm fails in the Ptex mipmap-loader path on two Moana Island subtrees. | OpenUSD [#4168](https://github.com/PixarAnimationStudios/OpenUSD/issues/4168) and [#4169](https://github.com/PixarAnimationStudios/OpenUSD/issues/4169) are open; crash-prevention [PR #4176](https://github.com/PixarAnimationStudios/OpenUSD/pull/4176) is under review |

Additional run-level findings are tracked in the
[benchmark issues](https://github.com/nicolaspopravka/usd-render-benchmark/issues).

## Community coordination

Use the
[Ideas discussion](https://github.com/nicolaspopravka/usd-render-benchmark/discussions/18)
to suggest delegate/version combinations, available hardware and drivers,
licensed-renderer interest, scenes, upstream relevance, and priorities.
Failures are valid results, and ASWF reference, Pixar control, and delegate
diagnostic runs remain separate.

This phase accepts feedback and coordination only. External code and benchmark
artifact submissions will wait until the MIT license and contribution terms
are restored on `main`.

## Reading the results

The default branch is intentionally a README-only landing page. Each result
link points to a pinned snapshot of the run's outputs whose README describes
the branch and whose `render_summary.md`, `logs/`, and `renderers/`
directories preserve the observed result.

A result README is a starting point, not a guarantee of exact replay. Unknown
or historically unrecorded inputs remain limitations rather than being
inferred.
