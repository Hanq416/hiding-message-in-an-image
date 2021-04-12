# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from time import time, sleep
import os
# notes: algorithm modification notice, skip overexposed pixel


class ImgEncryption(object):

    def __init__(self, fname, iname):
        self.info = fname
        self.img = iname

    def main(self):
        t1 = time()
        info_encrypted = self.encryption()
        img_embedded = self.info_embed(info_encrypted)
        self.imgwrite(img_embedded)
        t2 = time()
        print('Time consumption: %f sec\n' % (t2 - t1))
        input('Done, press [Enter] to exit...\n')
        exit(0)

    def fileload(self):
        f = open(self.info, 'r')
        message = f.readlines()
        f.close()
        mlist = ''
        for line in message:
            mlist += line
        msg = np.array([[ord(i)] for i in mlist])
        return msg

    def imgload(self):
        img = np.array(plt.imread(self.img))
        shape = [len(img), len(img[0])]
        return img, shape

    def imgwrite(self, image):
        plt.imsave('message_encrypted.png', image)

    def encryption(self):
        msg_array = self.fileload()
        key = input('Input a password for encryption [length: 4 to 16]\n')
        k_len = len(key)
        key_array = key * (len(msg_array) // k_len) + key[0:(len(msg_array) % k_len)]
        key_array = np.array([[ord(i)] for i in key_array])
        if len(key_array) != len(msg_array):
            print('key index not aligned...\n')
            sleep(1)
            exit(0)
        else:
            en_msg_array = msg_array ^ key_array
            print('message encryption.....OK!\n')
            return en_msg_array

    def info_embed(self, emsg):
        img_callback = self.imgload()
        img_shape = img_callback[1]
        img_array = img_callback[0]
        emsg_array = [[format(i[0], "b").zfill(9)] for i in emsg]
        emsg_bi = ''
        for bic in emsg_array:
            emsg_bi += bic[0]
        img_array = img_array.reshape(-1, 1)
        if len(emsg_bi) > len(img_array):
            print('Image space is not enough for embedding message.\n')
            sleep(2)
            exit(0)
        for j in range(len(emsg_bi)):
            if int(emsg_bi[j]):
                img_array[j][0] += 1
        return img_array.reshape(img_shape[0], img_shape[1], 3)


class ImgDecryption(object):

    def __init__(self, iname1, iname2):
        self.img_msg = iname1
        self.img_key = iname2

    def main(self):
        t1 = time()
        msg_bit = self.info_extraction()
        de_callback = self.decryption(msg_bit)
        self.message_write(de_callback[1],de_callback[0])
        t2 = time()
        print('Time consumption: %f sec\n' % (t2 - t1))
        input('Done, press [Enter] to exit...\n')
        exit(0)

    def info_extraction(self):
        img_tar = np.array(plt.imread(self.img_msg))
        img_original = np.array(plt.imread(self.img_key))
        if len(img_tar[0]) != len(img_original[0]) or len(img_tar) != len(img_original):
            input('critical error: image resolution not matched...press Enter to exit\n')
            exit(0)
        y = len(img_tar)
        x = len(img_tar[0])
        img_tar = img_tar.reshape(-1, 4)
        img_tar = np.delete(img_tar, [3], axis=1)
        img_tar = (img_tar * 255).astype(np.uint8).reshape(y, x, 3)
        bit_array = img_tar - img_original
        return bit_array.reshape(-1, 9)

    def decryption(self, bit_array):
        msg_array = []
        for i in range(len(bit_array)):
            bistr = ''
            for j in bit_array[i]:
                bistr += str(j)
            msg_array.append([int(bistr, 2)])
        msg_array = np.array(msg_array)
        key = input('Input a password for encryption [length: 4 to 16]\n')
        k_len = len(key)
        key_array = key * (len(msg_array) // k_len) + key[0:(len(msg_array) % k_len)]
        key_array = np.array([[ord(i)] for i in key_array])
        de_msg_array = msg_array ^ key_array
        print('message decryption.....OK!\n')
        return key, de_msg_array

    def message_write(self, msg_decrypted, dekey):
        msg_txt = ''
        ct = 0
        klen = len(dekey)
        for k in msg_decrypted:
            msg_txt += chr(k[0])
            if ct > klen:
                try:
                    if msg_txt[ct-klen:ct] == dekey:
                        msg_txt = msg_txt[:ct-klen]
                        break
                except Exception as err:
                    print(err)
            ct += 1
        fname = 'message_decrypted.txt'
        f = open(fname, 'w')
        f.write(msg_txt)
        f.close()


# embed & extract

def info_embed():
    while True:
        fpath = input('input the TEXT file name you want to hide in a image...\n')
        fpath = './' + fpath
        if os.path.exists(fpath):
            break
        else:
            print('Invalid txt file path...try again\n')
    while True:
        ipath = input('input the IMAGE name for embedding message...\n')
        ipath = './' + ipath
        if os.path.exists(ipath):
            break
        else:
            print('Invalid path...try again\n')
    sleep(1)
    print('OK...\n')
    imgen = ImgEncryption(fpath, ipath)
    imgen.main()


def info_extract():
    while True:
        ipath1 = input('input the [Message IMAGE] you want to get information...\n')
        ipath1 = './' + ipath1
        if os.path.exists(ipath1):
            break
        else:
            print('Invalid txt file path...try again\n')
    while True:
        ipath2 = input('input the [Original IMAGE] name for embedding message...\n')
        ipath2 = './' + ipath2
        if os.path.exists(ipath2):
            break
        else:
            print('Invalid path...try again\n')
    sleep(1)
    print('OK...\n')
    imgde = ImgDecryption(ipath1, ipath2)
    imgde.main()


# main function
print('Fun_Steganography\nHankun Li April, 1 2021\nver 1.0\n\n')
work_path = os.getcwd()
os.chdir(work_path)
while True:
    DoE = input('Encrypt [Enter E] or Decrypt [Enter D] message from Image?\n')
    if DoE in ['E', 'e']:
        info_embed()
        break
    elif DoE in ['D', 'd']:
        info_extract()
        break
    else:
        print('wrong input...\n')
