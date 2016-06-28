import json

import cv2
import math
import numpy as np
import GetCurrentNeedle
import GetCardinalContours
import GetBaseCardinals
import GetNeedleByThreshold


def initprocess(img_path, frame, mod_factor, size):

    meter_size = open("metersize.json", "r")
    json_data = json.load(meter_size)
    min_range = json_data[size]["min_range"]
    max_range = json_data[size]["max_range"]
    # TODO: get needle point and get base contours coordinates
    base_x, base_y = GetBaseCardinals.zero_needle_position(img_path, 3)

    # Todo: Generate all contours array
    contour_array = GetCardinalContours.get_contours(img_path, min_range, max_range)

    # Todo: get top contours coordinates
    top_x, top_y = GetCardinalContours.find_top_cardinal(contour_array, min_range, max_range)
    # Todo: get top contour distance
    min_dist = math.sqrt((top_x - top_x) ** 2 + (top_y - base_y) ** 2)

    # TODO: Draw initial cardinal line
    frame, cardinal_contour_list, cardinal_coordinates = GetCardinalContours.draw_main_cardinals(frame, contour_array,
                                                                                                 top_x, base_y,
                                                                                                 min_dist, min_range,
                                                                                                 max_range)
    length = len(cardinal_contour_list)

    frame = GetCardinalContours.draw_intermediate_cardinals(frame, (base_x, base_y), top_x, top_y)
    # get needle point
    tolerance = []

    if meter_size == "meter48":
        iterate = 4
    else:
        iterate = 3

    needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iteration=iterate)
    if not needle_x and not needle_y:
        needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iteration=iterate-1)

    try:
        pointer = ((needle_x, needle_y), (top_x, base_y))
        cardinal = ((base_x, base_y), (top_x, base_y))
        angle_list, cardinal_angle = GetCardinalContours.get_needle_angles(contour_array, top_x, base_y, pointer,
                                                                           cardinal, min_dist, min_range, max_range)
        len_angle = len(angle_list)
        count = 0
        while count < len_angle:
            # tolerance.append(round((angle_list[count] * 60) / 54, ndigits=2))
            tolerance.append(round((angle_list[count]) * mod_factor, ndigits=2))
            count += 1

        cv2.line(frame, (int(needle_x), int(needle_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
        cv2.circle(frame, (int(needle_x), int(needle_y)), 1, 255, -1)
        return frame, angle_list, tolerance
    except ValueError:
        return
