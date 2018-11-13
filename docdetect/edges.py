# -*- coding: utf-8 -*-
import cv2


def detect_edges(im, blur=9, thr1=100, thr2=200, remove_text=True):
    saturation = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[:, :, 2]
    saturation = cv2.medianBlur(saturation, blur)
    edges = cv2.Canny(saturation, thr1, thr2)
    if remove_text:
        characters = find_text_regions(im)
        for character in characters:
            edges[character[:, 1], character[:, 0]] = 0
    return edges


def find_text_regions(im):
    height, width = im.shape[:2]
    max_size = int((width * height) / 1e2)
    mser = cv2.MSER_create(_max_area=max_size)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    characters, _ = mser.detectRegions(gray)
    return characters
