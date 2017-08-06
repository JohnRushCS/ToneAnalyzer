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

	