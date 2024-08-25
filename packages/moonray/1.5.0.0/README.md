Package Description
===================

This Rez package configures an environment with MoonRay.

Build
-----

See [Building MoonRay on CentOS 7](https://github.com/dreamworksanimation/openmoonray/blob/openmoonray-1.5.0.0/building/Centos7/centos7_build.md) for explicit instructions. 

Note that this build excludes GPU and GUI support. First, the required RPM packages were installed as follows as root :
```
source building/Centos7/install_packages.sh --nocuda --noqt
```
Then, the `-DBUILD_QT_APPS=NO` and `-DMOONRAY_USE_CUDA=NO` options were used when configuring the CMake build of MoonRay itself.

Install
-------

The install command was run as follows as root :
```
cmake --install build --prefix /opt/openmoonray
```

References
----------
See [HdMoonRay Setup](https://docs.openmoonray.org/user-reference/tools/hydra/hdmoonray-setup/) for how to configure _hdMoonray_.
