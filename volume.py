import os
import drive

#Yee Wing Kristy Tsoi
#ytso868
from TinyDOS import TinyDOS


class Volume:

    #icons
    EMPTY_BLK_ICON = '-'
    USED_BLK_ICON = '+'
    FILE_ICON = 'f:'
    DIRECTORY_ICON = 'd:'

    MAX_FILE_NAME_SIZE = 8
    MAX_FILE_BLOCK_USE = 12
    FILE_DETAIL_SIZE = 64

    EMPTY_FILE_NAME = ' '*MAX_FILE_NAME_SIZE
    #" name5678 0000:000 000 000 000 000 000 000 000 000 000 000 000 "
    EMPTY_DETAIL = EMPTY_FILE_NAME+' '+('0'*4)+':'+((('0'*3)+' ')*MAX_FILE_BLOCK_USE)

    #block 0 data
    driveBlock0BitMap = ''
    driveBlock0FileDetails = ''

    #data to be written to or read from a block
    dataToWrite = ''
    dataRead = ''


    def __init__(self, name):
        self.name = name

    def format(self):
        pass


    def intialBitmapFormat(self):
        #write intial bit map string
        self.driveBlock0BitMap = Volume.USED_BLK_ICON + (Volume.EMPTY_BLK_ICON*127)
        self.dataToWrite = self.driveBlock0BitMap

        #write 6 empty file details
        for x in range(0,6):
            self.dataToWrite = self.dataToWrite + self.FILE_ICON +self.EMPTY_DETAIL

        return self.dataToWrite


    #get block 0 data and save to variables for easier data access
    def getBlock0Data(self,data):
        self.driveBlock0BitMap = data[:drive.Drive.DRIVE_SIZE]
        self.driveBlock0FileDetails = data[drive.Drive.DRIVE_SIZE:]


    #adds spaces to fill up the rest of the block for writing
    def finishFormatingBlockData(self):
        i = len(self.dataToWrite)
        sizeToAdd = drive.Drive.BLK_SIZE - i
        self.dataToWrite = self.dataToWrite + (' '*sizeToAdd)


    def createDirectoryFormat(self):
        self.dataToWrite =''
        for x in range(0,8):
            self.dataToWrite = self.dataToWrite + self.FILE_ICON + self.EMPTY_DETAIL

        return self.dataToWrite


    def makeFile(self, fileName):

        #if there is space in directory to write
        if self.EMPTY_FILE_NAME in self.dataRead:
            self.writeNameFirstFreeSpace(self.dataRead,fileName)
            print(self.dataToWrite)

        #else is there is no room get the next avaiable block
        else:
            #format block into directory before writing file name to it
            self.createDirectoryFormat()
            self.writeNameFirstFreeSpace(self.dataToWrite,fileName)
            print(self.dataToWrite)

            #set block to write to
            blockNumber = self.nextAvaiableBlock()

        return blockNumber




    #finds the next empty block
    def nextAvaiableBlock(self):
        return str(self.driveBlock0BitMap).find(self.EMPTY_BLK_ICON)


    #writes name to the first free name space found
    def writeNameFirstFreeSpace(self, data,fileName=''):
        self.dataToWrite = data.replace(self.EMPTY_FILE_NAME,str(fileName).ljust(self.MAX_FILE_NAME_SIZE),' ')


