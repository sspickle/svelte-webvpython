import{w as t}from"./paths-e19757bb.js";let s=`
from vpython import *
import numpy as np

import sys
print(sys.version)

r = 2 + 3j
s = sphere(pos=vec(r.real,r.imag,0), color=color.blue, make_trail=True)
print("hello" + f"{abs(3 + 4j)}")

while True:
   rate(30)
   r = r*np.exp(1j*0.05)
   s.pos = vec(r.real, r.imag, 0)
`;const e="code",r=localStorage.getItem(e),a=t(r||s);a.subscribe(o=>{localStorage.setItem(e,o)});export{a as s};
