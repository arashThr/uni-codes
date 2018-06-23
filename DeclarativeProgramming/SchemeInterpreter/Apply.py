import Eval
import REPL
import Env
# Note: Circular import is fine as long as we don't use from

# This function will apply the function, which has been retrieved from env,
# to a list of arguments
def Apply(proc, args):
    if isinstance(proc, Env.Procedure) :
        body, newEnv = proc.getValues(args)
        return Eval.eval_seq(body, newEnv)
    else :
        # Primitives functions
        #print 'Proc :', proc
        #print 'Args :', args
        return proc(args)


