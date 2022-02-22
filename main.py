import numpy as np 
import time
import slmpy
from PIL import Image
from vimba import *

slmWaiting = 0.02  #second
step  = 30    # superpixels length  {10,15,20,30,60,120}   
phase = 8      # {2,4,8,16,32}

#concentration points range
r1=20
r2=40
c1=20
c2=40


'''
VIMBA  
frame=Vimba.get_instance().get_all_cameras()[0].get_frame()
frame=frame.convert_pixel_format(PixelFormat.Mono8).as_numpy_ndarray()

ccd_initial=Image.fromarray(frame)
ccd_initial.save("ccd_initial.jpeg")

'''
# getIntensity will be updated as getting real intensity from CCD 
def getIntensity(frame,r1,r2,c1,c2):
    return np.random.rand()

#initial time
t1=time.time()  


slm = slmpy.SLMdisplay(monitor = 1,isImageLock = True) 
col,row = slm.getSize()  #return col,row


#initialize pattern 
#slmPattern=np.random.randint(0,255,(row,col)).astype('uint8')   
slmPattern=np.zeros((row,col)).astype('uint8')   

#save initial pattern
slmPattern_Image=Image.fromarray(slmPattern)
slmPattern_Image.save("slm_pattern_initial.jpeg")


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
            intent_temp=getIntensity(frame,r1, r2, c1, c2)

            if(intent_temp>intensity):
                phase_i =ph
                intensity=intent_temp
            

        slmPattern[r:(r+step):,c:(c+step):]=phase_i
        slm.updateArray(slmPattern)
        time.sleep(slmWaiting) 

slmPattern_Image=Image.fromarray(slmPattern)
slmPattern_Image.save("slm_pattern_final.jpeg")



'''
VIMBA  
frame=Vimba.get_instance().get_all_cameras()[0].get_frame()
frame=frame.convert_pixel_format(PixelFormat.Mono8).as_numpy_ndarray()

ccd_final=Image.fromarray(frame)
ccd_final.save("ccd_final.jpeg")

'''


time.sleep(2)
slm.close()

t2=time.time()

print(f"{t2-t1} seconds")




