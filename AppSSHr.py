import configparser
import os

import paramiko
from flask import Blueprint, Flask

app = Blueprint("app_sshr_blurprint", __name__, url_prefix="/sshr")


def config_sample_out():
    # ensure config file exists
    if os.path.exists("sshr.ini"):
        return
    conf = configparser.ConfigParser()
    conf.add_section("host-sample")
    conf.set("host-sample", "host", "192.168.1.1")
    conf.set("host-sample", "port", "22")
    conf.set("host-sample", "username", "root")
    conf.set("host-sample", "password", "password___")
    conf.set("host-sample", "cmd", "echo qqqqq")
    with open('sshr.ini', 'w') as fw:
        conf.write(fw)


def ssh_command_onetime(host, port, username, password, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=int(port), username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode())
    print('执行完毕')
    ssh.close()


@app.route("/session/<session_name>", methods=['GET'])
def session_name(session_name):
    config_sample_out()
    conf = configparser.ConfigParser()
    conf.read("sshr.ini")
    sections = conf.sections()
    if session_name not in sections:
        return {
            "server-name": "",
            "app": "SSHr",
            "message": f"find none of {session_name}",
            "code": 404
        }
    else:
        ssh_command_onetime(
            host=conf.get(session_name, "host"),
            port=conf.getint(session_name, "port"),
            username=conf.get(session_name, "username"),
            password=conf.get(session_name, "password"),
            cmd=conf.get(session_name, "cmd")
        )
        return {
            "server-name": "",
            "app": "SSHr",
            "message": f"{session_name} run done",
            "code": 200
        }


def init_app_sshr(server: Flask):
    config_sample_out()
    server.register_blueprint(app)
