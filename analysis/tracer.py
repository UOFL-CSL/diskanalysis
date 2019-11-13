import os
import errno
import fcntl

class Tracer:
    pipeName = "/tmp/blkpipe"

    totalBlocks = 0

    # Calls the defined callback from the start method with the starting and ending LBA
    def generateTransaction(self, data, callback):
        startLBA = int(data[0] / 512)
        blocks = int(data[1] / 512)

        print("Starting LBA: " + str(startLBA) + "; Blocks: " + str(blocks))

        callback(startLBA, startLBA+blocks)

    # Creates the named pipe
    def createPipe(self):
        pipeName = self.pipeName

        os.mkfifo(pipeName)

    # Starts reading from the named pipe, sends the data to the callback function
    # Format of the data in the pipe: 
    # "SECTOR OFFSET"
    # offset is in number of blocks
    def start(self, callback):
        pipeName = self.pipeName

        with open(pipeName) as pipe:
            fcntl.fcntl(pipe, fcntl.F_SETFL, os.O_NONBLOCK)
            while True:
                data = pipe.readline()

                if len(data) > 0:
                    if data == "end":
                        break

                    data = [int(x) for x in data.split(" ")]
                    self.generateTransaction(data, callback)

    # Sets the named pipe buffer size
    # System max = 1MB
    def setPipeSize(self, size):
        pipeName = self.pipeName

        pipe = os.open(pipeName, os.O_NONBLOCK)
        fcntl.fcntl(pipe, 1031, size)

        print("New size: " + str(fcntl.fcntl(pipe, 1032)))
    