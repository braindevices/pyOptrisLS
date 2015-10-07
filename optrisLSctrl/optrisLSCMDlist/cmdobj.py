'''
Created on Oct 6, 2015-11:57:36 PM

@author: Ling Wang<LingWangNeuralEng@gmail.com>
'''
from checksum import checkData, genChecksum, genCMDwithChecksum
class CMDOBJ(object):
    def __init__(self, cmd, data_size, bytePackType = ">H", checksum_size = 1, *args, **kwargs):
        """
        in this version the checksum_size can only be 1
        """
        self.cmd = cmd
        self.data_size = data_size
        if checksum_size != 1:
            raise ValueError("In this version the checksum_size can only be 1")
        self.checksum_size = checksum_size
        self.data_size_cs = checksum_size + data_size
        if len(self.cmd)>1:
            
            self.cmd_cs = genCMDwithChecksum(cmd)
        else:
            self.cmd_cs = cmd*2
        self.bytePackType = bytePackType
        object.__init__(self, *args, **kwargs)