name = "rfh"

version = "26.1"

requires = [
    'houdini'
]

def commands():
    env.HOUDINI_PACKAGE_DIR.append("/opt/pixar/RenderManForHoudini-26.1/packages")

    env.PATH.prepend("{root}/bin")  # Local patched version of usdrecord
