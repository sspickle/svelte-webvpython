from .vec_js import vector_js as vector
from js import vector as js_vec

"""
Convert vectors back and forth between python and js
"""

py_vec = vector

def py2js_vec(v):
    return js_vec(v.x, v.y, v.z)

def js2py_vec(v, jsObj=None):
    return py_vec(v.x, v.y, v.z, jsObj=jsObj)
