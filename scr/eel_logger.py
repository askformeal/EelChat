import logging

class EelLogger(logging.Logger):
    def __init__(self, root, name, level = logging.DEBUG):
        super().__init__(name, level)
        self.root = root
        
        path = self.root.settings.log_path
        max_size = self.root.settings.log_max_size
        
        handler = logging.handlers.RotatingFileHandler(path, maxBytes=max_size)
        tmp = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(tmp)
        self.addHandler(handler)