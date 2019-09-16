import struct
import time

import lmdb
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

me = lmdb.open("/var/HHPP/me")
us = lmdb.open("/var/HHPP/us")
asia = lmdb.open("/var/HHPP/asia")
eur = lmdb.open("/var/HHPP/eur")


def plot():
    my_quality = me.begin()
    us_quality = us.begin()
    asia_quality = asia.begin()
    eur_quality = eur.begin()
    cur = my_quality.cursor()
    key_list = []
    for index, (key, value) in enumerate(cur):
        key_list.append(struct.unpack("d", key)[0])
        if index / 14400 > 0:
            key_list.sort(reverse=True)
            key_list = key_list[:14400]
    key_list.sort()
    print(len(key_list))
    myself = list(map(lambda x: struct.unpack("i", my_quality.get(struct.pack("d", x)))[0], key_list))
    glo = list(map(lambda x: struct.unpack("i", us_quality.get(struct.pack("d", x)))[0], key_list))
    cn = list(map(lambda x: struct.unpack("i", asia_quality.get(struct.pack("d", x)))[0], key_list))
    fr = list(map(lambda x: struct.unpack("i", eur_quality.get(struct.pack("d", x)))[0], key_list))
    plt.title('Quality')
    plt.plot(key_list, myself, color='green', label='myself')
    plt.plot(key_list, glo, color='red', label='us')
    plt.plot(key_list, cn, color='blue', label='asia')
    plt.plot(key_list, fr, color='black', label='eur')
    # plt.legend()
    plt.xlabel('time')
    plt.ylabel('quality')
    this_time = "plot.jpg"
    # this_time = str(time.time())+".jpg"
    plt.savefig(this_time)
    return this_time
    # plt.show()


if __name__ == '__main__':
    plot()
