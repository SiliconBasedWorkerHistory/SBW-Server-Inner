from flask import Flask
from configparser import ConfigParser
import os
import sys

from AppSSHr import init_app_sshr

app = Flask(__name__)


class ServerConfig:
    host = "0.0.0.0"
    port = 5000
    debug = True


class Config:
    config_file_name = "config.ini"
    config_section_name = "Global"
    server_config = None

    def __init__(self):
        self.server_config = ServerConfig()
        self.conf = ConfigParser()
        if not os.path.exists(self.config_file_name):
            self.conf.add_section(self.config_section_name)
            self.conf.set(self.config_section_name, "host", self.server_config.host)
            self.conf.set(self.config_section_name, "port", str(self.server_config.port))
            self.conf.set(self.config_section_name, "debug", str(self.server_config.debug))
            with open(self.config_file_name, 'w') as fw:
                self.conf.write(fw)
        else:
            self.conf.read(self.config_file_name)
            self.server_config.host = self.conf.get(self.config_section_name, "host")
            self.server_config.port = self.conf.getint(self.config_section_name, "port")
            self.server_config.debug = self.conf.getboolean(self.config_section_name, "debug")


init_app_sshr(app)

if __name__ == '__main__':
    c = Config()
    app.run(host=c.server_config.host, port=c.server_config.port, debug=c.server_config.debug)
