# -*- coding: utf-8 -*-
import numpy as np
from docdetect.line_utils import lines_angle


def find_corners(lines, im, angle_thr=45):
    height, width = im.shape[:2]
    corners = []
    vertex_id = 0
    for line1 in lines:
        for line2 in lines:
            if not _angle_is_valid(line1, line2, angle_thr):
                continue
            x, y = _find_intersection_coordinates(line1, line2)
            if _coordinates_are_valid(x, y, width, height) and not already_present(x, y, corners):
                corners.append({'id': vertex_id, 'lines': (line1, line2), 'corner': (x, y)})
                vertex_id += 1
    return corners


def _find_intersection_coordinates(line1, line2):
    rho1, theta1 = line1
    rho2, theta2 = line2
    a = np.array([[np.cos(theta1), np.sin(theta1)], [np.cos(theta2), np.sin(theta2)]])
    b = np.array([[rho1], [rho2]])
    try:
        # aX = b, solve for x
        x, y = np.round(np.linalg.solve(a, b))
        return int(x), int(y)
    except np.linalg.linalg.LinAlgError:
        # singular matrix
        return -1, -1


def already_present(_x, _y, corners):
    for corner in corners:
        x = corner['corner'][0]
        y = corner['corner'][1]
        if _x == x and _y == y:
            return True
    return False


def _angle_is_valid(line1, line2, angle_thr):
    return lines_angle(line1, line2) > angle_thr


def _coordinates_are_valid(x, y, width, height):
    return 0 < x < width and 0 < y < height