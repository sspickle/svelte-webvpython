from js import vec as js_vec
from .vector import *
#from cyvector import *

# List of names imported from this module with import *
__all__ = ['vector_js']

class vector_js(vector):
    'python vector class with internal jsObj tracking'

    def __init__(self, *args, jsObj = None):
        super().__init__(*args)

        if jsObj:
            self.jsObj = jsObj
        else:
            self.jsObj = js_vec(self._x, self._y, self._z)

        self.on_change = self.cpJsObj

    def cpJsObj(self):
        self.jsObj.x = self._x
        self.jsObj.y = self._y
        self.jsObj.z = self._z

