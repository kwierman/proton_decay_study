from keras.layers.convolutional import MaxPooling3D, Conv3D
from keras.layers import Input, Dropout, Dense, Flatten
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
    self.sgd = optimizers.SGD(lr=0.01, 
                              decay=1e-6,
                              momentum=0.9, 
                              nesterov=True)
    self.compile(loss='mean_squared_error', optimizer=self.sgd,
                 metrics=['accuracy'])

  def assemble(self, generator):

    self.logger.info("Assembling Model")
    self._input = Input(shape=generator.output,
                        dtype='float32',
                        name='main_input')
    self.logger.info(self._input)

    layer = Conv3D(32, (1, 5, 3), strides=(1, 4, 2),
                   activation='relu', padding='same',
                   data_format='channels_first',
                   name='block1_conv1')(self._input)
    self.logger.info(layer)
    layer = MaxPooling3D((1, 5, 3), strides=(1, 4, 2),
                         data_format='channels_first',
                         name='block1_pool')(layer)
    self.logger.info(layer)

    layer = Conv3D(64, (1, 3, 3), strides=(1, 2, 2),
                   activation='relu', padding='same',
                   data_format='channels_first',
                   name='block2_conv1')(layer)
    self.logger.info(layer)
    layer = MaxPooling3D((1, 3, 3), strides=(1, 2, 2),
                         data_format='channels_first',
                         name='block2_pool')(layer)
    self.logger.info(layer)

    layer = Conv3D(128, (1, 3, 3), strides=(1, 2, 2),
                   activation='relu', padding='same',
                   data_format='channels_first',
                   name='block3_conv1')(layer)
    self.logger.info(layer)
    layer = MaxPooling3D((1, 3, 3), strides=(1, 2, 2),
                         data_format='channels_first',
                         name='block3_pool')(layer)
    self.logger.info(layer)

    layer = Conv3D(256, (3, 3, 3), strides=(3, 2, 2),
                   activation='relu', padding='same',
                   data_format='channels_first',
                   name='block4_conv1')(layer)
    self.logger.info(layer)
    layer = MaxPooling3D((1, 3, 3), strides=(1, 2, 2),
                         data_format='channels_first',
                         name='block4_pool')(layer)
    self.logger.info(layer)

    layer = Conv3D(512, (1, 3, 3), strides=(1, 3, 3),
                   activation='relu', padding='same',
                   data_format='channels_first',
                   name='block5_conv1')(layer)
    self.logger.info(layer)
    layer = MaxPooling3D((1, 3, 3), strides=(1, 3, 3),
                         data_format='channels_first',
                         name='block5_pool')(layer)
    self.logger.info(layer)
    self.last_conv_layer = layer

    # Classification block
    layer = Flatten(name='flatten')(layer)
    layer = Dropout(0.01)(layer)
    layer = Dense(2048, activation='relu', name='fc1')(layer)
    layer = Dropout(0.01)(layer)
    layer = Dense(generator.input,
                  activation='softmax',
                  name='predictions')(layer)
    self.logger.info(layer)
    return layer
