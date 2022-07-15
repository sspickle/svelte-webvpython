from .vec_js import vector_js as vector
from js import vector as js_vec

"""
Convert vectors back and forth between python and js
"""

py_vec = vector

def py2js_vec(v):
    if isinstance(v, list) or isinstance(v,tuple):
        return js_vec(v[0], v[1], v[2])
    return js_vec(v.x, v.y, v.z)

def js2py_vec(v, jsObj=None):
    return py_vec(v.x, v.y, v.z, jsObj=jsObj)
