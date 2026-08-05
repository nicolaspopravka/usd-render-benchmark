name = "cycles"

version = "5.0.0"

variants = [
    ["usd-25.08"]
]

def commands():
    path = "/opt/cycles"

    env.LD_LIBRARY_PATH.prepend(path + "/lib")
    env.PXR_PLUGINPATH_NAME.prepend(path + "/hydra")
