'''
Created on Oct 6, 2015-11:29:18 PM

@author: Ling Wang<LingWangNeuralEng@gmail.com>
'''
from cmdobj import CMDOBJ

revision_firmware = CMDOBJ('\x10', 2)

revision_hardware = CMDOBJ('\x11', 2)

model_code = CMDOBJ('\x17', 2)
