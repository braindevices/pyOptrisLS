'''
Created on Oct 6, 2015-11:32:14 PM

@author: Ling Wang<LingWangNeuralEng@gmail.com>
'''
from cmdobj import CMDOBJ
T_obj = CMDOBJ('\x01', 2)

status_general = CMDOBJ('\x1E', 2)

datalogger_burst = CMDOBJ('\x1A\x00', 22)

_datalogger_entry_query = '\x1A' # 1ANN the nn is number of entries we want