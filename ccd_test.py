from vimba import *
import cv2


with Vimba.get_instance () as vimba :
    cams = vimba.get_all_cameras ()
    with cams [0] as cam:
        frame = cam.get_frame ()
        frame=frame.convert_pixel_format(PixelFormat.Rgb8).as_numpy_ndarray()
        ccd_init= cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        cv2.imwrite("ccd_init",ccd_init)


'''
frame=Vimba.get_instance().get_all_cameras()[0].get_frame()
frame=frame.convert_pixel_format(PixelFormat.Rgb8).as_numpy_ndarray()

#cv2.COLOR_BGR2RGB
ccd_init= cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
cv2.imwrite("ccd_init",ccd_init)

'''