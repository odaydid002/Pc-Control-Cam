import cv2, math, os
import numpy as np
import handdetectfunc as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#---#########-----##########---#
wCam, hCam = 640, 480
wCam, hCam = 640, 480
wDisplay, hDisplay = 1366, 768
cap = cv2.VideoCapture(0)  
cap.set(3, wCam)
cap.set(4, hCam)
#---#########-----##########---#

#----------------------Volume Control----------------------# 

detector = htm.handDetector(detectionCon=int(0.7))
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

#----------------------------------------------------------#

while True:
    
    success, img = cap.read()
    img = detector.findHands(img,False)
    lnList = detector.findPosition(img,draw=False)
    
    if len(lnList)!=0:

        x1,y1 = lnList[4][1], lnList[4][2]
        x2,y2 = lnList[8][1], lnList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2
        
        lf1 =  lnList[6][1] - lnList[8][1]
        lf2 =  lnList[10][1] - lnList[12][1]
        lf3 =  lnList[14][1] - lnList[16][1]
        lf4 =  lnList[18][1] - lnList[20][1]    
        
        # cv2.circle(img, (x1, y1), 10, (255,0,0), cv2.FILLED)
        # cv2.circle(img, (x2, y2), 10, (255,0,0), cv2.FILLED)
        # cv2.line(img, (x1,y1),(x2,y2),(255,0,0),3)
        
        if lf1 > 0 and lf2 > 0 and lf3 > 0 and lf4 > 0:
            volume.GetMute()
        else:
            length = math.hypot(x2 -x1, y2 - y1)
            
            vol = np.interp(length,[50,200],[minVol, maxVol])    
            volume.SetMasterVolumeLevel(vol, None)

        

        
    cv2.imshow("image", img)
    cv2.waitKey(1)