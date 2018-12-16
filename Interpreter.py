# Author: Jeb Alawi
# Description: Reads in a file containing a CORE program, parses it into a parse tree, and then executes the program.
# Date: 11/19/18

from Parser import ParseTree, Node
from Tokenizer import Tokenizer
import sys

class Interpreter:
    def __init__(self, parseTree):
        self.pt = parseTree
        self.execProg()


    # executes the program
    def execProg(self):
        self.pt.moveToChild(3) # move to <stmt-seq> bc <decl-seq> is handled by parser
        self.execStmtSeq()
        self.pt.moveToParent()


    # executes a statement sequence
    def execStmtSeq(self):
        self.pt.moveToChild(0)
        self.execStmt()
        self.pt.moveToParent()
        if(self.pt.getAlt() == 1):
            self.pt.moveToChild(1)
            self.execStmtSeq()
            self.pt.moveToParent()


    # executes a statement
    def execStmt(self):
        alt = self.pt.getAlt()
        self.pt.moveToChild(0)
        if(alt == 0): # assign
            self.execAssign()
        elif(alt == 1): #if
            self.execIf()
        elif(alt == 2): #loop
            self.execLoop()
        elif(alt == 3): #in
            self.execIn()
        elif(alt == 4): #out
            self.execOut()
        else:
            print("Error executing statement, alt not found "+str(alt))
        self.pt.moveToParent()


    # executes an if statement
    def execIf(self):
        alt = self.pt.getAlt()
        self.pt.moveToChild(1)
        cond = self.execCond()
        self.pt.moveToParent()
        if(cond):
            self.pt.moveToChild(3)
            self.execStmtSeq()
            self.pt.moveToParent()
        elif((not cond) and (alt == 1)):
            self.pt.moveToChild(5)
            self.execStmtSeq()
            self.pt.moveToParent()


    # executes and prints an output
    def execOut(self):
        self.pt.moveToChild(1)
        idList = self.execIdList()
        self.pt.moveToParent()
        for id in idList:
            value = self.pt.getSymbolValue(id)
            print(id+" = "+str(value))


    # assigns variables, executes an input
    def execIn(self):
        self.pt.moveToChild(1)
        idList = self.execIdList()
        self.pt.moveToParent()
        for id in idList:
            value = input(id+" = ? ")
            while(not value.isnumeric()):
                print("identifier must be an integer")
                value = input(id+" = ? ")
            self.pt.updateSymbolTable(id, value)


    # returns a list of identifiers
    def execIdList(self):
        idList = []
        self.pt.moveToChild(0)
        idList.append(self.execId())
        self.pt.moveToParent()
        if(self.pt.getAlt() == 1):
            self.pt.moveToChild(2)
            idList.extend(self.execIdList())
            self.pt.moveToParent()
        return idList


    # executes a loop
    def execLoop(self):
        self.pt.moveToChild(1)
        cond = self.execCond()
        self.pt.moveToParent()
        while(cond):
            self.pt.moveToChild(3)#loop stmt-seq
            self.execStmtSeq()
            self.pt.moveToParent()
            self.pt.moveToChild(1)
            cond = self.execCond()
            self.pt.moveToParent()
    

    # executes a condition and returns as true or false
    def execCond(self):
        alt = self.pt.getAlt()
        if(alt == 0):
            self.pt.moveToChild(0)
            comp = self.execComp()
            self.pt.moveToParent()
        elif(alt == 1):
            self.pt.moveToChild(1)
            comp = (not self.execCond())
            self.pt.moveToParent()
        elif(alt == 2 or alt == 3):
            self.pt.moveToChild(1)
            comp = self.execCond()
            self.pt.moveToParent()
            self.pt.moveToChild(3)
            comp2 = self.execCond()
            self.pt.moveToParent()
            if(alt == 2):
                comp = comp and comp2
            else:
                comp = comp or comp2
        else:
            print("Error executing cond, alt not found?")
            sys.exit()
        return comp

    # executes a comparison and returns whether it was true or false
    def execComp(self):       
        self.pt.moveToChild(1)
        fac1 = int(self.execFac())
        self.pt.moveToParent()
        self.pt.moveToChild(3)
        fac2 = int(self.execFac())
        self.pt.moveToParent()
        self.pt.moveToChild(2)
        alt = self.execCompOp()
        self.pt.moveToParent()
        if(alt == 0): #!=
            return fac1 != fac2
        elif(alt == 1):
            return fac1 == fac2
        elif(alt == 2):
            return fac1 < fac2
        elif(alt == 3):
            return fac1 > fac2
        elif(alt == 4):
            return fac1 <= fac2
        elif(alt == 5):
            return fac1 >= fac2
        else:
            print("Error getting alt for comp-op")
            sys.exit()


    # returns the alt of a comp op for use in comparison execution
    def execCompOp(self):
        alt = self.pt.getAlt()
        return alt


    # assigns a value to a variable in the symbol table
    def execAssign(self):
        self.pt.moveToChild(0)
        var = self.execId()
        self.pt.moveToParent()
        self.pt.moveToChild(2)
        exp = self.execExp()
        self.pt.moveToParent()
        self.pt.updateSymbolTable(var, exp)


    # executes an expression
    def execExp(self):
        alt = self.pt.getAlt()
        self.pt.moveToChild(0)
        term = int(self.execTerm())
        self.pt.moveToParent()
        if(alt == 1 or alt == 2):
            self.pt.moveToChild(2)
            exp = int(self.execExp())
            self.pt.moveToParent()
            if(alt == 1):
                term = term + exp
            else:
                term = term - exp
        return term
            

    # executes a term and returns it for use in execExp()
    def execTerm(self):
        alt = self.pt.getAlt()
        self.pt.moveToChild(0)
        fac = int(self.execFac())
        self.pt.moveToParent()
        if(alt == 1):
            self.pt.moveToChild(2)
            term = int(self.execTerm())
            self.pt.moveToParent()
            fac = fac * term
        return fac


    # executes a fac and returns in for use in execTerm()
    def execFac(self):
        alt = self.pt.getAlt()
        if(alt == 0):
            self.pt.moveToChild(0)
            fac = self.execInt()
            self.pt.moveToParent()
        elif(alt == 1):
            self.pt.moveToChild(0)
            identifier = self.execId()
            fac = self.pt.getIdValue(identifier)
            if(fac == None):
                print("Error, identifier: "+ identifier + "is not assigned a value")
                sys.exit()
            self.pt.moveToParent()
        elif(alt == 2):
            self.pt.moveToChild(1)
            fac = self.execExp()
            self.pt.moveToParent()
        else:
            print("Error executing Fac, alt not found")
            sys.exit()
        return fac

    
    # returns the name of an identifiers
    def execId(self):
        self.pt.moveToChild(0)
        identifier = self.pt.getName()
        self.pt.moveToParent()
        return identifier


    # executes and returns a number from the parse tree
    def execInt(self):
        self.pt.moveToChild(0)
        num = int(self.pt.getName())
        self.pt.moveToParent()
        return num
            

i = Interpreter(ParseTree(Tokenizer(str(sys.argv[1]))))