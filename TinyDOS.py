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
    def list(self):
        pass

    # -----------------------------------------------------------------------------------------------------------------------
    def makeFile(self, pathname):
        if ' ' in pathname:
            print("path can not contain any spaces")

        elif pathname[0] != '/':
            print('root directory is not in pathname')

        else:

            args = pathname.split('/')
            fileName = args[len(args) - 1]

            # set default directory block number where file is to be created in
            directoryDetBlkNum = 0

            # initalise block number where file data is
            blockNumber = 0

            # reset data to write to ''
            self.volumeInst.dataToWrite = ''

            # if nested directory, find blk where directory detail is stored
            if len(args) != 2:
                # TODO find directoryDetBlkNum
                pass

            # reads directory data
            dirDet = self.driveInst.read_block(directoryDetBlkNum)

            # check if file or directory of same name is in the directory
            if fileName in dirDet:
                raise IOError("Sorry you can not have the same named file/directory within a single directory")
            else:
                #get bitmap details
                if directoryDetBlkNum != 0 :
                    self.volumeInst.dataRead = self.driveInst.read_block(0)

                # pass in file name and directly blk number into volume to create data to write
                dirDet =self.volumeInst.makeBlkFile(fileName,directoryDetBlkNum,dirDet)
                self.driveInst.write_block(directoryDetBlkNum,dirDet)

                #update bitmape
                if directoryDetBlkNum != 0:
                    self.driveInst.write_block(0,self.volumeInst.dataToWrite)




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

            #reset data to write to ''
            self.volumeInst.dataToWrite = ''

            # if nested directory, find blk where directory detail is stored
            if len(args) != 2:
                #TODO find directoryDetBlkNum
                pass

            #reads directory data
            directoryDetail = self.driveInst.read_block(directoryDetBlkNum)

            #check if file or directory of same name is in the directory
            if fileName in directoryDetail:
                raise IOError("Sorry you can not have the same named file/directory within a single directory")

            else:
                # get bitmap details if not block 0
                if directoryDetBlkNum != 0:
                    self.volumeInst.dataRead = self.driveInst.read_block(0)

                # TODO create directory
                directoryDetail = self.volumeInst.makeDir(fileName,directoryDetBlkNum,directoryDetail)
                newDirData = self.volumeInst.extraReturn
                newDirBlkNum = self.volumeInst.childBlkNum

                #write new dir data into directory
                self.driveInst.write_block(int(newDirBlkNum),newDirData)
                self.driveInst.write_block(blockNumber,directoryDetail)


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

            # if nested directory, find blk where directory detail is stored
            if len(args) != 2:
                #TODO find directoryDetBlkNum
                pass



            #reads directory data
            directoryDetail = self.driveInst.read_block(directoryDetBlkNum)

            #check if file or directory of same name is in the directory
            if fileName in directoryDetail:
                fileDetPosInBlock = str(directoryDetail).find(fileName) - self.volumeInst.FILE_ICON_SIZE
                fileDet = self.volumeInst.getFileDetail(fileName,directoryDetail)

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
                while lenDataToWrite !=0 :

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
                self.driveInst.write_block(directoryDetBlkNum, directoryDetail)

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

            # if not nested directory (ie only change  directory details in root directory
            if len(args) == 2:

                #reads block 0 data
                directoryDetail = self.driveInst.read_block(directoryDetBlkNum)

                #check if file or directory of same name is in the directory
                if fileName in directoryDetail:
                    fileDetPosInBlock = str(directoryDetail).find(fileName) - self.volumeInst.FILE_ICON_SIZE
                    fileDet = self.volumeInst.getFileDetail(fileName,directoryDetail)

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



            #if not a nested directory
            else:
                pass


    # -----------------------------------------------------------------------------------------------------------------------
    def deleteFile(self):
        pass

    # -----------------------------------------------------------------------------------------------------------------------
    def deleteDirectory(self):
        pass

    # -----------------------------------------------------------------------------------------------------------------------
    def quitProgram(self):

        #close file if a file is open
        if self.driveInst != None:
            self.driveInst.disconnect()

        # exit program
        sys.exit(0)

     # -----------------------------------------------------------------------------------------------------------------------
        def findDirectoryBlock(self):
            pass


    # -----------------------------------------------------------------------------------------------------------------------

    def processCommandLine(self,line):

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
            pass

        #Make file in directory
        elif command == "mkfile"and len(args)==2:
            try:
                self.makeFile(args[1])
            except IOError as e:
                print(e)

        #make directory
        elif command == "mkdir"and len(args)==2:
            self.makeDirectory(args[1])

        #append data into file
        elif command == "append"and len(args)==2:
            data = line[firstQuote:]
            data = str(data).replace('"','')
            self.appendToFile(args[1],data)

        #print content in file
        elif command == "print"and len(args)==2:
            try:
                self.printFile(args[1])
            except IOError as e:
                print(e)

        #delete file
        elif command == "delfile"and len(args)==2:
            pass

        #delete empty directory
        elif command == "deldir"and len(args)==2:
            pass

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



