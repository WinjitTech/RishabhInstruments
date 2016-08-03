import cv2
import numpy as np


def zero_needle_position(img_path, iteration):
    try:
        # # Todo: Read Image
        # image = cv2.imread(img_path+"\\MeterImages\\cardinal.jpg", 0)
        # # TODO: Find corner of needle
        # color = int(image[300, 300])
        # # print color
        # cv2.rectangle(image, (0, 0), (150, 1000), (color, color, color), -1)
        # kernel = np.ones((5, 5), np.uint8)
        # dilation = cv2.dilate(image, kernel, iterations=iteration)
        # corners = cv2.goodFeaturesToTrack(dilation, 2, 0.1, 10)
        # cx = cy = 0
        # for i in corners:
        #     x, y = i.ravel()
        #     cv2.circle(dilation, (x, y), 2, (0, 255, 0), -1)
        #     cx += x
        #     cy += y
        # cx /= len(corners)
        # cy /= len(corners)
        # return int(round(cx)), int(round(cy))

        image = cv2.imread(img_path+"\\MeterImages\\cardinal.jpg", 0)
        # cv2.rectangle(image, (0, 0), (150, 1200), (166, 166, 166), -1)
        # cv2.rectangle(image, (450, 0), (1000, 800), (166, 166, 166), -1)
        kernel = np.ones((5, 5), np.uint8)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        # ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_OTSU)
        dilation = cv2.dilate(image, kernel, iterations=iteration)
        # ret, img = cv2.threshold(dilation, 127, 255, cv2.THRESH_BINARY)
        # cv2.imshow("fd", dilation)
        corners = cv2.goodFeaturesToTrack(dilation, 100, 0.1, 10)
        # print "Corners", len(corners)
        cx = cy = 0
        listx = []  # Todo : base x & y
        listy = []  # Todo : top x & y
        for i in corners:
            x, y = i.ravel()
            cv2.circle(dilation, (x, y), 2, (0, 255, 0), -1)
            cx += x
            cy += y
            listx.append(x)
            listy.append(y)
            # print "Co-ordinates: ", x, y
        listx.sort()
        listy.sort()
        for i in corners:
            x, y = i.ravel()
            if x == listx[0]:
                cv2.circle(dilation, (int(x), int(y)), 10, (0, 255, 0), -1)
                # return x, y
                x1 = x
                y1 = y
                break

        for i in corners:
            x, y = i.ravel()
            if y == listy[0]:
                cv2.circle(dilation, (int(x), int(y)), 10, (0, 255, 0), -1)
                x2 = x
                y2 = y
                break
                # return x, y
        # cv2.imshow("cvhj", dilation)
        return x1, y1, x2, y2

    except Exception, e:
        print "Exception in Base Needle Detection Dilute Image:", str(e)


