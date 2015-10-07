'''
Created on Oct 7, 2015-12:01:38 AM

@author: Ling Wang<LingWangNeuralEng@gmail.com>
'''
import operator

def genChecksum(x):
    """
    x is a bytearray
    """
    return reduce(operator.xor, x)
    
def checkData(x, debug = False):
    
    flag = genChecksum(x) == '\x00'
    if debug and not flag:
        print "\n checksum does not match: ", x.__repr__()
    return flag

def genCMDwithChecksum(cmd):
    """
    cmd is a bytearray with len > 1. With len ==1, just do cmd*2
    """
    
    _checksum = genChecksum(cmd)
    return cmd.append(_checksum)