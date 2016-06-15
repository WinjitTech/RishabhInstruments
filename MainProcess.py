import cv2
import math
import numpy as np
import GetCurrentNeedle
import GetCardinalContours
import GetBaseCardinals
import GetNeedleByThreshold


def initprocess(img_path, frame):
    f = open(img_path + "\\Needlelog.txt", "w")
    # TODO: get needle point and get base contours coordinates
    base_x, base_y = GetBaseCardinals.zero_needle_position(img_path, 3)
    f.write("Base Success\n")
    # if base_y <= 450:
    #     base_x, base_y = GetBaseCardinals.zero_needle_position(img_path, 2)

    # Todo: Generate all contours array
    contour_array = GetCardinalContours.get_contours(img_path)
    f.write("contour_array Success\n")
    # if len(contour_array) <= 0:
    # print "Please refresh Image, Did not find any cardinal!"

    # get top contours coordinates
    top_x, top_y = GetCardinalContours.find_top_cardinal(contour_array)
    f.write("find_top_cardinal Success\n")
    # Todo: get top contour distance
    min_dist = math.sqrt((top_x - top_x) ** 2 + (top_y - base_y) ** 2)

    # TODO: Draw initial cardinal line
    frame, cardinal_contour_list, cardinal_coordinates = GetCardinalContours.draw_main_cardinals(frame, contour_array,
                                                                                                 top_x, base_y,
                                                                                                 min_dist)
    f.write("draw_main_cardinals Success\n")
    length = len(cardinal_contour_list)

    frame = GetCardinalContours.draw_intermediate_cardinals(frame, (base_x, base_y), top_x, top_y)
    f.write("draw_intermediate_cardinals Success\n")
    # get needle point
    tolerance = []
    cv2.imwrite(img_path+"\\Cards.jpg", frame)

    needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iteration=3)
    # needle_x, needle_y = GetCurrentNeedle.get_needle_tip(img_path, top_x, base_y, iteration=3)
    # needle_x, needle_y = GetCurrentNeedle_New.get_needle_tip(img_path, iteration=3)
    f.write("get_needle_tip Success\n")
    if not needle_x and not needle_y:
        needle_x, needle_y = GetNeedleByThreshold.get_needle_tip(img_path, top_x, base_y, iteration=2)
        # needle_x, needle_y = GetCurrentNeedle.get_needle_tip(img_path, top_x, base_y, iteration=2)
        # needle_x, needle_y = GetCurrentNeedle_New.get_needle_tip(img_path, iteration=2)

    try:
        pointer = ((needle_x, needle_y), (top_x, base_y))
        cardinal = ((base_x, base_y), (top_x, base_y))
        angle_list, cardinal_angle = GetCardinalContours.get_needle_angles(contour_array, top_x, base_y, pointer,
                                                                           cardinal, min_dist)
        len_angle = len(angle_list)
        count = 0
        while count < len_angle:
            tolerance.append(round((angle_list[count] * 60) / 54, ndigits=2))
            count += 1

        cv2.line(frame, (int(needle_x), int(needle_y)), (int(top_x), int(base_y)), (0, 255, 0), 1)
        cv2.circle(frame, (int(needle_x), int(needle_y)), 1, 255, -1)
        f.write("needle_tip Success\n")
        f.close()
        return frame, angle_list, tolerance
    except Exception, e:
        return
