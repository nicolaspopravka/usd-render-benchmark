name = "usd"

version = "20.11"

variants = [
    ["maya==2022"]
]

def commands():
    path = "/usr/autodesk/mayausd/maya2022/0.8.0_202102180129-2f83c8f/mayausd/USD2"

    env.PYTHONPATH.append(path + "/lib/python")
    env.PATH.append(path + "/bin")
