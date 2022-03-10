import cv2

from pymba import Vimba, VimbaException
from ccd_vimba import display_frame

with Vimba() as vimba:
    camera = vimba.camera(0)
    camera.open()
    camera.arm('SingleFrame')

    frame = camera.acquire_frame()
    ccd_init=display_frame(frame, 0)
    
    cv2.imwrite("ccd_init.jpeg",ccd_init)
    camera.disarm()
    camera.close()