
// Simple red matrix rain effect
(function () {
  const canvas = document.getElementById('matrix');
  const ctx = canvas.getContext('2d');

  let w, h, cols, ypos;

  function resize() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
    cols = Math.floor(w / 14) + 1;
    ypos = Array(cols).fill(0);
  }
  window.addEventListener('resize', resize);
  resize();

  function draw() {
    // translucent background for trail effect
    ctx.fillStyle = 'rgba(0,0,0,0.05)';
    ctx.fillRect(0,0,w,h);

    ctx.fillStyle = '#ff1a1a';
    ctx.font = '14px monospace';

    ypos.forEach((y, ind) => {
      const text = String.fromCharCode(0x30A0 + Math.random() * 96);
      const x = ind * 14;
      ctx.fillText(text, x, y);
      if (y > h + Math.random() * 10000) ypos[ind] = 0;
      else ypos[ind] = y + 14;
    });

    requestAnimationFrame(draw);
  }
  requestAnimationFrame(draw);
})();
