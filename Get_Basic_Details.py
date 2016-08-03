import json
import cv2
import math
import GetCardinalContours
import GetBaseCardinals


def get_cardianls_from_image(img_path, supression, min_range, max_range):
    meter_info = open(img_path+"\\meterinfo.json", "w")
    meterinfo = {}


    cardinal_coordinates = []
    base_x, base_y, top_x, top_y = GetBaseCardinals.zero_needle_position(img_path, 0)
    # print "meter_No:", meter_no, base_x, base_y, top_x, top_y

    # Todo: Generate all contours array
    contour_array = GetCardinalContours.get_contours(img_path, min_range, max_range)
    # print "cardinals count :", len(contour_array)
    if supression == "x2" or supression == "x5":
        # Todo: supression cardinals length should
        skip_last_cardinal = len(contour_array)
    else:
        # Todo: skip last cardinal for geting plot on Image
        skip_last_cardinal = len(contour_array) - 1

    # Todo: get top contours coordinates
    # top_x, top_y = GetCardinalContours.find_top_cardinal(contour_array, min_range, max_range)
    # Todo: get top contour distance
    min_dist = math.sqrt((top_x - top_x) ** 2 + (top_y - base_y) ** 2)

    # TODO: Draw initial cardinal line
    img = GetCardinalContours.draw_intermediate_cardinals(img_path, (base_x, base_y), top_x, top_y)

    # Todo: Generate all contours array
    img, cardinal_contour_list, cardinal_coordinates, xlist, ylist = GetCardinalContours.draw_main_cardinals(img,
           contour_array, top_x, base_y, min_dist, min_range, max_range, skip_last_cardinal)

    print "cardinal_x:", xlist
    print "cardinal_y:", ylist
    print "cardinal(x,y):", cardinal_coordinates
    cv2.imwrite(img_path + "\\MeterImages\\cardinals.jpg", img)
    # Todo: save details of meter base and top (x,y) co-ordinate to skip recall to this module
    meterinfo["meter1"] = {
        "base_x": str(int(base_x)),
        "base_y": str(int(base_y)),
        "top_x": str(int(top_x)),
        "top_y": str(int(top_y)),
        "cardinal_x": xlist,
        "cardinal_y": ylist
    }
    meter_info.write(json.JSONEncoder().encode(meterinfo))
    # print json.JSONEncoder().encode(meterinfo)
    meter_info.close()
print ""
cv2.waitKey(0)
