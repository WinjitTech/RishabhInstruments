import json

import cv2
import imutils

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if not ret:
    print "Check if Camera is Available"
    cap.release()
    cv2.destroyAllWindows()
else:
    cv2.imwrite("Cam_calibrate.jpg", frame)
image = cv2.imread("Cam_calibrate.jpg")
data = {}
config = open("frame.json", "w")
while 1:
    ret, image = cap.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    for c in cnts:
        M = cv2.moments(c)
        cX = int((M["m10"]))
        cY = int((M["m01"]))
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "square"
            if ar >= 0.95 and ar <= 1.05:
                if cv2.contourArea(c) > 40000:
                    (x, y, w, h) = cv2.boundingRect(approx)
                    (cx, cy), radius = cv2.minEnclosingCircle(approx)
                    cv2.rectangle(image, (int(x), int(y)), (int(w+x), int(h+y)), (0, 255, 0), thickness=2)
                    cv2.rectangle(image, (int(x+38), int(y+38)), (int((w+x)-98), int(h+y)-98), (0, 255, 0), thickness=2)
                    meter_frame = image[int(y+40):int(h+y)-100, int(x+40):int(w+x)-100]
                    cv2.imwrite("MeterImages/cardinals.jpg", meter_frame)
                    data["x1"] = int(x+40)
                    data["x2"] = int(w+x)-100
                    data["y1"] = int(y+40)
                    data["y2"] = int(h+y)-100
                    json_data = json.dumps(data)
                    config.write(json_data)
                    print int(y+40), int(h+y)-100, int(x+40), int(w+x)-100
                    config.close()
                    exit()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
