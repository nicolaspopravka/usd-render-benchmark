name = "moonray"

version = "1.5.0.0"

variants = [
    ["usd-22.05"]
]

def commands():
    # setup environment variables to use release
    # see /opt/openmoonray/scripts/setup.sh

    path = "/opt/openmoonray"

    # NB required for Arras to function (it needs to find execComp)
    env.PATH.append(path + "/bin")

    # tell moonray where to find dsos
    env.RDL2_DSO_PATH.append(path + "/rdl2dso")

    # tell Arras where to find session files
    env.ARRAS_SESSION_PATH.append(path + "/sessions")

    # tell Hydra Ndr plugins where to find shader descriptions
    env.MOONRAY_CLASS_PATH.append(path + "/shader_json")

    # add Hydra plugins to path
    env.PXR_PLUGINPATH_NAME.append(path + "/plugin/usd")

    if True:
        # in-process render (if MoonRay crashes usdrecord crashes)
        env.HDMOONRAY_DEBUG_MODE = 1 
    else:
        unsetenv("REZ_MOONRAY_VERSION") # XXX usdrecord hangs otherwise with :
                                        # Error: Failed to create an Arras session: 
                                        # Failed to create local session :
                                        # Environment variable REZ2_DEFAULT_VERSION is not set
