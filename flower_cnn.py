import numpy as np
import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D

DATA_DIR = '/Volumes/Photos/flower_ai/'
DATASET_FNAME = 'flower.npy'
MODEL_FNAME = 'flower_cnn.h5'

# CATEGORIES = ['tulip', 'garbera', 'anemone',
#               'rose', 'cherryblossom', 'viola',
#               'daisy', 'poppy', 'carnation']
CATEGORIES = ['tulip', 'garbera', 'rose']
IMG_SIZE = 50
EPOCHS = 25

num_classes = len(CATEGORIES)

def main():
    dataset_fpath = DATA_DIR + DATASET_FNAME

    X_train, X_test, y_train, y_test = np.load(dataset_fpath, allow_pickle=True)

    X_train = X_train.astype('float32') / 255
    X_test = X_test.astype('float32') / 255

    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)

    model = model_train(X_train, y_train)
    model_eval(model, X_test, y_test)


def model_train(X, y):
    model = Sequential()

    model.add(Conv2D(32, (3, 3), padding='same', input_shape=X.shape[1:]))
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

    model.fit(X, y, batch_size=32, epochs=EPOCHS)

    model.save(DATA_DIR + MODEL_FNAME)

    return model


def model_eval(model, X, y):
    # Score trained model.
    scores = model.evaluate(X, y, verbose=1)
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])


if __name__ == "__main__":
    main()
