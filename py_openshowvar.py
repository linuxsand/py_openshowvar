'''
A Python port of KUKA VarProxy client (OpenShowVar).
'''

from __future__ import print_function
import sys
import struct
import random
import socket

PY2 = sys.version_info[0] == 2
if PY2: input = raw_input

ENCODING = 'utf-8'

class openshowvar(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.msg_id = random.randint(1, 100)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.ip, self.port))
        except socket.error:
            pass
        
    def test_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ret = sock.connect_ex((self.ip, self.port))
            return ret == 0
        except socket.error:
            print('socket error')
            return False

    can_connect = property(test_connection)

    def read(self, var, debug=True):
        if not isinstance(var, str):
            raise Exception('Var name is a string')
        else:
            self.varname = var if PY2 else var.encode(ENCODING)
        return self._read_var(debug)

    def write(self, var, value, debug=True):
        if not (isinstance(var, str) and isinstance(value, str)):
            raise Exception('Var name and its value should be string')
        self.varname = var if PY2 else var.encode(ENCODING)
        self.value = value if PY2 else value.encode(ENCODING)
        return self._write_var(debug)

    def _read_var(self, debug):
        req = self._pack_read_req()
        self._send_req(req)
        _value = self._read_rsp(debug)
        print(_value)
        return _value

    def _write_var(self, debug):
        req = self._pack_write_req()
        self._send_req(req)
        _value = self._read_rsp(debug)
        print(_value)
        return _value

    def _send_req(self, req):
        self.rsp = None
        self.sock.sendall(req)
        self.rsp = self.sock.recv(256)

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
        if self.rsp is None: return None
        var_value_len = len(self.rsp) - struct.calcsize('!HHBH') - 3
        result = struct.unpack('!HHBH'+str(var_value_len)+'s'+'3s', self.rsp)
        _msg_id, body_len, flag, var_value_len, var_value, isok = result
        if debug:
            print('[DEBUG]', result)
        if result[-1].endswith(b'\x01') and _msg_id == self.msg_id:   # todo
            self.msg_id += 1
            return var_value

    def close(self):
        self.sock.close()

def minus_ov_pro(ip, port):
    foo = openshowvar(ip, port)
    if not foo.can_connect:
        print('connection error')
        import sys
        sys.exit(-1)
    foo.write('$OV_PRO', str(random.randint(30, 50)))
    print('start: $OV_PRO minus one, until zero')

    ov = int(current_ov)
    for i in range(ov, 0, -1):
        foo.write('$OV_PRO', str(i))

def run_shell(ip, port):
    foo = openshowvar(ip, port)
    if not foo.can_connect:
        print('connection error')
        import sys
        sys.exit(-1)
    print('\nConnected KRC Name: ', end=' ')
    foo.read('$ROBNAME[]', False)
    while True:
        data = input('\nInput var_name [, var_value]\n(`q` for quit): ')
        if data.lower() == 'q':
            print('Bye')
            foo.close()
            break
        else:
            parts = data.split(',')
            if len(parts) == 1:
                foo.read(data.strip(), True)
            else:
                foo.write(parts[0], parts[1].lstrip(), True)

     
if __name__ == '__main__':
    # minus_ov_pro('127.0.0.1', 7001)
    ip = input('IP Address: ')
    port = input('Port: ')
    run_shell(ip, int(port))

