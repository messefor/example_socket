'''Socket client: Realtime processing trial.


  https://docs.python.org/ja/3/library/socket.html

  > 常に同じ結果が必要であれば、 host に数値のアドレスを指定してください。

  2021. 2.21 Oda Daisuke

'''

import sys
import socket
import logging
import datetime
import struct
import time

import numpy as np

from utils import get_logger


# -----------------------------------------------------


def save(fname, x):
  np.savetxt(fname, x)

def gather_data(nrows=5, sleep_sec=0.5):
  vs = []
  for _ in range(nrows):
    v = np.random.uniform(-100, 100)
    logger.debug(f'extracted data value={v}')
    vs.append(v)
    time.sleep(sleep_sec)
  data = np.array(vs)
  return data

# -----------------------------------------------------


logger = get_logger(__name__)

dtstr = datetime.datetime.now().strftime('%H%M%S')
fname = f'data/data_{dtstr:}.txt'

buffsize = 1024

# AF_INET address (host, port)
HOST = '127.0.0.1'
PORT = 50007  # Arbitrary non-privileged port
addr = (HOST, PORT)

data = gather_data(nrows=5)

save(fname, data)
logger.info(f'Saved: {fname}')
logger.debug('-' * 40)

# Create socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

  client.connect(addr)  # make connection
  logger.debug(f'connected {addr}')

  data_send = dtstr.encode()
  client.sendall(data_send)
  logger.debug(f'sent data_send={data_send}')

  data_rcv = client.recv(buffsize)  # buffsize = 1024
  # data_rcv_str = struct.unpack('<1f', data_rcv)[0]
  # logger.debug(f'recieved stat={data_rcv_str:.3f}')

  msg = data_rcv.decode()
  logger.debug(f'recieved msg={msg}')

client.close()
logger.debug('Closed connection.')



