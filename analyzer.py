import aubio 
import numpy as np
import math


class Analyzer():
	def __init__(self, audio_fpath):
		self.audio_fpath = audio_fpath

	def classify_tone(self):
		"""
		Returns the tone of the given audio file
		"""
		pass

	def classify_particle(self):
		"""
		Returns the particle of the given audio file
		"""
		pass

	def classify_sound(self):
		return self.classify_particle() + self.classify_tone()


class ToneFitter():
	def __init__(self, frequency_data):
		self.freq_data = frequency_data

	def identify_tone(self):
		pass

class GradientDescent():
	def __init__(self, x_data, y_data, gd_type='linear'):
		assert x_data.shape[0] == y_data.shape[0]
		self.X = np.array([np.ones(len(x_data)), x_data]).T
		self.y = y_data.T
		if gd_type == 'linear':
			self.gd_func = self.normal_func_eval
		elif gd_type == "height":
			self.gd_func = self.height_eval
		elif gd_type == "quadratic":
			self.gd_func = self.quadratic_eval

		self.theta = np.ones(x_data.shape[1]) 

	def normal_func_eval(self):
		pass

