import{w as r}from"./paths-e19757bb.js";let e=`
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
`;const s=r(e);export{s};
