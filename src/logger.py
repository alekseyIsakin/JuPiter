import logging as lg

def initLogger():
  lg.basicConfig(format='[%(asctime)s][%(filename)s][%(levelname)s] %(message)s', level=lg.DEBUG)