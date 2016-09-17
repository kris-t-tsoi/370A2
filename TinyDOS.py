import os
import sys
import fileinput
import drive
import volume
from subprocess import call


class TinyDOS:

    vdriveName = None
    vdrive = None

    def format(self):
        pass

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

        if command == "format":
            TinyDOS.vdriveName = args[1]
            TinyDOS.vdrive = drive.Drive(TinyDOS.vdriveName)
            TinyDOS.vdrive.format()
            volData = volume.Volume.intialBitampFormat()
            TinyDOS.vdrive.write_block(0,volData)
        elif command == "reconnect":
            TinyDOS.vdriveName = args[1]
            TinyDOS.vdrive = drive.Drive(args[1])
            TinyDOS.vdrive.reconnect()
        elif command == "ls":
            pass
        elif command == "mkfile":
            pass
        elif command == "mkdir":
            pass
        elif command == "append":
            pass
        elif command == "print":
            pass
        elif command == "delfile":
            pass
        elif command == "deldir":
            pass
        elif command == "quit":
            TinyDOS.vdrive.disconnect()
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
        while (True):
            line = input()
            if line != "":
                tdos.processCommandLine(line)
            else:
                print("Please put in a command")



