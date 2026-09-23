<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Автомат - 20 секунд</title>
<style>
  body { margin:0; background:#111; color:white; font-family:Arial; overflow:hidden; display:flex; justify-content:center; align-items:center; height:100vh; }
  #gameBox { position:relative; width:400px; height:600px; background:linear-gradient(#1a1a2e, #0f0f1e); border:3px solid #444; border-radius:15px; overflow:hidden; }
  #top { display:flex; justify-content:space-between; padding:10px 15px; font-weight:bold; font-size:18px; background:rgba(0,0,0,0.5); }
  #canvas { display:block; width:100%; height:500px; }
  #gun { position:absolute; bottom:10px; left:50%; transform:translateX(-50%); font-size:40px; }
  #playScreen { position:absolute; inset:0; background:rgba(0,0,0,0.85); display:flex; flex-direction:column; justify-content:center; align-items:center; z-index:10; }
  #playBtn { padding:15px 50px; font-size:28px; font-weight:bold; background:#00ff88; border:none; border-radius:30px; cursor:pointer; box-shadow:0 0 20px #00ff88; }
  #playBtn:active { transform:scale(0.95); }
  #result { font-size:24px; margin-top:15px; text-align:center; }
</style>
</head>
<body>
<div id="gameBox">
  <div id="top">
    <div>Время: <span id="time">20</span>c</div>
    <div>Очки: <span id="score">0</span>/400</div>
  </div>
  <canvas id="canvas" width="400" height="500"></canvas>
  <div id="gun">🔫</div>
  <div id="playScreen">
    <h1 style="margin-bottom:10px">🔫 АВТОМАТ</h1>
    <p style="margin-bottom:20px; opacity:0.8;">Набери 400 очков за 20 секунд!</p>
    <button id="playBtn">PLAY ▶</button>
    <div id="result"></div>
  </div>
</div>

<script>
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const timeEl = document.getElementById('time');
const scoreEl = document.getElementById('score');
const playScreen = document.getElementById('playScreen');
const playBtn = document.getElementById('playBtn');
const resultEl = document.getElementById('result');

let targets = [];
let bullets = [];
let score = 0;
let timeLeft = 20;
let gameRunning = false;
let gameLoop, timerLoop, spawnLoop, shootLoop;

function resetGame() {
  targets = [];
  bullets = [];
  score = 0;
  timeLeft = 20;
  scoreEl.textContent = 0;
  timeEl.textContent = 20;
  resultEl.textContent = '';
}

function spawnTarget() {
  targets.push({
    x: Math.random() * 340 + 20,
    y: Math.random() * 150 + 20,
    r: 20 + Math.random()*15,
    color: `hsl(${Math.random()*60+0}, 100%, 60%)`,
    speed: Math.random()*1.5+0.5
  });
}

function shoot() {
  if (!gameRunning) return;
  bullets.push({ x: 200, y: 460, speed: 10 });
}

function update() {
  ctx.clearRect(0,0,400,500);
  
  // targets
  for (let i = targets.length-1; i>=0; i--) {
    let t = targets[i];
    t.y += t.speed;
    if (t.y > 480) { targets.splice(i,1); continue; }
    ctx.beginPath();
    ctx.fillStyle = t.color;
    ctx.arc(t.x, t.y, t.r, 0, Math.PI*2);
    ctx.fill();
    ctx.fillStyle = 'white';
    ctx.font = '12px Arial';
    ctx.fillText('+20', t.x-12, t.y+4);
  }
  
  // bullets
  for (let i = bullets.length-1; i>=0; i--) {
    let b = bullets[i];
    b.y -= b.speed;
    ctx.fillStyle = '#ffff00';
    ctx.fillRect(b.x-3, b.y, 6, 15);
    
    // check hit
    for (let j = targets.length-1; j>=0; j--) {
      let t = targets[j];
      let dist = Math.hypot(b.x - t.x, b.y - t.y);
      if (dist < t.r + 8) {
        targets.splice(j,1);
        bullets.splice(i,1);
        score += 20;
        scoreEl.textContent = score;
        break;
      }
    }
    if (b.y < 0 && bullets[i]) bullets.splice(i,1);
  }
}

function startGame() {
  resetGame();
  gameRunning = true;
  playScreen.style.display = 'none';
  
  timerLoop = setInterval(() => {
    timeLeft--;
    timeEl.textContent = timeLeft;
    if (timeLeft <= 0) endGame();
  }, 1000);
  
  spawnLoop = setInterval(spawnTarget, 300);
  shootLoop = setInterval(shoot, 120);
  gameLoop = setInterval(update, 16);
  
  // сразу 3 цели
  spawnTarget(); spawnTarget(); spawnTarget();
}

function endGame() {
  gameRunning = false;
  clearInterval(timerLoop);
  clearInterval(spawnLoop);
  clearInterval(shootLoop);
  clearInterval(gameLoop);
  
  playScreen.style.display = 'flex';
  if (score >= 400) {
    resultEl.innerHTML = `🏆 ПОБЕДА!<br>Ты набрал ${score} очков!`;
    playBtn.textContent = 'ИГРАТЬ СНОВА';
  } else {
    resultEl.innerHTML = `😢 Не хватило<br>Ты набрал ${score}/400`;
    playBtn.textContent = 'ПОПРОБОВАТЬ СНОВА';
  }
}

playBtn.onclick = startGame;
canvas.onclick = (e) => {
  if (!gameRunning) return;
  const rect = canvas.getBoundingClientRect();
  const x = (e.clientX - rect.left) * (400 / rect.width);
  bullets.push({ x: x, y: 460, speed: 10 });
}
</script>
</div>
</body>
</html>
