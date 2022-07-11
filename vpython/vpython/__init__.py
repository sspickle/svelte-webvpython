print("Initializing vpython module")
from .core_funcs import pyramid, ring, sphere, box, color, js_vec, async_rate, cylinder, arrow, cone, helix, label, scene
from .core_funcs import ellipsoid, pyramid, ring, text
from .vector import *
from js import distant_light, textures, attach_light

py_vec = vector
vec = vector

__all__ = ["sphere", "box", "color", "vec", "py_vec", "js_vec", "vector", "async_rate",
"cylinder", "arrow", "cone", "helix", 'adjust_axis', 'adjust_up', 'comp', 'cross', 'diff_angle', 'dot',
'hat', 'mag', 'mag2', 'norm', 'object_rotate', 'proj', 'rotate', 'scene', 'distant_light','label',
'ellipsoid', 'pyramid', 'ring', 'text', 'textures', 'attach_light']
