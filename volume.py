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
    POSITION_FILE_LENGTH = 11
    POSITION_3_DIGIT = 16

    TOTAL_FILE_DETAIL_SIZE = 64
    DETAIL_SIZE = 62
    FILE_ICON_SIZE =2

    EMPTY_FILE_NAME = ' '*MAX_FILE_NAME_SIZE
    #" name5678 0000:000 000 000 000 000 000 000 000 000 000 000 000 "
    EMPTY_DETAIL = EMPTY_FILE_NAME+' '+('0'*4)+':'+((('0'*3)+' ')*MAX_FILE_BLOCK_USE)

    #block 0 data
    driveBlock0BitMap = ''

    #data to be written to or read from a block
    dataToWrite = ''
    dataRead = ''

    # -----------------------------------------------------------------------------------------------------------------------
    def __init__(self, name):
        self.name = name

    # -----------------------------------------------------------------------------------------------------------------------
    def intialBitmapFormat(self):
        #write intial bit map string
        self.driveBlock0BitMap = Volume.USED_BLK_ICON + (Volume.EMPTY_BLK_ICON*127)
        self.dataToWrite = self.driveBlock0BitMap

        #write 6 empty file details
        for x in range(0,6):
            self.dataToWrite = self.dataToWrite + self.FILE_ICON +self.EMPTY_DETAIL

        return self.dataToWrite

    # -----------------------------------------------------------------------------------------------------------------------
    #get block 0 data and save to variables for easier data access
    def getBlock0Data(self,data):
        self.driveBlock0BitMap = data[:drive.Drive.DRIVE_SIZE]

    # -----------------------------------------------------------------------------------------------------------------------
    def updateBlk0BitmapToBeWritten(self,data):
        self.dataToWrite = self.driveBlock0BitMap + data[128:]

    # -----------------------------------------------------------------------------------------------------------------------
    #adds spaces to fill up the rest of the block for writing
    def finishFormatingBlockData(self,data):
        i = len(data)
        sizeToAdd = drive.Drive.BLK_SIZE - i
        data = data + (' '*sizeToAdd)
        return data

    # -----------------------------------------------------------------------------------------------------------------------
    #format for new directory
    def createDirectoryFormat(self):
        self.dataToWrite =''
        for x in range(0,8):
            self.dataToWrite = self.dataToWrite + self.FILE_ICON + self.EMPTY_DETAIL

        return self.dataToWrite

    # -----------------------------------------------------------------------------------------------------------------------
    #TODO create method which change parent directory detail for nested directories

    #TODO does not change dir details in parent block
    def makeFile(self, fileName):

        #if there is space in directory to write
        if self.EMPTY_FILE_NAME in self.dataRead:
            self.writeFileFirstFreeSpace(self.dataRead,fileName)

        #else is there is no room get the next avaiable block
        else:

            #TODO change detail in parent directory

            # set block to write to
            blockNumber = self.nextAvaiableBlock()

            #format block into directory before writing file name to it
            self.createDirectoryFormat()
            self.writeFileFirstFreeSpace(self.dataToWrite,fileName)

        return blockNumber

    # -----------------------------------------------------------------------------------------------------------------------
    #makes a file in the root directory
    def makeBlkFile(self, fileName,dirBlk, dirDetail):

        # if there is space in directory to write
        if self.EMPTY_FILE_NAME in dirDetail:
            det = self.writeFileFirstFreeSpace(dirDetail, fileName)

            #change block 0 bitmap detail
            driveBlock0FileDetails = self.dataRead[drive.Drive.DRIVE_SIZE:]
            self.dataToWrite = self.driveBlock0BitMap +driveBlock0FileDetails

            return det

        # else is there is no room let the user know and keep data in blk 0 as it is
        else:
            raise IOError("These is no more room in this directory, please create the file in another directory")


    # -----------------------------------------------------------------------------------------------------------------------
    #finds the next empty block
    def nextAvaiableBlock(self):
        blkNum = str(self.driveBlock0BitMap).find(self.EMPTY_BLK_ICON)

        #change bitmap
        self.driveBlock0BitMap = self.driveBlock0BitMap[:blkNum]+self.USED_BLK_ICON+self.driveBlock0BitMap[(blkNum+1):]

        return blkNum

    # -----------------------------------------------------------------------------------------------------------------------
    #writes name to the first free name space found
    def writeFileFirstFreeSpace(self, data,fileName=''):

        #allocate next free block to newly created file
        blkNum = self.nextAvaiableBlock()

        #write name to first free space
        dirDetail = data.replace(str(self.EMPTY_FILE_NAME),str(fileName).ljust(self.MAX_FILE_NAME_SIZE,' '),1)

        #find where file name was written in the block detail string
        namePos = str(dirDetail).find(fileName)

        #get position of file details
        posFileDetail = dirDetail[namePos+self.POSITION_3_DIGIT-self.FILE_ICON_SIZE:(namePos+self.DETAIL_SIZE)]
        posFileDetail = posFileDetail.replace('0'*3, str(blkNum).rjust(3,'0'),1)

        dirDetail = dirDetail[:(namePos+self.POSITION_3_DIGIT-self.FILE_ICON_SIZE)]+posFileDetail+dirDetail[(namePos+self.DETAIL_SIZE):]
        return dirDetail

    # -----------------------------------------------------------------------------------------------------------------------
    def getFileDetail(self, fileName,dataReadFrom):

        startDetail = str(dataReadFrom).find(fileName) - self.FILE_ICON_SIZE

        return dataReadFrom[startDetail:(startDetail+self.TOTAL_FILE_DETAIL_SIZE)]
