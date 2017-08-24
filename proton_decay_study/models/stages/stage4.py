from .stage3 import Stage3
from keras.layers.convolutional import MaxPooling3D, Conv3D
from keras.regularizers import l1, l2
import logging

class Stage4(Stage3):
  logger = logging.getLogger('pdk.stage4')
  fc_name='fc_stage4'

  def assemble_layers(self, layer):
    layer = super(Stage4, self).assemble_layers(layer)
    layer = Conv3D(128, (3, 3, 3), strides=(3, 2, 2),
                   activation='relu', padding='same',
                   data_format='channels_first',
                   kernel_initializer='random_uniform',
                   bias_initializer='zeros',
                   kernel_regularizer=l2(0.01),
                   activity_regularizer=l1(0.01),
                   name='conv4_1')(layer)
    self.logger.info(layer)
    layer = MaxPooling3D((1, 2, 2), strides=(1, 2, 2),
                         data_format='channels_first',
                         name='pool4_1')(layer)
    self.logger.info(layer)
    return layer