from icecream import ic
import io
import socket
import sys

def auth(sock: socket.socket, xauthority):
    sys_byteorder = sys.byteorder
    assert(sys_byteorder == "little")

    byteorder = 0x6c # little
    align_byteorder = 0x00

    major = 11
    minor = 0

    auth_proto = xauthority.name
    align_proto = bytes(len(auth_proto) % 2)
    auth_proto_len = len(auth_proto)

    auth_data = xauthority.data
    auth_data_len = len(auth_data)
    align_data = bytes(len(auth_data) % 2)

    def itob(i: int, len):
        return i.to_bytes(len, byteorder=sys_byteorder, signed=False)

    def stob(s: str):
        return s.encode(encoding="ascii")

    # rw = socket.SocketIO(sock, mode="rw")
    rw = io.BytesIO()
    rw.write(itob(byteorder, 1))
    rw.write(itob(align_byteorder, 1))
    rw.write(itob(major, 2))
    rw.write(itob(minor, 2))
    rw.write(itob(ic(auth_proto_len), 2))
    rw.write(itob(ic(auth_data_len), 2))
    rw.write(stob(auth_proto))
    rw.write(ic(align_proto))
    rw.write(auth_data)
    rw.write(ic(align_data))
    rw.flush()

    sock.send(ic(rw.getvalue()))
    data = sock.recv(1024)
    # data = rw.readall()
    assert(ic(data[0]) == 2)

def main(xauthority, display):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    sock.settimeout(10)
    sock.connect(ic(f"/tmp/.X11-unix/X{display.display}"))

    auth(sock, xauthority)


    




