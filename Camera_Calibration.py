import cv2
import imutils
from Get_Basic_Details import *

# img_path = str(sys.argv[1])
img_path = "C:\\Users\\rohitsalunke\\PycharmProjects\\RishabhInstruments_PahseI_Dev"
# size = "meter" + str(sys.argv[2])
size = "meter96"

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if not ret:
    print ("Check if Camera is Available")
    cap.release()
    cv2.destroyAllWindows()
else:
    data = {}
    # config = open(img_path + "\\frame.json", "w")
    # config = open("frame.json", "w")
    cam_status = open(img_path + "\\camerastatus.txt", "w")
    # cam_status = open("camerastatus.txt", "w")
    msg = "Press 'Esc' or 'space' button to proceed..."

    meter_crop = open(img_path + "\\cropping.json", "r")
    json_data = json.load(meter_crop)
    x1 = json_data[size]["x1"]
    y1 = json_data[size]["y1"]
    x2 = json_data[size]["x2"]
    y2 = json_data[size]["y2"]
    rx1 = json_data[size]["rec_x1"]
    ry1 = json_data[size]["rec_y1"]
    rx2 = json_data[size]["rec_x2"]
    ry2 = json_data[size]["rec_y2"]
    meter_crop.close()
    try:
        while 1:

            ret, image = cap.read()
            img_show = image
            if not ret:
                print ("Check if Camera is Available")
            else:
                # cv2.rectangle(img_show, (342, 172), (882, 700), (0, 255, 0), thickness=2)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                #
                # cv2.putText(image, msg, (80, 80), cv2.QT_FONT_NORMAL, 0.5, (0, 255, 0), thickness=1,
                #             lineType=cv2.CV_8U)
                # cv2.rectangle(img_show, (rx1, ry1), (rx2 + rx1, ry2 + ry1), (0, 255, 0), thickness=2)
                cv2.imshow("Meter", image)
                meter_frame = {}
                meter_no = 0
                config = open(img_path + "\\frame.json", "w")
                json_data = ""
                meter_obj = {}
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
                        if 0.95 <= ar <= 1.05:
                            if cv2.contourArea(c) > 40000:
                                (x, y, w, h) = cv2.boundingRect(approx)
                                # print (x, y, w, h)
                                (cx, cy), radius = cv2.minEnclosingCircle(approx)
                                cv2.rectangle(image, (int(x + x1), int(y + y1)), (int((w + x) - x2), int(h + y) - y2),
                                              (0, 255, 0), thickness=2)
                                meter_frame = image[int(y + y1 + 2):int(h + y) - y2 - 2,
                                              int(x + x1 + 2):int(w + x) - x2 - 2]

                                data["x1"] = int(x + x1 + 2)
                                data["x2"] = int(w + x) - x2 - 2
                                data["y1"] = int(y + y1 + 2)
                                data["y2"] = int(h + y) - y2 - 2
                                # Todo: generate cropping property for number of meters on gig
                                # meter_obj[meter_no+1] = json.dumps(data)

                                cv2.putText(image, msg, (20, 20), cv2.QT_FONT_NORMAL, 0.5, (0, 255, 0), thickness=1,
                                            lineType=cv2.CV_8U)
                                cv2.imshow("Meter", img_show)
                                # print int(y + 40), int(h + y) - 100, int(x + 40), int(w + x) - 100
                                meter_no += 1
                                cv2.imwrite(img_path + "\\MeterImages\\crop\\" + str(meter_no) + ".jpg", meter_frame)
                # print meter_obj
                # break
                if cv2. waitKey(1) & 0xFF == ord(' '):
                    cap.release()
                    cv2.destroyAllWindows()
                    break
                if cv2.waitKey(1) == 27:
                    cap.release()
                    cv2.destroyAllWindows()
                    break
        # meter_obj = json.JSONEncoder().encode(meter_obj)
        json_data = json.dumps(data)
        config.write(json_data)
        cam_status.write("true")
        config.close()
    except ValueError:
        cap.release()
        cv2.destroyAllWindows()
        # print str(e)
        print "error"


    supression = "x2"
    cv2.imwrite(img_path + "\\MeterImages\\cardinal.jpg", meter_frame)

    meter_size = open(img_path + "\\metersize.json", "r")
    json_data = json.load(meter_size)
    min_range = json_data[size]["min_range"]
    max_range = json_data[size]["max_range"]
    # print min_range, max_range
    meter_size.close()
    get_cardianls_from_image(img_path, supression, min_range, max_range)
