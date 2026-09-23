<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Игра 20 сек</title>
<style>
body{margin:0;background:#111;color:white;font-family:Arial;display:flex;justify-content:center;align-items:center;height:100vh}
#box{width:380px;height:600px;background:#222;border:2px solid white;border-radius:10px;position:relative;overflow:hidden}
#top{display:flex;justify-content:space-between;padding:10px;font-size:20px;background:black}
#field{width:100%;height:540px;position:relative;background:#1a1a2e;overflow:hidden}
.target{position:absolute;width:40px;height:40px;background:red;border-radius:50%;display:flex;justify-content:center;align-items:center;cursor:pointer;font-weight:bold}
.bullet{position:absolute;width:6px;height:15px;background:yellow;left:50%}
#gun{position:absolute;bottom:5px;left:50%;transform:translateX(-50%);font-size:35px}
#start{position:absolute;inset:0;background:rgba(0,0,0,0.9);display:flex;flex-direction:column;justify-content:center;align-items:center;z-index:10}
#play{padding:15px 40px;font-size:30px;background:lime;border:none;border-radius:20px;cursor:pointer}
</style>
</head>
<body>
<div id="box">
<div id="top"><span>Время:<span id="tm">20</span></span><span>Очки:<span id="sc">0</span>/400</span></div>
<div id="field"><div id="gun">🔫</div></div>
<div id="start"><h2>Набери 400 очков<br>за 20 секунд!</h2><button id="play">PLAY</button><h3 id="msg"></h3></div>
</div>

<script>
let score=0,time=20,playing=false,timer,spawner,shooter;
let field=document.getElementById('field');
let scEl=document.getElementById('sc');
let tmEl=document.getElementById('tm');
let startEl=document.getElementById('start');
let msgEl=document.getElementById('msg');

function createTarget(){
  let t=document.createElement('div');
  t.className='target';
  t.textContent='20';
  t.style.left=Math.random()*320+'px';
  t.style.top=Math.random()*200+'px';
  t.style.background=`hsl(${Math.random()*50},100%,60%)`;
  field.appendChild(t);
  let fall=setInterval(()=>{t.style.top=(parseFloat(t.style.top)+2)+'px'; if(parseFloat(t.style.top)>500){t.remove();clearInterval(fall);}},30);
  t.onclick=()=>{score+=20;scEl.textContent=score;t.remove();clearInterval(fall);};
  setTimeout(()=>{if(t.parentNode){t.remove();clearInterval(fall);}},3000);
}

document.getElementById('play').onclick=()=>{
  score=0;time=20;scEl.textContent=0;tmEl.textContent=20;msgEl.textContent='';
  startEl.style.display='none';playing=true;
  field.querySelectorAll('.target').forEach(e=>e.remove());
  
  timer=setInterval(()=>{
    time--;tmEl.textContent=time;
    if(time<=0){end();}
  },1000);
  
  spawner=setInterval(createTarget,250);
  
  shooter=setInterval(()=>{
    if(!playing)return;
    let b=document.createElement('div');
    b.className='bullet';
    b.style.bottom='50px';
    b.style.left='50%';
    field.appendChild(b);
    let up=setInterval(()=>{
      b.style.bottom=(parseFloat(b.style.bottom)+10)+'px';
      let br=b.getBoundingClientRect();
      document.querySelectorAll('.target').forEach(t=>{
        let tr=t.getBoundingClientRect();
        if(Math.abs(br.left-tr.left)<25 && Math.abs(br.top-tr.top)<25){
          score+=20;scEl.textContent=score;t.remove();b.remove();clearInterval(up);
        }
      });
      if(parseFloat(b.style.bottom)>550){b.remove();clearInterval(up);}
    },20);
  },150);
};

function end(){
  playing=false;clearInterval(timer);clearInterval(spawner);clearInterval(shooter);
  startEl.style.display='flex';
  if(score>=400){msgEl.textContent='ПОБЕДА! '+score+' очков!';document.getElementById('play').textContent='ЕЩЕ РАЗ';}
  else{msgEl.textContent='Проиграл: '+score+'/400';document.getElementById('play').textContent='СНОВА';}
}
</script>
</body>
</html>
