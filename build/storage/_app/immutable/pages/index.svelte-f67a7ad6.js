import{_ as I}from"../chunks/preload-helper-60cab3ee.js";import{S,i as M,s as x,e as h,t as W,k as A,c as k,a as v,h as y,d as p,m as R,b as c,g as f,J as b,K as V,E as g,L as j,v as q,M as z}from"../chunks/index-f57992c5.js";import{s as D,p as E}from"../chunks/prefs-79816110.js";import{b as C}from"../chunks/paths-3a77cd68.js";function P(){return new Worker("/_app/immutable/assets/editor.worker.6369e042.js",{type:"module"})}function L(){return new Worker("/_app/immutable/assets/json.worker.cc26763b.js",{type:"module"})}function O(){return new Worker("/_app/immutable/assets/css.worker.57c3cb89.js",{type:"module"})}function T(){return new Worker("/_app/immutable/assets/html.worker.ae09e20d.js",{type:"module"})}function U(){return new Worker("/_app/immutable/assets/ts.worker.bcb033c8.js",{type:"module"})}function J(u){let s,l,d,r,o,i,n,a,m,_;return{c(){s=h("a"),l=W("Run this program"),d=A(),r=h("input"),i=W(`
Apply Default Imports
`),n=h("div"),a=h("div"),this.h()},l(e){s=k(e,"A",{href:!0});var t=v(s);l=y(t,"Run this program"),t.forEach(p),d=R(e),r=k(e,"INPUT",{type:!0,name:!0}),i=y(e,`
Apply Default Imports
`),n=k(e,"DIV",{class:!0});var w=v(n);a=k(w,"DIV",{class:!0,id:!0}),v(a).forEach(p),w.forEach(p),this.h()},h(){c(s,"href",C+"/run"),c(r,"type","checkbox"),c(r,"name","default includes"),r.checked=o=u[1].add_default_imports,c(a,"class","editor svelte-z5d0oq"),c(a,"id","editor"),c(n,"class","remainder svelte-z5d0oq")},m(e,t){f(e,s,t),b(s,l),f(e,d,t),f(e,r,t),f(e,i,t),f(e,n,t),b(n,a),u[4](a),m||(_=V(r,"change",u[3]),m=!0)},p(e,[t]){t&2&&o!==(o=e[1].add_default_imports)&&(r.checked=o)},i:g,o:g,d(e){e&&p(s),e&&p(d),e&&p(r),e&&p(i),e&&p(n),u[4](null),m=!1,_()}}}function K(u,s,l){let d,r;j(u,D,e=>l(7,d=e)),j(u,E,e=>l(1,r=e));let o=null,i,n,a=()=>{let e=!r.add_default_imports;E.set({add_default_imports:e})};q(async()=>(self.MonacoEnvironment={getWorker(e,t){return t==="json"?new L:t==="css"||t==="scss"||t==="less"?new O:t==="html"||t==="handlebars"||t==="razor"?new T:t==="typescript"||t==="javascript"?new U:new P}},n=await I(()=>import("../chunks/editor.main-7ea83a81.js").then(function(e){return e.e}),["chunks/editor.main-7ea83a81.js","assets/editor.main-fb5c4d06.css","chunks/preload-helper-60cab3ee.js"]),i=n.editor.create(o,{value:d,language:"python",fixedOverflowWidgets:!0}),i.onDidChangeModelContent(()=>{D.set(i.getValue())}),()=>{i.dispose()}));const m=()=>{a()};function _(e){z[e?"unshift":"push"](()=>{o=e,l(0,o)})}return[o,r,a,m,_]}class H extends S{constructor(s){super(),M(this,s,K,J,x,{})}}export{H as default};
