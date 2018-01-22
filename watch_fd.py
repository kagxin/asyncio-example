import asyncio
import socket
import logging

logging.getLogger('asyncio').setLevel(logging.DEBUG)


HOST = 'localhost'
PORT = 8003
ADDR = (HOST, PORT)


def print_read_data(sock, loop):  # 读事件的回调函数
    data = sock.recv(1024)
    print(data.decode())


def stop_loop(loop, sock):
    sock.close()
    loop.stop()


def main():
    sock = socket.socket()
    sock.bind(ADDR)
    sock.listen(1)
    c_sock, _ = sock.accept()  # 只接受一个客户端

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.add_reader(c_sock, print_read_data, c_sock, loop)  # 监控客户端描述符的读事件,出现读事件触发回调函数
    loop.call_at(loop.time()+50, stop_loop, loop, c_sock)  # 在50s之后停掉主事件循环

    try:
        loop.run_forever()
    finally:
        sock.close()
        loop.close()


if __name__ == '__main__':
    """
    可以使用 telnet localhost 8003 进行测试.
    """
    main()
