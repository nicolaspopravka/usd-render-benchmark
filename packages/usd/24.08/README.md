Package Description
===================

This Rez package configures an environment with USD.

Build
-----

The build of USD includes the Embree and RenderMan rendering backends for Hydra. The build script was run as root as follows :
```
python3 build_scripts/build_usd.py --embree --prman --prman-location /opt/pixar/RenderManProServer-26.1 /opt/pixar/USD-24.08
```

Reference
---------
See [RenderMan USD Imaging Plugin](https://openusd.org/docs/RenderMan-USD-Imaging-Plugin.html) for how to configure _hdPrman_.
