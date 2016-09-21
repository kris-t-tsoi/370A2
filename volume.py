import os

#Yee Wing Kristy Tsoi
#ytso868


class Volume:

    BLK_SIZE = 512
    DRIVE_SIZE = 128

    EMPTY_BLK_ICON = '-'
    USED_BLK_ICON = '+'

    MAX_FILE_NAME_SIZE = 8
    MAX_FILE_BLOCK_USE = 12

    driveBitMapString = ""
    dataToWrite = ""
    dataRead = ""

    def __init__(self, name):
        self.name = name

    def format(self):
        pass

    def intialBitmapFormat(self):
        #write intial bit map string
        data = Volume.USED_BLK_ICON + (Volume.EMPTY_BLK_ICON*127)
        self.dataToWrite = data

        #write 6 empty file


        self.finishFormatingBlockData()
        return self.dataToWrite

    def getBitmapString(self):


        pass

    #adds spaces to fill up the rest of the block for writing
    def finishFormatingBlockData(self):
        i = len(self.dataToWrite)
        sizeToAdd = self.BLK_SIZE - i
        self.dataToWrite = self.dataToWrite + (' '*sizeToAdd)


