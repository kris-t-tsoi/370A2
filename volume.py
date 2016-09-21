import os
import drive

#Yee Wing Kristy Tsoi
#ytso868


class Volume:

    #icons
    EMPTY_BLK_ICON = '-'
    USED_BLK_ICON = '+'
    FILE_ICON = 'f:'
    DIRECTORY_ICON = 'd:'

    MAX_FILE_NAME_SIZE = 8
    MAX_FILE_BLOCK_USE = 12
    FILE_DETAIL_SIZE = 64

    driveBitMapString = ''
    dataToWrite = ''
    dataRead = ''

    def __init__(self, name):
        self.name = name

    def format(self):
        pass

    def intialBitmapFormat(self):
        #write intial bit map string
        data = Volume.USED_BLK_ICON + (Volume.EMPTY_BLK_ICON*127)
        self.dataToWrite = data

        #write 6 empty file details
        for x in range(0,6):
            self.dataToWrite = self.dataToWrite +self.FILE_ICON+(' '*self.MAX_FILE_NAME_SIZE)+' '+('0'*4)+':'+((('0'*3)+' ')*self.MAX_FILE_BLOCK_USE)
            pass

        return self.dataToWrite

    def getBitmapString(self,data):
        self.driveBitMapString = data[:drive.Drive.DRIVE_SIZE]


    #adds spaces to fill up the rest of the block for writing
    def finishFormatingBlockData(self):
        i = len(self.dataToWrite)
        sizeToAdd = drive.Drive.BLK_SIZE - i
        self.dataToWrite = self.dataToWrite + (' '*sizeToAdd)


