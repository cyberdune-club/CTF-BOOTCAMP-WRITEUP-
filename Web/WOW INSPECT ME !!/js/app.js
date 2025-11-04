// Part 3/3 — JavaScript:
// javascript}
// The pieces together form the full flag. Nothing dynamic here; it's all in the files.

// Console greeting + tiny nudge
console.log("%cCYBERDUNE", "color:#43ff64;font-weight:bold;");
console.log("Hint: files aren't only what you see on screen. View Source, open the CSS/JS files.");


// Matrix rain effect
(function () {
  const canvas = document.getElementById('matrix');
  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  window.addEventListener('resize', resize);
  resize();

  const glyphs = 'アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const fontSize = 16;
  let columns = Math.floor(window.innerWidth / fontSize);
  let drops = new Array(columns).fill(1);

  function draw() {
    if (columns !== Math.floor(window.innerWidth / fontSize)) {
      columns = Math.floor(window.innerWidth / fontSize);
      drops = new Array(columns).fill(1);
    }
    ctx.fillStyle = 'rgba(0, 0, 0, 0.07)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#43ff64';
    ctx.shadowColor = '#43ff64';
    ctx.shadowBlur = 8;
    ctx.font = fontSize + 'px "Share Tech Mono", monospace';

    for (let i = 0; i < drops.length; i++) {
      const text = glyphs.charAt(Math.floor(Math.random() * glyphs.length));
      const x = i * fontSize;
      const y = drops[i] * fontSize;

      ctx.fillText(text, x, y);

      if (y > canvas.height && Math.random() > 0.975) {
        drops[i] = 0;
      }
      drops[i]++;
    }
    requestAnimationFrame(draw);
  }
  draw();
})();
