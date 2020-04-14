import matplotlib.pyplot as plt
import os
import glob
import random

import numpy as np
from PIL import Image
import cv2

DATA_DIR = '/Volumes/Photos/flower_ai/'
CATEGORIES = ['tulip', 'garbera', 'anemone',
                'rose', 'cherryblossom', 'viola',
                'daisy', 'poppy', 'carnation']
IMG_SIZE = 50

def main():
    num_test_data = 30
    X_train = [] # 画像データ(学習用)
    X_test  = [] # 画像データ(評価用)
    y_train = [] # ラベル情報(学習用)
    y_test  = [] # ラベル情報(評価用)

    for class_index, category in enumerate(CATEGORIES):
        path = os.path.join(DATA_DIR, category)
        files = glob.glob(path + '/*.jpg')

        for i, file in enumerate(files):
            img_array = cv2.imread(file)
            img_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))

            if i < num_test_data:
                X_test.append(img_array)
                y_test.append(class_index)
            else:
                # -20度〜20度まで5度ずつ回転させる
                img = Image.fromarray(img_array)
                for angle in range(-20, 20, 5):
                    img_r = np.asarray(img.rotate(angle))
                    X_train.append(img_r)
                    y_train.append(class_index)

                    # 左右反転データも作成する
                    img_f = cv2.flip(img_r, 1)
                    X_train.append(img_f)
                    y_train.append(class_index)


    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    npy_fpath = DATA_DIR + 'flower.npy'
    np.save(npy_fpath, (X_train, X_test, y_train, y_test))


if __name__ == "__main__":
    main()
