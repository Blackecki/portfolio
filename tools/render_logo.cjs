/* Rasterize the hand-authored SVG assets with Sharp. */
const fs = require('node:fs/promises');
const path = require('node:path');
const sharp = require(process.env.BRAND_NODE_MODULES
  ? path.join(process.env.BRAND_NODE_MODULES, 'sharp') : 'sharp');
const folder = path.resolve(__dirname, '../brand');

(async () => {
  const metadata = JSON.parse(await fs.readFile(path.join(folder, 'assets.json'), 'utf8'));
  for (const file of metadata.files) {
    const size = file.includes('-logo-') ? 2400 : 1024;
    await sharp(path.join(folder, file), { density: 300 }).resize({width:size}).png()
      .toFile(path.join(folder, file.replace('.svg', '.png')));
  }
  await sharp(path.join(folder, 'blackecki-avatar.svg'), {density:300}).resize(32,32).png()
    .toFile(path.join(folder, 'blackecki-icon-32.png'));
  await sharp(path.join(folder, 'blackecki-avatar.svg'), {density:300}).resize(16,16).png()
    .toFile(path.join(folder, 'blackecki-icon-16.png'));
  console.log('Built transparent PNGs and 16/32 px icon proofs.');
})().catch(error => { console.error(error); process.exitCode = 1; });
