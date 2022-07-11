from js import sphere as js_sphere, box as js_box, color, vec as js_vec, rate as async_rate
from js import cylinder as js_cylinder, arrow as js_arrow, cone as js_cone, helix as js_helix
from js import label as js_label, scene as js_scene, text as js_text, ellipsoid as js_ellipsoid
from js import pyramid as js_pyramid, ring as js_ring, text as js_text
from js import button as js_button, distant_light as js_distant_light, local_light as js_local_light
from js import slider as js_slider, wtext as js_wtext, radio as js_radio, checkbox as js_checkbox
from js import menu as js_menu, curve as js_curve

from pyodide.ffi import create_proxy, to_js

from .vector import vector
py_vec = vector

def py2js_vec(v):
    return js_vec(v.x, v.y, v.z)

def js2py_vec(v, jsObj=None):
    return py_vec(v.x, v.y, v.z, jsObj=jsObj)

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

    GP_defaults = {'vecAttrs':[], 'oType':None, 'jsObj':None, 'listAttrs':[], 'funcAttrs':[]}
    GP_keys = list(GP_defaults.keys())

    def __init__(self, factory=None, jsObj=None, *args, **kwargs):
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

def sphere(*args, **kwargs):
    return glowProxy(vecAttrs=['pos','color'], oType='sphere', factory=js_sphere, *args, **kwargs)

def box(*args, **kwargs):
    return glowProxy(vecAttrs=['pos','color','size'], oType='box', factory=js_box, *args, **kwargs)

def cylinder(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'axis', 'color'], oType='cylinder', factory=js_cylinder, *args, **kwargs)

def arrow(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'axis', 'color'], oType='arrow', factory=js_arrow, *args, **kwargs)

def cone(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'axis', 'color'], oType='cone', factory=js_cone, *args, **kwargs)

def helix(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'axis', 'color'], oType='helix', factory=js_helix, *args, **kwargs)

def label(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'color'], oType='label', factory=js_label, *args, **kwargs)

def ellipsoid(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'color', 'axis', 'size'], oType='ellipsoid', factory=js_ellipsoid, *args, **kwargs)

def pyramid(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'color', 'axis', 'size'], oType='pyramid', factory=js_pyramid, *args, **kwargs)

def ring(*args, **kwargs):
    return glowProxy(vecAttrs=['pos', 'color', 'axis'], oType='ring', factory=js_ring, *args, **kwargs)

def text(*args, **kwargs):
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

class sceneProxy(glowProxy):
    """
    A proxy for a glowscript scene.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(vecAttrs = ['forward', 'center', 'background'], listAttrs=['lights'], oType='scene', jsObj = js_scene)

    def bind(self, action, py_func):
        self.jsObj.bind(action, create_proxy(py_func))

class curveMethods(object):

    def process_args(self, *args1, **args):
        c = None
        r = None
        vis = None
        if 'color' in args:
            c = args['color']
        if 'radius' in args:
            r = args['radius']
        if 'visible' in args:
            vis = args['visible']
        if len(args1) > 0:
            if len(args1) == 1:
                tpos = self.parse_pos(args1[0])
            else:  ## avoid nested tuples
                tlist = list(args1)
                tpos = self.parse_pos(tlist)
        elif 'pos' in args:
            pos = args['pos']
            tpos = self.parse_pos(pos)  ## resolve pos arguments into a list
        if len(tpos) == 0:
            raise AttributeError("To add a point to a curve or points object, specify pos information.")
        pts = []
        for pt in tpos:
            col = c
            rad = r
            vi = vis
            if 'pos' in pt:
                pt['pos'] = js_vec(pt['pos'])
            if 'color' in pt:
                col = js_vec(pt['color'])
            if 'radius' in pt:
                rad = pt['radius']
            if 'visible' in pt:
                vi = pt['visible']
            if col is not None:
                pt['color'] = js_vec(col)
            if rad is not None:
                pt['radius'] = rad
            if vi is not None:
                pt['visible'] = vi
            pts.append(pt)
        return pts

    def parse_pos(self, *vars): # return a list of dictionaries of the form {pos:vec, color:vec ....}
        # In constructor can have pos=[vec, vec, .....]; no dictionaries
        ret = []
        if isinstance(vars, tuple) and len(vars) > 1 :
            vars = vars[0]
        if isinstance(vars, tuple) and isinstance(vars[0], list):
            vars = vars[0]

        for v in vars:
            if isinstance(v, vector) or isinstance(v, list) or isinstance(v, tuple):
                if not isinstance(v, vector): # legal in GlowScript: pos=[(x,y,z), (x,y,z)] and pos=[[x,y,z], [x,y,z]]
                    v = vector(v[0],v[1],v[2])
                if not self._constructing:
                    ret.append({'pos':vector(v)}) # make a copy of the vector; it could be (and often is, e.g. in a trail) object.pos
                else:
                    ret.append(vector(v))
            elif isinstance(v, dict) and not self._constructing:
                ret.append(v)
            else:
                if not self._constructing:
                    raise AttributeError("Point information must be a vector or a dictionary")
                else:
                    raise AttributeError("Point pos must be a vector")
        return ret

    def append(self, *args1, **args):
        pts, cps = self.process_args(*args1, **args)
        self.jsObj.append(cps[:])

class curveProxy(glowProxy, curveMethods):
    def __init__(self, *args, **kwargs):
        self.__dict__['_constructing'] = False
        pts = self.process_args(*args, **kwargs)
        pts = to_js(({'pos':js_vec(1,1,1)},{'pos':js_vec(2,2,2)}))
        jsObj = js_curve(pts)

    def append(self, *args, **kwargs):
        self.jsObj.append(*args, **kwargs)
        return self

def curve(*args, **kwargs):
    return curveProxy(factory=js_curve, *args, **kwargs)

scene = sceneProxy()

