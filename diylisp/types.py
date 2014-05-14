# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The LispError class you can have for free :)
"""

class LispError(Exception): 
	"""General lisp error class."""
	pass

class Closure:
	
	def __init__(self, env=None, params=[], body=''):
		self.env = env if env else Environment()
		self.params = params
		self.body = body

	def __str__(self):
		return "<closure/%d>" % len(self.params)

class Environment:

	def __init__(self, variables=None):
		self.variables = variables if variables else {}

	def lookup(self, symbol):
		if symbol in self.variables:
			return self.variables[symbol]
		else:
			raise LispError('Variable not in the environment: %s' % symbol)

	def extend(self, variables):
		new_vars = self.variables.copy()
		new_vars.update(variables)
		return Environment(new_vars)

	def set(self, symbol, value):
		if symbol in self.variables:
			raise LispError('Variable already defined: %s' % symbol)
		else:
			self.variables[symbol] = value