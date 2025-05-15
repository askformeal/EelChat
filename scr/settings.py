import json
import os.path

from scr.eel_logger import EelLogger

class Settings():
    def __init__(self, root):
        self.root = root
        self.path = './settings.json'

    def load(self):
        settings = {}
        if os.path.exists(self.path):
            with open(self.path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        else:
            with open(self.root.DATA_PATHS['default_settings'], 
                      'r', encoding='utf-8') as f1:
                settings = json.load(f1)
                with open(self.path, 'w', encoding='utf-8') as f2:
                    json.dump(settings, f2)

        self.host = settings['network']['host']
        self.port = settings['network']['port']
        self.max_listen = settings['network']['max_listen']
        
        self.log_path = settings['log']['path']
        self.log_level = settings['log']['level']
        self.log_max_size = settings['log']['max_bytes']