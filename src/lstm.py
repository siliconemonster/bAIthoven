import glob
import pickle
import numpy
from music21 import converter, instrument, note, chord
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.layers import Activation
from keras.layers import BatchNormalization as BatchNorm
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import json

from data_translation_funcs import *

def train_network(sonates, n_vocab):

    network_input, network_output = prepare_sequences(sonates, n_vocab)

    model = create_network(network_input, n_vocab)

    train(model, network_input, network_output)

def prepare_sequences(sonates, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    sequence_length = 700

    # get all pitch names
    pitchnames = set(item for item in sonates)

     # create a dictionary to map pitches to integers
    event_to_int = dict((event, number) for number, event in enumerate(pitchnames))
    print('The dictionary has', len(event_to_int), 'key-value pairs.\n')
    with open("dictionary.txt", "w") as fp:
        json.dump(event_to_int, fp, indent = True)

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(sonates) - sequence_length, 1):
        sequence_in = sonates[i:i + sequence_length]
        sequence_out = sonates[i + sequence_length]
        network_input.append([event_to_int[char] for char in sequence_in])
        network_output.append(event_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
    # normalize input
    network_input = network_input / float(n_vocab)

    network_output = np_utils.to_categorical(network_output)

    return (network_input, network_output)

def create_network(network_input, n_vocab):
    """ create the structure of the neural network """
    model = Sequential()
    model.add(LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        recurrent_dropout=0.3,
        return_sequences=True
    ))
    model.add(LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    model.add(LSTM(512))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(BatchNorm())
    model.add(Dropout(0.3))
    model.add(Dense(n_vocab))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    # Load the weights to each node
    model.load_weights('weights-improvement-193-0.1417-bigger.hdf5')

    return model

def train(model, network_input, network_output):
    """ train the neural network """
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = ModelCheckpoint(
        filepath,
        save_weights_only = True,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]

    model.fit(network_input, network_output, epochs=200, batch_size=512, callbacks=callbacks_list, initial_epoch = 100)

if __name__ == '__main__':
    sonates, n_vocab = rearrange_received_data()
    print('All the sonates together add up to', len(sonates), 'entries.')
    train_network(sonates, n_vocab)