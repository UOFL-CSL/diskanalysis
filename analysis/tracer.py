import os
import errno
import fcntl

class Tracer:
    def generateTransaction(self, data, callback):
        startLBA = int(data[0] / 4096)
        blocks = data[1]

        transaction = []

        for i in range(0, blocks+1):
            transaction.append(startLBA+i)

        callback(transaction)

    def start(self, callback):
        pipeName = "/tmp/blkpipe"

        with open(pipeName) as pipe:
            fcntl.fcntl(pipe, fcntl.F_SETFL, os.O_NONBLOCK)
            while True:
                data = pipe.readline()

                if len(data) > 0:
                    print(data + "\n")

                    if data == "end":
                        break

                    data = [int(x) for x in data.split(" ")]
                    self.generateTransaction(data, callback)

