from .core_funcs import pyramid, ring, sphere, box, js_vec, rate, cylinder, arrow, cone, helix, label, scene
from .core_funcs import ellipsoid, pyramid, ring, text, distant_light, local_light, button
from .core_funcs import slider, radio, checkbox, menu, wtext, curve, points, get_library
from .core_funcs import vertex, triangle, quad, extrusion, canvas, attach_light, compound
from .core_funcs import graph, gcurve, gvbars, gdots, js_debug, simple_sphere
from .shapespaths_orig import *
from .vector import adjust_axis, adjust_up, comp, cross, diff_angle, dot, hat, mag, mag2, norm, object_rotate, proj, rotate
from .vec_js import vector_js as vector
from .color import color
from js import textures, bumpmaps, winput

import time
clock = time.perf_counter

def sleep(dt): # don't use time.sleep because it delays output queued up before the call to sleep
    t = clock()+dt
    while clock() < t:
        rate(60)

vec = vector
py_vec = vector

__all__ = ["sphere", "box", "color", "vec", "py_vec", "js_vec", "vector", "rate","sleep",
"cylinder", "arrow", "cone", "helix", 'adjust_axis', 'adjust_up', 'comp', 'cross', 'diff_angle', 'dot',
'hat', 'mag', 'mag2', 'norm', 'object_rotate', 'proj', 'rotate', 'scene', 'distant_light','label',
'ellipsoid', 'pyramid', 'ring', 'text', 'textures', 'attach_light', 'local_light','button',
'slider', 'wtext', 'radio', 'checkbox', 'menu', 'curve', 'points','vertex', 'triangle','quad',
'extrusion', 'paths','shapes', 'canvas','textures', 'compound','color','js_debug', 'winput',
'graph', 'gcurve', 'gvbars', 'gdots','bumpmaps', 'clock', 'simple_sphere', 'get_library']
