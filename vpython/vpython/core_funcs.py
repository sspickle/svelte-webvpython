from xml.dom.domreg import well_known_implementations
from js import sphere as js_sphere, box as js_box, color, vec as js_vec, rate as async_rate
from js import cylinder as js_cylinder, arrow as js_arrow, cone as js_cone, helix as js_helix
from js import label as js_label, scene as js_scene, text as js_text, ellipsoid as js_ellipsoid
from js import pyramid as js_pyramid, ring as js_ring, text as js_text

from .vector import vector as py_vec

def py2js_vec(v):
    return js_vec(v.x, v.y, v.z)

def js2py_vec(v, jsObj=None):
    return py_vec(v.x, v.y, v.z, jsObj=jsObj)

def translate_kwargs(kwargs, vecAttrs):
    # Translate the vecAttrs from kwargs to js vectors.
    for attr in vecAttrs:
        if attr in kwargs:
            kwargs[attr] = py2js_vec(kwargs[attr])
    return kwargs

class glowProxy(object):
    """
    A proxy for a glowscript library object.
    """

    GP_defaults = {'vecAttrs':[], 'oType':None, 'jsObj':None}

    def __init__(self, vecAttrs, oType, factory=None, jsObj=None, *args, **kwargs):
        """
        vecAttrs is a list of vector attributes.
        oType is the name of the JS object type (e.g., sphere...)
        factory is JS function that constructs the jsObj.
        kwArgs are the keyword arguments for the factory.
        args are the positional arguments for the factory.
        """
        self.vecAttrs = vecAttrs
        self.funcs = ['rotate']
        self.oType = oType
        kwargs = translate_kwargs(kwargs, self.vecAttrs)
        if factory is None:
            self.jsObj = jsObj
        else:
            self.jsObj = factory(*args, **kwargs)

    def __setattr__(self, name, value):
        if name in ['jsObj', 'vecAttrs', 'oType', 'funcs']:
            self.__dict__[name] =  value
        elif name in self.vecAttrs:
            setattr(self.jsObj, name, py2js_vec(value))
        else:
            setattr(self.jsObj, name, value)
    
    def __getattr__(self, name):
        #if name in ['jsObj', 'vecAttrs', 'oType','funcs'] + self.funcs:  # it's tricky with __getattr__. Might want to re-think this...
        if name in ['jsObj', 'vecAttrs', 'oType']:
            return self.__dict__.get(name, 
                glowProxy.GP_defaults.get(name, None))
        elif name in self.vecAttrs:
            return js2py_vec(getattr(self.jsObj, name), jsObj=getattr(self.jsObj,name))
        else:
            return getattr(self.jsObj, name)

    def rotate(self, *args, **kwargs): # We may need to intercept certain functions and assignements to do js/py vec conversions
        """
        Rotate the object.
        """
        kwargs = translate_kwargs(kwargs=kwargs, vecAttrs=['axis','origin'])
        self.jsObj.rotate(*args, **kwargs)
        return self

def sphere(*args, **kwargs):
    return glowProxy(['pos','color'], 'sphere', factory=js_sphere, *args, **kwargs)

def box(*args, **kwargs):
    return glowProxy(['pos','color','size'], 'box', factory=js_box, *args, **kwargs)

def cylinder(*args, **kwargs):
    return glowProxy(['pos', 'axis', 'color'], 'cylinder', factory=js_cylinder, *args, **kwargs)

def arrow(*args, **kwargs):
    return glowProxy(['pos', 'axis', 'color'], 'arrow', factory=js_arrow, *args, **kwargs)

def cone(*args, **kwargs):
    return glowProxy(['pos', 'axis', 'color'], 'cone', factory=js_cone, *args, **kwargs)

def helix(*args, **kwargs):
    return glowProxy(['pos', 'axis', 'color'], 'helix', factory=js_helix, *args, **kwargs)

def label(*args, **kwargs):
    return glowProxy(['pos', 'color'], 'label', factory=js_label, *args, **kwargs)

def ellipsoid(*args, **kwargs):
    return glowProxy(['pos', 'color', 'axis', 'size'], 'ellipsoid', factory=js_ellipsoid, *args, **kwargs)

def pyramid(*args, **kwargs):
    return glowProxy(['pos', 'color', 'axis', 'size'], 'pyramid', factory=js_pyramid, *args, **kwargs)

def ring(*args, **kwargs):
    return glowProxy(['pos', 'color', 'axis'], 'ring', factory=js_ring, *args, **kwargs)

def text(*args, **kwargs):
    return glowProxy(['pos', 'color', 'axis'], 'text', factory=js_text, *args, **kwargs)

scene = glowProxy(['forward', 'center'], 'scene', jsObj = js_scene)
