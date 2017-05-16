from keras.models import Model

class IntermediateVisualizer(Model):
  def __init__(self, model, layer_name, generator):
    self.generator = generator
    super(self, IntermediateVisualizer).__init__(inputs=model.input,
                                 outputs=model.get_layer(layer_name).output)
  def infer(self):
    return self.predict(self.generator.next())
