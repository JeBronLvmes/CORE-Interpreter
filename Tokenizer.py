# Author: Jeb Alawi
# Description: Tokenizer for CORE programming language.
# Date: 9/19/2018
import sys
import re

class Tokenizer:
    words = ['program', 'begin', 'end', 'int', 'if', 'then', 'else', 'while', 'loop', 'read', 'write', 'and', 'or']
    symbols = [';', ',', '=', '!', '[', ']', '(', ')', '+', '-', '*', '!=', '==', '>=', '<=', '>', '<']
    wSpace = ['\t', ' ', '\n']


    def __init__(self, inFileName):
        self.tokenList = [] #list of tokens
        self.builder = '' #temporary string to build the current token
        self.token = '' #the current token
        self.c = '' #the current character
        self.line = 0 #the current line
        self.inFile = open(inFileName, 'r')
        if self.inFile.mode == 'r':
            self.c = self.inFile.read(1)
            self.line = 1

    def getLine(self):
        return self.line

    def getTokenList(self):
        return self.tokenList

    #check if token is legal, add to tokenList or error and quit
    def tokenize(self):
        #check if token is an identifier
        matchedToken = re.match( r'([A-Z]+[0-9]*)', self.token, re.M)
        if matchedToken:
            identifier = matchedToken.group() == self.token
        else:
            identifier = False

        #check if token is a number
        matchedToken = re.match( r'([0-9]+)', self.token, re.M)
        if matchedToken:
            number = matchedToken.group() == self.token
        else:
            number = False

        #add appropriate token to tokenList
        if (identifier):
            if(len(self.token) > 8):
                print('Error [Line ' + str(self.line) + '] Invalid identifier \'' + self.token +'\'')
                sys.exit()
            self.tokenList.append(32)
        elif (number):
            if(len(self.token) > 8):
                print('Error [Line ' + str(self.line) + '] Invalid numeric constant \'' + self.token +'\'')
                sys.exit()
            self.tokenList.append(31)
        elif (self.token in self.symbols):
            self.tokenList.append(self.symbols.index(self.token)+14)
        elif (self.token in self.words):
            self.tokenList.append(self.words.index(self.token)+1)
        else:
            if(self.token[0].isalpha() and self.token[0].isupper()):
                print('Error [Line ' + str(self.line) + '] Invalid identifier \'' + self.token +'\'')
            elif(self.token[0].isalpha and self.token[0].islower()):
                print('Error [Line ' + str(self.line) + '] Invalid reserved word \'' + self.token +'\'')
            elif(self.token[0].isnumeric()):
                print('Error [Line ' + str(self.line) + '] Invalid numeric constant \'' + self.token +'\'')
            else:
                print('Error [Line ' + str(self.line) + '] Invalid symbols \'' + self.token +'\'')
            
            self.inFile.close()
            sys.exit()

    # advances to the next token
    # current token must not be end-of-inFile token
    def nextToken(self):
        #eat white space
        while (self.c in self.wSpace):
            # count lines
            if self.c == '\n': self.line += 1
            self.c = self.inFile.read(1)
        if (self.c in self.symbols):
            
            #get all consec symbol chars to token
            while ((self.builder+self.c) in self.symbols):
                self.builder += self.c
                self.c = self.inFile.read(1)
        else:
            #get all chars not in whitesp or symbols
            while (self.c not in self.wSpace and self.c not in self.symbols and self.c != ''):
                    self.builder += self.c
                    self.c = self.inFile.read(1)
        if self.builder != '':
            #set token
            self.token = self.builder
            self.tokenize()
            
            self.builder = ''
        if self.c == '':
            self.token=self.c

    #returns the current token    
    def currentToken(self):
        return self.token

    #populates tokenList with tokens from file
    def run(self):
        self.nextToken()
        while(self.currentToken()!='end'):
            self.nextToken()
        self.tokenList.append('33')
        self.inFile.close()

    #print list of tokens
    def printTokens(self):
        for t in self.tokenList:
            print(t)


#t = Tokenizer(str(sys.argv[1]))
#t.run()
#t.printTokens()
