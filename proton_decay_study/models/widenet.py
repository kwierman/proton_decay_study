from keras.layers import Input, Dropout, Dense, Flatten
from keras.layers.convolutional import MaxPooling3D, Conv3D
from keras.models import Model
from keras import optimizers

import logging


class Kevnet(Model):
  logger = logging.getLogger('pdk.kevnet')

  def __init__(self, generator):

    self.generator = generator

    layer = self.assemble(generator)
    super(Kevnet, self).__init__(self._input, layer)
    self.logger.info("Compiling Model")
    # TODO: Config below
    self.sgd = optimizers.SGD(lr=0.1, 
                              decay=1e-3,
                              momentum=0.9, 
                              nesterov=True)
    self.compile(loss='mean_squared_error', optimizer=self.sgd,
                 metrics=['accuracy'])

  def assemble(self, generator):

    self.logger.info("Assembling Model")
    self._input = Input(shape=generator.output)
    self.logger.info(self._input)
    self.logger.info(self._input.shape)

    layer = Conv3D(128, (1, 15, 9), strides=(1, 14, 8),
                   activation='relu', padding='same',
                   data_format='channels_first',
                   name='block1_conv1')(self._input)
    self.logger.info(layer.shape)
    layer = MaxPooling3D((1, 15, 9), strides=(1, 14, 8),
                         data_format='channels_first',
                         name='block1_pool')(layer)
    self.logger.info(layer.shape)

    layer = Conv3D(512, (3, 15, 9), strides=(1, 14, 8),
                   activation='relu', padding='same',
                   data_format='channels_first',
                   name='block3_conv1')(layer)
    self.logger.info(layer.shape)
    layer = MaxPooling3D((3, 15, 9), strides=(1, 14, 8),
                         data_format='channels_first',
                         name='block3_pool')(layer)
    self.logger.info(layer.shape)

    layer = Conv3D(1024, (1, 4, 7), strides=(1, 4, 7),
                   activation='relu', padding='same',
                   data_format='channels_first',
                   name='block4_conv1')(layer)
    self.logger.info(layer.shape)
    layer = MaxPooling3D((1, 4, 7), strides=(1, 4, 7),
                         data_format='channels_first',
                         name='block4_pool')(layer)
    self.logger.info(layer.shape)


    # Classification block
    layer = Flatten(name='flatten')(layer)
    layer = Dropout(0.01)(layer)
    layer = Dense(1024, activation='relu', name='fc1')(layer)
    layer = Dropout(0.01)(layer)
    layer = Dense(generator.input,
                  activation='softmax',
                  name='predictions')(layer)
    self.logger.info(layer.shape)
    return layer