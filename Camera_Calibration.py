import json
import sys
import cv2
import imutils

img_path = str(sys.argv[1])

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
if not ret:
    print ("Check if Camera is Available")
    cap.release()
    cv2.destroyAllWindows()
else:
    data = {}
    config = open(img_path + "\\frame.json", "w")
    # config = open("frame.json", "w")
    cam_status = open(img_path + "\\camerastatus.txt", "w")
    # cam_status = open("camerastatus.txt", "w")
    msg = "Press 'Esc' or 'space' button to proceed..."
    try:
        while 1:

            ret, image = cap.read()
            if not ret:
                print ("Check if Camera is Available")
            else:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                #
                # cv2.putText(image, msg, (80, 80), cv2.QT_FONT_NORMAL, 0.5, (0, 255, 0), thickness=1,
                #             lineType=cv2.CV_8U)
                cv2.imshow("Meter", image)
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
                                (cx, cy), radius = cv2.minEnclosingCircle(approx)
                                cv2.rectangle(image, (int(x), int(y)), (int(w + x), int(h + y)), (0, 255, 0), thickness=2)                                # cv2.rectangle(image, (int(x + 24), int(y + 24)), (int((w + x) - 98), int(h + y) - 98),(0, 255, 0), thickness=2)
                                meter_frame = image[int(y + 24):int(h + y) - 100, int(x + 24):int(w + x) - 100]
                                data["x1"] = int(x + 24)
                                data["x2"] = int(w + x) - 100
                                data["y1"] = int(y + 24)
                                data["y2"] = int(h + y) - 100
                                json_data = json.dumps(data)

                                cv2.putText(image, msg, (80, 80), cv2.QT_FONT_NORMAL, 0.5, (0, 255, 0), thickness=1,
                                            lineType=cv2.CV_8U)
                                cv2.imshow("Meter", image)
                                # print int(y + 40), int(h + y) - 100, int(x + 40), int(w + x) - 100
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    cap.release()
                    cv2.destroyAllWindows()
                    break
                if cv2.waitKey(1) == 27:
                    cap.release()
                    cv2.destroyAllWindows()
                    break

    except Exception, e:
        cap.release()
        cv2.destroyAllWindows()
        # print str(e)
        print "error"
    cv2.imwrite(img_path + "\\MeterImages\\cardinals.jpg", meter_frame)
    # cv2.imwrite("MeterImages/cardinals.jpg", meter_frame)
    config.write(json_data)
    cam_status.write("true")
    config.close()
    cam_status.close()
    cap.release()
    cv2.destroyAllWindows()
