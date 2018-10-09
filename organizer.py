import os
import cv2
from datetime import datetime
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol

start_time = datetime.now()

timeStamps = {}
video = 'test_files\QRTest.mov'
cap = cv2.VideoCapture(video)

fps = cap.get(cv2.CAP_PROP_FPS)

success, image = cap.read()
frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
count = 0
success = True

while (success):
    if((count%(fps/2)) == 0):
        cv2.imwrite('tester.jpg', frame)
        success,frame = cap.read()
        count += 1
        data = decode(cv2.imread('tester.jpg'), symbols=[ZBarSymbol.QRCODE])
        if (data == []):
            continue
        else:
            dataClean = (data[0].data).decode('utf8')
            timeStamps[dataClean] = count
            
    else:
        success,frame = cap.read()
        count += 1


os.remove('tester.jpg')
print(timeStamps)

cap.release()
cv2.destroyAllWindows()


timeStampsCleaned = {}
for key in timeStamps:
    sceneNum = int(key.split(':')[0])
    takeNum = int(key.split(':')[1])
    try:
        timeStampsCleaned[sceneNum][takeNum] = timeStamps[key]
    except:
        timeStampsCleaned[sceneNum] = {}
        timeStampsCleaned[sceneNum][takeNum] = timeStamps[key]
print(timeStampsCleaned)


capture = cv2.VideoCapture(video)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
for key in timeStampsCleaned:
    if not (os.path.exists('output/Scene %d' % (key))):
        os.makedirs('output/Scene %d' % (key))
    os.chdir('output/Scene %d' % (key))
    for i, subKey in enumerate(timeStampsCleaned[key]):
        out = cv2.VideoWriter('Take_%d.mp4' % subKey, fourcc, fps, (1920, 1080))

        t1 = (timeStampsCleaned[key][subKey])
        t2 = 0
        if (i < len(timeStampsCleaned[key]) - 1):
            t2 = (timeStampsCleaned[key][subKey+1])
        else:
            t2 = 650

        counter = 0
        while(capture.isOpened()):
            ret, framer = capture.read()
            if ret == True:
                if (counter in range(t1,t2)):
                    out.write(framer)
                    counter += 1
                else:
                    counter += 1
            else:
                break

capture.release()
out.release()

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))