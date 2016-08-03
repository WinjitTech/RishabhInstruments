import json

import cv2
import math
import numpy as np

import Find_Angle
import GetCurrentNeedle
import GetCardinalContours
import GetBaseCardinals
import GetNeedleByThreshold


def initprocess(img_path, frame, mod_factor, size):
    supression = ""
    meter_size = open(img_path + "\\metersize.json", "r")
    json_data = json.load(meter_size)
    min_range = json_data[size]["min_range"]
    max_range = json_data[size]["max_range"]
    meter_size.close()
    # Todo: Load pre-calcluated settings
    meter_info = open(img_path + "\\meterinfo.json", "r")
    json_data = json.load(meter_info)
    base_x = int(json_data["meter1"]["base_x"])
    base_y = int(json_data["meter1"]["base_y"])
    top_x = int(json_data["meter1"]["top_x"])
    top_y = int(json_data["meter1"]["top_y"])
    xlist = json_data["meter1"]["cardinal_x"]
    ylist = json_data["meter1"]["cardinal_y"]
    # TODO: Draw basic structure
    cv2.line(frame, (int(base_x), int(base_y)), (int(top_x), int(base_y)), (0, 0, 255), 1)
    cv2.line(frame, (int(top_x), int(top_y)), (int(top_x), int(base_y)), (0, 0, 255), 1)
    # todo: Draw cardinals
    for i in range(len(xlist)):
        cv2.line(frame, (int(xlist[i]), int(ylist[i])), (int(top_x), int(base_y)), (255, 0, 0), 1)

    min_dist = math.sqrt((top_x - top_x) ** 2 + (top_y - base_y) ** 2)
    # Todo: get Needle
    iterate = 3
    needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iteration=iterate)
    if not needle_x and not needle_y:
        needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iteration=iterate - 1)
    cv2.line(frame, (int(needle_x), int(needle_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
    i = 0
    angle_list = []
    cardinal_angle = []
    pointer = ((needle_x, needle_y), (top_x, base_y))
    base_line = ((base_x, base_y), (top_x, base_y))
    for i in range(len(xlist)):
        dist = round(math.sqrt((xlist[i] - top_x) ** 2 + (ylist[i] - base_y) ** 2), ndigits=2)
        if min_dist - 40 <= dist <= min_dist + 40:
            cardinal = ((xlist[i], ylist[i]), (top_x, base_y))
            cardinal_ang = round(Find_Angle.ang(cardinal, base_line), ndigits=2)
            cardinal_angle.append(cardinal_ang)
            base_and_pointer_angle = Find_Angle.ang(base_line, pointer)
            needle_angle = Find_Angle.ang(cardinal, pointer)
            if base_and_pointer_angle >= cardinal_ang:
                angle_list.append(round(needle_angle, ndigits=2))
            else:
                angle_list.append(round(-needle_angle, ndigits=2))
    i += 1
    cv2.imshow("cfds", frame)
    cv2.waitKey(0)
    tolerance = []
    try:
        len_angle = len(angle_list)
        count = 0
        while count < len_angle:
            tolerance.append(round((angle_list[count]) * mod_factor, ndigits=2))
            count += 1

        cv2.line(frame, (int(needle_x), int(needle_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
        cv2.circle(frame, (int(needle_x), int(needle_y)), 1, 255, -1)
        return frame, angle_list, tolerance
    except ValueError:
        return
