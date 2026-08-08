name = "usd"

version = "26.05"

requires = []


def commands():
    path = "/opt/usd"

    alias("usdrecord", "/workspace/usd-render-benchmark/tools/usdrecord_egl.py")

    env.PYTHONPATH.append(path + "/lib/python")
    env.PATH.append(path + "/bin")
