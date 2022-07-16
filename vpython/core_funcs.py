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
from js import graph as js_graph, gcurve as js_gcurve, gvbars as js_gvbars, gdots as js_gdots

from pyodide.ffi import create_proxy, to_js

from .curveArgs import getStdForm
from .vec_js import vector_js as vector

from .vec_conversion import js2py_vec, py2js_vec
from .shapes_piodide import convertPyVecsToJSList

class GSRegistry(object):
    """
    Manage a registry of objects so we can look up the python object
    from the corresponding javascript object.
    """
    def __init__(self):
        self.counter = 0
        self.registry = {}

    def register(self, obj):
        result = self.counter
        self.registry[self.counter] = obj
        self.counter += 1
        return result

    def get(self, index):
        result = self.registry.get(index,None)
        if result is None:
            raise Exception("GSRegistry: object with index %d not found" % index)
        return result

gsRegistry = GSRegistry()
gsRegKey = '__gsIndex__'

def js_debug(*args, convert=True):
    if convert:
        args = to_js(args)
    js_window.__reportScriptError(args)

def translate_kwargs_rest(kwargs, notAttrs):
    # Handle everything else
    for attr in kwargs:
        if attr not in notAttrs:
            kwargs[attr] = to_js(kwargs[attr], dict_converter=Object.fromEntries)

    return kwargs

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

        kwargs = self.translate_all_kwargs(kwargs)

        for attr in glowProxy.GP_keys:
            if attr in kwargs:
                del kwargs[attr] # don't pass these to js

        if factory is None:
            self.jsObj = jsObj
            if (not hasattr(jsObj, gsRegKey)):
                setattr(jsObj, gsRegKey, gsRegistry.register(self))
        else:
            self.jsObj = factory(*args, **kwargs)
            setattr(self.jsObj, gsRegKey, gsRegistry.register(self))

    def translate_all_kwargs(self, kwargs):
        """
        Convert kwargs to save js objects.
        """
        kwargs = translate_kwargs_vecs(kwargs, self.vecAttrs)
        kwargs = translate_kwargs_lists(kwargs, self.listAttrs)
        kwargs = translate_kwargs_funcs(kwargs, self.funcAttrs)
        kwargs = translate_kwargs_nest(kwargs, self.nestAttrs)
        kwargs = translate_kwargs_rest(kwargs, self.vecAttrs + self.listAttrs + self.funcAttrs + self.nestAttrs)
        return kwargs

    def __setattr__(self, name, value):
        if name in glowProxy.GP_keys:
            self.__dict__[name] =  value
        elif name in self.vecAttrs:
            setattr(self.jsObj, name, py2js_vec(value))
        elif name in self.listAttrs:
            setattr(self.jsObj, name, to_js(value))
        else:
            setattr(self.jsObj, name, to_js(value, dict_converter=Object.fromEntries))
    
    def __getattr__(self, name):
        if name in glowProxy.GP_keys:
            return self.__dict__.get(name, 
                glowProxy.GP_defaults.get(name, None))
        elif name in self.vecAttrs:
            return js2py_vec(getattr(self.jsObj, name), jsObj=getattr(self.jsObj,name)) # keep jsObj embedded in pyObj
        else:
            result = getattr(self.jsObj, name)
            if hasattr(result,gsRegKey):
                return gsRegistry.get(getattr(result,gsRegKey))
            return result

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

    def modify(self, *args, **kwargs):
        """
        Modify the object.
        """
        kwargs = self.translate_all_kwargs(kwargs)
        self.jsObj.modify(*args, **kwargs)
        return self
    
    def clone(self, *args, **kwargs):
        if 'pos' in kwargs:
            kwargs['pos'] = py2js_vec(kwargs['pos'])
        cjs = self.jsObj.clone(*args, **kwargs)
        for attr in glowProxy.GP_defaults:
            kwAdd = {}
            if attr in self.__dict__:
                kwAdd[attr] = self.__dict__[attr]

        return glowProxy(*args, jsObj=cjs, **{**kwargs, **kwAdd})

