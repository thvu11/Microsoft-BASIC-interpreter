#!/usr/bin/env python2.7
"""
A DUMBBASIC interpreter written in Python2.7

See the information for FIT3140 Assignment 1 for more
information
Author: <robert.merkel@monash.edu>
Modified: Darren Wong and Huy Vu
"""
import sys
from time import clock

out_file = 0

class Op(object):
    ''' base class for internal representation of commands
        anything that subclasses Op should implement execute
        subclasses should generally invoke the base class __init__
        instance variables:
            next - line number of next command (for normal execution)
    '''
    def __init__(self):
        self.next = None

    def execute(self, context):
        '''do whatever the command indicates to do.  Base class execute
        should never be called
        '''
	global out_file
	out_file.write("operation is undefined\n")
        return


class NoOp(Op):
    """Do nothing.  Used by the REM command
    """
    def __init__(self):
        super(NoOp, self).__init__()

    def execute(self, context):
        context.ip = self.next

class Assign(Op):
    """Assign the result of an expression to a variable.  Corresponds
    to the LET command
    instance variables: var - variable name
                        expression - the Expression that calculates the new value
    """
    def __init__(self,var, expression):
        super(Assign, self).__init__()
        self.var = var
        self.expression = expression
        self.next = None

    def execute(self, context):
        newval = self.expression.evaluate(context)
        context.assignval(self.var, newval)
        context.ip = self.next

class PrintOp(Op):
    """Print a variable or constant.  Corresponds to the PRINT command
    instance variables: var - the variable or constant to print
    """
    def __init__(self, var):
        super(PrintOp, self).__init__()
        self.var=var

    def execute(self, context):
        val = context.getval(self.var)
        print val
	global out_file
	out_file.write(str(val) + '\n')
        context.ip = self.next

class Goto(Op):
    """Make the next op to execute the one at the line number
    designated by self.value.  Note that value can either be
    a variable or a numeric constant"""

    def __init__(self, value):
        self.value = value

    def execute(self, context):
        val = context.getval(self.value)
        context.ip = val
	#print(val)

class IfGoto(Op):
    """If the expression evaluates to non-zero, go to the
    line specified by the value (which can be a variable or constant)
    """
    def __init__(self, expression, iftrue):
        super(IfGoto, self).__init__()
        self.iftrue=iftrue
        self.expression = expression

    def execute(self, context):
    #    print "executing IfGoto"
    #    print "self.iftrue = ", self.iftrue
        expval = self.expression.evaluate(context)
        print "expval = ", expval
	
        if expval == 0:
            context.ip = self.next
        elif expval == 1:
            iftrueval = context.getval(self.iftrue)
            context.ip = iftrueval
	else:
	    context.ip = None

class Expression(object):
    """Expression is the base class for an arithmetical or logical
    expression.
    Expressions have precisely two arguments - complex Expressions
    involving multiple operators and parentheses are not currently
    supported

    instance variables: lhs - variable name or constant forming the left
    hand side of the expression
    rhs - variable name or constant forming the RHS of the expression
    """

    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def evaluate(self, context):
	global out_file
	out_file.write("operation unsupported\n")
        return

class AddExpression(Expression):
    """addition expression"""
    def __init__(self, lhs, rhs):
        super(AddExpression, self).__init__(lhs, rhs)

    def evaluate(self, context):
        lhsval = context.getval(self.lhs)
        rhsval = context.getval(self.rhs)
        return lhsval + rhsval

class SubExpression(Expression):
    """subtraction expression"""
    def __init__(self, lhs, rhs):
        super(SubExpression, self).__init__(lhs, rhs)

    def evaluate(self, context):
        lhsval = context.getval(self.lhs)
        rhsval = context.getval(self.rhs)
        return lhsval - rhsval

class MultiplyExpression(Expression):
    """multiplication expression"""
    def __init__(self, lhs, rhs):
        super(MultiplyExpression, self).__init__(lhs, rhs)

    def evaluate(self, context):
        lhsval = context.getval(self.lhs)
        rhsval = context.getval(self.rhs)
        return lhsval * rhsval
    
class DivideExpression(Expression):
    """division expression"""
    def __init__(self, lhs, rhs):
        super(DivideExpression, self).__init__(lhs, rhs)

    def evaluate(self, context):
        lhsval = context.getval(self.lhs)
        rhsval = context.getval(self.rhs)
        return lhsval / rhsval

class EqualsExpression(Expression):
    """equality testing expression"""
    def __init__(self, lhs, rhs):
        super(EqualsExpression, self).__init__(lhs, rhs)

    def evaluate(self, context):
        lhsval = context.getval(self.lhs)
        rhsval = context.getval(self.rhs)
        if lhsval == rhsval:
            return 1
        else:
            return 0

class LHSBiggerExpression(Expression):
    "greater-than logical expression"
    def __init__(self, lhs, rhs):
        super(LHSBiggerExpression, self).__init__(lhs, rhs)

    def evaluate(self, context):
        lhs = context.getval(self.lhs)
        rhs = context.getval(self.rhs)
	#print('lhs',lhs)
	#print('rhs',rhs)
	if lhs is None or rhs is None:
		return
	else:
		if lhs > rhs:
		    return 1
		else:
		    return 0

