import sys, numpy as np
from PIL import Image, ImageSequence, ImageDraw, ImageFont
src, mark, out = sys.argv[1:4]
g = Image.open(src); frames=[]; durs=[]
for f in ImageSequence.Iterator(g):
    frames.append(f.convert("RGB")); durs.append(f.info.get("duration",80))
W,H = frames[0].size; BOARD=np.array([29,31,28.]); CHALK=np.array([241,237,226.])
m = Image.open(mark).convert("L"); m = m.resize((480, int(480*m.height/m.width)), Image.LANCZOS)
ink = np.clip((200 - np.asarray(m).astype(float))/170, 0, 1)[...,None]
card = np.zeros((H,W,3)); card[:] = BOARD
y0 = H//2 - m.height//2 - 40; x0 = (W-480)//2
card[y0:y0+m.height, x0:x0+480] = BOARD*(1-ink) + CHALK*ink
# keep original colored squares visible: copy color pixels from wordmark
mc = np.asarray(Image.open(mark).convert("RGB").resize((480,m.height), Image.LANCZOS)).astype(float)
sat = mc.max(2)-mc.min(2) > 60
reg = card[y0:y0+m.height, x0:x0+480]; reg[sat] = mc[sat]
cimg = Image.fromarray(card.astype(np.uint8)); d = ImageDraw.Draw(cimg)
f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
t = "@yaelmendez · #grandesmodelosdelenguaje"; d.text(((W-d.textlength(t,font=f))/2, y0+m.height+40), t, font=f, fill=tuple(CHALK.astype(int)))
last = np.asarray(frames[-1]).astype(float); cc = np.asarray(cimg).astype(float)
for i in range(10):
    a=(i+1)/10; frames.append(Image.fromarray((last*(1-a)+cc*a).astype(np.uint8))); durs.append(100)
frames.append(cimg); durs.append(2000)
pf = [fr.convert("P", palette=Image.ADAPTIVE, colors=64) for fr in frames]
pf[0].save(out, save_all=True, append_images=pf[1:], duration=durs, loop=0, optimize=True, disposal=1)
cimg.save(out.replace(".gif","-end.png")); print(sum(durs)/1000, "s")
