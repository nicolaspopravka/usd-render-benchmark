name = "usd"

version = "23.08"

requires = []


def commands():
    path = "/usr/local"

    alias("usdrecord", "/workspace/usd-render-benchmark/tools/usdrecord_egl.py")

    env.PYTHONPATH.append(path + "/lib/python")
    env.PATH.append(path + "/bin")
