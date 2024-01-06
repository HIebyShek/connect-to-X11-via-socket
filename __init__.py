import io
import os
import argparse
import socket

import main

env_var_xauthority = "XAUTHORITY";
env_var_display = "DISPLAY"
DISPLAY = os.environ[env_var_display]
XAUTHORITY = os.environ[env_var_xauthority]

args_parser = argparse.ArgumentParser()
args_parser.add_argument("--xauthority", default=XAUTHORITY)
args_parser.add_argument("--display", default=DISPLAY)


def read_file(path: os.PathLike):
    with open(path, mode="+rb") as f:
        return f.read()

class Display:
    def __init__(self, display: str):
        [self.hostname, display_dot_screen] = display.split(":")
        if not self.hostname:
            self.hostname = socket.gethostname()

        ds = display_dot_screen.split(".")
        self.display = int(ds[0])
        if len(ds) == 1:
            self.screen = 0

    def __repr__(self):
        return self.__dict__.__repr__();

class XAuth:
    def __init__(self, reader: io.BytesIO):

        def btoi(bytes):
            return int.from_bytes(bytes, byteorder="big", signed=False)
        
        FAMILY_LEN = 2
        LEN = 2
        self.family = btoi(reader.read(FAMILY_LEN))
        
        host_len = btoi(reader.read(LEN))
        self.hostname = reader.read(host_len).decode(encoding="ascii")

        display_len = btoi(reader.read(LEN))
        self.display = int(reader.read(display_len))

        name_len = btoi(reader.read(LEN))
        self.name = reader.read(name_len).decode(encoding="ascii")

        data_len = btoi(reader.read(LEN))
        self.data = reader.read(data_len)
    
    def __repr__(self):
        return self.__dict__.__repr__();
        


from icecream import ic
if __name__ == "__main__":
    args = args_parser.parse_args()
    xauth_data = read_file(args.xauthority)
    reader = io.BytesIO(xauth_data)
    xauths = []
    while reader.tell() < len(reader.getvalue()):
        xauths.append(XAuth(reader))

    display = Display(args.display)

    def eq_hostname_display(xauth):
        return xauth.hostname == display.hostname and \
               xauth.display == display.display

    xauthority = next(filter(eq_hostname_display, xauths))

    main.main(xauthority, display)