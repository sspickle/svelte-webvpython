import{S as I,i as R,s as j,e as w,t as P,k as g,c as y,a as _,h as S,d as r,m as E,b as m,g as d,J as b,E as k,v as z,L as C}from"../chunks/index-26a557cf.js";import{w as D,b as L}from"../chunks/paths-e19757bb.js";import{s as M}from"../chunks/codeSrc-adb860ce.js";const v=D(""),T=async n=>{console.log("loading prep");const a=fetch("vpython.zip").then(o=>o.arrayBuffer());let c=await loadPyodide({indexURL:"https://cdn.jsdelivr.net/pyodide/dev/full/",stdout:n||null,stderr:n||null});const p=await a;return console.log("Unpacking package"),c.unpackArchive(p,"zip"),console.log("Importing vpython package"),c},U=async()=>{let n,a;return window.__context={glowscript_container:$("#glowscript").removeAttr("id")},n=window.canvas,a=n(),a};function V(n){let a,c,p,o,f,i,l,h,u,e;return{c(){a=w("a"),c=P("Edit this code"),p=g(),o=w("h2"),f=P("Running...."),i=g(),l=w("div"),h=g(),u=w("div"),e=w("textarea"),this.h()},l(t){a=y(t,"A",{href:!0,target:!0});var s=_(a);c=S(s,"Edit this code"),s.forEach(r),p=E(t),o=y(t,"H2",{});var x=_(o);f=S(x,"Running...."),x.forEach(r),i=E(t),l=y(t,"DIV",{id:!0,class:!0}),_(l).forEach(r),h=E(t),u=y(t,"DIV",{});var A=_(u);e=y(A,"TEXTAREA",{rows:!0,cols:!0}),_(e).forEach(r),A.forEach(r),this.h()},h(){m(a,"href",L+"/"),m(a,"target","_self"),m(l,"id","glowscript"),m(l,"class","glowscript"),m(e,"rows","10"),m(e,"cols","80")},m(t,s){d(t,a,s),b(a,c),d(t,p,s),d(t,o,s),b(o,f),d(t,i,s),d(t,l,s),d(t,h,s),d(t,u,s),b(u,e),n[1](e)},p:k,i:k,o:k,d(t){t&&r(a),t&&r(p),t&&r(o),t&&r(i),t&&r(l),t&&r(h),t&&r(u),n[1](null)}}}function q(n,a,c){function p(e){v.update(t=>t+=e+`
`)}z(async()=>{l=await U(),o=await T(p),window.scene=l,v.set(""),h()});let o=null,f,i,l;M.subscribe(e=>{f=e,console.log("src loaded")}),v.subscribe(e=>{console.log("stdout:",e),i&&c(0,i.value=e,i)});async function h(){try{if(o){let t=f.split("rate(").join("await async_rate(");await o.loadPackagesFromImports(t);var e=await o.runPythonAsync(t);v.update(s=>s+=e)}}catch(t){console.log("Error:"+t),v.update(s=>s+="Error:"+t+`
`)}}function u(e){C[e?"unshift":"push"](()=>{i=e,c(0,i)})}return[i,u]}class H extends I{constructor(a){super(),R(this,a,q,V,j,{})}}export{H as default};
