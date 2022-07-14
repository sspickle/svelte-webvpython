from js import sphere as js_sphere, box as js_box, shapes, paths, vec as js_vec, rate
from js import cylinder as js_cylinder, arrow as js_arrow, cone as js_cone, helix as js_helix
from js import label as js_label, scene as js_scene, textures
from js import pyramid as js_pyramid, ring as js_ring, text as js_text
from js import button as js_button, distant_light as js_distant_light, local_light as js_local_light
from js import slider as js_slider, wtext as js_wtext, radio as js_radio, checkbox as js_checkbox
from js import menu as js_menu, curve as js_curve, Object
from js import points as js_points, extrusion as js_extrusion
from js import window as js_window, fontloading as js_fontloading, waitforfonts as js_waitforfonts
from js import quad as js_quad, vertex as js_vertex, triangle as js_triangle, ellipsoid as js_ellipsoid
from js import canvas as js_canvas, attach_light as js_attach_light, compound as js_compound

from pyodide.ffi import create_proxy, to_js

from .curveArgs import getStdForm
from .vec_js import vector_js as vector

from .vec_conversion import js2py_vec, py2js_vec
from .shapes_piodide import convertPyVecsToJSList

def translate_kwargs_nest(kwargs, nestAttrs):
    """
    Handle nested structures of lists of vectors.
    """
    for attr in nestAttrs:
        if attr in kwargs:
            kwargs[attr] = convertPyVecsToJSList(kwargs[attr])
    return kwargs

def translate_kwargs_vecs(kwargs, vecAttrs):
    # Translate the vecAttrs from kwargs to js vectors.
    for attr in vecAttrs:
        if attr in kwargs:
            kwargs[attr] = py2js_vec(kwargs[attr])
    return kwargs

def translate_kwargs_lists(kwargs, listAttrs):
    for attr in listAttrs:
        if attr in kwargs:
            kwargs[attr] = to_js(kwargs[attr])
    return kwargs

def translate_kwargs_funcs(kwargs, funcAttrs):
    for attr in funcAttrs:
        if attr in kwargs:
            kwargs[attr] = create_proxy(kwargs[attr])
    return kwargs

class glowProxy(object):
    """
    A proxy for a glowscript library object. Most attributes are stored as js objects/attributes of
    the mirrored javascript object handled/used by the glowscript library.

    vecAttrs is a list of names of vector attributes.
    listAttrs is a list of names of list attributes (e.g., lights, points, etc.)
    funcAttrs is a list of names of function attributes (e.g., bind)
    oType is the name of the JS object type (e.g., sphere...)
    GP_keys are the names of attributes stored in self.__dict__, not proxied from jsObj.
    """

    GP_defaults = {'vecAttrs':[], 'oType':None, 'jsObj':None, 'listAttrs':[], 'funcAttrs':[], 'nestAttrs':[]}
    GP_keys = list(GP_defaults.keys())

    def __init__(self, *args, factory=None, jsObj=None, **kwargs):
        """
        factory is JS function that constructs the jsObj.
        kwArgs are the keyword arguments for the factory.
        args are the positional arguments for the factory.
        """
        for attr in glowProxy.GP_keys:
            self.__dict__[attr] = kwargs.get(attr, glowProxy.GP_defaults.get(attr, None)) # grab kwargs for GP_keys

        kwargs = translate_kwargs_vecs(kwargs, self.vecAttrs)
        kwargs = translate_kwargs_lists(kwargs, self.listAttrs)
        kwargs = translate_kwargs_funcs(kwargs, self.funcAttrs)
        kwargs = translate_kwargs_nest(kwargs, self.nestAttrs)

        for attr in glowProxy.GP_keys:
            if attr in kwargs:
                del kwargs[attr] # don't pass these to js

        if factory is None:
            self.jsObj = jsObj
        else:
            self.jsObj = factory(*args, **kwargs)

    def __setattr__(self, name, value):
        if name in glowProxy.GP_keys:
            self.__dict__[name] =  value
        elif name in self.vecAttrs:
            setattr(self.jsObj, name, py2js_vec(value))
        elif name in self.listAttrs:
            setattr(self.jsObj, name, to_js(value))
        else:
            setattr(self.jsObj, name, value)
    
    def __getattr__(self, name):
        if name in glowProxy.GP_keys:
            return self.__dict__.get(name, 
                glowProxy.GP_defaults.get(name, None))
        elif name in self.vecAttrs:
            return js2py_vec(getattr(self.jsObj, name), jsObj=getattr(self.jsObj,name)) # keep jsObj embedded in pyObj
        else:
            return getattr(self.jsObj, name)

    def __str__(self):
        return "glowProxy: " + self.oType

    def rotate(self, *args, **kwargs): # We may need to intercept certain functions and assignements to do js/py vec conversions
        """
        Rotate the object.
        """
        kwargs = translate_kwargs_vecs(kwargs=kwargs, vecAttrs=['axis','origin'])
        self.jsObj.rotate(*args, **kwargs)
        return self

    def append(self, *args, **kwargs):
        """
        Append to the object.
        """
        kwargs = translate_kwargs_vecs(kwargs=kwargs, vecAttrs=['origin'])
        self.jsObj.append(*args, **kwargs)
        return self
    
    def clone(self, *args, **kwargs):
        cjs = self.jsObj.clone(*args, **kwargs)
        for attr in glowProxy.GP_defaults:
            kwAdd = {}
            if attr in self.__dict__:
                kwAdd[attr] = self.__dict__[attr]

        return glowProxy(*args, jsObj=cjs, **{**kwargs, **kwAdd})

