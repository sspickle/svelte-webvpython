import{S as P,i as I,s as T,e as g,t as A,k as E,c as _,a as y,h as S,d as i,m as b,b as m,g as f,J as k,E as x,v as O,L as z}from"../chunks/index-26a557cf.js";import{w as C,b as D}from"../chunks/paths-e19757bb.js";import{s as H}from"../chunks/codeSrc-adb860ce.js";const v=C(""),J=async o=>{console.log("loading prep");const a=fetch("vpython.zip").then(r=>r.arrayBuffer());let n=await loadPyodide({indexURL:"https://cdn.jsdelivr.net/pyodide/dev/full/",stdout:o||null,stderr:o||null});const p=await a;return console.log("Unpacking package"),n.unpackArchive(p,"zip"),console.log("Importing vpython package"),n},L=async()=>{let o,a;return window.__context={glowscript_container:$("#glowscript").removeAttr("id")},o=window.canvas,a=o(),a};function M(o){let a,n,p,r,w,s,l,u,d,c;return{c(){a=g("a"),n=A("Edit this code"),p=E(),r=g("h2"),w=A("Running...."),s=E(),l=g("div"),u=E(),d=g("div"),c=g("textarea"),this.h()},l(t){a=_(t,"A",{href:!0,target:!0});var e=y(a);n=S(e,"Edit this code"),e.forEach(i),p=b(t),r=_(t,"H2",{});var h=y(r);w=S(h,"Running...."),h.forEach(i),s=b(t),l=_(t,"DIV",{id:!0,class:!0}),y(l).forEach(i),u=b(t),d=_(t,"DIV",{});var R=y(d);c=_(R,"TEXTAREA",{rows:!0,cols:!0}),y(c).forEach(i),R.forEach(i),this.h()},h(){m(a,"href",D+"/"),m(a,"target","_self"),m(l,"id","glowscript"),m(l,"class","glowscript"),m(c,"rows","10"),m(c,"cols","80"),c.hidden=!0},m(t,e){f(t,a,e),k(a,n),f(t,p,e),f(t,r,e),k(r,w),f(t,s,e),f(t,l,e),f(t,u,e),f(t,d,e),k(d,c),o[1](c)},p:x,i:x,o:x,d(t){t&&i(a),t&&i(p),t&&i(r),t&&i(s),t&&i(l),t&&i(u),t&&i(d),o[1](null)}}}function U(o,a,n){function p(t){u&&v.update(e=>e+=t+`
`)}let r=null,w,s,l,u=!1;O(async()=>(l=await L(),r=await J(p),window.scene=l,window.__reportScriptError=t=>{p("REPORT ERROR:"+JSON.stringify(t))},v.set(""),u=!0,d(),()=>{u=!1})),H.subscribe(t=>{w=t}),v.subscribe(t=>{s&&(t.length>0&&(console.log("in stdout update:",t),s.removeAttribute("hidden")),n(0,s.value=t,s),n(0,s.scrollTop=s.scrollHeight,s))});async function d(){try{if(r){let e=w.replace(/[^\.\w]rate[\ ]*\(/g," await rate(");e=e.replace(/[^\.\w]text[\ ]*\(/g," await text("),await r.loadPackagesFromImports(e);var t=await r.runPythonAsync(e);t&&v.update(h=>h+=t)}}catch(e){console.log("Error:"+e),v.update(h=>h+="Error:"+e+`
`)}}function c(t){z[t?"unshift":"push"](()=>{s=t,n(0,s)})}return[s,c]}class B extends P{constructor(a){super(),I(this,a,U,M,T,{})}}export{B as default};