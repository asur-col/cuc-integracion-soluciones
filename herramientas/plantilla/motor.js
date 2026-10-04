(function(){
  var S=[].slice.call(document.querySelectorAll('.slide'));
  var N=S.length, i=0;
  var NARR=JSON.parse(document.getElementById('narracion').textContent);
  var q=new URLSearchParams(location.search);
  if(q.has('captura')) document.body.classList.add('captura');

  // Auto-ajuste: si el dibujo se sale del viewBox, se amplía el viewBox (nunca se recorta).
  function autoajustar(){
    S.forEach(function(s){
      var prev=s.style.display; s.style.display='block';
      s.querySelectorAll('.s-body svg[viewBox]').forEach(function(sv){
        if(sv.closest('symbol')) return;
        var vb=sv.viewBox.baseVal, bb; try{bb=sv.getBBox();}catch(e){return;}
        if(!bb||bb.width===0) return;
        var x0=Math.min(vb.x,bb.x-6), y0=Math.min(vb.y,bb.y-6);
        var x1=Math.max(vb.x+vb.width,bb.x+bb.width+6), y1=Math.max(vb.y+vb.height,bb.y+bb.height+6);
        if(x0<vb.x-1||y0<vb.y-1||x1>vb.x+vb.width+1||y1>vb.y+vb.height+1){
          sv.setAttribute('data-autoajuste',[vb.x,vb.y,vb.width,vb.height].join(' '));
          sv.setAttribute('viewBox',[x0,y0,x1-x0,y1-y0].map(function(v){return Math.round(v)}).join(' '));
        }
      });
      s.style.display=prev;
    });
  }

  function escalar(){
    var st=document.getElementById('stage');
    if(window.matchMedia('print').matches){st.style.transform='none';return;}
    var k=Math.min(window.innerWidth/1280,window.innerHeight/720);
    st.style.transform='scale('+k+')';
  }
  function mostrar(n){
    i=Math.max(0,Math.min(N-1,n));
    S.forEach(function(s,j){s.classList.toggle('active',j===i);});
    document.getElementById('progreso').style.width=((i+1)/N*100)+'%';
    document.getElementById('cont').textContent=(i+1)+' / '+N;
    var d=NARR[i]||{};
    document.getElementById('panel-narr').innerHTML='<b>Narración · diapositiva '+(i+1)+' · Parte '+(d.parte||'-')+'</b><br>'+(d.texto||'(sin narración)');
    if(!q.has('captura')) history.replaceState(null,'','#'+(i+1));
  }
  window.CURSO={irA:mostrar,total:N,narracion:NARR,actual:function(){return i;}};
  document.addEventListener('keydown',function(e){
    if(['ArrowRight','PageDown',' '].indexOf(e.key)>=0){mostrar(i+1);e.preventDefault();}
    else if(['ArrowLeft','PageUp'].indexOf(e.key)>=0){mostrar(i-1);e.preventDefault();}
    else if(e.key==='Home') mostrar(0);
    else if(e.key==='End') mostrar(N-1);
    else if(e.key==='n'||e.key==='N') document.body.classList.toggle('ver-narr');
  });
  document.getElementById('b-ant').onclick=function(){mostrar(i-1);};
  document.getElementById('b-sig').onclick=function(){mostrar(i+1);};
  window.addEventListener('resize',escalar);
  var ini=parseInt((location.hash||'#1').slice(1),10)||1;
  function arrancar(){autoajustar();escalar();mostrar(ini-1);document.body.setAttribute('data-listo','1');}
  if(document.fonts&&document.fonts.ready){document.fonts.ready.then(arrancar);}else{arrancar();}
})();
