import os
import glob
import random

import numpy as np
from PIL import Image

DATA_DIR = '/Volumes/Photos/flower_ai/'
DATASET_FNAME = 'flower.npy'
# CATEGORIES = ['tulip', 'garbera', 'anemone',
#                 'rose', 'cherryblossom', 'viola',
#                 'daisy', 'poppy', 'carnation']
CATEGORIES = ['tulip', 'garbera', 'rose']
IMG_SIZE = 50

def main():
    num_data = 290
    num_test_data = 100
    X_train = [] # 画像データ(学習用)
    X_test  = [] # 画像データ(評価用)
    y_train = [] # ラベル情報(学習用)
    y_test  = [] # ラベル情報(評価用)

    for class_index, category in enumerate(CATEGORIES):
        path = os.path.join(DATA_DIR, category)
        files = glob.glob(path + '/*.jpg')

        for i, file in enumerate(files):
            if i > num_data: break

            img = Image.open(file)
            img = img.convert("RGB")
            img = img.resize((IMG_SIZE, IMG_SIZE))

            if i < num_test_data:
                X_test.append(np.asarray(img))
                y_test.append(class_index)
            else:
                # -20度〜20度まで5度ずつ回転させる
                for angle in range(-20, 20, 5):
                    img_r = img.rotate(angle)
                    X_train.append(np.asarray(img_r))
                    y_train.append(class_index)

                    # 左右反転データも作成する
                    img_t = img_r.transpose(Image.FLIP_LEFT_RIGHT)
                    X_train.append(np.asarray(img_t))
                    y_train.append(class_index)

    X_train, y_train = shuffle_samples(X_train, y_train)
    X_test, y_test = shuffle_samples(X_test, y_test)
    # X_train = np.array(X_train)
    # X_test = np.array(X_test)
    # y_train = np.array(y_train)
    # y_test = np.array(y_test)

    npy_fpath = DATA_DIR + DATASET_FNAME
    np.save(npy_fpath, (X_train, X_test, y_train, y_test))


def shuffle_samples(X, y):
    zipped = list(zip(X, y))
    np.random.shuffle(zipped)
    X_result, y_result = zip(*zipped)
    return np.asarray(X_result), np.asarray(y_result)


if __name__ == "__main__":
    main()
