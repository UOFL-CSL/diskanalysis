from tracer import Tracer

tracer = Tracer()

# Increase max buffer size to 1MB
tracer.createPipe()
tracer.setPipeSize(1000000)