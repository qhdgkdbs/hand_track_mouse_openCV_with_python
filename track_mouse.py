import cv2
import numpy as np
from pynput.mouse import Button, Controller
# pynput 은 마우스 혹은 키보드를 관리하는 라이브러리
import wx


mouse=Controller()
# pynput의 마우스 제어

app=wx.App(False)
# 객체 생성해줌
# wx라이브러리의 시작

(sx,sy)=wx.GetDisplaySize()
# 스크린의 크기를 픽셀 단위로 출력해줌

(camx,camy)=(320,240)
# 영상의 크기를 320 340으로 리사이징할 예정
# 추후 마우스 포인트 위치를 잡는데 사용

lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])
# 초록색 한계 HSV 값
# 녹색 물체만을 마스킹

cam= cv2.VideoCapture(0)
# 카메라 내장
# 2개 이상의 카메라가 장착 되었을 경우 0 > 내장 캠 ~

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
# 5,5의 크기와 동일한 배열을 만듬 > 1로 채움

pinchFlag=0
# 이따가 마우스제어 로직에 사용함

while True:
    ret, img=cam.read()
    # 비디오의 한 프레임을 읽음
    # 성공하면 첫 번째 인자로 true or false
    
    img=cv2.resize(img,(340,220))
    # 빠른 연산을 위해서 이미지 크기를 줄임

    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #convert BGR to HSV
    # HSV코드로 변경 
    # HSV는 색상 채도 명도로 색상을 표현함
    
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    # lowerBound와 upperBound 사이에 있는 HSV값은 0으로 그렇지 않으면 1로 만든다.
    
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    #morphology
    # 모폴로지 필터링
    # 미리 특정한 형태를 띠는 필터를 만들고 이 필터를 영상에 씌워 새로운 영상을 얻어내는 것

    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    # cv2.findContours(image, mode, method)
    
    # mode – contours를 찾는 방법
    ## cv2.RETR_EXTERNAL : contours line중 가장 바같쪽 Line만 찾음.
    ## cv2.RETR_LIST : 모든 contours line을 찾지만, hierachy 관계를 구성하지 않음.
    ## cv2.RETR_CCOMP : 모든 contours line을 찾으며, hieracy관계는 2-level로 구성함.
    ## cv2.RETR_TREE : 모든 contours line을 찾으며, 모든 hieracy관계를 구성함.
    
    #method – contours를 찾을 때 사용하는 근사치 방법
    ## cv2.CHAIN_APPROX_NONE : 모든 contours point를 저장.
    ## cv2.CHAIN_APPROX_SIMPLE : contours line을 그릴 수 있는 point 만 저장. (ex; 사각형이면 4개 point)
    ## cv2.CHAIN_APPROX_TC89_L1 : contours point를 찾는 algorithm
    ## cv2.CHAIN_APPROX_TC89_KCOS : contours point를 찾는 algorithm
    
    if(len(conts)==2):
        if(pinchFlag==1):
            # 두 손가락이 접촉되면,
            # elif로 감
            pinchFlag=0
            mouse.release(Button.left)
            # 마우스 클릭 해제
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        # 컨투어를 둘러싸는 박스의 좌표와 너비와 높이
        # 스크린샷 참조
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
            #  cv.rectangle(
            #             img,        사각형이 그려질 이미지 
            #        (x1, y1),        사각형의 시작점
            #        (x2, y2),        시작점과 대각선에 있는 사각형의 끝점
            #           color,        사각형의 색 ( B, G , R )
            #       thickness,        선굵기(디폴트값 1), -1 이면 사각형 내부가 채워짐
            ##        lineType,        디폴트값 cv.LINE_8(=8-connected line)
            ##          shift )       디폴트값 0
        
        cx1=np.int0(x1+w1/2)
        cy1=np.int0(y1+h1/2)
        # 박스1의 중간
        
        cx2=np.int0(x2+w2/2)
        cy2=np.int0(y2+h2/2)
        # 박스2의 중간
        
        cx=np.int0((cx1+cx2)/2)
        cy=np.int0((cy1+cy2)/2)
        # 박스1 과 박스2의 중간
        
        cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
        # 선분그리기
        # 박스1 과 박스2의 중점을 잇는 선분을 그림
        
        cv2.circle(img, (cx,cy),2,(0,0,255),2)
        # 박스1과 박스2의 중점에 원을 그림
        ## cv2.circle(img, center, radian, color, thickness)
        ## img – 그림을 그릴 이미지
        ## center – 원의 중심 좌표(x, y)
        ## radian – 반지름
        ## color – BGR형태의 Color
        ## thickness – 선의 두께, -1 이면 원 안쪽을 채움

        
        mouseLoc=(sx-(cx*sx/camx), cy*sy/camy)
        
        
        mouse.position=mouseLoc 
        while mouse.position!=mouseLoc:
            # 마우스의 현 좌표와 움직이는 좌표가 다를 경우에만 실행
            # 마우스의 현 좌표와 손가락으로 움직이려고 하는 좌표가 같은 경우에는 대기
            pass
        
    elif(len(conts)==1):
        x,y,w,h=cv2.boundingRect(conts[0])
        # 박스1의 좌표와 높이 너비
        if(pinchFlag==0):
            pinchFlag=1
            mouse.press(Button.left)
            # 마우스 클릭
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        # 박스1에 그림칠
        
        cx=np.int0(x+w/2)
        cy=np.int0(y+h/2)
        # 박스1의 중점
        
        cv2.circle(img,(cx,cy),(w+h)/4,(0,0,255),2)
        # 위
        
        mouseLoc=(sx-(cx*sx/camx), cy*sy/camy)
        # 스크린 픽셀 - (박스1의 중점*스크린의 픽셀 / 영상 x축 크기)
        mouse.position=mouseLoc 
        while mouse.position!=mouseLoc:
            pass
    cv2.imshow("cam",img)
    cv2.waitKey(5)