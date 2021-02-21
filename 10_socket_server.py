'''Socket server: Realtime processing trial.


  https://docs.python.org/ja/3/library/socket.html

  > 常に同じ結果が必要であれば、 host に数値のアドレスを指定してください。

  2021. 2.21 Oda Daisuke

'''


import sys
import socket
import logging


import numpy as np
from .utils import get_logger


def load(fname):
  return np.loadtxt(fname)

def process(data):
  return np.mean(data)

# -----------------------------------------------------
logger = get_logger(__name__)


buffsize = 1024

# AF_INET address (host, port)
HOST = '127.0.0.1'
PORT = 50007  # Arbitrary non-privileged port
addr = (HOST, PORT)



# Create socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.bind(addr)
  logger.debug('bind')
  server.listen(1)
  logger.debug('listen')
  conn, addr = server.accept()  # get socket = make connection
  logger.debug('accepted')
  with conn:
    logger.debug(f'Connected by {addr}')
    while True:  # keep listening
      data = conn.recv(buffsize)  # buffsize = 1024
      logger.debug(f'recieved data={data}')
      if data:
        idx = int.from_bytes(data, sys.byteorder)
        logger.debug(f'recieved idx={idx}')
        try:
          name = names[idx]
        except IndexError as e:
          logger.error(e)
          data_send = 'error'.encode()
        else:
          data_send = name.encode()
        conn.sendall(data_send)
        logger.debug(f'sent {data_send}')
        logger.debug('--------------------------------')
      else:
        logger.info(f'no data recieved. break')
        break

server.close()
logger.debug('Closed connection.')


