# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""
    if is_boolean(ast) or is_integer(ast): # evaluate booleans and integers
    	return ast
    if is_list:
    	if ast[0] == 'quote': # evaluate quotes
    		return ast[1]
    	elif ast[0] == 'atom': # evaluate atoms
    		return is_atom(evaluate(ast[1], env))
    	elif ast[0] == 'eq': # evaluate equality
    		a1 = evaluate(ast[1], env)
    		a2 = evaluate(ast[2], env)
    		return is_atom(a1) and is_atom(a2) and a1 == a2
    	# evaluate basic math operators
    	# (!): built-in python operators used
    	elif ast[0] in ['+', '-', '/', '*', 'mod', '>', '<', '=']:
    		a1 = evaluate(ast[1], env)
    		a2 = evaluate(ast[2], env)
    		if is_integer(a1) and is_integer(a2):
	    		if ast[0] == 'mod':
	    			ast[0] = '%'
	    		py_math = str(a1) + " " + ast[0] + " " + str(a2)
	    		return eval(py_math)
	    	else:
	    		raise LispError("Math operator only works on integers!")