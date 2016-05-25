import cv2
import math
import numpy as np
import GetCurrentNeedle
import GetCardinalContours
import GetBaseCardinals



def initprocess(frame):
    # TODO: get needle point and get base contours coordinates
    base_x, base_y = GetBaseCardinals.zero_needle_position(3)
    if base_y <= 450:
        base_x, base_y = GetBaseCardinals.zero_needle_position(2)

    # Todo: Generate all contours array
    contour_array = GetCardinalContours.get_contours()
    if len(contour_array) <= 0:
        print "Please refresh Image, Did not find any cardinal!"

    # get top contours coordinates
    top_x, top_y = GetCardinalContours.find_top_cardinal(contour_array)
    # Todo: get top contour distance
    min_dist = math.sqrt((top_x - top_x) ** 2 + (top_y - base_y) ** 2)

    # TODO: Draw initial cardinal line
    frame, cardinal_contour_list, cardinal_coordinates = GetCardinalContours.draw_main_cardinals(frame, contour_array,
                                                                                                 top_x, base_y, min_dist)
    length = len(cardinal_contour_list)

    frame = GetCardinalContours.draw_intermediate_cardinals(frame, (base_x, base_y), cardinal_contour_list[length - 1])

    # get needle point
    tolerance = []
    try:
        needle_x, needle_y = GetCurrentNeedle.get_needle_tip(top_x, base_y, iteration=3)
    except Exception, e:
        needle_x, needle_y = GetCurrentNeedle.get_needle_tip(top_x, base_y, iteration=2)

    pointer = ((needle_x, needle_y), (top_x, base_y))
    cardinal = ((base_x, base_y), (top_x, base_y))
    angle_list, cardinal_angle = GetCardinalContours.get_needle_angles(contour_array, top_x, base_y, pointer,
                                                                       cardinal, min_dist)
    len_angle = len(angle_list)
    count = 0
    while count < len_angle:
        tolerance.append(round((angle_list[count]*60)/54, ndigits=4))
        count += 1
    needle_len = math.sqrt((needle_x - top_x) ** 2 + (needle_y - base_y) ** 2)
    if 100 < needle_len < 500:
        count = 0
        while count < len_angle:
            cv2.line(frame, (int(needle_x), int(needle_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
            cv2.circle(frame, (needle_x, needle_y), 1, 255, -1)
            count += 1
    cv2.imwrite("MeterImages/result.jpg", frame)
    return frame, angle_list, tolerance
