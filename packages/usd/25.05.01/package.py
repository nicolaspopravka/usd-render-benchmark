name = "usd"

version = "25.05.01"

variants = [
    ['embree-3.2.2']
]

def commands():
    path = "/usr/local"

    alias("usdrecord", "/workspace/usd-render-benchmark/tools/usdrecord_egl.py")

    env.PYTHONPATH.append(path + "/lib/python")
    env.PATH.append(path + "/bin")
