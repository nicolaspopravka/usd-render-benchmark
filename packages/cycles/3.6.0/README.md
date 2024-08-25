Package Description
===================

This Rez package configures an environment with Cycles.

Build
-----

The build command was run as follows :
```
make update
mkdir build && cd build
cmake -DHOUDINI_ROOT=/opt/hfs20.0.751 -DWITH_CXX11_ABI=OFF -DCMAKE_INSTALL_PREFIX=/opt/cycles ..
make
```

Install
-------

The install command was run as follows as root :
```
cd build
make install
```

References
----------
See [Cycles Renderer](https://projects.blender.org/blender/cycles) on GitHub.

