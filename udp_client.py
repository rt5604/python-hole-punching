import logging
import socket
import sys
from util import *
import sysutil

logger = logging.getLogger()

def main(host='127.0.0.1', port=9999):

    ipAddr = sysutil.get_ip()
    print('my ipAddr = {}'.format(ipAddr))

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP

    systemId = sysutil.getSystemSerial()
    data = systemId.encode('utf-8')
    print('data = {}'.format(data))
    sock.sendto(data, (host, port))

    count = 1

    while True:
        data, addr = sock.recvfrom(1024)
        print('client received: {} {}'.format(addr, data))
        addr = msg_to_addr(data)

        ipAddr = sysutil.get_ip()
        ipAddrEnc = ipAddr.encode()
        print('client: send {} to {}'.format(ipAddr, addr))
        sock.sendto(ipAddrEnc, addr)
        data, addr = sock.recvfrom(1024)
        print('client received: {} {}'.format(addr, data))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    main(*addr_from_args(sys.argv))
