name = "cycles"

version = "3.6.0"

variants = [
    ["usd-23.08"]
]

def commands():
    path = "/opt/cycles"

    env.LD_LIBRARY_PATH.prepend(path + "/lib")
    env.PXR_PLUGINPATH_NAME.prepend(path + "/hydra")
