import{_ as G}from"../chunks/preload-helper-60cab3ee.js";import{S as J,i as K,s as N,e as u,t as X,k as W,c as d,a as f,h as H,d as h,m as T,b as a,K as V,g as Q,J as s,L as Y,n as D,w as Z,M}from"../chunks/index-19bb5ac6.js";function tt(){return new Worker("/_app/immutable/assets/editor.worker.6369e042.js",{type:"module"})}function et(){return new Worker("/_app/immutable/assets/json.worker.cc26763b.js",{type:"module"})}function rt(){return new Worker("/_app/immutable/assets/css.worker.57c3cb89.js",{type:"module"})}function st(){return new Worker("/_app/immutable/assets/html.worker.ae09e20d.js",{type:"module"})}function nt(){return new Worker("/_app/immutable/assets/ts.worker.bcb033c8.js",{type:"module"})}const ot=async i=>{console.log("loading prep");let t;const n=fetch("vpython.zip").then(v=>v.arrayBuffer());let c=await loadPyodide({indexURL:"https://cdn.jsdelivr.net/pyodide/dev/full/",stdout:i||null,stderr:i||null});const m=await n;return console.log("Unpacking package"),c.unpackArchive(m,"zip"),console.log("Importing vpython package"),window.__context={glowscript_container:$("#glowscript").removeAttr("id")},t=window.canvas,t(),c};function at(i){let t,n,c,m,v,o,r,w,p,I,x,y,q,C,g,e,l,k,P,E,b,A,S;return{c(){t=u("div"),n=u("div"),c=u("button"),m=X("Run"),v=W(),o=u("div"),r=u("meta"),w=W(),p=u("script"),x=W(),y=u("script"),C=W(),g=u("script"),l=W(),k=u("div"),P=W(),E=u("div"),b=u("textarea"),this.h()},l(R){t=d(R,"DIV",{class:!0});var _=f(t);n=d(_,"DIV",{class:!0});var z=f(n);c=d(z,"BUTTON",{});var B=f(c);m=H(B,"Run"),B.forEach(h),z.forEach(h),v=T(_),o=d(_,"DIV",{id:!0,class:!0});var j=f(o);r=d(j,"META",{"http-equiv":!0,content:!0}),w=T(j),p=d(j,"SCRIPT",{type:!0,src:!0});var U=f(p);U.forEach(h),x=T(j),y=d(j,"SCRIPT",{type:!0,src:!0});var O=f(y);O.forEach(h),C=T(j),g=d(j,"SCRIPT",{type:!0,src:!0});var F=f(g);F.forEach(h),j.forEach(h),l=T(_),k=d(_,"DIV",{class:!0}),f(k).forEach(h),P=T(_),E=d(_,"DIV",{class:!0});var L=f(E);b=d(L,"TEXTAREA",{rows:!0,cols:!0}),f(b).forEach(h),L.forEach(h),_.forEach(h),this.h()},h(){c.disabled=!0,a(n,"class","buttonCol svelte-1hh0l62"),a(r,"http-equiv","Content-Type"),a(r,"content","text/html; charset=utf-8"),a(p,"type","text/javascript"),V(p.src,I="https://www.glowscript.org/lib/jquery/2.1/jquery.min.js")||a(p,"src",I),a(y,"type","text/javascript"),V(y.src,q="https://www.glowscript.org/lib/jquery/2.1/jquery-ui.custom.min.js")||a(y,"src",q),a(g,"type","text/javascript"),V(g.src,e="https://www.glowscript.org/package/glow.3.2.min.js")||a(g,"src",e),a(o,"id","glowscript"),a(o,"class","glowscript glowCol svelte-1hh0l62"),a(k,"class","editCol svelte-1hh0l62"),a(b,"rows","20"),a(b,"cols","80"),a(E,"class","stdoutRow svelte-1hh0l62"),a(t,"class","container svelte-1hh0l62")},m(R,_){Q(R,t,_),s(t,n),s(n,c),s(c,m),i[4](c),s(t,v),s(t,o),s(o,r),s(o,w),s(o,p),s(o,x),s(o,y),s(o,C),s(o,g),s(t,l),s(t,k),i[6](k),s(t,P),s(t,E),s(E,b),i[7](b),A||(S=Y(c,"click",i[5]),A=!0)},p:D,i:D,o:D,d(R){R&&h(t),i[4](null),i[6](null),i[7](null),A=!1,S()}}}function it(i,t,n){let c=`
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
`,m=null,v,o,r=null,w,p;Z(async()=>(self.MonacoEnvironment={getWorker(e,l){return l==="json"?new et:l==="css"||l==="scss"||l==="less"?new rt:l==="html"||l==="handlebars"||l==="razor"?new st:l==="typescript"||l==="javascript"?new nt:new tt}},o=await G(()=>import("../chunks/editor.main-7ea83a81.js").then(function(e){return e.e}),["chunks/editor.main-7ea83a81.js","assets/editor.main-fb5c4d06.css","chunks/preload-helper-60cab3ee.js"]),v=o.editor.create(m,{value:c,language:"python"}),p=await ot(x),r&&n(1,r.disabled=!1,r),()=>{v.dispose()}));async function I(){r&&(n(1,r.disabled=!0,r),n(1,r.innerText="Running...",r));var e=v.getValue().split("rate(").join("await async_rate(");try{await p.loadPackagesFromImports(e);var l=await p.runPythonAsync(e)}catch(k){console.log("Error:"+k)}}function x(e){n(2,w.value+=e+`
`,w)}function y(e){M[e?"unshift":"push"](()=>{r=e,n(1,r)})}const q=()=>{I()};function C(e){M[e?"unshift":"push"](()=>{m=e,n(0,m)})}function g(e){M[e?"unshift":"push"](()=>{w=e,n(2,w)})}return[m,r,w,I,y,q,C,g]}class pt extends J{constructor(t){super(),K(this,t,it,at,N,{})}}export{pt as default};
