#!/usr/bin/env python3
"""Daily #zeitgeist chalk GIF: line art reveals along its own strokes, then captions type in.
usage: make_gif.py art.png out.gif "HEADLINE" "SUBLINE" "FOOTER"
art: white/light lines on dark board (or dark on light; auto-detected), 9:16."""
import sys, numpy as np
from collections import deque
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
art, out, head, sub, foot = sys.argv[1:6]
W, H = 540, 960
BOARD=(29,31,28); CHALK=(241,237,226)
im = Image.open(art).convert("L").resize((W, H), Image.LANCZOS)
a = np.asarray(im).astype(float)
dark_bg = a.mean() < 128
line = a > 110 if dark_bg else a < 145
line = ndimage.binary_opening(line, iterations=0) if False else line
lab, n = ndimage.label(line, structure=np.ones((3,3)))
sizes = ndimage.sum(line, lab, range(1, n+1))
dist = np.full(line.shape, -1, int)
order = sorted(range(1, n+1), key=lambda k: -sizes[k-1])
offset = 0
for k in order:
    if sizes[k-1] < 8: continue
    ys, xs = np.nonzero(lab == k)
    i = np.argmin(xs + ys*0.2)
    q = deque([(ys[i], xs[i])]); dist[ys[i], xs[i]] = offset; mx = offset
    while q:
        y, x = q.popleft(); d = dist[y, x]
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                yy, xx = y+dy, x+dx
                if 0<=yy<H and 0<=xx<W and line[yy,xx] and dist[yy,xx] < 0:
                    dist[yy,xx] = d+1; q.append((yy,xx)); mx = max(mx, d+1)
    offset = mx + 1
total = max(offset, 1)
alpha = np.clip((a - (a.min() if dark_bg else 0)) / 255.0, 0, 1) if dark_bg else np.clip((255-a)/255.0,0,1)
alpha = np.clip(alpha*1.6, 0, 1)
B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; M="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur+" "+w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
fh, fs, ff = ImageFont.truetype(B, 38), ImageFont.truetype(R, 22), ImageFont.truetype(M, 17)
DRAW, TYPE, HOLD = 40, 18, 30
frames = []
base = np.zeros((H, W, 3)); base[:] = BOARD
for f in range(DRAW + TYPE + HOLD):
    t = min(1, (f+1)/DRAW)
    vis = (dist >= 0) & (dist <= t*total)
    al = (alpha * vis)[..., None]
    rgb = base*(1-al) + np.array(CHALK)*al
    img = Image.fromarray(rgb.astype(np.uint8)); d = ImageDraw.Draw(img)
    k = 0 if f < DRAW else min(1, (f-DRAW+1)/TYPE)
    hl = wrap(d, head, fh, W-60); y = 70
    chars = int(k*len(head)); used = 0
    for L in hl:
        s = L[:max(0, chars-used)]; used += len(L)+1
        d.text((30, y), s, font=fh, fill=CHALK); y += 48
    if k >= 1:
        for L in wrap(d, sub, fs, W-60):
            d.text((30, y+6), L, font=fs, fill=(200,196,186)); y += 30
    if f >= DRAW//2:
        for i,c in enumerate([(242,195,24),(43,134,209),(52,168,83)]):
            d.rectangle([30+i*24, H-62, 48+i*24, H-44], fill=c)
        d.text((112, H-64), foot, font=ff, fill=CHALK)
    frames.append(img.convert("P", palette=Image.ADAPTIVE, colors=64))
frames[0].save(out, save_all=True, append_images=frames[1:], duration=[80]*(DRAW+TYPE) + [120]*HOLD, loop=0, optimize=True, disposal=1)
frames[-1].convert("RGB").save(out.replace(".gif", "-last.png"))
print("ok", n, total)
