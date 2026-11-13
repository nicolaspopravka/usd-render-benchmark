name = "openusd"

version = "26.08"


def commands():
    env.HD_DEFAULT_RENDERER = "GL"
    alias("usdrecord", "./tools/usdrecord_egl.py")
