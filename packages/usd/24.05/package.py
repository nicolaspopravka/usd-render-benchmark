name = "usd"

version = "24.05"

def commands():
    path = "/opt/usd"

    alias("usdrecord", "/workspace/usd-render-benchmark/tools/usdrecord_egl.py")

    env.PYTHONPATH.append(path + "/lib/python")
    env.PATH.append(path + "/bin")
