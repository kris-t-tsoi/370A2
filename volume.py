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

    EMPTY_NAME_PLACE = ' '*9
    #"name5678 0000:000 000 000 000 000 000 000 000 000 000 000 000 "
    EMPTY_DETAIL = EMPTY_FILE_NAME+' '+('0'*4)+':'+((('0'*3)+' ')*MAX_FILE_BLOCK_USE)

    #block 0 data
    driveBlock0BitMap = ''

    #data to be written to or read from block 0
    dataToWrite = ''
    dataRead = ''

    extraReturn = ''
    childBlkNum =''

    #block number that contains the child's file detail(64bit)
    glbGrandParentBlkNum = ''

    # block number that contains the parent's file detail(64b
    glbParentBlkNum = ''

    # parent file detail (64bit) detail string
    glbGrandParentdet = ''

    # child file detail (64bit) detail string
    glbParentdet = ''


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
        det = ''
        for x in range(0,8):
            det = det + self.FILE_ICON + self.EMPTY_DETAIL

        return det

    # -----------------------------------------------------------------------------------------------------------------------

    def makeFile(self, fileName):

        #if there is space in directory to write
        if self.EMPTY_NAME_PLACE in self.dataRead:
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
        if self.EMPTY_NAME_PLACE in dirDetail:
            det = self.writeFileFirstFreeSpace(dirDetail, fileName)

            #change block 0 bitmap detail is dirblk is not blk0
            if dirBlk != 0:
                driveBlock0FileDetails = self.dataRead[drive.Drive.DRIVE_SIZE:]
                self.dataToWrite = self.driveBlock0BitMap +driveBlock0FileDetails

            return det

        # else is there is no room let the user know
        else:
            raise IOError("These is no more room in this directory, please create the file in another directory")

    # -----------------------------------------------------------------------------------------------------------------------
    # makes a file in the root directory
    def makeDir(self, dirName, dirBlk, parentDirDetail):

        print("volume")

        # if there is space in directory to write
        if self.EMPTY_NAME_PLACE in parentDirDetail:

            det = self.writeDirectoryFirstFreeSpace(parentDirDetail,dirName)


            print("return")
            print(det)


            return det

        # else is there is no room and directory is not blk 0
        elif dirBlk != 0:
            #to find next block

            #change file det in grandparent to add in new block

            #recursive call this funtion with new next directory


            pass
            #TODO extend somehow



        #todo if not blk 0 but reach max directory size

        #if block 0 and cant extend anymore
        else:
            raise IOError("There is no more room in root directory")

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
        dirDetail = data.replace(str(self.EMPTY_NAME_PLACE),str(fileName).ljust(self.MAX_FILE_NAME_SIZE+1,' '),1)

        #find where file name was written in the block detail string
        namePos = str(dirDetail).find(fileName)

        #get position of file details   TODO will need ot change once do nested directorys
        posFileDetail = dirDetail[namePos+self.POSITION_3_DIGIT-self.FILE_ICON_SIZE:(namePos+self.DETAIL_SIZE)]
        posFileDetail = posFileDetail.replace('0'*3, str(blkNum).rjust(3,'0'),1)

        dirDetail = dirDetail[:(namePos+self.POSITION_3_DIGIT-self.FILE_ICON_SIZE)]+posFileDetail+dirDetail[(namePos+self.DETAIL_SIZE):]
        return dirDetail


    # -----------------------------------------------------------------------------------------------------------------------
    def writeDirectoryFirstFreeSpace(self,parentDirData,dirName):

        # allocate next free block to newly created directory
        blkNum = self.nextAvaiableBlock()
        self.childBlkNum = int(blkNum)

        #format directory
        self.extraReturn = self.createDirectoryFormat()

        # write name to first free space
        parentDirData = parentDirData.replace(str(self.EMPTY_NAME_PLACE), str(dirName).ljust(self.MAX_FILE_NAME_SIZE+1, ' '), 1)

        #get position in data to write dir details to
        detPosInBlock = str(parentDirData).find(dirName) - self.FILE_ICON_SIZE

        # write name to first free space
        dirDet = self.DIRECTORY_ICON + str(dirName).ljust(self.MAX_FILE_NAME_SIZE, ' ')+' '+('0'*4)+':'+((('0'*3)+' ')*self.MAX_FILE_BLOCK_USE)

        #Add new block allocation to parent
        posFileDetail = dirDet[self.POSITION_3_DIGIT:(detPosInBlock + self.TOTAL_FILE_DETAIL_SIZE)]
        posFileDetail = posFileDetail.replace('0' * 3, str(blkNum).rjust(3, '0'), 1)

        dirDet = dirDet[:self.POSITION_3_DIGIT]+posFileDetail

        fullParentDirDet = parentDirData[:detPosInBlock] + dirDet + parentDirData[(detPosInBlock+self.TOTAL_FILE_DETAIL_SIZE):]

        return fullParentDirDet



    # -----------------------------------------------------------------------------------------------------------------------
    def getFileDetail(self, fileName,dataReadFrom):

        startDetail = str(dataReadFrom).find(fileName) - self.FILE_ICON_SIZE

        return dataReadFrom[startDetail:(startDetail+self.TOTAL_FILE_DETAIL_SIZE)]

    def emptyFileName(self):
        return self.FILE_ICON+self.EMPTY_DETAIL








