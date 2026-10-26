// Usage: node scripts/record.js <html file> <out.mp4> [seconds=30] [width=1920] [height=1080] [fps=30]
// Records the page by stepping a virtual clock is not possible for arbitrary pages, so this uses real-time capture.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs'), path = require('path'), os = require('os');
(async () => {
  const [html, out, s = '30', w = '1920', h = '1080', fps = '30'] = process.argv.slice(2);
  if (!html || !out) { console.error('usage: record.js <html> <out.mp4> [sec] [w] [h] [fps]'); process.exit(1); }
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'rec-'));
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: +w, height: +h }, recordVideo: { dir: tmp, size: { width: +w, height: +h } } });
  const pg = await ctx.newPage();
  await pg.goto('file://' + path.resolve(html));
  await pg.waitForTimeout(+s * 1000);
  await ctx.close(); await b.close();
  const webm = fs.readdirSync(tmp).find(f => f.endsWith('.webm'));
  execFileSync('ffmpeg', ['-y', '-i', path.join(tmp, webm), '-r', fps, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', out], { stdio: 'inherit' });
  console.log('wrote', out);
})();
