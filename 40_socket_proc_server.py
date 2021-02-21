'''Socket server: Realtime processing trial.


  https://docs.python.org/ja/3/library/socket.html

  > 常に同じ結果が必要であれば、 host に数値のアドレスを指定してください。

  2021. 2.21 Oda Daisuke

'''


import sys
import socket
import logging
import struct

import numpy as np
from utils import get_logger


# -----------------------------------------------------

def load(fname):
  return np.loadtxt(fname, delimiter='\n')

def process(data):
  return np.mean(data)

def save(fname, x):
  np.savetxt(fname, x)

# -----------------------------------------------------
logger = get_logger(__name__)



buffsize = 1024

# AF_INET address (host, port)
HOST = '127.0.0.1'
PORT = 50007  # Arbitrary non-privileged port
addr = (HOST, PORT)

fname_tmp = 'data/data_{dtstr:}.txt'
fname_feats_tmp = 'features/feats_{dtstr:}.txt'


# Create socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:

  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  server.bind(addr)
  logger.info(f'binded addr={addr}')

  server.listen(1)
  logger.info('listening ...')

  conn, addr = server.accept()  # get socket = make connection
  logger.debug(f'Connected by {addr}')

  with conn:

    while True:  # keep listening

      data = conn.recv(buffsize)

      if data:

        dtstr = data.decode() # data file path
        fname = fname_tmp.format(dtstr=dtstr)
        logger.info(f'recieved fname={fname}')

        try:
          data = load(fname)
        except FileNotFoundError as e:
          logger.error(e)
          data_send = 'error'.encode()
        else:
          logger.info(f'Loaded fname={fname}')
          stats = process(data)
          data_send = 'ok'.encode()

          fname = fname_feats_tmp.format(dtstr=dtstr)
          with open(fname, mode='w') as f:
            f.write(f'{stats:.2f}')

        conn.sendall(data_send)
        logger.debug(f'sent {stats}')
        logger.debug('--------------------------------')

      else:

        logger.info(f'Recieved no data. break')
        break

server.close()
logger.debug('Closed connection.')


