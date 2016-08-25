'''
A Python port of KUKA Varproxy client (OpenShowVar).

run test() to see usage.
'''

import struct
import random
import socket

class openshowvar(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.msg_id = random.randint(1, 100)

    def read(self, var):
        if not isinstance(var, str):
            raise Exception('Var name is a string')
        else:
            self.varname = var
        return self._read_var()

    def write(self, var, value):
        if not (isinstance(var, str) and isinstance(value, str)):
            raise Exception('Var name and its value should be string')
        self.varname = var
        self.value = value
        return self._write_var()

    def _read_var(self):
        req = self._pack_read_req()
        self._send_req(req)
        _value = self._read_rsp()
        print '[read req] data recv:', _value
        return _value

    def _write_var(self):
        req = self._pack_write_req()
        self._send_req(req)
        _value = self._read_rsp()
        print '[write req] data recv:', _value
        return _value

    def _send_req(self, req):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.port))
        sock.sendall(req)
        self.rsp = sock.recv(256)
        sock.close()

    def _pack_read_req(self):
        var_name_len = len(self.varname)
        flag = 0
        req_len = var_name_len + 3

        return struct.pack(
            '!HHBH'+str(var_name_len)+'s',
            self.msg_id,
            req_len,
            flag,
            var_name_len,
            self.varname
            )

    def _pack_write_req(self):
        var_name_len = len(self.varname)
        flag = 1
        value_len = len(self.value)
        req_len = var_name_len + 3 + 2 + value_len

        return struct.pack(
            '!HHBH'+str(var_name_len)+'s'+'H'+str(value_len)+'s',
            self.msg_id,
            req_len,
            flag,
            var_name_len,
            self.varname,
            value_len,
            self.value
            )

    def _read_rsp(self, debug=False):
        var_value_len = len(self.rsp) - struct.calcsize('!HHBH') - 3
        result = struct.unpack('!HHBH'+str(var_value_len)+'s'+'3s', self.rsp)
        _msg_id, body_len, flag, var_value_len, var_value, isok = result
        if debug:
            print result,
        if result[-1].endswith('\x01') and _msg_id == self.msg_id:   # todo
            self.msg_id += 1
            return var_value

def test():
    foo = openshowvar('192.168.19.247', 7000)

    foo.write('$OV_PRO', str(random.randint(30, 50)))
    current_ov = foo.read('$OV_PRO')
    print 'start: $OV_PRO minus one, until zero'

    counter = int(current_ov)
    for i in range(int(current_ov)):
        foo.write('$OV_PRO', str(counter - 1))
        counter -= 1

if __name__ == '__main__':
    test()
