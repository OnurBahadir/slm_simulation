import numpy as np 
import time
import slmpy
import cv2

from pymba import Vimba, VimbaException
from ccd_vimba import display_frame


slmWaiting = 0.8  #seconds
step  = 90    # superpixels length n X n {10,15,20,30,60,120}   
phase = 30    # 0 - 255 

#concentration points 
r1=700
r2=800
c1=700
c2=800



def getIntensity(r1,r2,c1,c2,image):
     return 0.299*np.mean(image[r1:r2:,c1:c2:,0]) +0.587*np.mean(image[r1:r2:,c1:c2:,1])+0.114*np.mean(image[r1:r2:,c1:c2:,2])


#SLM initialize
slm = slmpy.SLMdisplay(monitor = 1,isImageLock = True) 
col,row = slm.getSize()  #return col,row

#col = 1920
#row = 1080

#initialize pattern 
#slmPattern=np.random.randint(0,255,(row,col)).astype('uint8')   
slmPattern=np.zeros((row,col)).astype('uint8')   

#save initial pattern
cv2.imwrite("slm_pattern_initial.jpeg",slmPattern)

#update slm with init pattern 
slm.updateArray(slmPattern)   
# wait for update
time.sleep(slmWaiting)  

#Reading image from CCD
with Vimba() as vimba:
    camera = vimba.camera(0)
    camera.open()
    camera.arm('SingleFrame')
    frame = camera.acquire_frame()
    ccd_init=display_frame(frame, 0)
    cv2.imwrite("ccd_init.jpeg",ccd_init)
    camera.disarm()
    camera.close()




with Vimba() as vimba:
    camera = vimba.camera(0)
    camera.open()
    camera.arm('SingleFrame')
    for r in range(0,row,step):
        for c in range(0,col,step):

            frame = camera.acquire_frame()
            image=display_frame(frame, 0)
            intensity=getIntensity(r1, r2, c1, c2,image)

            phase_i=slmPattern[r:(r+step):,c:(c+step):]
    
            
            for ph in range(0,255,phase):

                slmPattern[r:(r+step):,c:(c+step):]=ph
                slm.updateArray(slmPattern)
                
                time.sleep(slmWaiting) 
                
                frame = camera.acquire_frame()
                image=display_frame(frame, 0)
                intent_temp=getIntensity(r1, r2, c1, c2,image)

                if(intent_temp>intensity):
                    phase_i =ph
                    intensity=intent_temp
            

            slmPattern[r:(r+step):,c:(c+step):]=phase_i
            slm.updateArray(slmPattern)
            time.sleep(slmWaiting) 

    camera.disarm()
    camera.close()


cv2.imwrite("slm_pattern_final.jpeg",slmPattern)

time.sleep(2)
with Vimba() as vimba:
    camera = vimba.camera(0)
    camera.open()
    camera.arm('SingleFrame')
    frame = camera.acquire_frame()
    ccd_final=display_frame(frame, 0)
    cv2.imwrite("ccd_final.jpeg",ccd_final)
    camera.disarm()
    camera.close()

time.sleep(2)

slm.close()

time.sleep(2)



