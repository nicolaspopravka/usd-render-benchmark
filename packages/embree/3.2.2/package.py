name = "embree"

version = "3.2.2"

def commands():
    path = "/opt/hdembree/hydra"

    env.PXR_PLUGINPATH_NAME.append(path)
