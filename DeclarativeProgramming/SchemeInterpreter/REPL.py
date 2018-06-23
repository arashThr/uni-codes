#!/usr/bin/env python
# Arash Taher
# Jun 2013
# A rudimentary implementation for scheme interpreter 
# Based on original implementation of SICP

# Main part of our program : REPL
# Running evaluator as a program
import Env
import Eval
import Apply
import Lexical
import logging

# Global enviroment
global_env = Env.Env({}, None)

# Primitives evaluation helper function
def primitive_ops(func):
    def op(params):
        acc = params[0]
        for num in params[1:]:
            acc = func(acc, num)
        return acc
    return op

# Definition of primitive operations
global_env.define_var('+', primitive_ops(lambda x, y: x+y) )
global_env.define_var('-', primitive_ops(lambda x, y: x-y) )
global_env.define_var('*', primitive_ops(lambda x, y: x*y) )
global_env.define_var('/', primitive_ops(lambda x, y: x/y) )
global_env.define_var('=', lambda x: x[0]==x[1])
global_env.define_var('>', lambda x: x[0]>x[1])
global_env.define_var('<', lambda x: x[0]<x[1])

in_prompt = '>>> '
out_prompt = '--> '

def user_print(output):
    print out_prompt + repr(output)

def transform_input(exp):
    '''Transform Scheme input into it's 
    some-how-equivalent-list-representaion in python'''
    buf = Lexical.Lexical(exp)
    logging.info('Lexical gives : ' + str(buf))
    return buf

# Load and execute scheme code from a file
def load_exec_file(addr):
    f = open(addr, 'r')
    buf = ''
    for line in f:
        if line.strip()=='' and buf != '':
            #print 'LINE :', line
            #print 'BUF :', buf
            buf = transform_input(buf)
            if type(buf) == tuple :
                for exp in buf :
                    result = Eval.Eval(exp, global_env)
            else :
                result = Eval.Eval(buf, global_env)
            user_print(result)
            buf = ''
        else:
            buf = buf + ' ' + line.strip()

# REPL
def driver_loop():
    print '*** SCHEME RUDIMENTARY AND INEFFICIENT INETRPRETER IN PYTHON ***'
    print '-- Load [addr] to load and execute file : load test.scm'
    print '-- EOF to quit'

    while True:
        try :
            read_input = raw_input(in_prompt)
        except (EOFError, KeyboardInterrupt) as e:
            print 'Good bye'
            break

        read_input = read_input.lower()
        #print 'READ :', read_input
        if read_input == 'log':
            logging.basicConfig(filename='details.log', filemode='w', 
                    format='INFO : %(message)s', level=logging.INFO)
            print 'Logging enabled, check detail.log file'
            continue

        if read_input.startswith("load"):
            load_exec_file( read_input.strip("load").strip() )
            continue

        read_input = transform_input(read_input)
        if type(read_input) == tuple :
            for exp in read_input :
                result = Eval.Eval(exp, global_env)
        else :
            result = Eval.Eval(read_input, global_env)
        user_print(result)

def main():
    driver_loop()
    return 0

if __name__ == '__main__':
    main()

