"""
File: utility.py
Authors: Namu

Description:
Utility functions.
"""


from inspect import currentframe, getframeinfo # for printing debug info

# print the current line + a message for debugging
#
def dmsg(msg):
    info = getframeinfo(currentframe().f_back)
    print (f"{info.filename}:{info.lineno} | {msg}")