def sphere(*args, **kwargs):
    return glowProxy(vecAttrs=['pos','color','size','trail_color'], oType='sphere', factory=js_sphere, *args, **kwargs)

def box(*args, **kwargs):
    return glowProxy(vecAttrs=['pos','color','size','axis'], oType='box', factory=js_box, *args, **kwargs)

def cylinder(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'axis', 'color','size'], oType='cylinder', factory=js_cylinder, *args, **kwargs)

def arrow(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'axis', 'color'], oType='arrow', factory=js_arrow, *args, **kwargs)

def cone(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'axis', 'color','size'], oType='cone', factory=js_cone, *args, **kwargs)

def helix(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'axis', 'color'], oType='helix', factory=js_helix, *args, **kwargs)

def label(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'color'], oType='label', factory=js_label, *args, **kwargs)

def ellipsoid(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'color', 'axis', 'size'], oType='ellipsoid', factory=js_ellipsoid, *args, **kwargs)

def pyramid(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'color', 'axis', 'size'], oType='pyramid', factory=js_pyramid, *args, **kwargs)

def ring(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'color', 'axis', 'size'], oType='ring', factory=js_ring, *args, **kwargs)

async def text(*args, **kwargs):
    if (not hasattr(js_window,'.__font_sans')):
        js_fontloading()
    await js_waitforfonts()
    return glowProxy(vecAttrs=['pos', 'color', 'axis'], oType='text', factory=js_text, *args, **kwargs)

def button(*args, **kwargs):
    return glowProxy(funcAttrs=['bind'], oType='button', factory=js_button, *args, **kwargs)

def slider(*args, **kwargs):
    return glowProxy(funcAttrs=['bind'], oType='slider', factory=js_slider, *args, **kwargs)

def radio(*args, **kwargs):
    return glowProxy(funcAttrs=['bind'], oType='radio', factory=js_radio, *args, **kwargs)

def checkbox(*args, **kwargs):
    return glowProxy(funcAttrs=['bind'], oType='checkbox', factory=js_checkbox, *args, **kwargs)

def menu(*args, **kwargs):
    return glowProxy(funcAttrs=['bind'], listAttrs=['choices'], oType='menu', factory=js_menu, *args, **kwargs)

def wtext(*args, **kwargs):
    return glowProxy(oType='wtext', factory=js_wtext, *args, **kwargs)

def distant_light(*args, **kwargs):
    return glowProxy(vecAttrs=['color','direction'], oType='distant_light', factory=js_distant_light, *args, **kwargs)

def local_light(*args, **kwargs):
    return glowProxy(vecAttrs=['color','pos'], oType='local_light', factory=js_local_light, *args, **kwargs)

def vertex(*args, **kwargs):
    return glowProxy(vecAttrs=['pos','color'], oType='vertex', factory=js_vertex, *args, **kwargs)

def extrusion(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'axis', 'color','up', 'start_face_color','end_face_color'], nestAttrs=['shape','path'], oType='extrusion', factory=js_extrusion, *args, **kwargs)

class triangleProxy(glowProxy):
    def __init__(self, *args, **kwargs):
        if ('v0' in kwargs) and ('v1' in kwargs) and ('v2' in kwargs):
            vDict = {**kwargs, 'v0':kwargs['v0'].jsObj, 'v1':kwargs['v1'].jsObj, 'v2':kwargs['v2'].jsObj}
        elif 'vs' in kwargs:
            vertices = to_js(list(map(lambda v: v.jsObj, kwargs['vs'])))
            if len(vertices) != 3:
                raise Exception("triangleProxy: must have exactly 3 vertices")
            vDict = {**kwargs, 'vs':vertices}
        else:
            raise Exception("triangleProxy: must specify v0, v1, v2 or vs")
        jsObj = js_triangle(**vDict)
        super().__init__(oType='triangle', jsObj=jsObj)

