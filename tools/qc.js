// QC tools for the tee viewer. build.py copies this to dist/qc.js; open the page with #qc to load it
// (e.g. http://localhost:8770/index.html#qc), then run from the browser console:
//
//   await QC.numbers()          every blank x size: length vs spec, pins on the fabric, layout fit
//   QC.sheet([...shots], cols, maxH)  contact sheet of renders (maxH = picture height, default 230); each shot:
//                               {label, blank, size, cw, finish, view|pos, zoom, ty, meas}
//   QC.sheet(QC.standard())     the standard visual pass for the current blank (views, inside neck, hem, sizes)
//   QC.back()                   restore the page (reload)
//
// Saved 2026-09-28 so QC passes don't get rebuilt by hand each time (token spend -> assets).
(function(){
  const wait=ms=>new Promise(r=>setTimeout(r,ms));
  const QC={};
  QC.numbers=async()=>{
    const r={layout:{docH:document.documentElement.scrollHeight,vh:innerHeight,
      controls:document.querySelector('.controls').scrollHeight+'/'+document.querySelector('.controls').clientHeight},bad:[]};
    const keep={blank:st.blank,size:st.size};
    for(const bk of Object.keys(BL.blanks)){
      setBlank(bk);await ensureModel(curModel());
      for(const z of blank().run){
        document.getElementById('size-'+z).click();
        const sz=sizeNow(),bb=new THREE.Box3().setFromObject(teeMesh),H=bb.max.y-bb.min.y;
        if(Math.abs(H-sz.length)>.05)r.bad.push(`${bk} ${z}: length ${H.toFixed(2)} vs spec ${sz.length}`);
        for(const v of ['front','back','q'])goView(v);
        const miss=HOT.filter(h=>!(h.el&&h.el.hidden)&&(!h.p||Math.abs(h.p[2])<.05)).map(h=>h.key);   // hidden pins (nothing to mark) don't count
        if(miss.length)r.bad.push(`${bk} ${z}: pins off the fabric: ${miss.join(', ')}`);
      }
    }
    setBlank(keep.blank);document.getElementById('size-'+keep.size)&&document.getElementById('size-'+keep.size).click();
    if(!r.bad.length)r.bad='OK: every blank and size, length exact, pins on the fabric';
    return r;
  };
  QC.shot=(o)=>{
    if(o.blank&&o.blank!==st.blank)setBlank(o.blank);
    if(o.size)st.size=o.size; if(o.cw)setCw(o.cw); if(o.finish)st.finish=o.finish;
    st.meas=!!o.meas;st.pins=false;applySize();paint();
    let p;
    if(o.pos)p=new THREE.Vector3(...o.pos);
    else{const v=VIEWS.find(x=>x.k===(o.view||'front'));p=new THREE.Vector3(...v.dir).normalize();p.multiplyScalar(camDist(p)*(o.zoom||.8));p.y+=o.ty||0;}
    camera.position.copy(p);controls.target.set(0,o.ty||0,0);camera.lookAt(0,o.ty||0,0);
    renderer.render(scene,camera);return renderer.domElement.toDataURL('image/png');
  };
  QC.sheet=(shots,cols,maxH)=>{
    const W=420,H=520;renderer.setPixelRatio(1);renderer.setSize(W,H,false);camera.aspect=W/H;camera.updateProjectionMatrix();
    const out=shots.map(o=>[o.label,QC.shot(o)]);
    document.documentElement.style.overflow='auto';
    document.body.innerHTML='<div style="display:grid;grid-template-columns:repeat('+(cols||4)+',1fr);gap:3px;background:#999;font:11px monospace">'+
      out.map(([l,u])=>`<div style="background:#fff"><img src="${u}" style="width:100%;display:block;max-height:${maxH||230}px;object-fit:contain"><div>${l}</div></div>`).join('')+'</div>';
    return out.length+' shots';
  };
  QC.standard=(bk)=>{
    bk=bk||st.blank;const run=BL.blanks[bk].run,lo=run[0],hi=run[run.length-1];
    return [
      {label:`${bk} M front, measurements`,blank:bk,size:'M',cw:'harbour',view:'front',meas:true},
      {label:`${bk} M back`,blank:bk,size:'M',cw:'harbour',view:'back'},
      {label:`${bk} M side`,blank:bk,size:'M',cw:'harbour',view:'left'},
      {label:`${bk} M 3/4`,blank:bk,size:'M',cw:'bush',view:'q'},
      {label:`${bk} M inside neck`,blank:bk,size:'M',cw:'jacaranda',pos:[0,52,-14],ty:11},
      {label:`${bk} M hem from below`,blank:bk,size:'M',cw:'classic',pos:[0,-40,26],ty:-10},
      {label:`${bk} ${lo} front`,blank:bk,size:lo,cw:'sandstone',view:'front',meas:true},
      {label:`${bk} ${hi} front`,blank:bk,size:hi,cw:'sandstone',view:'front',meas:true},
    ];
  };
  // tag heroes (3.1): every tag spot close up on a plain tee, plus front/back overviews. o = {blank, size, cw, dist}
  QC.tags=(o)=>{o=o||{};const W=420,H=520;renderer.setPixelRatio(1);renderer.setSize(W,H,false);camera.aspect=W/H;camera.updateProjectionMatrix();
    if(o.blank&&o.blank!==st.blank)setBlank(o.blank);if(o.size)st.size=o.size;setCw(o.cw||'classic');
    Object.assign(st,{noArt:true,pocket:true,meas:false,pins:false});TR.trims.forEach(t=>st.trims[t.key]=true);applySize();paint();
    const out=[];for(const v of ['front','back']){const d=new THREE.Vector3(...VIEWS.find(x=>x.k===v).dir).normalize();camera.position.copy(d.multiplyScalar(camDist(d)*.8));controls.target.set(0,0,0);camera.lookAt(0,0,0);renderer.render(scene,camera);out.push([v,renderer.domElement.toDataURL()]);}
    for(const t of TR.trims){const c=trimCam(t.key,o.dist);if(!c){out.push([t.key+' NOT PLACED','']);continue;}camera.position.copy(c.pos);controls.target.copy(c.target);camera.lookAt(c.target);renderer.render(scene,camera);out.push([t.key+' '+t.name,renderer.domElement.toDataURL()]);}
    document.documentElement.style.overflow='auto';
    document.body.innerHTML='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:3px;background:#999;font:11px monospace">'+out.map(([l,u])=>`<div style="background:#fff"><img src="${u}" style="width:100%;display:block;max-height:${o.maxH||240}px;object-fit:contain"><div>${l}</div></div>`).join('')+'</div>';
    return out.length+' shots';};
  QC.back=()=>location.reload();
  window.QC=QC;
})();