class sphere(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos','color','size','trail_color'], oType='sphere', factory=js_sphere, *args, **kwargs)

class box(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos','color','size','axis'], oType='box', factory=js_box, *args, **kwargs)

class cylinder(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos', 'axis', 'color','size'], oType='cylinder', factory=js_cylinder, *args, **kwargs)

class arrow(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos', 'axis', 'color'], oType='arrow', factory=js_arrow, *args, **kwargs)

class cone(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos', 'axis', 'color','size'], oType='cone', factory=js_cone, *args, **kwargs)

class helix(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos', 'axis', 'color','size'], oType='helix', factory=js_helix, *args, **kwargs)

class label(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos', 'color'], oType='label', factory=js_label, *args, **kwargs)

class ellipsoid(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos', 'color', 'axis', 'size'], oType='ellipsoid', factory=js_ellipsoid, *args, **kwargs)

class pyramid(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos', 'color', 'axis', 'size'], oType='pyramid', factory=js_pyramid, *args, **kwargs)

class ring(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos', 'color', 'axis', 'size'], oType='ring', factory=js_ring, *args, **kwargs)

class text(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos', 'color', 'axis'], oType='text', factory=js_text, *args, **kwargs)

class button(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, funcAttrs=['bind'], oType='button', factory=js_button, *args, **kwargs)

class slider(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, funcAttrs=['bind'], oType='slider', factory=js_slider, *args, **kwargs)

class radio(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, funcAttrs=['bind'], oType='radio', factory=js_radio, *args, **kwargs)

class checkbox(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, funcAttrs=['bind'], oType='checkbox', factory=js_checkbox, *args, **kwargs)

class menu(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, funcAttrs=['bind'], listAttrs=['choices'], oType='menu', factory=js_menu, *args, **kwargs)

class wtext(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, oType='wtext', factory=js_wtext, *args, **kwargs)

class distant_light(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['color','direction'], oType='distant_light', factory=js_distant_light, *args, **kwargs)

class local_light(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['color','pos'], oType='local_light', factory=js_local_light, *args, **kwargs)

class vertex(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos','color','normal'], oType='vertex', factory=js_vertex, *args, **kwargs)

class extrusion(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, vecAttrs=['pos', 'axis', 'up', 'color', 'start_face_color','end_face_color'], nestAttrs=['shape','path'], oType='extrusion', factory=js_extrusion, *args, **kwargs)

class graph(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, oType='graph', factory=js_graph, *args, **kwargs)

class gcurve(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, oType='gcurve', vecAttrs=['color','marker_color'], factory=js_gcurve, *args, **kwargs)

class gvbars(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, oType='gvbars', vecAttrs=['color','marker_color'], factory=js_gvbars, *args, **kwargs)

class gdots(glowProxy):
    def __init__(self, *args, **kwargs):
        glowProxy.__init__(self, oType='gdots', vecAttrs=['color','marker_color'], factory=js_gdots, *args, **kwargs)

class triangle(glowProxy):
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
        super().__init__(oType='triangle', vecAttrs=['color','v0','v1','v2'], jsObj=jsObj)

class quad(glowProxy):
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
            raise Exception("quadProxy: must specify v0, v1, v2, v3 or vs")
        jsObj = js_quad(**vDict)
        glowProxy.__init__(self, oType='quad', vecAttrs=['color'], jsObj=jsObj)

class canvasProxy(glowProxy):
    """
    A proxy for a glowscript scene.
    """
    def __init__(self, *args, jsObj=None, factory=None, **kwargs):
        super().__init__(vecAttrs = ['forward', 'center', 'background', 'ambient','up'], listAttrs=['lights'], oType='canvas', jsObj = jsObj, factory=factory, **kwargs)

    def bind(self, action, py_func):
        self.jsObj.bind(action, create_proxy(py_func))

    @property
    def camera(self):
        return cameraProxy(jsObj=self.jsObj.camera)

    @property
    def mouse(self):
        return mouseProxy(jsObj=self.jsObj.mouse)

scene = canvasProxy(jsObj=js_scene)

class canvas(glowProxy):
    def __init__(self, *args, **kwargs):
        canvasProxy.__init__(self, factory=js_canvas, *args, **kwargs)

def curveDictToJS(d):
    """
    Convert a curve dict with python vectors to js vectors.
    """
    if 'pos' in d:
        d['pos'] = py2js_vec(d['pos'])
    if 'color' in d:
        d['color'] = py2js_vec(d['color'])
    return d

class curve(glowProxy):
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

    def point(self, n):
        pt = self.jsObj.point(n)
        return {'pos':pt.pos, 'color':pt.color, 'radius':pt.radius, 'visible':pt.visible}

def points(curveProxy):
    def __init__(self, *args, **kwargs):
        curveProxy.__init__(self, *args, oType='points', factory=js_points, **kwargs)

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

class cameraProxy(glowProxy):
    def __init__(self, *args, jsObj=None):
        if not jsObj:
            raise Exception("must specify a camera as a jsObj")
        super().__init__(vecAttrs=['pos','axis'], oType='camera', jsObj=jsObj)

class mouseProxy(glowProxy):
    def __init__(self, *args, jsObj=None):
        if not jsObj:
            raise Exception("must specify a mouse as a jsObj")
        super().__init__(vecAttrs=['pos'], oType='mouse', jsObj=jsObj)

    @property
    def pick(self):
        picked = self.jsObj.pick()
        if picked is None:
            return None

        index = getattr(picked,gsRegKey,None)
        if index is None:
            return picked # it's not in the registry? Just return the JS object
        
        pyObj = gsRegistry.get(index)
        return pyObj
