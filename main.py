import HandDetector
import cv2
import time
import pyautogui

pTime = 0
cTime = 0
cap = cv2.VideoCapture(1)
detector = HandDetector.handDetector()

motions = {300000000.0:"DOWN",
           2000000000.0:"LEFT",
           3000000000.0:"UP",
           4000000000.0:"RIGHT",}

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)

    if len(lmlist) != 0:
        datalist = []
        for l in lmlist:
            datalist.append([l[1],l[2]])
        norm = 0

        minX = datalist[0][0]
        minY = datalist[0][1]
        for e in datalist:
            if e[0] < minX:
                minX=e[0]
            if e[1] < minY:
                minY=e[1]
        for j in range(2):
            for i in range(21):
                if j == 0:
                    norm+=datalist[i][j] - minX
                if j == 1:
                    norm+=datalist[i][j] - minY
        norm = pow(norm, 5)
        norm = pow(norm, 0.5)
        answer = list(motions.items())[0][1]
        diff = abs(list(motions.items())[0][0]-norm)
        # print(norm)
        for k,v in motions.items():
            if abs(k - norm) < diff:
                diff = abs(k - norm)
                answer = v
        print(answer)
        if answer == "DOWN":
            pyautogui.press('pagedown')
        if answer == "UP":
            pyautogui.press('pageup')
        if answer == "LEFT":
            pyautogui.press('left')
        if answer == "RIGHT":
            pyautogui.press('right')
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
