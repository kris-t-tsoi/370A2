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

    def reconnect(self):
        self.driveInst = drive.Drive(os.getcwd()+'/'+self.driveName)
        self.driveInst.reconnect()

        #get block 0 information
        self.volumeInst = volume.Volume(self.driveName)
        self.volumeInst.getBlock0Data(self.driveInst.read_block(0))
        self.volumeInst.tinydos = self

        print("Successful reconnection to: "+self.driveName)

    def list(self):
        pass

    def makeFile(self, pathname):

        if ' ' in pathname:
            print("path can not contain any spaces")

        elif pathname[0] != '/':
            print('root directory is not in pathname')

        else:

            args = pathname.split('/')
            fileName = args[len(args) - 1]

            #set default block number where file to be created is
            blockNumber = 0

            #reset data to write to ''
            self.volumeInst.dataToWrite = ''

            #if not nested directory (ie only change  directory details in root directory
            if len(args) == 2:

                #reads block 0 data
                self.volumeInst.dataRead = self.driveInst.read_block(blockNumber)

                #check if file or directory of same name is in the directory
                if fileName in self.volumeInst.dataRead:
                    print("Sorry you can not have the same named file/directory within a single directory")
                else:
                    #pass in file name into volume to create data to write
                    self.volumeInst.makeBlk0File(fileName)
                    self.driveInst.write_block(blockNumber,self.volumeInst.dataToWrite)





                # TODO do this later
                # if len(args) != 1:
                #     #go through all directories
                #     for x in range(0,len(args)-1):
                #         #clear the data read for each directory check
                #         self.volumeInst.dataRead=''
                #
                #         #TODO find the block in which directory is in
                #
                #
                #         pass
                #
                # #read block
                # #TODO read block of data and store into vol.dataread




    def makeDirectory(self):
        pass

    def appendToFile(self, pathname, data):

        if ' ' in pathname:
            print("path can not contain any spaces")

        elif pathname[0] != '/':
            print('root directory is not in pathname')

        else:

            args = pathname.split('/')
            fileName = args[len(args) - 1]

            #set default block number where file to be created is
            blockNumber = 0

            #reset data to write to ''
            self.volumeInst.dataToWrite = ''

            # if not nested directory (ie only change  directory details in root directory
            if len(args) == 2:

                #reads block 0 data
                self.volumeInst.dataRead = self.driveInst.read_block(blockNumber)

                #check if file or directory of same name is in the directory
                if fileName in self.volumeInst.dataRead:

                    fileDet = self.volumeInst.getFileDetail(fileName,self.volumeInst.dataRead)

                    #get 4dig rep legth

                    #divide to find which of 12 blocks 3dig to go to

                    #loop check to see if any data left to write


                    #see how muchh space is in that block and write that much to it



                    #if any data left write to next block flo



                    #get that block and write to it

                    pass

                else:
                    print("Sorry this file does not exist in directory")




    def printFile(self):
        pass


    def deleteFile(self):
        pass

    def deleteDirectory(self):
        pass

    def quitProgram(self):

        #close file if a file is open
        if self.driveInst != None:
            self.driveInst.disconnect()

        # exit program
        sys.exit(0)





    def processCommandLine(self,line):

        #split line into arguments
        args = line.split()
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
            print("path from arg: "+args[1])
            self.makeFile(args[1])

        #make directory
        elif command == "mkdir"and len(args)==2:
            pass

        #append data into file
        elif command == "append"and len(args)==3:
            self.appendToFile(args[1],args[2])

            pass

        #print content in file
        elif command == "print"and len(args)==2:
            pass

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



