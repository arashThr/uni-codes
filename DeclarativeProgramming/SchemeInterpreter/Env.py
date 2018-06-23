#!/usr/bin/env python
# Definition of Env class and Procedure class

class Env:
    '''Each enviroment consists of a dictionatry which is var-val pair,
    and a pointer to its base env'''
    def __init__(self, pairs, base_env):
        self.base_env = base_env
        self.pairs = pairs
        
    def lookup_var_val(self, var):
        if self.pairs.has_key(var):
            return self.pairs[var]
        # No such var in this scope has been defined
        if self.base_env == None :
            #raise Exception, 'Variable does not exist : ' + var
            print 'Variable not defined :', var
        else: return self.base_env.lookup_var_val(var)
        
    def define_var(self, var, val):
        self.pairs[var] = val
        
    def set_var_val(self, var, val):
        if self.pairs.has_key(var):
            self.pairs[var] = val
            return 'ok'
        # If no such var is defined here and we have no upper env
        elif self.base_env == None :
            #raise Exception, 'Variable not defined : ' + var
            print 'Variable not defined :', var
        else: return self.base_env.set_var_val(var, val)
            
# Create new env which inherites previous one
def extend_env(pairs, base_env):
    return Env(pairs, base_env)

class Procedure:
    def __init__(self, args, body, env, proc_type=None):
        # We may need it later
        self.proc_type = proc_type

        # args is a list of arguments names
        self.args = args
        self.body = body
        self.env = env

    # Returns required values to call this function in Apply.Apply
    # ISSUE : I could import Apply in here !
    def getValues(self, params):
        if len(params) != len(self.args):
            raise Exception, 'Parameteres mismatch !'

        # New pairs to be added to new env
        newPaires = dict(zip(self.args, params))
        newEnv = extend_env(newPaires, self.env)
        #return Eval.eval_seq(self.body, newEnv)
        return (self.body, newEnv)

