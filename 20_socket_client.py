'''Socket client: Realtime processing trial.


  https://docs.python.org/ja/3/library/socket.html

  > 常に同じ結果が必要であれば、 host に数値のアドレスを指定してください。

  2021. 2.21 Oda Daisuke

'''

import sys
import socket
import logging

import numpy as np

from .utils import get_logger


logger = get_logger(__name__)

buffsize = 1024


# AF_INET address (host, port)
HOST = '127.0.0.1'
PORT = 50007  # Arbitrary non-privileged port
addr = (HOST, PORT)


# Create socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:

  client.connect(addr)  # make connection
  logger.debug('connected')

  for i in range(10):
    ind = np.random.randint(0, 3)
    data = bytes([ind])
    client.sendall(data)
    logger.debug(f'i={i} sent data={data}')

    data_rcv = client.recv(buffsize)  # buffsize = 1024
    data_rcv_str = data_rcv.decode()
    logger.debug(f'i={i} recieved name={data_rcv_str}')

client.close()
logger.debug('Closed connection.')



