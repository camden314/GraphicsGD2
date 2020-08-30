import math
import sys
import numpy as np
from svgpathtools import svg2paths, wsvg, parse_path, CubicBezier, Arc, QuadraticBezier, Line
import level
import msgport
from xml.dom import minidom

def mad(data, axis=None):
    return np.mean(abs(data - np.mean(data, axis)), axis)


def slope(x1, y1, x2, y2):
    try:
        m = math.atan2(y2 - y1, x2 - x1)
    except Exception:
        return 0
    else:
        return m


def generate(file_path, scale, density, block_size):
    scale/=density

    # new data~
    """mydoc = minidom.parse(file_path)
    path_tag = mydoc.getElementsByTagName("path")
    d_string = path_tag[0].attributes['d'].value"""
    #end new data
    pths, _ = svg2paths(file_path)
    wsvg(pths, filename='.tmp.svg')
    paths, _ = svg2paths('.tmp.svg')
    pathsxy = []
    lvl = level.Level("ggd")
    for path in paths:
        x_paths = [0.1]
        y_paths = [0.1]
        slopes = []
        for p in path:
            p.start /= scale
            p.end /= scale
            if isinstance(p, CubicBezier):
                p.control1 /= scale
                p.control2 /= scale
            elif isinstance(p, Arc):
                p.radius /= scale
            elif isinstance(p, QuadraticBezier):
                p.control /= scale
            elif not isinstance(p, Line):

                print(p)
            for i in range(int(round(p.length()))):
                comp = p.point(i / p.length())
                slopes.append(slope(x_paths[-1], y_paths[-1], comp.real, comp.imag))
                x_paths.append(comp.real)
                y_paths.append(comp.imag)
        pathsxy.append(np.column_stack((x_paths[1:], y_paths[1:], slopes, )))
    svglengthy = max(np.concatenate([l[:, 1] for l in pathsxy]))
    total = 0
    for path in pathsxy:
        for point in path:
            total += 1
            lvl.addBlock(917, (point[0]*2)/density, (((-1*point[1])+svglengthy)*2)/density,
                         rotation=math.degrees(point[2]), size=block_size,
                         dont_fade=1, dont_enter=1)

    return lvl
