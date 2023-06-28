import struct
import time
import socket

FORMAT = '!B B B b 11I'
SNTP_DIFF = 2208988800

class SNTPPacket:

    def __init__(self, delay_seconds=0, mode=4):
        self.leap = 0
        self.version = 4
        self.mode = mode
        self.stratum = 2
        self.poll = 10
        self.precision = 0
        self.root_delay = 0
        self.root_dispersion = 0x0aa7
        self.ref_id = 0x808a8c2c
        timestamp = time.time() + delay_seconds + SNTP_DIFF
        self.reference_timestamp = timestamp
        self.originate_timestamp = timestamp
        self.receive_timestamp = timestamp
        self.transmit_timestamp = timestamp

    def to_bytes(self):
        return struct.pack(FORMAT,
                           (self.leap << 6 | self.version << 3 | self.mode),
                           self.stratum,
                           self.poll,
                           self.precision,
                           self.root_delay,
                           self.root_dispersion,
                           self.ref_id,
                           int(self.reference_timestamp),
                           self.frac(self.reference_timestamp),
                           int(self.originate_timestamp),
                           self.frac(self.originate_timestamp),
                           int(self.receive_timestamp),
                           self.frac(self.receive_timestamp),
                           int(self.transmit_timestamp),
                           self.frac(self.transmit_timestamp))

    def frac(self, timestamp):
        return int(abs(timestamp - int(timestamp)) * 2**32)

if __name__ == '__main__':
    with open('delay.txt') as f:
        delay_seconds = int(f.read())

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('127.0.0.1', 123))

        while True:
            data, addr = sock.recvfrom(1024)
            print(addr)
            packet = SNTPPacket(delay_seconds)
            sock.sendto(packet.to_bytes(), addr)