# Core of the evaluator : Eval function
# Processes expression and applies appropriate functions
import Env
import Apply
import re
import logging

primitive_proc = ['car', 'cdr', 'cons',
        '+', '-', '*', '/', '>', '<', '=', 'null?']
keywords = ['define', 'quote', 'set!', 'if', 'else', 'true', 'false'
        'lambda', 'cond', 'begin']

def Eval(exp, env):
    # classifing expressions
    if self_eval(exp): return eval_self_eval(exp)
    elif is_var(exp): return env.lookup_var_val(exp)
    elif is_quoted(exp): return text_of_quotation(exp)
    elif is_assign(exp): return eval_assign(exp, env)
    elif is_def(exp): return eval_def(exp, env)
    elif is_if(exp): return eval_if(exp, env)
    elif is_lambda(exp): return Env.Procedure(exp[1], exp[2:], env)
    elif is_begin(exp): return eval_seq(exp[1:], env)
    elif is_cond(exp): return eval_cond2if(exp, env)
    elif is_app(exp, env):
        logging.info(str(exp[0]) + ' will be applied')
        return Apply.Apply( Eval(exp[0], env),
            list_of_vals(exp[1:], env))
    else: raise Exception, 'Unknonw expression : Eval '+ str(exp)

# Returns a list contains evaluated args
def list_of_vals(exps, env):
    lst = []
    for exp in exps:
        lst.append( Eval(exp, env) )
    logging.info('List of arguments : ' + str(lst))
    return lst

# Self-Evaluating expressions
def self_eval(exp):
    # Everything that has been left after parsing a list
    # Strings and numbers
    if type(exp) == str and \
    (exp.isdigit() or \
    (exp.startswith('"') and exp.endswith('"')) ):
        return True
    return False

def eval_self_eval(exp):
    if exp.isdigit():
        return int(exp)
    else :
        # It's a string
        return exp

# Variables
# Note that function (like +,...) are stored as vars too
def is_var(exp):
    # We know it's not sel-evaluating
    if type(exp) == str and not exp.isdigit():
        #print 'Variable :', exp
        return True
    return False

# Quouted
def is_quoted(exp):
    if exp[0] == 'quote':
        return True
    return False

def text_of_quotation(exp):
    return "'" + str(exp[1])

# Assignment!
def is_assign(exp):
    if exp[0] == 'set!':
        return True
    return False

def eval_assign(exp, env):
    val = Eval(exp[2], env)
    #print 'Val :', val
    #print 'Var :', exp[1]
    env.set_var_val(exp[1], val)
    logging.info('set! on : ' + str(exp[1]))
    return 'ok'

# Definitions
def is_def(exp):
    if exp[0] == 'define':
        return True

def eval_def(exp, env):
    # Define a function
    if type(exp[1]) == list:
        proc = Env.Procedure(exp[1][1:], exp[2:], env)
        env.define_var(exp[1][0], proc)
        return 'ok'
    # Define variable
    elif len(exp) == 3:
        val = exp[2]
        env.define_var( exp[1], Eval(val, env) )
        return 'ok'
    else :
        raise ValueError, 'Bad syntax :' + str(exp)

# IF evaluation
def is_if(exp):
    if exp[0] == 'if':
        return True
    return False

def eval_if(exp, env):
    def if_pred(): return exp[1]
    def if_cons(): return exp[2]
    def if_alte():
        if len(exp)==4: return exp[3]
        else: return False

    if Eval(if_pred(), env) == True:
        return Eval(if_cons(), env)
    else:
        return Eval(if_alte(), env)

# Lambda expressions
def is_lambda(exp):
    if exp[0] == 'lambda':
        return True
    return False

# Begin expr
def is_begin(exp):
    if exp[0] == 'begin':
        return True
    return False

# Sequnces Evaluation
def eval_seq(exps, env):
    for exp in exps[:-1]:
        Eval(exp, env)
    return Eval(exps[-1], env)

# Conditions
def is_cond(exp):
    if exp[0] == 'cond':
        return True
    return False

def eval_cond2if(exp, env):
    for cond in exp[1:]:
        pred = cond[0]
        cons = cond[1]
        if (type(pred)==str and pred=='else') \
                or Eval(pred, env):
            return Eval(cons, env)

# Applications
def is_app(exp, env):
    # The result of evaluating first parameter should be applied on rest
    if type(exp[0]) == list:
        return True
    # Already defined function in env
    if isinstance(env.lookup_var_val(exp[0]), Env.Procedure):
        return True
    if primitive_proc.count(exp[0]) != 0:
        return True
    return False

