from js import sphere as js_sphere, box as js_box, color, vec as js_vec, rate as async_rate
from js import cylinder as js_cylinder, arrow as js_arrow, cone as js_cone, helix as js_helix
from .vector import vector as py_vec

def py2js_vec(v):
    return js_vec(v.x, v.y, v.z)

def js2py_vec(v):
    return py_vec(v.x, v.y, v.z)

class glowProxy(object):
    """
    A proxy for a glowscript library object.
    """

    def __init__(self, vecAttrs, oType, factory, *args, **kwargs):
        """
        vecAttrs is a list of vector attributes.
        oType is the name of the JS object type (e.g., sphere...)
        factory is JS function that constructs the jsObj.
        kwArgs are the keyword arguments for the factory.
        args are the positional arguments for the factory.
        """
        self.vecAttrs = vecAttrs
        self.oType = oType
        for attr in self.vecAttrs:
            if attr in kwargs:
                kwargs[attr] = py2js_vec(kwargs['pos'])
        self.jsObj = factory(*args, **kwargs)

    def __setattr__(self, name, value):
        if name in ['jsObj', 'vecAttrs', 'oType']:
            self.__dict__[name] =  value
        elif name in self.vecAttrs:
            setattr(self.jsObj, name, py2js_vec(value))
        else:
            setattr(self.jsObj, name, value)
    
    def __getattr__(self, name):
        if name in ['jsObj', 'vecAttrs', 'oType']:
            return self.__dict__[name]
        elif name in self.vecAttrs:
            return js2py_vec(getattr(self.jsObj, name))
        else:
            return getattr(self.jsObj, name)

def sphere(*args, **kwargs):
    return glowProxy(['pos'], 'sphere', js_sphere, *args, **kwargs)

def box(*args, **kwargs):
    return glowProxy(['pos'], 'box', js_box, *args, **kwargs)

def cylinder(*args, **kwargs):
    return glowProxy(['pos', 'axis'], 'cylinder', js_cylinder, *args, **kwargs)

def arrow(*args, **kwargs):
    return glowProxy(['pos', 'axis'], 'arrow', js_arrow, *args, **kwargs)

def cone(*args, **kwargs):
    return glowProxy(['pos', 'axis'], 'cone', js_cone, *args, **kwargs)

def helix(*args, **kwargs):
    return glowProxy(['pos', 'axis'], 'helix', js_helix, *args, **kwargs)
