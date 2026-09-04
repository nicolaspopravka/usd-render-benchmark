name = "usd"

version = "26.08"

variants = [
    ['embree-4.3.3']
]

def commands():
    path = "/usr/local"

    alias("usdrecord", "/workspace/usd-render-benchmark/tools/usdrecord_egl.py")

    env.PYTHONPATH.append(path + "/lib/python")
    env.PATH.append(path + "/bin")
    env.HDEMBREE_USE_LIGHTING.set("1")
