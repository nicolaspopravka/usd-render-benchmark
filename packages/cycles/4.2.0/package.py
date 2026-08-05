name = "cycles"

version = "4.2.0"

variants = [
    ["usd-24.05"]
]

def commands():
    path = "/opt/cycles"

    env.LD_LIBRARY_PATH.prepend(path + "/lib")
    env.PXR_PLUGINPATH_NAME.prepend(path + "/hydra")
