import{w as t}from"./paths-58176f9b.js";let s=`
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
`;const a="code",o=localStorage.getItem(a),i=t(o||s);i.subscribe(e=>{localStorage.setItem(a,e)});let c={add_default_imports:!0,last_doc_id:""};const l="prefs";let r=null;{let e=localStorage.getItem(l);e&&(r=JSON.parse(e))}const p=t(r||c);p.subscribe(e=>{e&&localStorage.setItem(l,JSON.stringify(e))});export{p,i as s};
