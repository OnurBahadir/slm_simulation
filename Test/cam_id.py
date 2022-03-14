from vimba import *
import time

#### start Vimba
vimba = Vimba()
vimba.startup()

#### show Vimba version
print 'Version:', vimba.getVersion()

#### get system object
system = vimba.getSystem()

#### if has GigE, send out a broadcast to allow camera discovery
if system.GeVTLIsPresent:
    system.runFeatureCommand("GeVDiscoveryAllOnce")
    time.sleep(0.2)
else:
    print "GigE transport layer not found!"

#### list available cameras after enabling discovery
camIds = vimba.getCameraIds()
for cam in camIds:
    print 'Camera ID:', cam

#### shutdown Vimba
vimba.shutdown()
