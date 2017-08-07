import aubio 
import copy
import numpy as np
import math

NUM_ITERS = 1500
ALPHA = .1

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

class LinearRegression():
"""
The class implements the process of gradient descent and use of the
normal equation in order to find the Linear Regression fit of data.
"""
	def __init__(self, x_data, y_data, gd_type='normal'):
		assert x_data.shape[0] == y_data.shape[0]
		self.X = np.array([np.ones(len(x_data)), x_data]).T
		self.y = y_data.T
		self.num_samples = len(self.y)
		if gd_type == 'normal':
			self.gd_func = self.normal_func_eval
		else:
			self.gd_func = self.gradient_descent

	def get_error(self):
		return self.gd_func()

	def normal_func_eval(self):
		try:
			return self.normal_func_error
		except AttributeError:
			self.theta = np.linalg.solve(self.X.T.dot(self.X), self.X.T.dot(self.y))
			self.normal_func_error = self._calc_linear_error()
			return self.normal_func_error

	def height_eval(self):
		assert len(self.theta) == 0
		return self.theta[0]

	def gradient_descent(self):
		iters = 0
		self.theta = np.ones(self.X.shape[1])
		while iters < NUM_ITERS:
			initial_theta = copy.deepcopy(self.theta)
			for theta_idx in range(len(self.theta)):
				total = 0
				for sample_idx in range(self.num_samples):
					hypothesis_cost = self._eval_hypothesis(initial_theta, self.X[sample_idx, :])
					total += (hypothesis_cost - self.y[sample_idx])*self.X[sample_idx, theta_idx]
				self.theta[theta_idx] -= (ALPHA*total)/self.num_samples
			iters += 1
		return self._calc_linear_error()

	def _eval_hypothesis(self, thetas, sample):
		return np.dot(thetas, sample)

	def _calc_linear_error(self):
		y_hat = np.dot(self.X, self.theta)
		error = self.y - y_hat
		return np.square(error).sum()




