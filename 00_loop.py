'''Loop: Realtime processing trial.


  2021. 2.21 Oda Daisuke

'''

import datetime
import time

names = ['aaa', 'bbb', 'ccc', 'ddd']

i = 0
while True:

    dt = datetime.datetime.now()
    dtstr = dt.strftime('%Y-%m-%d %H:%M:%S')

    try:
      name = names[i]
    except IndexError as e:
      print(e)
      break

    print(f'{name}: time:{dtstr}')

    time.sleep(2)

    i += 1


