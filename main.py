from multiprocessing import Process
import time

import HHProbe
import Poster

def main():
    hhp = Process(target = HHProbe.Loop)
    poster = Process(target = Poster.Loop)
    hhp.start()
    poster.start()
    hhp.join()
    poster.join()

if __name__ == '__main__':
	main()
