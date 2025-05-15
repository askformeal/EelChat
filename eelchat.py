import logging.handlers
import socket
import tkinter as tk
import logging
import sys
import os

from scr.settings import Settings
from scr.contact import Contact
from scr.eel_logger import EelLogger

class EelChat():
    def __init__(self):
        self.version = 'v0.0.0'

        self.DATA_PATHS = {
            'icon': './data/icon.svg',
            'send_icon' : './data/send.svg',
            'default_settings' : './data/default_settings.json'
        }
        

        self.settings = Settings(self)
        self.settings.load()

        self.WIDTH = 800
        self.HEIGHT = 500
        self.TITLE = 'EelChat - Demons1014'

        """ self.logger = logging.getLogger('root')
        self.logger.setLevel(self.settings.log_level)
        handler = logging.handlers.RotatingFileHandler(self.settings.log_path,
                                                       maxBytes=self.settings.log_max_size)
        tmp = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(tmp)
        self.logger.addHandler(handler) """
        self.logger = EelLogger(self, 'root', self.settings.log_level)

        self.check_files()
        
        self.win = tk.Tk()
        self.setup_win()

    def check_files(self):
        for name, path in self.DATA_PATHS.items():
            if os.path.exists(path):
                self.logger.debug(f'\"{name}\" file {path} found')
            else:
                self.logger.critical(f'\"{name}\" file {path} not found')
                self.exit_eel(1)

    def setup_win(self):
        self.win.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.win.title(self.TITLE)
        self.win.iconbitmap('./data/icon.ico')
        # self.win.iconphoto(False, tk.PhotoImage(file='./data/icon.png'))
        self.win.protocol('WM_DELETE_WINDOW', self.exit_eel)

    def send(self, msg: str, target: Contact):
        with socket.socket() as sender:
            sender.connect((target.ip, target.port))
            msg = f'{msg}'
            self.logger.debug(f'Send to {target.ip}:{target.port}: {msg}')
            sender.send(msg.encode('utf-8'))
            recv_data = sender.recv(1024).decode('utf-8')
            self.logger.debug(f'Received from {target.ip}:{target.port}: {recv_data}')

    def listen(self):
        with socket.socket() as listener:
            listener.bind(self.settings.host, self.settings.port)
            tmp = listener.accept(self.settings.max_listen)
            
            conn: socket.socket = tmp[0]
            address: int = tmp[1]

            recv_data = conn.recv(1024).decode('utf-8')
            self.logger.debug(f'Received from {address}: {recv_data}')
            conn.send("Got it".encode('utf-8'))


    def exit_eel(self, code: int=0):
        try:
            self.logger.debug('Exit EelChat')
            self.win.destroy()
            self.win.quit()
        except Exception:
            pass
        sys.exit(code)
        

    def main(self):
        self.logger.debug('EelChat started')
        self.win.mainloop()

if __name__ == '__main__':
    eelchat = EelChat()
    eelchat.main()