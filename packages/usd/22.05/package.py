name = "usd"

version = "22.05"

def commands():
    path = "/usr/local"

    env.PYTHONPATH.append(path + "/lib/python")
    env.PATH.append(path + "/bin")
