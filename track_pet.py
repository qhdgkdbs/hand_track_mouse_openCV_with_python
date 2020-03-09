import cv2
import numpy as np

lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])
# 초록색 한계 HSV 값
# 녹색 물체만을 마스킹

cam= cv2.VideoCapture(0)
# 카메라 내장
# 2개 이상의 카메라가 장착 되었을 경우 0 > 내장 캠 ~
kernelOpen=np.ones((5,5))
# 5,5의 크기와 동일한 배열을 만듬 > 1로 채움
kernelClose=np.ones((20,20))

font=cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX,2,0.5,0,3,1)
#cvInitFont(CvFont* font, int font_face, double hscale, double vscale, double shear=0, int thickness=1, int line_type=8 )
# hscale – 수평크기
# vscale – 수직크기
# shear - 수직라인에서의 글꼴 기울기
# thickness – 두께
# line_type - 몇 줄
while True:
    ret, img=cam.read()
    # 비디오의 한 프레임을 읽음
    # 성공하면 첫 번째 인자로 true or false
    img=cv2.resize(img,(340,220))
    # 빠른 연산을 위해서 이미지 크기를 줄임

    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    # HSV코드로 변경 
    # HSV는 색상 채도 명도로 색상을 표현함
    
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    # lowerBound와 upperBound 사이에 있는 HSV값은 0으로 그렇지 않으면 1로 만든다.
     
    # 모폴로지 필터링
    # 미리 특정한 형태를 띠는 필터를 만들고 이 필터를 영상에 씌워 새로운 영상을 얻어내는 것
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    # 

    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    cv2.drawContours(img,conts,-1,(255,0,0),3)
    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
        cv2.cv.PutText(cv2.cv.fromarray(img), str(i+1),(x,y+h),font,(0,255,255))
    cv2.imshow("maskClose",maskClose)
    cv2.imshow("maskOpen",maskOpen)
    cv2.imshow("mask",mask)
    cv2.imshow("cam",img)
    cv2.waitKey(10)