def triangle(*args, **kwargs):
    return triangleProxy(*args, **kwargs)

class quadProxy(glowProxy):
    def __init__(self, *args, **kwargs):
        if ('v0' in kwargs) and ('v1' in kwargs) and ('v2' in kwargs) and ('v3' in kwargs):
            vDict = {**kwargs,
                'v0':kwargs['v0'].jsObj, 
                'v1':kwargs['v1'].jsObj,
                'v2':kwargs['v2'].jsObj,
                'v3':kwargs['v3'].jsObj}
        elif 'vs' in kwargs:
            vertices = to_js(list(map(lambda v: v.jsObj, kwargs['vs'])))
            del kwargs['vs']
            if len(vertices) != 4:
                raise Exception("quadProxy: must have exactly 4 vertices")
            vDict = {**kwargs, 'vs':vertices}
        else:
            raise Exception("triangleProxy: must specify v0, v1, v2, v3 or vs")
        jsObj = js_quad(**vDict)
        super().__init__(oType='triangle', jsObj=jsObj)

def quad(*args, **kwargs):
    return quadProxy(*args, **kwargs)

class sceneProxy(glowProxy):
    """
    A proxy for a glowscript scene.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(vecAttrs = ['forward', 'center', 'background'], listAttrs=['lights'], oType='scene', jsObj = js_scene)

    def bind(self, action, py_func):
        self.jsObj.bind(action, create_proxy(py_func))

def curveDictToJS(d):
    """
    Convert a curve dict with python vectors to js vectors.
    """
    if 'pos' in d:
        d['pos'] = py2js_vec(d['pos'])
    if 'color' in d:
        d['color'] = py2js_vec(d['color'])
    return d

class curveProxy(glowProxy):
    """
    curves are a bit special because there are so many ways to call the constructor.
    """
    def __init__(self, *args, factory = js_curve, oType = 'curve', **kwargs):
        if not factory:
            factory = js_curve
        std_list, std_kwargs = getStdForm(*args, **kwargs)
        if (len(std_list)) > 0:
            std_list_js = to_js(list(map(lambda d: curveDictToJS(d), std_list)), dict_converter=Object.fromEntries)
            super().__init__(oType='curve', factory = factory, vecAttrs=['color'], **std_kwargs) # doesn't like args + kwargs at the same time?
            self.jsObj.append(std_list_js)
        else:
            super().__init__(oType='curve', factory = factory, vecAttrs=['color'], **std_kwargs)

    def append(self, *args, **kwargs):
        std_list,std_kwargs = getStdForm(*args, **kwargs)
        if (len(std_list)) > 0:
            std_list_js = to_js(list(map(lambda d: curveDictToJS(d), std_list)), dict_converter=Object.fromEntries)
            self.jsObj.append(std_list_js)
        else:
            self.jsObj.append(**std_kwargs)

def curve(*args, **kwargs):
    return curveProxy(*args, **kwargs)

def points(*args, **kwargs):
    return curveProxy(*args, oType='points', factory=js_points, **kwargs)

scene = sceneProxy()

def canvas(*args, **kwargs):
    return glowProxy(vecAttrs = ['forward', 'center', 'background'], listAttrs=['lights'], oType='canvas', factory=js_canvas, *args, **kwargs)

def compound(*args, **kwargs):
    if len(args) != 1:
        raise Exception("compound: must have exactly 1 unnamed argument")
    if not isinstance(args[0],list) or isinstance(args[0],tuple):
        raise Exception("compound: must be passed a list or tuple of objects")
    newArgs = to_js(list(map(lambda o: o.jsObj, args[0])))
    return glowProxy(vecAttrs=['pos','axis'], *(newArgs,) , oType='compound', factory=js_compound, **kwargs)

def attach_light(*args, **kwargs):
    if (len(args) != 1):
        raise Exception("attach_light: must have exactly 1 unnamed argument")
    elif (not isinstance(args[0], glowProxy)):
        raise Exception("attach_light: must have a glowProxy as the unnamed argument")
    return glowProxy(vecAttrs=['offset','color'], oType='attach_light', factory=js_attach_light, *(args[0].jsObj,), **kwargs)