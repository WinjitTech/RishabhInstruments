import json
import numpy as np
import cv2
from MainProcess import *
import sys


def start_capture():
    if len(sys.argv) == 3:
        cardinal_number = int(sys.argv[1])
        img_path = "MeterImages/"+str(cardinal_number) + "_" + str(sys.argv[2])+".jpg"

    elif str(sys.argv[1]) == '-h':
        print "Capture_Image.py -cardinal_number <space> minimum_scale/full_scale"
        exit()
    else:
        print "Incorrect call !\nType Capture_Image.py -h for help"
        exit()

    print img_path
    config = open("frame.json", "r")
    data = json.load(config)
    x1 = data["x1"]
    x2 = data["x2"]
    y1 = data["y1"]
    y2 = data["y2"]
    config.close()
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print "Check if Camera is Available"
        cap.release()
        cv2.destroyAllWindows()
    else:
        while True:
            try:
                # Capture frame-by-frame
                ret, frame = cap.read()
                if ret:
                    # Todo: Crop image in a rectangular fence
                    meter = frame[y1:y2, x1:x2]
                    # Todo: write mater image continuously to get current meter image
                    cv2.imwrite("MeterImages/Needle.jpg", meter)
                    try:
                        meter, angles, deflection = initprocess(meter)
                        cv2.imwrite(img_path, meter)
                        print str(angles[cardinal_number-1]), str(deflection[cardinal_number-1])
                        break
                    except Exception, e:
                        print ("Exception in InitProcess :", str(e))
                else:
                    print "Check if Camera is Available"
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            except Exception, e:
                print "main", str(e)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # When everything done, release the camera
        cap.release()
        cv2.destroyAllWindows()

start_capture()
