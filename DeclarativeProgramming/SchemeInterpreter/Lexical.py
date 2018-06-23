# A simple lexical analyzer for Scheme
# Returns a tuple that consisted of parts of expression grouped together
# Example : (define x 2) (+ x x) =>
# (['define', 'x', '2'], ['+', 'x', 'x'])
import re

def addQuote(match):
    val = match.group()
    return "'"+val+"'"

def addComma(match):
    val = match.group()
    return val+', '

def addCommaBet(match):
    val = match.group()
    return ', '.join(val.split())    

def removeExtraComma(match):
    return ']'

def Lexical(exp):
    exp = exp.replace("(", "[")
    exp = exp.replace(")", "]")

    p = re.compile(r'[^ \[\]]+')
    exp = p.sub(addQuote, exp)

    p = re.compile(r'[^ \[\]]+') 
    exp = p.sub(addComma, exp)

    p = re.compile(r"\] *\[|\] *'")
    exp = p.sub(addCommaBet, exp)

    p = re.compile(r', *\]')
    exp = p.sub(removeExtraComma, exp)

    return eval(exp)
