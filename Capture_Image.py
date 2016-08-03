import json
from MainProcess import *
import sys
import time


def start_capture():
    try:
        if sys.argv:
            # cardinal_number = int(sys.argv[1])
            # img_name = str(cardinal_number) + "_" + str(sys.argv[2]) + ".jpg"
            # img_path = str(sys.argv[3])
            # mod_factor = float(sys.argv[4])
            # size = "meter" + str(sys.argv[5])
            #
            cardinal_number = 1
            img_name = "1" + "_" + "FULL_Test" + ".jpg"
            img_path = "C:\\Users\\rohitsalunke\\PycharmProjects\\RishabhInstruments_PahseI_Dev"
            mod_factor = 1.11
            size = "meter96"
            config = open("frame.json", "r")
            data = json.load(config)
            x1 = data["x1"]
            x2 = data["x2"]
            y1 = data["y1"]
            y2 = data["y2"]
            config.close()
    except ValueError:
        exit()

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        print ("Check if Camera is Available")
        cap.release()
        cv2.destroyAllWindows()
    else:
        # while True:
        for i in range(0, 10):
            try:
                # Todo: Capture frame-by-frame
                ret, frame = cap.read()
                ret, frame = cap.read()
                if ret:
                    # Todo: Crop image in a rectangular fence
                    meter = frame[y1:y2, x1:x2]
                    # Todo: write mater image continuously to get current meter image
                    cv2.imwrite(img_path + "\\MeterImages\\Needle.jpg", meter)
                    try:
                        meter, angles, deflection = initprocess(img_path, meter, mod_factor, size)
                        cv2.imwrite(img_path + '\\MeterImages\\' + img_name, meter)
                        print (str(angles[cardinal_number - 1]) + "," + str(deflection[cardinal_number - 1]))
                        break
                    except ValueError:
                        print ("error")
                        cap.release()
                        cv2.destroyAllWindows()
                        break
                else:
                    print ("Check if Camera is Available")
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            except ValueError:
                print ("error")
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

start_capture()
