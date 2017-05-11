from keras.layers import Input, merge, Dropout, Dense, Flatten, Activation
from keras.layers.convolutional import MaxPooling3D, Conv3D
from keras.layers.normalization import BatchNormalization
from keras.models import Model

from keras import backend as K
from keras.utils.data_utils import get_file

import tensorflow as tf
import logging


class Kevnet(Model):
  logger = logging.getLogger('pdk.kevnet')
  
  def __init__(self, generator):

    self.generator = generator
    self.logger.info("Assembling Model")
    self._input = Input(shape=generator.output)
    self.logger.info(self._input)
    self.logger.info(self._input.shape)

    layer = Conv3D(32, (1,5,5), strides=(1,5,5), 
                   activation='relu', padding='same', 
                   data_format='channels_first',
                   name='block1_conv1')(self._input)
    self.logger.info(layer.shape)
    layer = MaxPooling3D((1, 5, 5), strides=(1,5, 5),  
                          data_format='channels_first', 
                          name='block1_pool')(layer)
    self.logger.info(layer.shape)
    layer = BatchNormalization(axis=2, name="block1_norm")(layer)
    self.logger.info(layer.shape)

    layer = Conv3D(64, (1,5,5), strides=(1,5,5), 
                   activation='relu', padding='same', 
                   data_format='channels_first',
                   name='block2_conv1')(self._input)
    self.logger.info(layer.shape)
    layer = MaxPooling3D((1, 5, 5), strides=(1,5, 5),  
                          data_format='channels_first', 
                          name='block2_pool')(layer)
    self.logger.info(layer.shape)
    layer = BatchNormalization(axis=2, name="block2_norm")(layer)
    self.logger.info(layer.shape)

    layer = Conv3D(128, (3,5,5), strides=(3,5,5), 
                   activation='relu', padding='same', 
                   data_format='channels_first',
                   name='block3_conv1')(self._input)
    self.logger.info(layer.shape)
    layer = MaxPooling3D((3, 5, 5), strides=(3,5, 5),  
                          data_format='channels_first', 
                          name='block3_pool')(layer)
    self.logger.info(layer.shape)
    layer = BatchNormalization(axis=2, name="block3_norm")(layer)
    self.logger.info(layer.shape)

    layer = Conv3D(256, (1,5,5), strides=(1,5,5), 
                   activation='relu', padding='same', 
                   data_format='channels_first',
                   name='block4_conv1')(self._input)
    self.logger.info(layer.shape)
    layer = MaxPooling3D((1, 5, 5), strides=(1,5, 5),  
                          data_format='channels_first', 
                          name='block4_pool')(layer)
    self.logger.info(layer.shape)
    layer = BatchNormalization(axis=2, name="block4_norm")(layer)
    self.logger.info(layer.shape)

    # Classification block
    layer = Flatten(name='flatten')(layer)
    #layer = Dense(1024, activation='relu', name='fc1')(layer)
    layer = Dense(256, activation='relu', name='fc2')(layer)
    layer = Dense(generator.input, activation='softmax', name='predictions')(layer)
    self.logger.info(layer.shape)

    super(Kevnet, self).__init__(self._input, layer)
    self.logger.info("Compiling Model")
    self.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])


