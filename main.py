from multiprocessing import Process

import HHProbe
import Poster

def main():
	 hhp = Process(target = HHProbe.Loop, args = (, ))
	 poster = Process(target = Poster.Loop, args = (, ))
	 hhp.start()
	 poster.start()
	 hhp.join()
	 poster.join()

if __name__ == '__main__':
	main()
