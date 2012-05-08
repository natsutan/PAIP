#-*- coding: utf-8 -*-
__author__ = 'Natsutani'
import sys

def prompt(prompt_str = '> '):
    print (prompt_str, end='')
    sys.stdout.flush()

def pyloop():
    interactive_interactive('> ', eval)

def interactive_interactive (prompt_str, transformer):
    prompt(prompt_str)
    for line in sys.stdin:
        print("%s" % transformer(line))
        prompt(prompt_str)


pyloop()

#(defun interactive-interpreter (prompt transformer)
#(loop
#     (print prompt)
#(print (funcall transformer (read)))))