class LHSSmallerExpression(Expression):
    "greater-than logical expression"
    def __init__(self, lhs, rhs):
        super(LHSSmallerExpression, self).__init__(lhs, rhs)

    def evaluate(self, context):
        lhs = context.getval(self.lhs)
        rhs = context.getval(self.rhs)
	if lhs is None or rhs is None:
		return
        if lhs < rhs:
            return 1
        else:
            return 0

class Context:
    """the execution context for the code.
    instance variables: ip - the instruction pointer - the line numbe of the next instruction to be executed
    vars - a dictionary where the keys are the variable names and the values are the, well, variable values"""

    def __init__(self):
        self.ip = None
        self.vars = dict()

    def getval(self, varexp):
        """get the value of a variable expression in this context.  If varexp is a number, return that number, if it's a defined variable, return the value, otherwise throw an exception"""
        if varexp.isdigit():
            return int(varexp)
        elif varexp in self.vars:
            return self.vars[varexp]
        else:
	    global out_file
	    out_file.write("Unknown variable\n")
            return

    def assignval(self, var, val):
        """Assign the value val to the variable var"""
        #print("Assigning value {} to variable {}".format(val, var))
        self.vars[var]=val

expressionclasses = dict([('+', AddExpression),('-', SubExpression), ('*', MultiplyExpression),('/', DivideExpression), ('==', EqualsExpression),('>', LHSBiggerExpression), ('<', LHSSmallerExpression)])

# parse the various commands defined by the language

def parselet(explist):
    global out_file
    if explist[1] != "LET":
	out_file.write("LET expression invalid\n")
        return
    var = explist[2]
    if explist[3] != "=":
	out_file.write("LET expression invalid\n")
        return
    
    expression = parseexpression(explist[4], explist[5], explist[6])
    return Assign(var, expression)

def parseprint(explist):
    if explist[1] != "PRINT":
	global out_file
	out_file.write("PRINT expression invalid\n")
        return
    var = explist[2]
    return PrintOp(var)

def parsegoto(explist):
    if explist[1] != "GOTO":
	global out_file
	out_file.write("GOTO expression invalid\n")
        return
    var = explist[2]
    return Goto(var)

def parseifgoto(explist):
    global out_file
    if explist[1] != "IF":
	out_file.write("IF expression invalid\n")
        return
    expression = parseexpression(explist[2], explist[3], explist[4])
    if( explist[5] != "GOTO"):
	out_file.write("IF expression invalid\n")
        return
    dest = explist[6]
    check = IfGoto(expression, dest)
    if check is None:
	return
    else:
	return check

def parserem(explist):
    if explist[1] != "REM":
	global out_file
	out_file.write("REM expression invalid\n")
        return
    return NoOp()

opclasses = dict([("LET", parselet), ("PRINT", parseprint), ("GOTO", parsegoto), ("IF", parseifgoto), ("REM", parserem)])

def parseexpression(lhs, op, rhs):
    #print "op = ", op
    #print "Expressionclasses[op] = ", expressionclasses[op]
    return expressionclasses[op](lhs, rhs)

def parseline(line, opdict):
    '''parse a line of code'''
    #print "line = ", line
    explist = line.split()
    global out_file
    if explist[0].isdigit():
        lineno = int(explist[0])
    else:
	out_file.write("Invalid line number\n")
        return

    if explist[1] in opclasses:
        op = opclasses[explist[1]](explist)
        opdict[lineno] = op
    else:
	out_file.write("Invalid operation\n")
        return

def addnextlines(opdict):
    '''second pass of the compilation process - add the successor line to each member of the opdict'''
    linenos = sorted(opdict.keys())
    #print linenos
    nextlinenos = linenos[1:]
    nextlinenos.append(None)
    #print nextlinenos
    linetuples = zip(linenos, nextlinenos)

    for linetuple in linetuples:
        opdict[linetuple[0]].next = linetuple[1]

def run(opdict):
    '''main execution loop after passing has been done'''
    context = Context()
    firstlineno = sorted(opdict.keys())[0]

    context.ip = firstlineno
    start = 0
    while context.ip is not None and start < 70:
    #    print("Executing line {}".format(context.ip))
	try:
        	op = opdict[context.ip]
        	op.execute(context)
		start += 0.05
	except KeyError:
		global out_file
		out_file.write("Not enough data to continue the code\n")
		return
    if start >= 70:
	global out_file
	out_file.seek(0)
	out_file.write("Loop has been detected\n")
	return

def parse(filename):
    '''parse the input, returning a dictionary of Ops with the keys as line numbers'''
    opdict = dict()
    for line in filename:
	line_1 = line.strip('\n')
        parseline(line_1, opdict)
    addnextlines(opdict)
    return opdict


def main():
    global out_file
    filename = open("INPUT.txt", "r")
    out_file = open('output.txt', 'w')
    opdict = parse(filename)
    run(opdict)
    filename.close()
    out_file.close()
    return


