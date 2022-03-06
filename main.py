import numpy as np 
import time
import slmpy
import cv2
from vimba import *


slmWaiting = 0.8  #seconds
step  = 90    # superpixels length n X n {10,15,20,30,60,120}   
phase = 30    # 0 - 255 

#concentration points 
r1=700
r2=800
c1=700
c2=800



# getIntensity will be updated as getting real intensity from CCD 
def getIntensity(r1,r2,c1,c2):
    frame=Vimba.get_instance().get_all_cameras()[0].get_frame()
    frame=frame.convert_pixel_format(PixelFormat.Rgb8).as_numpy_ndarray()

    return 0.299*np.mean(frame[r1:r2:,c1:c2:,0]) +0.587*np.mean(frame[r1:r2:,c1:c2:,1])+0.114*np.mean(frame[r1:r2:,c1:c2:,2])

    #gray_=np.zeros((frame.shape[0],frame.shape[1]))
    #gray_+=0.299*frame[::,::,0]+0.587*frame[::,::,1]+0.114*frame[::,::,2]
    #return np.mean(gray_[r1:r2:,c1:c2:])  


#initial time
t1=time.time()  

#Reading image from CCD
frame=Vimba.get_instance().get_all_cameras()[0].get_frame()
frame=frame.convert_pixel_format(PixelFormat.Rgb8).as_numpy_ndarray()

#save inital image from CCD
ccd_init= cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
cv2.imwrite("ccd_init.jpeg",ccd_init)


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


for r in range(0,row,step):
    for c in range(0,col,step):
        phase_i=slmPattern[r:(r+step):,c:(c+step):]
        intensity=getIntensity(r1, r2, c1, c2)
        for ph in range(0,255,phase):

            slmPattern[r:(r+step):,c:(c+step):]=ph
            slm.updateArray(slmPattern)
            time.sleep(slmWaiting) 
            intent_temp=getIntensity(r1, r2, c1, c2)

            if(intent_temp>intensity):
                phase_i =ph
                intensity=intent_temp
            

        slmPattern[r:(r+step):,c:(c+step):]=phase_i
        slm.updateArray(slmPattern)
        time.sleep(slmWaiting) 



cv2.imwrite("slm_pattern_final.jpeg",slmPattern)

frame=Vimba.get_instance().get_all_cameras()[0].get_frame()
frame=frame.convert_pixel_format(PixelFormat.Rgb8).as_numpy_ndarray()

ccd_final= cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
cv2.imwrite("ccd_final.jpeg",ccd_final)



time.sleep(2)
slm.close()

t2=time.time()

print(f"{t2-t1} seconds")




'''
VIMBA  
frame=Vimba.get_instance().get_all_cameras()[0].get_frame()
frame=frame.convert_pixel_format(PixelFormat.Mono8).as_numpy_ndarray()

ccd_initial=Image.fromarray(frame)
ccd_initial.save("ccd_initial.jpeg")

'''