from config import get_config
import sys
def init():
    sys.path.append(get_config().root+"/aether_reflect")
    