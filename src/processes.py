import os
import subprocess
import getpass

def start(cfgfile, upfile=None):
    try:
        os.path.exists(upfile)
        autharg = ["--auth-user-pass", upfile]
    except FileNotFoundError:
        u = os.getenv("IPVANISH_AUTH_USER")
        p = os.getenv("IPVANISH_AUTH_PASSWORD")
        if not (u or p):
            raise RuntimeError
        else:
            cmd_append = [""]
            print(f"user/password file {upfile} not found - falling back to environment!")

    # must be run as root

    cmd = ['sudo', 'openvpn', 
            '--ca', 'tests/configs/ca.ipvanish.com.crt', 
            '--auth-user-pass', '"$HOME/.up"']
    cmd += ["--config", cfgfile]
    cmd += ["--user", getpass.getuser()]
    cmd += autharg
    print(cmd)
    with open("ipvanish.log", "a+") as logf:
        c = subprocess.Popen(cmd, stdout=logf, stderr=logf)
    with open("ipvanish.pid", "w+") as pidf:
        print(c.pid)
        pidf.write(str(c.pid))


def stop(self):
    with open(f"ipvanish.pid", "r") as pidf:
        p = pidf.read()


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            start(cfgfile="tests/configs/ipvanish-RS-Belgrade-beg-c01.ovpn", upfile="/home/zeebrow/.up")
        elif "stop" == sys.argv[1]:
            stop()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("no")
        sys.exit(1)

# sudo openvpn --config configs/ipvanish-RS-Belgrade-beg-c01.ovpn --ca configs/ca.ipvanish.com.crt     --user zeebrow --auth-user-pass "$HOME/.up"
