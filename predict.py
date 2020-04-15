import sys

import numpy as np
from PIL import Image
import keras
from keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

DATA_DIR = '/Volumes/Photos/flower_ai/'
MODEL_FNAME = 'flower_cnn.h5'

# CATEGORIES = ['tulip', 'garbera', 'anemone',
#               'rose', 'cherryblossom', 'viola',
#               'daisy', 'poppy', 'carnation']
CATEGORIES = ['tulip', 'garbera', 'rose']
IMG_SIZE = 50

num_classes = len(CATEGORIES)

def main():
    img = Image.open(sys.argv[1])
    img = img.convert('RGB')
    img = img.resize((IMG_SIZE, IMG_SIZE))

    X = [np.asarray(img)]
    X = np.array(X)

    model = build_model()

    result = model.predict([X])[0]
    print(result)

    predicted = result.argmax()
    percentage = int(result[predicted] * 100)
    print("{0} ({1} %)".format(CATEGORIES[predicted], percentage))


def build_model():
    model = Sequential()

    model.add(Conv2D(32, (3, 3), padding='same', input_shape=(50, 50, 1)))
    model.add(Activation('relu'))
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(Activation('relu'))
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    # initiate RMSprop optimizer
    opt = keras.optimizers.RMSprop(learning_rate=0.0001, decay=1e-6)

    # Let's train the model using RMSprop
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])

    model = load_model(DATA_DIR + MODEL_FNAME)

    return model


if __name__ == "__main__":
    main()
