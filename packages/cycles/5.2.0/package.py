name = "cycles"

version = "5.2.0"

variants = [
    ["usd-26.03"]
]

def commands():
    path = "/opt/cycles"

    env.LD_LIBRARY_PATH.prepend(path + "/lib")
    env.PXR_PLUGINPATH_NAME.prepend(path + "/hydra")
