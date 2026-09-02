name = "embree"

version = "4.3.3"

def commands():
    path = "/opt/hdembree/hydra"

    env.PXR_PLUGINPATH_NAME.append(path)
