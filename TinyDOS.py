import os
import sys
import fileinput
import drive
import volume
from subprocess import call

#Yee Wing Kristy Tsoi
#ytso868

class TinyDOS:

    vdriveName = None
    vdrive = None

    def format(self):
        self.vdrive = drive.Drive(self.vdriveName)
        self.vdrive.format()
        volData = volume.Volume(self.vdriveName)
        volData.intialBitmapFormat()
        self.vdrive.write_block(0, volData.dataToWrite)

    def reconnect(self):
        pass

    def list(self):
        pass

    def makeFile(self):
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

        #close file

        #exit program
        pass

    def processCommandLine(self,line):

        #split line into arguments
        args = line.split()
        command = args[0].lower()

        #Format drive
        if command == "format":
            self.vdriveName = args[1]
            self.format()
            print("Created "+self.vdriveName)

        #Reconnect to a drive
        elif command == "reconnect":
            TinyDOS.vdriveName = args[1]
            TinyDOS.vdrive = drive.Drive(args[1])
            TinyDOS.vdrive.reconnect()

        #List all items in a directory
        elif command == "ls":
            pass

        #Make file in directory
        elif command == "mkfile":
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

        #quit program
        elif command == "quit":
            TinyDOS.vdrive.disconnect()

         #if not a proper command
        else:
            print("Your command "+line+" is not a proper command, please try again")




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



