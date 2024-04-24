class Config:
    def __init__(self):
        self.root=""


g_config=Config()
g_config.root="D:/dev/AetherReflect"


def get_config():
    return g_config
