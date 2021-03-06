# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse
from operator import add, sub, floordiv, mul, mod as opmod, gt, lt, eq as opeq

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def evaluate(ast, env):
	"""Evaluate an Abstract Syntax Tree in the specified environment.
	"""
	if is_boolean(ast) or is_integer(ast): # evaluate booleans and integers
		return ast
	elif is_symbol(ast): # evaluate symbols
		return env.lookup(ast)
	elif is_list(ast): # evaluate lists
		if is_closure(ast[0]): # evaluate closure
			return eval_closure(ast, env)
		elif ast[0] == 'quote': # evaluate quotes
			return ast[1]
		elif ast[0] == 'atom': # evaluate atoms
			return is_atom(evaluate(ast[1], env))
		elif ast[0] == 'eq': # evaluate equality
			return eval_eq(ast, env)
		# evaluate basic math operators:
		elif ast[0] in ['+', '-', '/', '*', 'mod', '>', '<', '=']:
			return eval_math(ast, env)
		elif ast[0] == 'if': # evaluate if expression
			return eval_if(ast, env)
		elif ast[0] == 'define': # evaluate define statement
			eval_define(ast, env)
		elif ast[0] == 'lambda': # evaluate lambda statement
			return eval_lambda(ast, env)
		elif ast[0] == 'cons': # evaluate cons statement
			return eval_cons(ast, env)
		elif ast[0] == 'head': # evaluate head statement
			return eval_head(ast, env)
		elif ast[0] == 'tail': # evaluate tail statement
			return eval_tail(ast, env)
		elif ast[0] == 'empty': # evaluate empty statement
			return eval_empty(ast, env)
		elif is_symbol(ast[0]) or is_list(ast[0]): # evaluate closure from env
			return eval_closure_env(ast, env)
		else:
			raise LispError('Argument is not a function!')

def eval_eq(ast, env):
	"""Evaluate an eq statement in the specified environment.
	"""
	a1 = evaluate(ast[1], env)
	a2 = evaluate(ast[2], env)
	return is_atom(a1) and is_atom(a2) and a1 == a2

def eval_math(ast, env):
	"""Evaluate an mathematical operator and its
	arguments in the specified environment.
	Mathematical operations are carried out by the corresponding
	mathematical operators built into python.
	"""
	a1 = evaluate(ast[1], env)
	a2 = evaluate(ast[2], env)
	if is_integer(a1) and is_integer(a2):
		operators = {
		'+': add,
		'-': sub,
		'/': floordiv,
		'*': mul,
		'mod': opmod,
		'>': gt,
		'<': lt,
		'=': opeq}
		return operators[ast[0]](a1, a2)
	else:
		raise LispError("Math operators only work on integers!")

def eval_if(ast, env):
	"""Evaluate an 'if' expression in the specified environment.
	"""
	if evaluate(ast[1], env):
		return evaluate(ast[2], env)
	else:
		return evaluate(ast[3], env)

def eval_define(ast, env):
	"""Evaluate a 'define' statement in the specified environment.
	"""
	if len(ast) != 3:
		raise LispError("Wrong number of arguments: %d" % (len(ast) - 2))
	elif not is_symbol(ast[1]):
		raise LispError("Illegal use of define with non-symbol as variable")
	else:
		env.set(ast[1], evaluate(ast[2], env))

def eval_lambda(ast, env):
	"""Evaluate a 'lambda' statement in the specified environment.
	"""
	if len(ast) != 3:
		raise LispError("Wrong number of arguments: %d" % (len(ast) - 2))
	elif not is_list(ast[1]):
		raise LispError("The parameters to lambda need to be a list!")
	else:
		return Closure(env, ast[1], ast[2])

def eval_closure(ast, env):
	"""Evaluate a closure in the specified environment.
	"""
	closure = ast[0]
	arguments = ast[1:]
	parameters = closure.params
	if len(arguments) != len(parameters):
		raise LispError("Wrong number of arguments, expected %d got %d"
			% (len(parameters), len(arguments)))
	else:
		for i in range(len(arguments)):
			arg = evaluate(arguments[i], env)
			param = parameters[i]
			closure.env = closure.env.extend({param: arg})
		return evaluate(closure.body, closure.env)

def eval_cons(ast, env):
	"""Evaluate a 'cons' statement in the specified environment.
	Cons an element onto a list.
	"""
	if len(ast) != 3:
		raise LispError("Wrong number of arguments to 'cons'")
	s2 = evaluate(ast[2], env)
	if not is_list(s2):
		raise LispError("Cannot cons to a non-list!")
	else:
		return [evaluate(ast[1], env)] + s2

def eval_closure_env(ast, env):
	"""Evaluate to a closure from the env and evaluate it in the specified environment.
	"""
	closure = evaluate(ast[0], env)
	return evaluate([closure] + ast[1:], env)

def eval_head(ast, env):
	"""Evaluate a 'head' statement in the specified environment.
	Extract the first element of a list.
	"""
	l = evaluate(ast[1], env)
	if len(l) == 0:
		raise LispError("Cannot get the head of an empty list!")
	else:
		return l[0]

def eval_tail(ast, env):
	"""Evaluate a 'tail' statement in the specified environment.
	Extract all but the first element of a list.
	"""
	l = evaluate(ast[1], env)
	if len(l) == 0:
		raise LispError("Cannot get the tail of an empty list!")
	else:
		return l[1:]

def eval_empty(ast, env):
	"""Evaluate an 'empty' statement in the specified environment.
	"""
	return len(evaluate(ast[1], env)) == 0