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

        print("in tinydos make file: "+str(pathname))

        args = pathname.split('/')
        print(args)

        print("length arg: "+str(len(args)))

        fileName = args[len(args) - 1]

        if ' ' in fileName:
            print("Filename can not contain any spaces")
            return None #TODO find out how to throw execption

        #set default block number where file to be created is
        blockNumber = 0

        #reset data to write to ''
        self.volumeInst.dataToWrite = ''

        #if not nested directory (ie only change  directory details in root directory
        if len(args) == 2:

            #reads block 0 data
            self.volumeInst.dataRead = self.driveInst.read_block(blockNumber)
            print("read block")
            print(self.volumeInst.dataRead)

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



        pass


    def makeDirectory(self):
        pass

    def appendToFile(self):
        pass

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
        if command == "format":
            self.driveName = args[1]
            self.format()


        #Reconnect to a drive
        elif command == "reconnect":
            if self.driveName == None:
                self.driveName = args[1]

            #if another drive is in use
            #check if your want to swtich
            else:
                pass
            self.reconnect()

        #List all items in a directory
        elif command == "ls":
            pass

        #Make file in directory
        elif command == "mkfile":
            print("path from arg: "+args[1])
            self.makeFile(args[1])

            pass

        #make directory
        elif command == "mkdir":
            pass

        #append data into file
        elif command == "append":
            pass

        #print content in file
        elif command == "print":
            pass

        #delete file
        elif command == "delfile":
            pass

        #delete empty directory
        elif command == "deldir":
            pass

        # quit program
        elif command == "quit":
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



