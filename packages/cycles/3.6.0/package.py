name = "cycles"

version = "3.6.0"

variants = [
    ["houdini-20.0.751"]
]

def commands():
    env.PXR_PLUGINPATH_NAME.append("/opt/cycles/houdini/dso/usd_plugins")
