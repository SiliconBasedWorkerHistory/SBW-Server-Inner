import configparser
import os
import sys

import paramiko
from flask import Blueprint, Flask

app = Blueprint("app_sshr_blurprint", __name__, url_prefix="/sshr")


class Session:
    host = None
    port = None
    username = None
    password = None
    cmd = None

    def __init__(self, host, port, username, password, cmd):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.cmd = cmd


class SessionConfig:
    def __init__(self):
        config_sample_out()
        self.conf = configparser.ConfigParser()
        self.conf.read("sshr.ini")

    def list_session_name(self):
        return self.conf.sections()

    def get_session_by_name(self, name):
        return Session(
            self.conf.get(name, "host"),
            self.conf.getint(name, "port"),
            self.conf.get(name, "username"),
            self.conf.get(name, "password"),
            self.conf.get(name, "cmd")
        )


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


def ssh_command_onetime1(session: Session):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=session.host,
                port=int(session.port),
                username=session.username,
                password=session.password
                )
    stdin, stdout, stderr = ssh.exec_command(session.cmd)
    print("err:", stderr.read().decode())
    print("out:", stdout.read().decode())
    print('执行完毕')
    ssh.close()


def ssh_command_onetime(host, port, username, password, cmd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=int(port), username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print("err:", stderr.read().decode())
    print("out:", stdout.read().decode())
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


def print_help(status):
    print("help:")
    print("AppSSHr.py <args>")
    print("session: s session used to perform session by names")
    print("list: l list used to list sessions")
    exit(status)


if __name__ == '__main__':

    session_config = SessionConfig()

    args = sys.argv[1:]
    if len(args) == 0:
        print_help(-1)
    if args[0] in ["-s", "--session"]:
        if len(args) >= 2:
            for i in args[1:]:
                tmp_session_names = session_config.list_session_name()
                if i not in tmp_session_names:
                    print(f"err: find none of session name {i}, skipped")
                else:
                    print(f"find session of {i}, performing...")
                    ssh_command_onetime1(session_config.get_session_by_name(i))
        else:
            print("err: please input session name")
    elif args[0] in ["-l", "--list"]:
        tmp = session_config.list_session_name()
        for i in range(len(tmp)):
            print(i + 1, tmp[i])
