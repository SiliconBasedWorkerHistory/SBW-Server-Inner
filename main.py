import configparser
import os

from flask import Flask

from AppSSHr import init_app_sshr

app = Flask(__name__)


class Config:
    def __init__(self):
        if os.path.exists("server_config.ini"):
            return
        conf = configparser.ConfigParser()
        conf.add_section("server")
        conf.set("server", "name", "inner-server")
        conf.set("server", "host", "0.0.0.0")
        conf.set("server", "port", "22")
        conf.set("server", "debug", "True")
        with open('server_config.ini', 'w') as fw:
            conf.write(fw)


def config_sample_out():
    # ensure config file exists
    if os.path.exists("server_config.ini"):
        return
    conf = configparser.ConfigParser()
    conf.add_section("server")
    conf.set("server", "name", "inner-server")
    conf.set("server", "host", "0.0.0.0")
    conf.set("server", "port", "22")
    conf.set("server", "debug", "True")
    with open('server_config.ini', 'w') as fw:
        conf.write(fw)


init_app_sshr(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
