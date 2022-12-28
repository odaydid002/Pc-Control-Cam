import cv2
import mediapipe as mp


class handDetector():
    def __init__(self,mode=False,maxHands=1,detectionCon=int(0.5),trackCon=int(0.5)):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.npHands = mp.solutions.hands
        self.hands = self.npHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.npDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLns in self.results.multi_hand_landmarks:
                if draw:
                    self.npDraw.draw_landmarks(img, handLns,self.npHands.HAND_CONNECTIONS)
            
        return  img 
    
    def findPosition(self,img, handNo=0, draw=True):
        lnList = []
        if self.results.multi_hand_landmarks:
            
            myHand =  self.results.multi_hand_landmarks[handNo]
            
            for id, ln in enumerate(myHand.landmark):
                #print(id,ln)
                h, w, c = img.shape
                cx, cy = int(ln.x*w), int(ln.y*h)
                #print(id, cx, cy)
                lnList.append([id, cx, cy])
            #    if id==4:
                if draw:
                 cv2.circle(img,(cx,cy),5, (255,0,255),cv2.FILLED)
        
        return lnList


def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lnList = detector.findPosition(img)
        if len(lnList) !=0:
            print(lnList[4])
     
        cv2.imshow("Image", img)
        cv2.waitKey(1)                     
                
if __name__ == '__main__':
    main()
                    