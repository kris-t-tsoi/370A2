import os
import sys
import fileinput
import drive
import volume
from subprocess import call

#Yee Wing Kristy Tsoi
#ytso868

class TinyDOS:

    driveName = None
    driveInst = None
    volumeInst = None

    # -----------------------------------------------------------------------------------------------------------------------
    #gets file details and returns list of all blocks allovated to it
    def getAllocatedBlocks(self, fileDet):

        # get blocks allocated to file and split into array of allocations
        blksAllocated = fileDet[self.volumeInst.POSITION_3_DIGIT:]
        blkList = str(blksAllocated).split(' ')  # note has extra '' at last index as there was space

        return blkList
    # -----------------------------------------------------------------------------------------------------------------------

    #path is userPathFile[:-1] (so path does not contain the child (dir/fil that is to be read/written/made to
    def recurDOSFile(self, gpBlkNum,path=None,isFile = False):

        print("recursive")

        print("path length: " + str(len(path)))
        print(str(path))


        # get grandparent directory block allocations det from blk
        self.volumeInst.glbGrandParentdet = self.driveInst.read_block(gpBlkNum)

        # reads directory data
        directoryDetail = self.volumeInst.glbGrandParentdet

        print("gp blk: " + str(gpBlkNum))


        #
        if len(path) > 2:

            print(str(directoryDetail))
            print("argument 0 " + path[0])

            #if existing diretory
            if path[0] in directoryDetail:

                if self.isDirectory(directoryDetail,path[0]):

                    print("in multi")

                    # get position
                    dirDetPosInBlock = str(path[0]).find(directoryDetail) - self.volumeInst.FILE_ICON_SIZE

                    # get file detail
                    dirDet = self.volumeInst.getFileDetail(path[0], directoryDetail)


                    print("dir det")
                    print(dirDet)

                    # get 4dig rep length
                    dirLen = int(
                        dirDet[self.volumeInst.POSITION_FILE_LENGTH:(self.volumeInst.POSITION_FILE_LENGTH + 4)])

                    # get blocks allocated to file and split into array of allocations
                    blkList = self.getAllocatedBlocks(dirDet)

                    for x in range(0, 12):
                        blkNum = int(blkList[x])
                        if blkNum == 0:
                            break
                        else:
                            det = self.driveInst.read_block(blkNum)

                            if path[1] in det:
                                if self.isDirectory(det, path[1]):
                                    directoryDetail = det

                                    print("find ag1 "+path[1]+"in "+str(blkNum))
                                    print("dir det")
                                    print(directoryDetail)

                                    self.volumeInst.glbParentBlkNum = blkNum
                                    self.volumeInst.glbGrandParentBlkNum = gpBlkNum

                                    print("grandparent now changed to: " + str(self.volumeInst.glbGrandParentBlkNum))
                                    print("parent now changed to: " + str(self.volumeInst.glbParentBlkNum))

                                else:
                                    raise IOError("Path incorrect, can not use file as directory")



                    self.volumeInst.glbGrandParentdet = self.driveInst.read_block(self.volumeInst.glbGrandParentBlkNum)
                    self.volumeInst.glbParentdet = self.driveInst.read_block(self.volumeInst.glbParentBlkNum)

                    print("grand parent")
                    print(self.volumeInst.glbGrandParentBlkNum)

                    print("parent")
                    print(self.volumeInst.glbParentBlkNum)

                    #find next gp and p in path
                    return self.recurDOSFile(self.volumeInst.glbParentBlkNum, path[1:],isFile=isFile)

                #is a file type
                else:
                    raise IOError("Path is invalid, can not have a file type within path")
            #name not exist in dir detail
            else:
                raise IOError("Path is invalid")


        elif gpBlkNum == 0:

            # if existing diretory
            if path[0] in directoryDetail:

                if self.isDirectory(directoryDetail, path[0]):

                    print("in")

                    # get position
                    dirDetPosInBlock = str(directoryDetail).find(path[0]) - self.volumeInst.FILE_ICON_SIZE

                    # get file detail
                    dirDet = self.volumeInst.getFileDetail(path[0], directoryDetail)

                    # get 4dig rep length
                    dirLen = int(
                        dirDet[self.volumeInst.POSITION_FILE_LENGTH:(self.volumeInst.POSITION_FILE_LENGTH + 4)])

                    # divide to find how many block are used
                    index = int(dirLen / self.driveInst.BLK_SIZE)

                    lastDataLen = int(dirLen % self.driveInst.BLK_SIZE)

                    print("index " + str(index))
                    print("lastDataLen " + str(lastDataLen))

                    # if next file is not full
                    if lastDataLen != 0:  # and isFile == False:
                        index = index + 1

                    # get blocks allocated to file and split into array of allocations
                    blkList = self.getAllocatedBlocks(dirDet)

                    print("block allocation")
                    print(blkList)

                    parentBlk = 0

                    # if there is no data at all
                    if int(blkList[index]) == 0 and lastDataLen != 0:
                        # get first free block block to be written to
                        parentBlk = self.volumeInst.nextAvaiableBlock()
                        print("gg")

                    elif int(blkList[index]) == 0:
                        parentBlk = int(blkList[index - 1])
                        if parentBlk == 0:
                            parentBlk = int(blkList[index - 2])
                        print("hh")

                    else:
                        parentBlk = int(blkList[index])
                        print("aa")

                    print("parent")
                    print(parentBlk)

                    self.volumeInst.glbParentBlkNum = parentBlk
                    self.volumeInst.glbGrandParentBlkNum = gpBlkNum

                    print("grandparent now changed to: " + str(self.volumeInst.glbGrandParentBlkNum))
                    print("parent now changed to: " + str(self.volumeInst.glbParentBlkNum))

                    self.volumeInst.glbGrandParentdet = self.driveInst.read_block(self.volumeInst.glbGrandParentBlkNum)
                    self.volumeInst.glbParentdet = self.driveInst.read_block(self.volumeInst.glbParentBlkNum)

                    # return parent blk num
                    return self.volumeInst.glbParentBlkNum

                else:
                    raise IOError("Path incorrect, can not use file as directory")



        else:

            # if existing diretory
            if path[0] in directoryDetail:

                if self.isDirectory(directoryDetail, path[0]):

                    print("in")

                    # get position
                    dirDetPosInBlock = str(directoryDetail).find(path[0]) - self.volumeInst.FILE_ICON_SIZE

                    # get file detail
                    dirDet = self.volumeInst.getFileDetail(path[0], directoryDetail)

                    # get 4dig rep length
                    dirLen = int(
                        dirDet[self.volumeInst.POSITION_FILE_LENGTH:(self.volumeInst.POSITION_FILE_LENGTH + 4)])

                    # get blocks allocated to file and split into array of allocations
                    blkList = self.getAllocatedBlocks(dirDet)


                    print("block allocation")
                    print(blkList)

                    lastIn = 0


                    for x in range(0,12):
                        blkNo = int(blkList[x])
                        if blkNo == 0:
                            break
                        else:
                            lastIn = blkNo

                    parentBlk= lastIn


                    print("parent")
                    print(parentBlk)


                    self.volumeInst.glbParentBlkNum = parentBlk
                    self.volumeInst.glbGrandParentBlkNum = gpBlkNum


                    print("grandparent now changed to: " + str(self.volumeInst.glbGrandParentBlkNum))
                    print("parent now changed to: " + str(self.volumeInst.glbParentBlkNum))


                    self.volumeInst.glbGrandParentdet = self.driveInst.read_block(self.volumeInst.glbGrandParentBlkNum)
                    self.volumeInst.glbParentdet = self.driveInst.read_block(self.volumeInst.glbParentBlkNum)

                    # return parent blk num
                    return self.volumeInst.glbParentBlkNum

                else:
                    raise IOError("Path incorrect, can not use file as directory")


    # -----------------------------------------------------------------------------------------------------------------------
    def format(self):
        #initiate and format drive file and save instance
        self.driveInst = drive.Drive(self.driveName)
        self.driveInst.format()

        #create a volume instance and write the intial bitmap
        volData = volume.Volume(self.driveName)
        volData.intialBitmapFormat()
        self.driveInst.write_block(0, volData.dataToWrite)

        #save volData as the current volume instance
        self.volumeInst = volData
        self.volumeInst.tinydos = self

        #let the user know
        print("Created: " + self.driveName)

    # -----------------------------------------------------------------------------------------------------------------------
    def reconnect(self):
        self.driveInst = drive.Drive(os.getcwd()+'/'+self.driveName)
        self.driveInst.reconnect()

        #get block 0 information
        self.volumeInst = volume.Volume(self.driveName)
        self.volumeInst.getBlock0Data(self.driveInst.read_block(0))
        self.volumeInst.tinydos = self

        print("Successful reconnection to: "+self.driveName)

    # -----------------------------------------------------------------------------------------------------------------------
    def list(self,pathname):

        if ' ' in pathname:
            print("path can not contain any spaces")

        elif pathname[0] != '/':
            print('root directory is not in pathname')

        else:
            args = pathname.split('/')

            # set default directory block number where file is to be created in
            directoryDetBlkNum = 0

             # reset data to write to ''
            self.volumeInst.dataToWrite = ''

            #if root
            if len(args) == 2 and args[1] == '':

                # reads directory data
                dirDet = self.driveInst.read_block(directoryDetBlkNum)

                if self.checkIfDirectoryEmpty(dirDet,'',isRoot=True) == True:
                    print("Directory " + str(pathname) + " has no files")
                    return

                else:

                    if dirDet.count(' '*9) == 6:
                        raise IOError("Root Directory has no files")
                    else:
                        for x in range(0,6):

                            name = dirDet[self.driveInst.DRIVE_SIZE+(x*self.volumeInst.TOTAL_FILE_DETAIL_SIZE):
                                            self.driveInst.DRIVE_SIZE+(x*self.volumeInst.TOTAL_FILE_DETAIL_SIZE)+2+self.volumeInst.MAX_FILE_NAME_SIZE]
                            size = int(dirDet[self.driveInst.DRIVE_SIZE+(x*self.volumeInst.TOTAL_FILE_DETAIL_SIZE)+self.volumeInst.POSITION_FILE_LENGTH:
                                            (self.volumeInst.POSITION_FILE_LENGTH + 4)+self.driveInst.DRIVE_SIZE+(x*self.volumeInst.TOTAL_FILE_DETAIL_SIZE)])


                            if ('f:'+' '*8) == name or ('d:'+' '*8) == name:
                                pass
                            else:

                                print(str(name)+' has Size: '+str(size))


            else:

                dirName = args[len(args) - 1]

                parenttblk = 0

                if len(args) != 2:
                    directoryDetBlkNum = self.recurDOSFile(0, path=args[1:-1], isFile=False)

                gparentDet =''

                if len(args) < 3:
                    self.volumeInst.childBlkNum = self.findChildBlkNum(dirName, self.volumeInst.glbGrandParentdet)
                    gparentDet = self.volumeInst.glbGrandParentdet
                else:
                    self.volumeInst.childBlkNum = self.findChildBlkNum(dirName, self.volumeInst.glbParentdet)
                    gparentDet = self.volumeInst.glbParentdet

                if self.checkIfDirectoryEmpty(gparentDet,dirName, isRoot=False) == True:
                    print("Directory " + str(pathname) + " has no files")
                    return

                else:

                    # get allocated blks
                    fileDet = self.volumeInst.getFileDetail(dirName, gparentDet)

                    # get blocks allocated to directory and split into array of allocations
                    blksAllocated = fileDet[self.volumeInst.POSITION_3_DIGIT:]
                    blkList = str(blksAllocated).split(' ')  # note has extra '' at last index as there was space

                    for x in range(0, 12):
                        blknum = int(blkList[x])

                        if blknum != 0:

                            #read data in that block
                            dirDet = self.driveInst.read_block(blknum)

                            for y in range(0,8):

                                name = dirDet[(y * self.volumeInst.TOTAL_FILE_DETAIL_SIZE):(y * self.volumeInst.TOTAL_FILE_DETAIL_SIZE) + 2 + self.volumeInst.MAX_FILE_NAME_SIZE]

                                size =int(dirDet[(y*self.volumeInst.TOTAL_FILE_DETAIL_SIZE)+self.volumeInst.POSITION_FILE_LENGTH:
                                                (self.volumeInst.POSITION_FILE_LENGTH + 4)+(y*self.volumeInst.TOTAL_FILE_DETAIL_SIZE)])

                                if ('f:' + ' ' * 8) == name or ('d:' + ' ' * 8) == name:
                                    pass
                                else:
                                    print(str(name) + ' has Size: ' + str(size))


    # -----------------------------------------------------------------------------------------------------------------------
    def makeFile(self, pathname):

        if ' ' in pathname:
            print("path can not contain any spaces")

        elif pathname[0] != '/':
            print('root directory is not in pathname')

        else:

            args = pathname.split('/')
            fileName = args[len(args) - 1]

            print("args is")
            print(args)

            # set default directory block number where file is to be created in
            directoryDetBlkNum = 0

            # initalise block number where file data is
            blockNumber = 0

            # reset data to write to ''
            self.volumeInst.dataToWrite = ''

            self.volumeInst.childBlkNum = ''

            # if nested directory, find blk where directory detail is stored
            if len(args) != 2:
                directoryDetBlkNum = self.recurDOSFile(0,path=args[1:-1], isFile = True)
                if len(args) < 3:
                    self.volumeInst.childBlkNum = self.findChildBlkNum(args[-2], self.volumeInst.glbGrandParentdet)
                else:
                    self.volumeInst.childBlkNum = self.findChildBlkNum(args[-2], self.volumeInst.glbParentdet)



            writeblkNum = directoryDetBlkNum

            if self.volumeInst.childBlkNum != '':
                writeblkNum = self.volumeInst.childBlkNum

            dirDet = self.driveInst.read_block(writeblkNum)


            self.updateBitMap()

            if dirDet == self.driveInst.EMPTY_BLK:
                dirDet = self.volumeInst.createDirectoryFormat()
                self.driveInst.write_block(directoryDetBlkNum,dirDet)

            # check if file or directory of same name is in the directory
            if fileName in dirDet:
                raise IOError("Sorry you can not have the same named file/directory within a single directory")
            else:
                #get bitmap details
                if directoryDetBlkNum != 0 :
                    self.volumeInst.dataRead = self.driveInst.read_block(0)


                print("blk detail: " + str(writeblkNum))
                print(dirDet)

                # pass in file name and directly blk number into volume to create data to write
                dirDet =self.volumeInst.makeBlkFile(fileName,directoryDetBlkNum,dirDet)
                self.driveInst.write_block(int(writeblkNum),dirDet)

                print("detail: after create" + str(writeblkNum))
                print(dirDet)


                #update bitmape
                if directoryDetBlkNum != 0:
                    self.driveInst.write_block(0,self.volumeInst.dataToWrite)


    # -----------------------------------------------------------------------------------------------------------------------
    def findChildBlkNum(self,pDirName, pdirDet):

        print("in find child blk num")

        # get position
        dirDetPosInBlock = str(pdirDet).find(pDirName) - self.volumeInst.FILE_ICON_SIZE

        # get file detail
        dirDet = self.volumeInst.getFileDetail(pDirName, pdirDet)

        # get 4dig rep length
        dirLen = int(
            dirDet[self.volumeInst.POSITION_FILE_LENGTH:(self.volumeInst.POSITION_FILE_LENGTH + 4)])

        # get blocks allocated to file and split into array of allocations
        blkList = self.getAllocatedBlocks(dirDet)

        print("block allocation")
        print(blkList)


        # loop through all blocks allocated to GP direct
        for x in range(0, 12):
            blkNum = int(blkList[x])

            if blkNum == 0:
                break

            return blkNum


    # -----------------------------------------------------------------------------------------------------------------------
    def makeDirectory(self,pathname):

        if ' ' in pathname:
            print("path can not contain any spaces")

        elif pathname[0] != '/':
            print('root directory is not in pathname')

        else:

            args = pathname.split('/')
            fileName = args[len(args) - 1]

            #set default directory block number where file is to be created in
            directoryDetBlkNum = 0

            #initalise block number where file data is
            blockNumber = 0

            # reset data to write to ''
            self.volumeInst.dataToWrite = ''

            self.volumeInst.childBlkNum = ''

            #if nested directory, find blk where directory detail is stored
            if len(args) != 2:
                directoryDetBlkNum = self.recurDOSFile(0, path=args[1:-1], isFile=False)

                if len(args)>3:
                    self.volumeInst.childBlkNum = self.findChildBlkNum(args[-2],self.volumeInst.glbParentdet)


            writeblkNum = directoryDetBlkNum

            if self.volumeInst.childBlkNum != '':
                writeblkNum = self.volumeInst.childBlkNum


            dirDet = self.driveInst.read_block(writeblkNum)

            #update bitmap
            self.updateBitMap()

            # check if file or directory of same name is in the directory
            if fileName in dirDet:
                raise IOError("Sorry you can not have the same named file/directory within a single directory")
            else:


                # get bitmap details
                if directoryDetBlkNum != 0:
                    self.volumeInst.dataRead = self.driveInst.read_block(0)

                # pass in file name and directly blk number into volume to create data to write
                directoryDetail = self.volumeInst.makeDir(fileName, directoryDetBlkNum, dirDet)
                newDirData = self.volumeInst.extraReturn
                newDirBlkNum = self.volumeInst.childBlkNum

                #write new dir data into directory
                self.driveInst.write_block(int(newDirBlkNum),newDirData)
                self.driveInst.write_block(writeblkNum,directoryDetail)

                # update bitmap
                if directoryDetBlkNum != 0:
                    self.driveInst.write_block(0, self.volumeInst.dataToWrite)

                #if need to change file length of grandparent direct det
                if len(args) != 2:

                    parentName = args[len(args) - 2]
                    gpdata = self.volumeInst.glbGrandParentdet
                    gpBlkNum = self.volumeInst.glbGrandParentBlkNum

                    if len(args)>3:
                        gpdata = self.volumeInst.glbParentdet
                        gpBlkNum = self.volumeInst.glbParentBlkNum

                    detPosInBlock = str(gpdata).find(parentName) - self.volumeInst.FILE_ICON_SIZE

                    fileDet = self.volumeInst.getFileDetail(parentName, gpdata)

                    # get 4dig rep length
                    fileLen = int(fileDet[self.volumeInst.POSITION_FILE_LENGTH:(self.volumeInst.POSITION_FILE_LENGTH + 4)])

                    totalLength = fileLen+self.driveInst.BLK_SIZE

                    fileDet = fileDet[:self.volumeInst.POSITION_FILE_LENGTH] + str(totalLength).rjust(4, '0') + ':'+fileDet[(self.volumeInst.POSITION_3_DIGIT):]

                    toWriteGP =directoryDetail = gpdata[:detPosInBlock]+fileDet+gpdata[(detPosInBlock+self.volumeInst.TOTAL_FILE_DETAIL_SIZE):]

                    self.driveInst.write_block(gpBlkNum,toWriteGP)

                    if gpBlkNum == 0:
                        self.volumeInst.dataToWrite = self.driveInst.read_block(0)


                # update bitmap if not block 0
                if directoryDetBlkNum != 0:
                    self.driveInst.write_block(0, self.volumeInst.dataToWrite)




    #-----------------------------------------------------------------------------------------------------------------------

    def appendToFile(self, pathname, data):

        if ' ' in pathname:
            print("path can not contain any spaces")

        elif pathname[0] != '/':
            print('root directory is not in pathname')

        else:

            args = pathname.split('/')
            fileName = args[len(args) - 1]

            #set default directory block number where file is to be created in
            directoryDetBlkNum = 0

            #initalise block number where file data is
            blockNumber = 0

            #reset data to write to ''
            self.volumeInst.dataToWrite = ''

            self.volumeInst.childBlkNum = ''

            if len(args) != 2:
                directoryDetBlkNum = self.recurDOSFile(0, path=args[1:-1], isFile=True)
                if len(args) ==3:
                    directoryDetBlkNum = 0
                detail = self.driveInst.read_block(directoryDetBlkNum)
                self.volumeInst.childBlkNum = self.findChildBlkNum(args[-2],detail)


            writeblkNum = directoryDetBlkNum

            if self.volumeInst.childBlkNum != '':
                writeblkNum = self.volumeInst.childBlkNum


            #reads directory data
            directoryDetail = self.driveInst.read_block(writeblkNum)

            self.updateBitMap()

            #check if file or directory of same name is in the directory
            if fileName in directoryDetail:
                fileDetPosInBlock = str(directoryDetail).find(fileName) - self.volumeInst.FILE_ICON_SIZE
                fileDet = self.volumeInst.getFileDetail(fileName,directoryDetail)

                if fileDet[:2] != self.volumeInst.FILE_ICON:
                    raise IOError("This is not a file and therefore can not append data to it")


                #get 4dig rep length
                fileLen = int(fileDet[self.volumeInst.POSITION_FILE_LENGTH:(self.volumeInst.POSITION_FILE_LENGTH+4)])


                #get blocks allocated to file and split into array of allocations
                blksAllocated = fileDet[self.volumeInst.POSITION_3_DIGIT:]
                blkList = str(blksAllocated).split(' ') #note has extra '' at last index as there was space

                #length of data to write
                lenDataToWrite = len(data)

                #get total length of file
                totalFileLen = lenDataToWrite + fileLen

                # divide to find which of 12 blocks 3dig to go to
                index = int(fileLen / self.driveInst.BLK_SIZE)

                #if the the last blk is already full
                if index != 0 and int(fileLen % self.driveInst.BLK_SIZE) == 0:
                    index = index + 1

                #while there is still data to write
                while lenDataToWrite >0 :

                    dataLenInBlk = 0
                    writenIntoBlock = ''

                    #if there is no block allocated
                    if int(blkList[index]) == 0:

                        #allocate new block
                        blockNumber = self.volumeInst.nextAvaiableBlock()

                        blkList[index] = blockNumber

                    #block allocated already has written data in
                    else:
                        #get block that still has space
                        blockNumber = int(blkList[index])
                        #length of data already in block
                        dataLenInBlk = int(fileLen % self.driveInst.BLK_SIZE)


                    #get data to be written from user's input data
                    dataAdd = data[:(self.driveInst.BLK_SIZE-int(dataLenInBlk))]

                    #get data from block
                    dataFromBlock = self.driveInst.read_block(blockNumber)

                    #add new data after data stored in block
                    writenIntoBlock =  dataFromBlock[:int(dataLenInBlk)]+dataAdd
                    writenIntoBlock = self.volumeInst.finishFormatingBlockData(writenIntoBlock)

                    #remove data the was just written
                    data = data[len(dataAdd):]

                    #remove length added
                    lenDataToWrite = lenDataToWrite - len(dataAdd)

                    #write data into file block
                    self.driveInst.write_block(blockNumber,writenIntoBlock)

                    #get next index prepared if need to write to another file
                    index = index +1

                #convert blk allocation array into string
                blksAllocated = ''
                for x in range(0,12):
                    blksAllocated = blksAllocated +str(blkList[x]).rjust(3, '0')+' '

                #update file detail in directory details
                fileDet = fileDet[:self.volumeInst.POSITION_FILE_LENGTH] + str(totalFileLen).rjust(4, '0') + ':'+str(blksAllocated)
                directoryDetail = directoryDetail[:fileDetPosInBlock]+fileDet+directoryDetail[(fileDetPosInBlock+self.volumeInst.TOTAL_FILE_DETAIL_SIZE):]
                self.driveInst.write_block(writeblkNum, directoryDetail)

                #update bitmap in block 0
                blk0data = self.driveInst.read_block(0)
                self.volumeInst.updateBlk0BitmapToBeWritten(blk0data)
                self.driveInst.write_block(0,self.volumeInst.dataToWrite)


            else:
                print(str(fileName)+" does not exist in this directory")



    # -----------------------------------------------------------------------------------------------------------------------
    def printFile(self, pathname):

        if ' ' in pathname:
            print("path can not contain any spaces")

        elif pathname[0] != '/':
            print('root directory is not in pathname')
        else:

            args = pathname.split('/')
            fileName = args[len(args) - 1]

            #set default directory block number where file is
            directoryDetBlkNum = 0

            #initalise block number where file data is
            blockNumber = 0

            #reset data to write to ''
            self.volumeInst.dataToWrite = ''

            self.volumeInst.childBlkNum = ''

            if len(args) != 2:
                directoryDetBlkNum = self.recurDOSFile(0, path=args[1:-1], isFile=True)

                if len(args) ==3:
                    directoryDetBlkNum = 0

                detail = self.driveInst.read_block(directoryDetBlkNum)
                self.volumeInst.childBlkNum = self.findChildBlkNum(args[-2], detail)

            writeblkNum = directoryDetBlkNum

            if self.volumeInst.childBlkNum != '':
                writeblkNum = self.volumeInst.childBlkNum

            # reads directory data
            directoryDetail = self.driveInst.read_block(writeblkNum)

            self.updateBitMap()

            # check if file or directory of same name is in the directory
            if fileName in directoryDetail:
                fileDetPosInBlock = str(directoryDetail).find(fileName) - self.volumeInst.FILE_ICON_SIZE
                fileDet = self.volumeInst.getFileDetail(fileName, directoryDetail)

                if fileDet[:2] != self.volumeInst.FILE_ICON:
                    raise IOError("This is not a file and therefore can not print data")

                #get 4dig rep length
                fileLen = int(fileDet[self.volumeInst.POSITION_FILE_LENGTH:(self.volumeInst.POSITION_FILE_LENGTH+4)])

                # if there is no data
                if fileLen == 0:
                    raise IOError('This file is empty and has not data to print')

                # divide to find how many files are used
                index = int(fileLen / self.driveInst.BLK_SIZE)

                lastDataLen = int(fileLen % self.driveInst.BLK_SIZE)

                #get blocks allocated to file and split into array of allocations
                blksAllocated = fileDet[self.volumeInst.POSITION_3_DIGIT:]
                blkList = str(blksAllocated).split(' ') #note has extra '' at last index as there was space

                for x in range(0,(index+1)):
                    fileBlkNum = int(blkList[x])
                    dataPrint = self.driveInst.read_block(fileBlkNum)

                    #if last block, only print out actual data
                    if x == index:
                        print(str(dataPrint[:lastDataLen]))
                    else:
                        print(str(dataPrint))

    # -----------------------------------------------------------------------------------------------------------------------
    def deleteFile(self,pathname):

        if ' ' in pathname:
            print("path can not contain any spaces")

        elif pathname[0] != '/':
            print('root directory is not in pathname')

        else:

            args = pathname.split('/')
            fileName = args[len(args) - 1]

            #set default directory block number where file is to be created in
            directoryDetBlkNum = 0

            #initalise block number where file data is
            blockNumber = 0

            #reset data to write to ''
            self.volumeInst.dataToWrite = ''

            self.volumeInst.childBlkNum = ''

            if len(args) != 2:
                directoryDetBlkNum = self.recurDOSFile(0, path=args[1:-1], isFile=True)

                if len(args) ==3:
                    directoryDetBlkNum = 0

                detail = self.driveInst.read_block(directoryDetBlkNum)
                self.volumeInst.childBlkNum = self.findChildBlkNum(args[-2], detail)


            writeblkNum = directoryDetBlkNum

            if self.volumeInst.childBlkNum != '':
                writeblkNum = self.volumeInst.childBlkNum

            # reads directory data
            directoryDetail = self.driveInst.read_block(writeblkNum)

            self.updateBitMap()


            #check if file or directory of same name is in the directory
            if fileName in directoryDetail:
                fileDetPosInBlock = str(directoryDetail).find(fileName) - self.volumeInst.FILE_ICON_SIZE
                fileDet = self.volumeInst.getFileDetail(fileName,directoryDetail)

                #get blocks allocated to file and split into array of allocations
                blksAllocated = fileDet[self.volumeInst.POSITION_3_DIGIT:]
                blkList = str(blksAllocated).split(' ') #note has extra '' at last index as there was space
                bitmap = self.volumeInst.driveBlock0BitMap

                for x in range(0, 12):
                    fileBlkNum = int(blkList[x])

                    if fileBlkNum == 0:
                        break
                    else:
                        #remove from bitmap
                        self.volumeInst.driveBlock0BitMap=self.volumeInst.driveBlock0BitMap[:fileBlkNum] + self.volumeInst.EMPTY_BLK_ICON + self.volumeInst.driveBlock0BitMap[(fileBlkNum + 1):]
                        self.driveInst.write_block(fileBlkNum, self.driveInst.EMPTY_BLK)

                #update directory with empty file detail
                changeFilDet = directoryDetail[:fileDetPosInBlock]+self.volumeInst.emptyFileName()+directoryDetail[(fileDetPosInBlock+self.volumeInst.TOTAL_FILE_DETAIL_SIZE):]

                self.driveInst.write_block(writeblkNum,changeFilDet)

                # update bitmap in block 0
                blk0data = self.driveInst.read_block(0)
                self.volumeInst.updateBlk0BitmapToBeWritten(blk0data)
                self.driveInst.write_block(0, self.volumeInst.dataToWrite)


    # -----------------------------------------------------------------------------------------------------------------------
    def deleteDirectory(self, pathname):

        if ' ' in pathname:
            print("path can not contain any spaces")

        elif pathname[0] != '/':
            print('root directory is not in pathname')

        else:

            args = pathname.split('/')
            dirName = args[len(args) - 1]

            # set default directory block number where file is to be created in
            directoryDetBlkNum = 0

            # initalise block number where file data is
            blockNumber = 0

            # reset data to write to ''
            self.volumeInst.dataToWrite = ''

            self.volumeInst.childBlkNum = ''


            #get parent and grandparent blk num and details
            if len(args) != 2:
                directoryDetBlkNum = self.recurDOSFile(0, path=args[1:-1], isFile=True)  # todo fix

                #--

                if len(args) == 3:
                    directoryDetBlkNum = 0

                detail = self.driveInst.read_block(directoryDetBlkNum)
                self.volumeInst.childBlkNum = self.findChildBlkNum(args[-2], detail)


                # if len(args) > 3:
                #     self.volumeInst.childBlkNum = self.findChildBlkNum(args[-2], self.volumeInst.glbParentdet)

                #--



            writeblkNum = directoryDetBlkNum

            if self.volumeInst.childBlkNum != '':
                writeblkNum = self.volumeInst.childBlkNum

            # reads directory data
            directoryDetail = self.driveInst.read_block(writeblkNum)


            print("fr dir "+str(writeblkNum))
            print(directoryDetail)


            self.updateBitMap()

            # check if file or directory of same name is in the directory
            if dirName in directoryDetail:
                fileDetPosInBlock = str(directoryDetail).find(dirName) - self.volumeInst.FILE_ICON_SIZE
                fileDet = self.volumeInst.getFileDetail(dirName, directoryDetail)

                # get blocks allocated to file and split into array of allocations
                blksAllocated = fileDet[self.volumeInst.POSITION_3_DIGIT:]
                blkList = str(blksAllocated).split(' ')  # note has extra '' at last index as there was space
                bitmap = self.volumeInst.driveBlock0BitMap

                # check if all blocks allocated to diectory is empty
                if self.checkIfDirectoryEmpty(directoryDetail, dirName, isRoot=False) == False:
                    print("Directry " + pathname + " has data, so can not be deleted")
                    return

                else:
                    self.volumeInst.driveBlock0BitMap = self.volumeInst.driveBlock0BitMap[
                                                       :int(blkList[0])] + self.volumeInst.EMPTY_BLK_ICON + self.volumeInst.driveBlock0BitMap[
                                                                                                       (
                                                                                                           int(blkList[0]) + 1):]
                    self.driveInst.write_block(int(blkList[0]), self.driveInst.EMPTY_BLK)


                    # #for all block belonging to directory
                    # for x in range(0, 12):
                    #     fileBlkNum = int(blkList[x])
                    #
                    #     if fileBlkNum == 0:
                    #         break
                    #     else:
                    #
                    #         self.volumeInst.driveBlock0BitMap = self.volumeInst.driveBlock0BitMap[
                    #                                             :fileBlkNum] + self.volumeInst.EMPTY_BLK_ICON + self.volumeInst.driveBlock0BitMap[
                    #                                                                                             (
                    #                                                                                             fileBlkNum + 1):]
                    #         self.driveInst.write_block(fileBlkNum, self.driveInst.EMPTY_BLK)
                    #
                    #         #if so delete all
                    #
                    #         #else send erro syyaying ther eis still data in directory
                    #
                    #         # todo remove from bitmap and write empty value into blk
                    #         self.volumeInst.driveBlock0BitMap = self.volumeInst.driveBlock0BitMap[
                    #                                             :fileBlkNum] + self.volumeInst.EMPTY_BLK_ICON + self.volumeInst.driveBlock0BitMap[
                    #                                                                                             (
                    #                                                                                             fileBlkNum + 1):]
                    #         self.driveInst.write_block(fileBlkNum, self.driveInst.EMPTY_BLK)

                    # update directory with empty file detail
                    changeFilDet = directoryDetail[
                                   :fileDetPosInBlock] + self.volumeInst.emptyFileName() + directoryDetail[(
                        fileDetPosInBlock + self.volumeInst.TOTAL_FILE_DETAIL_SIZE):]

                    self.driveInst.write_block(writeblkNum, changeFilDet)

                    # update bitmap in block 0
                    blk0data = self.driveInst.read_block(0)
                    self.volumeInst.updateBlk0BitmapToBeWritten(blk0data)
                    self.driveInst.write_block(0, self.volumeInst.dataToWrite)

    # -----------------------------------------------------------------------------------------------------------------------
    def quitProgram(self):

        #close file if a file is open
        if self.driveInst != None:
            self.driveInst.disconnect()

        # exit program
        sys.exit(0)

     # -----------------------------------------------------------------------------------------------------------------------
    def checkIfDirectoryEmpty(self, blkData, dirName, isRoot = False):

        index = 8

        if isRoot == True:
            index = 6
            if blkData.count(' ' * 9) == index:
                return True;
            else:

                return False
        else:
            #get allocated blks

            fileDetPosInBlock = str(blkData).find(dirName) - self.volumeInst.FILE_ICON_SIZE
            fileDet = self.volumeInst.getFileDetail(dirName, blkData)

            # get blocks allocated to directory and split into array of allocations
            blksAllocated = fileDet[self.volumeInst.POSITION_3_DIGIT:]
            blkList = str(blksAllocated).split(' ')  # note has extra '' at last index as there was space

            for x in range(0, 12):
                if int(blkList[x]) != 0:
                    dir = self.driveInst.read_block(int(blkList[x]))
                    if dir.count(' ' * 9) != index:
                        return False
            return  True




    # -----------------------------------------------------------------------------------------------------------------------
    def isDirectory(self,parentBlkDet, name):

        # find where file name was written in the block detail string
        namePos = str(parentBlkDet).find(name)

        # get position of file details   TODO will need ot change once do nested directorys
        icon = parentBlkDet[(namePos - self.volumeInst.FILE_ICON_SIZE):namePos]

        print(str(icon)+'*')

        if str(icon) ==  str(self.volumeInst.DIRECTORY_ICON):
            return True

        return  False



    # -----------------------------------------------------------------------------------------------------------------------


    def updateBitMap(self):
        # update bitmap in block 0
        blk0data = self.driveInst.read_block(0)
        self.volumeInst.updateBlk0BitmapToBeWritten(blk0data)
        self.driveInst.write_block(0, self.volumeInst.dataToWrite)


    # -----------------------------------------------------------------------------------------------------------------------

    def processCommandLine(self,line):

        print(line)

        #split line into arguments
        firstQuote = int(str(line).find('"'))

        cmdline = line

        #if there is data (3rd param) remove it to get command
        if firstQuote != -1 :
            cmdline = line[:firstQuote]

        #get command and pathnames and convert command to lowercase
        args = cmdline.split()
        command = args[0].lower()


        #Format drive
        if command == "format" and len(args)==2:
            self.driveName = args[1]
            self.format()


        #Reconnect to a drive
        elif command == "reconnect"and len(args)==2:

            try:
                if self.driveName != None:
                    print("Currently connected drive "+self.driveName+" will not be disconnected and connected to drive "+str(args[1]))
                    self.driveInst.disconnect()

                self.driveName = args[1]
                self.reconnect()
            except IOError:
                print("Drive does not exist yet, creating now for you")
                self.driveName = args[1]
                self.format()

        #List all items in a directory
        elif command == "ls"and len(args)==2:
            try:
                self.list(args[1])
            except IOError as e:
                print(e)

        #Make file in directory
        elif command == "mkfile"and len(args)==2:
            try:
                self.makeFile(args[1])
            except IOError as e:
                print(e)

        #make directory
        elif command == "mkdir"and len(args)==2:

            try:
                self.makeDirectory(args[1])
            except IOError as e:
                print(e)


        #append data into file
        elif command == "append"and len(args)==2:
            try:
                data = line[firstQuote:]
                data = str(data).replace('"','')
                self.appendToFile(args[1],data)
            except IOError as e:
                print(e)

        #print content in file
        elif command == "print"and len(args)==2:
            try:
                self.printFile(args[1])
            except IOError as e:
                print(e)

        #delete file
        elif command == "delfile"and len(args)==2:
            try:
                self.deleteFile(args[1])
            except IOError as e:
                print(e)

        #delete empty directory
        elif command == "deldir"and len(args)==2:
            try:
                self.deleteDirectory(args[1])
            except IOError as e:
                print(e)

        # delete empty directory
        elif command == "quit"and len(args)==1:
            self.quitProgram()

            #if not a proper command
        else:
            print("Your command "+line+" is not a proper or complete command, please try again")
            print('If you are trying to add data into a file, please inclose data in " quote marks')



#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    tdos = TinyDOS()

    #if a file with commands has been given in command line
    if len(sys.argv) == 2:
        #reads data all at once
        for fileData in fileinput.input(sys.argv[1]):

             #split up input so that
            splitData = fileData.split('\n')
            if (splitData[0] != ""):
                 tdos.processCommandLine(splitData[0])

    else:
        while True:
            line = input('>')
            if line != "":
                tdos.processCommandLine(line)
            else:
                print("Please give a command")



