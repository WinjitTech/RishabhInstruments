import json
from MainProcess import *
import sys
import time


def start_capture():
    if sys.argv:
        cardinal_number = int(sys.argv[1])
        img_name = str(cardinal_number) + "_" + str(sys.argv[2]) + ".jpg"
        img_path = str(sys.argv[3])
    elif str(sys.argv[1]) == '-h':
        print "Capture_Image.py -cardinal_number <space> minimum_scale/full_scale"
        exit()
    else:
        print "Incorrect call !\nType Capture_Image.py -h for help"
        exit()

    config = open(img_path + "\\frame.json", "r")
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
        # while True:
        for i in range(10):
            try:
                # Capture frame-by-frame
                time.sleep(1)
                ret, frame = cap.read()
                if ret:
                    # Todo: Crop image in a rectangular fence
                    meter = frame[y1:y2, x1:x2]
                    # Todo: write mater image continuously to get current meter image
                    cv2.imwrite(img_path + "\\MeterImages\\Needle.jpg", meter)
                    try:
                        meter, angles, deflection = initprocess(img_path, meter)
                        cv2.imwrite(img_path + '\\MeterImages\\' + img_name, meter)
                        print str(angles[cardinal_number - 1]) + "," + str(deflection[cardinal_number - 1])
                        break
                    except Exception, e:
                        print "error:", str(e)
                        cap.release()
                        cv2.destroyAllWindows()
                        sys.exit()
                        break
                else:
                    print "Check if Camera is Available"
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            except Exception, e:
                print "error"
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # When everything done, release the camera
        cap.release()
        cv2.destroyAllWindows()

start_capture()
