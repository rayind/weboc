__author__ = 'Ray'
from parsers import XmlParser
import socket
from handler import Handler
from typedbytes import Input
from protocol_reader import ProtocolReader
protocol = ProtocolReader(file("Protocol.xml"))
handler =  Handler()

parser = XmlParser(protocol, handler)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8088))
sock.listen(5)
while True:
    connection,address = sock.accept()
    try:
        connection.settimeout(5)
#        buf = connection.makefile()
#        input = Input(buf)
#        print input.read_byte()
        buf = connection.recv(1024)
        parser.parse(buf[:-1])
        #if buf == '1':
        #    connection.send('welcome to server!')
        #else:
#            connection.send('please go out!')
    except socket.timeout:
        print 'time out'
connection.close()
