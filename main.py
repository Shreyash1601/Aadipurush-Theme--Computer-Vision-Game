import cv2
import cvzone
import random
import time
from cvzone.HandTrackingModule import HandDetector

cap=cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)
fire=cv2.imread("fire.png",cv2.IMREAD_UNCHANGED)
fire=cv2.resize(fire,(200,200))

class Image:
    def __init__(self,pos):
        self.pos=pos
        self.img=cv2.imread("arrow.png",cv2.IMREAD_UNCHANGED)
        self.isSpecial=False
        self.oPos=pos
        self.flag=False
    def draw(self,img,flag):
        if flag:
          return cvzone.overlayPNG(img,self.img,self.pos)
        else:
           return cvzone.overlayPNG(img,self.img,self.oPos)
    def update(self,cursor):
        ox,oy=self.pos
        try:
          if ox<cursor[0]<ox+150 and oy<cursor[1]<oy+150:
            self.pos=(cursor[0]-75,cursor[1]-75)
        except:
            self.pos=(ox,oy)
listArr=[]
for i in range(0,4):
    listArr.append(Image((10,10+i*150)))
special=random.choice(listArr)
special.isSpecial=True
detector=HandDetector(detectionCon=0.65)
Rav=cv2.imread("Ravan.png",cv2.IMREAD_UNCHANGED)
post=cv2.imread("Poster.png")
score=None
start_time=time.time()
cnt=0
flag=False
while True:
  if not flag:
    succ,img=cap.read()
    img=cv2.flip(img,1)
    hands, img=detector.findHands(img)
    img=cvzone.overlayPNG(img,Rav,[780 ,10])
    for obj in listArr:
        try:
          img=obj.draw(img,1)
        except:
          img=obj.draw(img,0)
    if hands:
        lmList=hands[0]["lmList"]
        length,info,img=detector.findDistance(lmList[8],lmList[12],img)
        if length<60:
            cursor=lmList[8]
            for obj in listArr:
                obj.update(cursor)
    # Checking Collision
    for obj in listArr:
       if 780<obj.pos[0]<1280 and 10<obj.pos[1]<510:
          cnt=cnt+1
          if obj.isSpecial and score==None:
             end_time=time.time()
             score=(((200/(end_time-start_time))*100)/cnt)
             score=round(score,2)
             print(f"Collision Detected {score}")
             img=post
             cv2.putText(img,f"{score}",(1150,800),cv2.FONT_HERSHEY_SIMPLEX,5,(49,49,255),20)   
             flag=True
          elif obj.flag:
             obj.img=cv2.resize(obj.img,(1,1))
          else:
             obj.img=fire
             obj.flag=True
             cv2.putText(img,"Try Again!!",(500,400),cv2.FONT_HERSHEY_SIMPLEX,5,(0,250,255),20)
  cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
  cv2.imshow("window",img)
  cv2.waitKey(1)