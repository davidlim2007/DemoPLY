## See Documentation for PLY :
## https://www.dabeaz.com/ply/ply.html
##
## See also Documentation on Python in General :
## Built-in Functions (https://docs.python.org/3/library/functions.html#globals)
## Learn Python Programming (https://pythonbasics.org/)
## An Informal Introduction to Python (https://docs.python.org/2/tutorial/introduction.html#)
##
## To debug a Python Program in IDLE, do the following :
## 1. Select Menu Item "Run|Python Shell"
## 2. A Python Shell Window will open.
## 3. In Python Shell, select Menu Item "Debug|Debugger"
## 4. The Debug Control Window will appear.
## 5. Return to the IDLE IDE, Select Menu Item "Run|Run Module".
##
## To learn more about how to debug a Python Program in IDLE,
## see : Debugging program in idle ide of python
## https://www.youtube.com/watch?v=AKmdfFpN5BM
##
import ply.lex as lexmodule
import sys

keyword_tokens = {
   'if',
   'else'
}

tokens = [
    "INT",
    "FLOAT",
    "IF",
    "ELSE",    
    "NAME",
    "PLUS",
    "MINUS",
    "DIVIDE",
    "MULTIPLY",
    "GREATER_THAN",
    "GREATER_THAN_OR_EQUAL_TO",
    "LESS_THAN",
    "LESS_THAN_OR_EQUAL_TO",    
    "EQUALS",
    "EQUALITY_TEST",
    "INEQUALITY_TEST",
    "TERMINATOR",
    "STATEMENT_BLOCK_START",
    "STATEMENT_BLOCK_END",
    "EXPRESSION_BLOCK_START",
    "EXPRESSION_BLOCK_END"    
]

## See PLY documentation : 4.3 Specification of tokens
## for information on how the PLY Framework determine how a PLY Module
## define the Regular Expressions associated with its List of Tokens.
##
## t_IF = r"if"  ## Advise from documentation states that Regular Expressions for keywords should be defined by functions.
## t_ELSE = r"else"
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
t_GREATER_THAN = r'>'
t_GREATER_THAN_OR_EQUAL_TO = r'>\='
t_LESS_THAN = '<'
t_LESS_THAN_OR_EQUAL_TO = '<\='
t_EQUALS = r'\='
t_EQUALITY_TEST = r"\=\="
t_INEQUALITY_TEST = r"!\="
t_ignore = " \t"
t_TERMINATOR = r';'
t_STATEMENT_BLOCK_START = r'{'
t_STATEMENT_BLOCK_END = r'}'
t_EXPRESSION_BLOCK_START = r'\('
t_EXPRESSION_BLOCK_END = r'\)'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

## t_FLOAT() must precede t_INT() otherwise a Float Value may be mistaken as an Integer.
def t_FLOAT(t) :
    r'\d+\.\d+'
    t.value = float(t.value)
    ## The now modified "t" is returned.
    ## This directly affects the return
    ## value of Lexer.token().
    return t

def t_INT(t) :
    r'\d+'  ## This line is the function documentation string. In the case of PLY, it also serves as the Regular Expression of the INT token.
    t.value = int(t.value)
    ## The now modified "t" is returned.
    ## This directly affects the return
    ## value of Lexer.token().    
    return t

def t_NAME(t) :
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    ## See PLY Documentation Section : 4.3 Specification of tokens
    ## starting at line that reads :
    ## To handle reserved words, you should write a single rule...
    if (t.value == "if"):
        t.type = 'IF'
    elif (t.value == "else"):
        t.type = 'ELSE'
    else:    
        t.type = 'NAME'
    ## The now modified "t" is returned.
    ## This directly affects the return
    ## value of Lexer.token().        
    return t

def t_error(t) :
    print("Illegal Characters : [" + t.value + "]")
    t.lexer.skip(1)    

def t_COMMENT(t):
    ## The regular expression below specifies a string that starts with ## or // followed by zero or more occurrences of any character (excpet newline)
    ## (that's what the .* indicates).
    ## Hence if PLY comes across a string that fits the above RegEx, the whole string (which is a comment) is treated as a token.
    ## See Python RegEx (https://www.w3schools.com/python/python_regex.asp).
    ##
    ## Also see PLY documentation 4.5 Discarded tokens
    ##
    r'[\#\#|//].*'  
    print("Single line comment : [" + t.value + "] Length : " + str(len(t.value)))
    pass
    ## No return value. Token discarded.
    ## This function does not return any value.
    ## This directly affects Lexer.token() in
    ## that Lexer.token() will skip this token
    ## and move onto the next token.
     
def iterate_tokens(theLexer):
    while True:
        tok = theLexer.token()
        if not tok:
            break
        print(tok)

def iterate_token_regex():
    ## Iterate over a list in Python
    ## https://www.geeksforgeeks.org/iterate-over-a-list-in-python/
    ##
    ## Note in the PLY Documentation :
    ## When a function is used to specify a Regular Expression, the regular expression rule is specified in the function documentation string.
    ## To see the Regular Expression of a Token Function, use Python Docstrings (https://www.geeksforgeeks.org/python-docstrings/)
    ##
    print("The following lists the Regular Expressions of Each Token :")
    for tok in tokens:
        print(tok, end=" : ")  ## See : How to print without newline in Python? (https://www.geeksforgeeks.org/print-without-newline-python/)
        if (tok == "IF"):
            print("if")
        elif (tok == "ELSE"):
            print("else")
        elif callable(eval("t_" + tok)):
            print(eval("t_" + tok).__doc__)
        else:        
            print(globals()["t_" + tok]) 
    
## For more information on usage of Command Line arguments in Python, see : Python - Command Line Arguments
## https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(parameters):
    iterate_token_regex()
    ## The following is a call to the ply folder lex.py source
    ## file's lex() function.
    ## The return value is an instance of a Lexer class.
    lexer = lexmodule.lex()  
    if (len(parameters) > 0):
        filename = parameters[0]
        print(filename)
        with open(filename) as f:
            content = f.read()
        print("Now about to Scan through the following Document :")
        print(content)
        lexer.input(content)
        iterate_tokens(lexer)
    else:
        while True:
            try:
                print("\r\nPlease enter code below : ")
                ## To get input from the console, code : input()
                content = input()
                lexer.input(content)
                iterate_tokens(lexer)            
            except EOFError:
                break            

## Note that Python sequentially executes all non-indented source code lines
## that it encounters in a .py file.
## See : Python Main Function
## https://www.geeksforgeeks.org/python-main-function/            
## See also : Python main function
## https://www.journaldev.com/17752/python-main-function            
##            
## For more info on the meaning of __name__ in Python, see :
## __name__ (A Special variable) in Python
## https://www.geeksforgeeks.org/__name__-special-variable-python/            
if __name__ == "__main__":
    if (len(sys.argv) > 0):
        main(sys.argv[1:])
    else:
        main([])
                    ## To understand the meaning of [1:], see : Python: What does for x in A[1:] mean?
                    ## https://stackoverflow.com/questions/27652686/python-what-does-for-x-in-a1-mean
                    ## See also :
                    ## Understanding slice notation (https://stackoverflow.com/questions/509211/understanding-slice-notation)
                    ## Python Lists and List Slices (https://docs.python.org/2/tutorial/introduction.html#lists)\
                    ## 15 Extended Slices (https://docs.python.org/2.3/whatsnew/section-slices.html)

    
    
    

