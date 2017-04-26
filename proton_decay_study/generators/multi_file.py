from proton_decay_study.generators.base import BaseDataGenerator
import h5py


class MultiFileDataGenerator(BaseDataGenerator):
  """
    Creates a generator for a list of files
  """
  logger = logging.getLogger("pdk.generator.single")

  def __init__(self, datapaths, datasetname, 
               labelsetname, batch_size=10):
    self._files = [h5py.File(i , 'r') for i in datapaths]
    self._dataset = datasetname
    self._labelset = labelsetname
    self.batch_size = batch_size
    self.file_index=0
    self.current_index=0

  def __len__(self):
    """
      Iterates over files to create the total sum length
      of the datasets in each file.
    """
    return sum([i[self._dataset].shape[0] for i in self._files] )

  def next(self):
    """
      This should iterate over both files and datasets within a file.
    """
    if self.current_index >= self._files[self.file_index][self._dataset].shape[0]:
      self.logger.info("Reached end of file: {} Moving to next file: {}".format(self._files[self.file_index], 
                                                                                self._files[self.file_index+1]))
      self.file_index +=1
    if self.file_index == len(self._files):
      self.logger.info("Reached end of file stack. Now reusing data")
      self.file_index = 0 
      self.current_index = 0
    if self.current_index+self.batch_size>= self._files[self.file_index][self._dataset].shape[0]:
      """
        This is the rare case of stitching together more than 1 file by crossing the boundary.
      """
      remainder = self._files[self.file_index][self._dataset].shape[0]- self.current_index
      self.logger.info("Crossing file boundary with remainder: {}".format(remainder))
      x =  self._files[self.file_index][self._dataset][self.current_index:]
      y =  self._files[self.file_index][self._labelset][self.current_index:]
      x += self._files[self.file_index+1][self._dataset][:remainder]
      y += self._files[self.file_index+1][self._labelset][:remainder]
      self.file_index+=1
      self.current_index = remainder
      return (x,y)

    x = self._files[self.file_index][self._dataset][self.current_index:self.current_index+self.batch_size]
    y = self._files[self.file_index][self._labelset][self.current_index:self.current_index+self.batch_size]
    self.current_index+=self.batch_size
    return (x,y)