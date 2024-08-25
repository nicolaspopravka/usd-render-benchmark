name = "usd"

version = "24.08"

variants = [
    ['prman-26.1', 'embree-3.3.2']
]

def commands():
    env.PYTHONPATH.append("/opt/pixar/USD-24.08/lib/python")
    env.PATH.append("/opt/pixar/USD-24.08/bin")

    # Running hdPrman
    # See https://openusd.org/docs/RenderMan-USD-Imaging-Plugin.html

    path = "/opt/pixar/RenderManProServer-26.1"
    usd_path = "/opt/pixar/USD-24.08"

    # Directory where Pixar's RenderMan is installed
    env.RMANTREE.append(path)
 
    # Search path for RenderMan OSL shader plugins
    env.RMAN_SHADERPATH.append(path + "/lib/shaders")
    env.RMAN_SHADERPATH.append(usd_path + "/plugin/usd/resources/shaders")

    # Search path for RenderMan RIS shading plugins
    env.RMAN_RIXPLUGINPATH.append(path + "/lib/plugins")

    # Search path for textures and RenderMan Rtx plugins
    env.RMAN_TEXTUREPATH.append(path + "/lib/textures")
    env.RMAN_TEXTUREPATH.append(path + "/lib/plugins")
    env.RMAN_TEXTUREPATH.append(usd_path + "/plugin/usd")
