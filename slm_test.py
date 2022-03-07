import numpy as np 
import time
import slmpy
import cv2

def getIntensity(r1,r2,c1,c2):
    return np.random.rand()

slmWaiting = 0.8  #seconds
step  = 90    # superpixels length n X n {10,15,20,30,60,120}   
phase = 30    # 0 - 255 

#concentration points 
r1=700
r2=800
c1=700
c2=800

t1=time.time()  

slm = slmpy.SLMdisplay(monitor = 1,isImageLock = True) 
col,row = slm.getSize()  #return col,row

slmPattern=np.random.randint(0,255,(row,col)).astype('uint8')   
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


time.sleep(2)
slm.close()

t2=time.time()

print(f"{t2-t1} seconds")