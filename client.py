import struct
import socket
import time

NTP_SERVER = '127.0.0.1'
NTP_PORT = 123
NTP_PACKET_FORMAT = '!12I'
NTP_DELTA = 2208988800

def get_ntp_time():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, (NTP_SERVER, NTP_PORT))
    data, address = client.recvfrom(1024)
    client.close()

    unpacked_data = struct.unpack(NTP_PACKET_FORMAT, data[0:struct.calcsize(NTP_PACKET_FORMAT)])
    timestamp = unpacked_data[10] + float(unpacked_data[11]) / 2**32 - NTP_DELTA

    return timestamp

if __name__ == '__main__':
    ntp_time = get_ntp_time()
    current_time = time.ctime(ntp_time)
    print("Текущее время: ", current_time)