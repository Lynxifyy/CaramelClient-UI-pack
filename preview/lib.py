"""Caramel Client preview toolkit: draws the UI spec at 2x and downsamples."""
import math, random, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np
S = 4          # supersampling factor (smooth edges); output is saved at 2x
OUT = 2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(ROOT, 'fonts')
_fc = {}
def font(spec, size):
    k = (spec, size)
    if k not in _fc:
        fam, w = spec.split(':')
        name = ('Inter-%s.otf' if fam == 'i' else 'Poppins-%s.ttf') % w
        _fc[k] = ImageFont.truetype(os.path.join(FD, name), int(round(size * S)))
    return _fc[k]

# ---- tokens ---------------------------------------------------------------
BG0=(6,11,26); BG1=(10,19,48); BG2=(15,27,68)
TXT=(234,240,255); TXT2=(154,168,208); TXT3=(102,116,158)
BLUE=(74,120,255); CARAMEL=(245,167,66); GREEN=(47,211,107); GREEN_D=(24,160,80)
RED=(255,84,104); ORANGE=(255,159,46); YELLOW=(255,208,64)
def A(c, a): return (c[0], c[1], c[2], a)

class Cv:
    def __init__(s, w, h):
        s.w, s.h = w, h
        s.im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0))
    def B(s, box): return tuple(int(round(v * S)) for v in box)
    def save(s, path, scale=OUT):
        out = s.im.resize((s.w * scale, s.h * scale), Image.LANCZOS)
        out.save(path, optimize=True)
    # --- primitives
    def _lay(s, box, fn, pad=0):
        x0, y0, x1, y1 = s.B(box); x0 -= pad; y0 -= pad; x1 += pad; y1 += pad
        lay = Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0))
        fn(ImageDraw.Draw(lay), pad, lay)
        s.im.alpha_composite(lay, (max(x0, 0), max(y0, 0))) if x0 >= 0 and y0 >= 0 else s.im.paste(lay, (x0, y0), lay)
    def rr(s, box, r, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = s.B(box)
        def f(d, p, l): d.rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), r * S, fill=fill, outline=outline, width=max(1, int(width * S)))
        s._lay(box, f)
    def ell(s, box, fill=None, outline=None, width=1):
        x0, y0, x1, y1 = s.B(box)
        def f(d, p, l): d.ellipse((0, 0, x1 - x0 - 1, y1 - y0 - 1), fill=fill, outline=outline, width=max(1, int(width * S)))
        s._lay(box, f)
    def mask(s, box, r):
        x0, y0, x1, y1 = s.B(box)
        m = Image.new('L', (x1 - x0, y1 - y0), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, x1 - x0 - 1, y1 - y0 - 1), r * S, fill=255)
        return m
    def grad(s, box, r, c0, c1, vertical=True):
        x0, y0, x1, y1 = s.B(box); w, h = x1 - x0, y1 - y0
        t = np.linspace(0, 1, h if vertical else w)[:, None] if vertical else np.linspace(0, 1, w)[None, :]
        t = np.broadcast_to(t, (h, w))[..., None]
        c0 = np.array(c0 if len(c0) == 4 else (*c0, 255), float); c1 = np.array(c1 if len(c1) == 4 else (*c1, 255), float)
        arr = (c0 * (1 - t) + c1 * t).astype('uint8')
        g = Image.fromarray(arr, 'RGBA'); g.putalpha(ImageChops.multiply(g.getchannel('A'), s.mask(box, r)))
        s.im.alpha_composite(g, (x0, y0))
    def shadow(s, box, r, blur=18, dy=10, alpha=120, color=(0, 0, 0)):
        x0, y0, x1, y1 = s.B(box); pad = int(blur * S * 2)
        lay = Image.new('RGBA', (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(lay).rounded_rectangle((pad, pad, pad + x1 - x0, pad + y1 - y0), r * S, fill=(*color, alpha))
        lay = lay.filter(ImageFilter.GaussianBlur(blur * S))
        s.im.alpha_composite(lay, (max(x0 - pad, 0), max(y0 - pad + int(dy * S), 0))) if x0 - pad >= 0 and y0 - pad + dy * S >= 0 else s.im.paste(lay, (x0 - pad, y0 - pad + int(dy * S)), lay)
    def glass(s, box, r, tint=(150, 175, 255, 16), blur=20, border=70, shadow=True, sh_alpha=110):
        if shadow: s.shadow(box, r, alpha=sh_alpha)
        x0, y0, x1, y1 = s.B(box)
        reg = s.im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(blur * S))
        reg = Image.blend(reg, Image.new('RGBA', reg.size, (12, 22, 56, 255)), 0.28)   # navy frost
        m = s.mask(box, r)
        s.im.paste(reg, (x0, y0), m)
        # tint + top sheen
        s.grad(box, r, A(tint[:3], tint[3] + 12), A(tint[:3], max(tint[3] - 8, 0)))
        # gradient hairline border (bright top-left -> dim bottom-right)
        w, h = x1 - x0, y1 - y0
        ring = Image.new('L', (w, h), 0); d = ImageDraw.Draw(ring)
        d.rounded_rectangle((0, 0, w - 1, h - 1), r * S, outline=255, width=max(1, int(S * 1.0)))
        gy = np.linspace(border, border * 0.28, h)[:, None]; gx = np.linspace(1.0, 0.55, w)[None, :]
        al = Image.fromarray((np.broadcast_to(gy * gx, (h, w))).astype('uint8'), 'L')
        ring = ImageChops.multiply(ring, al)
        white = Image.new('RGBA', (w, h), (255, 255, 255, 255)); white.putalpha(ring)
        s.im.alpha_composite(white, (x0, y0))
    def text(s, x, y, t, fn='i:Regular', sz=13, fill=TXT, anchor='lt', track=0):
        f = font(fn, sz)
        if track:
            w = sum(f.getlength(c) + track * S for c in t) - track * S
            ox = {'l': 0, 'm': -w / 2 / S, 'r': -w / S}[anchor[0]]
            for c in t:
                s.text(x + ox, y, c, fn, sz, fill, 'l' + anchor[1]); ox += (f.getlength(c) / S) + track
            return
        fill = fill if len(fill) == 4 else (*fill, 255)
        l, t_, r, b = f.getbbox(t, anchor=anchor); pad = 3
        lay = Image.new('RGBA', (r - l + 2 * pad, b - t_ + 2 * pad), (0, 0, 0, 0))
        ImageDraw.Draw(lay).text((pad - l, pad - t_), t, font=f, fill=fill, anchor=anchor)
        X, Y = int(round(x * S)) + l - pad, int(round(y * S)) + t_ - pad
        s.im.alpha_composite(lay, (max(X, 0), max(Y, 0))) if X >= 0 and Y >= 0 else s.im.paste(lay, (X, Y), lay)
    def tw(s, t, fn, sz): return font(fn, sz).getlength(t) / S
    def line(s, pts, fill, width=1.5):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        pad = width + 2; box = (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad); x0, y0, _, _ = s.B(box)
        def f(d, p, l):
            q = [((px * S) - x0, (py * S) - y0) for px, py in pts]
            d.line(q, fill=fill, width=int(width * S), joint='curve')
            for a in (q[0], q[-1]): d.ellipse((a[0] - width * S / 2, a[1] - width * S / 2, a[0] + width * S / 2, a[1] + width * S / 2), fill=fill)
        s._lay(box, f)
    def paste(s, img, x, y, w=None, h=None, alpha=1.0):
        if w: img = img.resize((int(w * S), int(h * S) if h else int(w * S * img.height / img.width)), Image.LANCZOS)
        if alpha < 1: img = img.copy(); img.putalpha(img.getchannel('A').point(lambda v: int(v * alpha)))
        X, Y = int(x * S), int(y * S)
        s.im.alpha_composite(img, (max(X, 0), max(Y, 0))) if X >= 0 and Y >= 0 else s.im.paste(img, (X, Y), img)
    def clip_round(s, box, r):
        """Cut canvas to rounded window shape."""
        m = Image.new('L', s.im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, s.im.width - 1, s.im.height - 1), r * S, fill=255)
        s.im.putalpha(ImageChops.multiply(s.im.getchannel('A'), m))

# ---- icons (24-grid, stroke style) -----------------------------------------
def icon(cv, name, cx, cy, sz=20, col=TXT, w=1.7, fill=None):
    k = sz / 24.0; ox, oy = cx - sz / 2, cy - sz / 2
    P = lambda x, y: (ox + x * k, oy + y * k)
    L = lambda pts, ww=w: cv.line([P(*p) for p in pts], col, ww * k * 24 / 24 * (sz / 20 if sz < 20 else 1) if False else ww * max(k * 1.0, 0.6) * 1.0 + 0.0)
    wd = max(w * k, 1.2)
    def E(b, **kw): cv.ell((ox + b[0] * k, oy + b[1] * k, ox + b[2] * k, oy + b[3] * k), **kw)
    def R(b, r, **kw): cv.rr((ox + b[0] * k, oy + b[1] * k, ox + b[2] * k, oy + b[3] * k), r * k, **kw)
    def Ln(pts): cv.line([P(*p) for p in pts], col, wd)
    wi = max(int(wd * S), 1)
    if name == 'gamepad':
        R((2.5, 7.5, 21.5, 17.5), 5, outline=col, width=wd); Ln([(8, 10.5), (8, 14.5)]); Ln([(6, 12.5), (10, 12.5)]); E((14.4, 10.2, 16.4, 12.2), fill=col); E((17, 12.8, 19, 14.8), fill=col)
    elif name == 'puzzle':
        arc = lambda cx_, cy_, r_, a0, a1, n=12: [(cx_ + r_ * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy_ - r_ * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        Ln([(4.5, 7), (9.5, 7)] + arc(12, 5.4, 2.8, 200, -20) + [(14.5, 7), (19.5, 7), (19.5, 9.2)] + arc(19.6, 12, 2.8, 110, -110) + [(19.5, 14.8), (19.5, 20), (4.5, 20), (4.5, 7)])
    elif name == 'globe':
        E((3, 3, 21, 21), outline=col, width=wd); E((8, 3, 16, 21), outline=col, width=wd); Ln([(3, 12), (21, 12)])
    elif name == 'cube':
        Ln([(12, 3), (20, 7.5), (20, 16.5), (12, 21), (4, 16.5), (4, 7.5), (12, 3)]); Ln([(4, 7.5), (12, 12), (20, 7.5)]); Ln([(12, 12), (12, 21)])
    elif name == 'news':
        R((4, 3.5, 20, 20.5), 3, outline=col, width=wd); Ln([(8, 8.5), (16, 8.5)]); Ln([(8, 12.5), (16, 12.5)]); Ln([(8, 16.5), (12.5, 16.5)])
    elif name == 'cart':
        Ln([(2.5, 4.5), (5.5, 4.5), (8, 15), (18, 15), (20.5, 7.5), (6.2, 7.5)]); E((8.2, 17.6, 11, 20.4), fill=col); E((15.6, 17.6, 18.4, 20.4), fill=col)
    elif name == 'gear':
        for i in range(8):
            a = i * math.pi / 4; Ln([(12 + 7.2 * math.cos(a), 12 + 7.2 * math.sin(a)), (12 + 9.6 * math.cos(a), 12 + 9.6 * math.sin(a))])
        E((5.2, 5.2, 18.8, 18.8), outline=col, width=wd); E((9, 9, 15, 15), outline=col, width=wd)
    elif name == 'user':
        E((8, 3.5, 16, 11.5), outline=col, width=wd); pts = [(4.5 + 15 * (i / 16), 20.5 - 5.5 * math.sin(math.pi * i / 16)) for i in range(17)]; Ln(pts)
    elif name == 'users':
        icon(cv, 'user', cx - sz * .12, cy, sz * .85, col, w); E((14, 4.5, 20, 10.5), outline=col, width=wd); Ln([(16, 14.5), (20.5, 14.5), (22, 19)])
    elif name == 'search':
        E((3.5, 3.5, 16.5, 16.5), outline=col, width=wd); Ln([(15, 15), (20.5, 20.5)])
    elif name in ('down', 'up', 'right', 'left'):
        pts = {'down': [(6, 9), (12, 15), (18, 9)], 'up': [(6, 15), (12, 9), (18, 15)], 'right': [(9, 6), (15, 12), (9, 18)], 'left': [(15, 6), (9, 12), (15, 18)]}[name]; Ln(pts)
    elif name in ('lock', 'unlock'):
        R((5.5, 10.5, 18.5, 21), 3, fill=col)
        if name == 'lock': Ln([(8, 10.5), (8, 7.5)] + [(12 + 4 * math.cos(math.pi + math.pi * i / 10), 7.5 + 4.5 * math.sin(math.pi + math.pi * i / 10)) for i in range(11)] + [(16, 7.5), (16, 10.5)])
        else: Ln([(8, 10.5), (8, 7.5)] + [(12 + 4 * math.cos(math.pi + math.pi * i / 10), 7.5 + 4.5 * math.sin(math.pi + math.pi * i / 10)) for i in range(11)] + [(16, 5.5), (16, 4.5)])
    elif name == 'bolt':
        pts = [P(13.5, 1.5), P(4.5, 13.5), P(11, 13.5), P(9.5, 22.5), P(19.5, 9.5), P(13, 9.5)]
        x0 = min(p[0] for p in pts); y0 = min(p[1] for p in pts); x1 = max(p[0] for p in pts); y1 = max(p[1] for p in pts)
        cv._lay((x0 - 1, y0 - 1, x1 + 1, y1 + 1), lambda d, p, l: d.polygon([((px - x0 + 1) * S, (py - y0 + 1) * S) for px, py in pts], fill=col))
    elif name == 'x': Ln([(6, 6), (18, 18)]); Ln([(18, 6), (6, 18)])
    elif name == 'check': Ln([(5, 12.5), (10, 17.5), (19, 7)])
    elif name == 'plus': Ln([(12, 5), (12, 19)]); Ln([(5, 12), (19, 12)])
    elif name == 'minus': Ln([(5, 12), (19, 12)])
    elif name == 'square': R((5.5, 5.5, 18.5, 18.5), 2, outline=col, width=wd)
    elif name == 'bell':
        pts = [(6, 17), (6, 11)] + [(12 + 6 * math.cos(math.pi + math.pi * i / 10), 11 + 7 * math.sin(math.pi + math.pi * i / 10)) for i in range(11)] + [(18, 11), (18, 17), (20, 17.5), (4, 17.5), (6, 17)]
        Ln(pts); Ln([(10, 20.5), (14, 20.5)])
    elif name == 'swap': Ln([(5, 9), (19, 9), (16, 6)]); Ln([(19, 15), (5, 15), (8, 18)])
    elif name == 'folder':
        pts = [(3, 7), (3, 19), (21, 19), (21, 8.5), (11, 8.5), (9.5, 5.5), (4.5, 5.5), (3, 7)]
        x0 = min(P(*p)[0] for p in pts); y0 = min(P(*p)[1] for p in pts); x1 = max(P(*p)[0] for p in pts); y1 = max(P(*p)[1] for p in pts)
        cv._lay((x0 - 1, y0 - 1, x1 + 1, y1 + 1), lambda d, p, l: d.polygon([((P(*q)[0] - x0 + 1) * S, (P(*q)[1] - y0 + 1) * S) for q in pts], fill=col))
    elif name == 'rocket':
        Ln([(12, 3), (16.5, 8), (16.5, 15), (7.5, 15), (7.5, 8), (12, 3)]); Ln([(7.5, 12), (4.5, 16.5), (7.5, 15.5)]); Ln([(16.5, 12), (19.5, 16.5), (16.5, 15.5)]); E((10.4, 8.4, 13.6, 11.6), outline=col, width=wd); Ln([(12, 17), (12, 21)])
    elif name == 'play':
        pts = [P(7, 4.5), P(19, 12), P(7, 19.5)]
        x0 = min(p[0] for p in pts); y0 = min(p[1] for p in pts)
        cv._lay((x0 - 1, y0 - 1, max(p[0] for p in pts) + 1, max(p[1] for p in pts) + 1), lambda d, p, l: d.polygon([((px - x0 + 1) * S, (py - y0 + 1) * S) for px, py in pts], fill=col))
    elif name == 'star':
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5; rr_ = 9.6 if i % 2 == 0 else 4.6; pts.append((12 + rr_ * math.cos(a), 12.6 + rr_ * math.sin(a)))
        Ln(pts + [pts[0]])
    elif name == 'dots': [E((x - 1.6, 10.4, x + 1.6, 13.6), fill=col) for x in (5, 12, 19)]
    elif name == 'sliders': Ln([(4, 8), (20, 8)]); Ln([(4, 16), (20, 16)]); E((7, 5.5, 12, 10.5), fill=BG1, outline=col, width=wd); E((13, 13.5, 18, 18.5), fill=BG1, outline=col, width=wd)
    elif name == 'trash': Ln([(4.5, 7), (19.5, 7)]); Ln([(6.5, 7), (7.5, 20.5), (16.5, 20.5), (17.5, 7)]); Ln([(9.5, 7), (9.5, 4), (14.5, 4), (14.5, 7)])
    elif name == 'map': Ln([(12, 21), (6, 11.5), (6, 8), (9, 4), (15, 4), (18, 8), (18, 11.5), (12, 21)]); E((9.8, 7.5, 14.2, 11.9), outline=col, width=wd)
    elif name == 'hud': R((3.5, 5, 20.5, 19), 3, outline=col, width=wd); R((6.5, 8, 12, 11), 1, fill=col); R((6.5, 13, 17, 16), 1, outline=col, width=max(wd * .7, 1))
    elif name == 'camera':
        R((3, 7, 21, 19.5), 4, outline=col, width=wd); E((8.2, 9.6, 15.8, 17.2), outline=col, width=wd); Ln([(8, 7), (9.6, 4.5), (14.4, 4.5), (16, 7)])
    elif name == 'mic':
        R((9, 3, 15, 13.5), 3, outline=col, width=wd); Ln([(5.5 + 13 * i / 14, 11 + 6.5 * math.sin(math.pi * i / 14)) for i in range(15)]); Ln([(12, 17.5), (12, 21)]); Ln([(8.5, 21), (15.5, 21)])
    elif name == 'replay':
        Ln([(12 + 8 * math.cos(math.radians(a)), 12 - 8 * math.sin(math.radians(a))) for a in range(60, 330, 10)]); Ln([(4.4, 4.4), (4.8, 9), (9.4, 8.6)]) if False else None
        Ln([(5.2, 3.6), (5.4, 8.2), (10, 8)]); pts = [P(10, 8.6), P(16, 12), P(10, 15.4)]
        x0 = min(p[0] for p in pts); y0 = min(p[1] for p in pts)
        cv._lay((x0 - 1, y0 - 1, max(p[0] for p in pts) + 1, max(p[1] for p in pts) + 1), lambda d, p, l: d.polygon([((px - x0 + 1) * S, (py - y0 + 1) * S) for px, py in pts], fill=col))
    elif name == 'edit': Ln([(4.5, 19.5), (5.2, 15.5), (16, 4.8), (19.2, 8), (8.5, 18.8), (4.5, 19.5)]); Ln([(13.5, 7.3), (16.7, 10.5)])
    elif name == 'copy': R((8.5, 8.5, 20, 20), 3, outline=col, width=wd); Ln([(15.5, 8.5), (15.5, 6), (6, 6), (4, 8), (4, 15.5), (8.5, 15.5)])
    elif name == 'star_fill':
        pts = []
        for i in range(10):
            a = -math.pi / 2 + i * math.pi / 5; rr_ = 9.6 if i % 2 == 0 else 4.6; pts.append(P(12 + rr_ * math.cos(a), 12.6 + rr_ * math.sin(a)))
        x0 = min(p[0] for p in pts); y0 = min(p[1] for p in pts); x1 = max(p[0] for p in pts); y1 = max(p[1] for p in pts)
        cv._lay((x0 - 2, y0 - 2, x1 + 2, y1 + 2), lambda d, p, l: d.polygon([((px - x0 + 2) * S, (py - y0 + 2) * S) for px, py in pts], fill=col))
        cv.line(pts + [pts[0]], col, max(wd, 1.6))
    elif name == 'info': E((3.5, 3.5, 20.5, 20.5), outline=col, width=wd); Ln([(12, 11), (12, 17)]); E((11, 6.6, 13, 8.6), fill=col)
    elif name == 'eye': Ln([(2.5 + 19 * i / 16, 12 - 6 * math.sin(math.pi * i / 16)) for i in range(17)]); Ln([(2.5 + 19 * i / 16, 12 + 6 * math.sin(math.pi * i / 16)) for i in range(17)]); E((9, 9, 15, 15), outline=col, width=wd)
    elif name == 'wifi':
        for i, rd in enumerate((3, 6.5, 10)): Ln([(12 + rd * math.cos(math.radians(a)), 18 - rd * math.sin(math.radians(a)) * 1.0) for a in range(40, 141, 10)])
        E((10.8, 17.2, 13.2, 19.6), fill=col)

# ---- pixel art / backgrounds -----------------------------------------------
def navy_bg(cv, seed=3, blobs=True):
    w, h = cv.w, cv.h
    cv.grad((0, 0, w, h), 0, (7, 13, 34), (5, 9, 24))
    if blobs:
        lay = Image.new('RGBA', cv.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for (x, y, r, c) in [(.18, .22, .34, (54, 96, 255, 150)), (.78, .12, .28, (40, 170, 255, 90)), (.62, .85, .36, (86, 60, 255, 110)), (.08, .88, .22, (245, 167, 66, 46)), (.92, .62, .2, (40, 120, 255, 90))]:
            d.ellipse(((x - r) * w * S, (y - r * w / h) * h * S, (x + r) * w * S, (y + r * w / h) * h * S), fill=c)
        lay = lay.filter(ImageFilter.GaussianBlur(min(w, h) * S * .09)); cv.im.alpha_composite(lay)
    # fine grain
    rnd = np.random.RandomState(seed); n = rnd.randint(-5, 6, (cv.im.height, cv.im.width, 1)); a = np.array(cv.im).astype(int)
    a[..., :3] = np.clip(a[..., :3] + n, 0, 255); cv.im = Image.fromarray(a.astype('uint8'), 'RGBA')

def game_bg(cv, seed=5):
    """Procedural blocky voxel landscape (stand-in for in-game screenshot)."""
    w, h = cv.w, cv.h; rnd = random.Random(seed)
    cv.grad((0, 0, w, h), 0, (126, 178, 245), (196, 226, 250))
    cv.rr((w * .74, h * .09, w * .74 + 54, h * .09 + 54), 0, fill=(255, 247, 200, 255))
    for i in range(7):
        cx = rnd.randint(0, w); cy = rnd.randint(30, int(h * .3)); cv.rr((cx, cy, cx + rnd.randint(90, 200), cy + 22), 0, fill=(255, 255, 255, 200))
    u = 28; base = int(h * .52)
    hh = [base + int(40 * math.sin(i * .35) + 25 * math.sin(i * .9 + 2)) for i in range(w // u + 2)]
    for i, y in enumerate(hh):
        y = y // u * u
        cv.rr((i * u, y, i * u + u, h), 0, fill=(94, 156, 62, 255)); cv.rr((i * u, y, i * u + u, y + 6), 0, fill=(124, 196, 80, 255))
        cv.rr((i * u, y + u, i * u + u, h), 0, fill=(134, 96, 62, 255))
        for j in range(int((h - y) / u)):
            if rnd.random() < .35: cv.rr((i * u, y + u * (j + 1), i * u + u, y + u * (j + 2)), 0, fill=(120, 86, 56, 255))
            if rnd.random() < .07: cv.rr((i * u + 6, y + u * (j + 1) + 6, i * u + 18, y + u * (j + 1) + 18), 0, fill=(110, 110, 120, 255))
    for tx in (.12, .42, .88):
        x = int(w * tx) // u * u; y = hh[x // u] // u * u
        for k in range(1, 5): cv.rr((x, y - k * u, x + u, y - (k - 1) * u), 0, fill=(102, 76, 44, 255))
        cv.rr((x - u, y - 6 * u, x + 2 * u, y - 4 * u), 0, fill=(56, 128, 52, 255)); cv.rr((x, y - 7 * u, x + u, y - 6 * u), 0, fill=(70, 150, 60, 255))
    cv.im = cv.im.filter(ImageFilter.GaussianBlur(1.2 * S))

def news_art(w, h, seed, theme):
    cv = Cv(w, h); rnd = random.Random(seed)
    pal = {'night': ((24, 38, 96), (74, 90, 190)), 'ember': ((90, 40, 24), (245, 150, 60)), 'mint': ((18, 72, 70), (90, 220, 170)), 'rose': ((84, 28, 76), (240, 110, 160)), 'sky': ((40, 90, 170), (150, 210, 255))}[theme]
    cv.grad((0, 0, w, h), 0, pal[0], pal[1])
    u = 12
    for i in range(w // u + 1):
        hh = int(h * .62 + 18 * math.sin(i * .5 + seed) + 10 * math.sin(i * 1.3)) // u * u
        cv.rr((i * u, hh, i * u + u, h), 0, fill=(*[int(c * .55) for c in pal[0]], 255))
        cv.rr((i * u, hh, i * u + u, hh + 3), 0, fill=(*[min(255, int(c * 1.15)) for c in pal[1]], 255))
    for _ in range(14):
        x, y = rnd.randint(0, w // u) * u, rnd.randint(0, int(h * .5) // u) * u
        cv.rr((x, y, x + u, y + u), 0, fill=(255, 255, 255, rnd.choice([40, 70, 110])))
    cv.rr((w // 2 - 20, int(h * .3), w // 2 + 20, int(h * .3) + 40), 4, fill=(*pal[1], 255), outline=(255, 255, 255, 90), width=1.5)
    return cv.im

# ---- UI components ---------------------------------------------------------
def label(cv, x, y, t, kind='release', h=20, anchor='l'):
    c = {'release': GREEN, 'beta': ORANGE, 'locked': RED, 'unlocked': GREEN, 'new': BLUE, 'online': GREEN, 'plus': CARAMEL, 'info': TXT2, 'ver': (120, 160, 255)}[kind]
    ic = {'locked': 'lock', 'unlocked': 'unlock'}.get(kind)
    tw = cv.tw(t, 'i:SemiBold', 10.5) + 18 + (14 if ic else 0); x = x - tw if anchor == 'r' else x
    cv.rr((x, y, x + tw, y + h), h / 2, fill=A(c, 40), outline=A(c, 130), width=1)
    ox = x + 9
    if ic: icon(cv, ic, ox + 5, y + h / 2, 11, c, 2.2); ox += 14
    cv.text(ox, y + h / 2, t, 'i:SemiBold', 10.5, c, 'lm'); return tw

def btn_primary(cv, box, t, color='green', sz=14, ic=None):
    x0, y0, x1, y1 = box; r = (y1 - y0) / 2.6
    c0, c1 = {'green': ((62, 226, 122), (24, 160, 80)), 'caramel': ((255, 190, 90), (222, 134, 36)), 'blue': ((98, 140, 255), (52, 88, 230)), 'red': ((255, 108, 126), (214, 52, 78))}[color]
    cv.shadow(box, r, blur=10, dy=5, alpha=110, color=c1)
    cv.grad(box, r, c0, c1); cv.rr((x0 + 1, y0 + 1, x1 - 1, y1 - 1), r - 1, outline=(255, 255, 255, 70), width=1)
    cv.grad((x0 + 2, y0 + 2, x1 - 2, y0 + (y1 - y0) * .5), r - 2, (255, 255, 255, 60), (255, 255, 255, 0))
    tx = (x0 + x1) / 2
    if ic: icon(cv, ic, tx - cv.tw(t, 'p:Medium', sz) / 2 - 12, (y0 + y1) / 2, sz + 3, (8, 40, 20) if color == 'green' else (255, 255, 255), 2); tx += 10
    cv.text(tx, (y0 + y1) / 2 + 1, t, 'p:Medium', sz, (6, 36, 18) if color == 'green' else (255, 255, 255), 'mm')

def btn_glass(cv, box, t, ic=None, sz=12.5, col=TXT, active=False, danger=False):
    x0, y0, x1, y1 = box; r = min(12, (y1 - y0) / 2.4)
    c = RED if danger else (BLUE if active else (255, 255, 255))
    cv.rr(box, r, fill=A(c, 36 if danger or active else 20), outline=A(c, 110 if danger or active else 44), width=1)
    cv.grad((x0 + 1, y0 + 1, x1 - 1, y0 + (y1 - y0) * .5), r - 1, (255, 255, 255, 16), (255, 255, 255, 0))
    colr = RED if danger else col; tw = cv.tw(t, 'i:SemiBold', sz) if t else 0; cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
    if ic and t:
        total = 15 + 8 + tw; st = cx - total / 2
        icon(cv, ic, st + 7.5, cy, 15, colr, 1.9); cv.text(st + 23, cy, t, 'i:SemiBold', sz, colr, 'lm')
    elif ic: icon(cv, ic, cx, cy, 17, colr, 1.9)
    else: cv.text(cx, cy, t, 'i:SemiBold', sz, colr, 'mm')

def toggle(cv, x, y, on=True, w=40, h=22):
    if on:
        cv.grad((x, y, x + w, y + h), h / 2, (62, 226, 122), (30, 170, 88)); cv.ell((x + w - h + 3, y + 3, x + w - 3, y + h - 3), fill=(255, 255, 255, 255))
    else:
        cv.rr((x, y, x + w, y + h), h / 2, fill=(255, 255, 255, 26), outline=(255, 255, 255, 60), width=1); cv.ell((x + 3, y + 3, x + h - 3, y + h - 3), fill=(190, 202, 235, 255))

def checkbox(cv, x, y, on=True, s=18):
    if on: cv.grad((x, y, x + s, y + s), 5, (98, 140, 255), (52, 88, 230)); icon(cv, 'check', x + s / 2, y + s / 2, 13, (255, 255, 255), 2.6)
    else: cv.rr((x, y, x + s, y + s), 5, fill=(255, 255, 255, 14), outline=(255, 255, 255, 70), width=1)

def radio(cv, x, y, on=True, s=18):
    cv.ell((x, y, x + s, y + s), fill=(255, 255, 255, 14), outline=A(BLUE, 255) if on else (255, 255, 255, 70), width=1.4)
    if on: cv.ell((x + 5, y + 5, x + s - 5, y + s - 5), fill=A(BLUE, 255))

def slider(cv, x, y, w, v=.5, show=True, fmt=None, col=BLUE):
    cv.rr((x, y - 3, x + w, y + 3), 3, fill=(255, 255, 255, 30))
    cv.grad((x, y - 3, x + w * v, y + 3), 3, (98, 140, 255), (74, 190, 255), vertical=False) if col == BLUE else cv.grad((x, y - 3, x + w * v, y + 3), 3, (255, 190, 90), (222, 134, 36), vertical=False)
    kx = x + w * v; cv.shadow((kx - 8, y - 8, kx + 8, y + 8), 8, blur=5, dy=2, alpha=140); cv.ell((kx - 8, y - 8, kx + 8, y + 8), fill=(255, 255, 255, 255)); cv.ell((kx - 3, y - 3, kx + 3, y + 3), fill=A(col, 255))

def field(cv, box, t='', ph='', ic=None, focus=False, mono=False):
    x0, y0, x1, y1 = box; r = 11
    cv.rr(box, r, fill=(4, 9, 26, 110), outline=A(BLUE, 190) if focus else (255, 255, 255, 40), width=1.3 if focus else 1)
    ox = x0 + 14
    if ic: icon(cv, ic, x0 + 20, (y0 + y1) / 2, 15, TXT3, 1.9); ox = x0 + 38
    cv.text(ox, (y0 + y1) / 2, t or ph, 'i:Regular', 13, TXT if t else TXT3, 'lm')
    if focus and t == '': cv.rr((ox, (y0 + y1) / 2 - 8, ox + 1.4, (y0 + y1) / 2 + 8), 1, fill=A(BLUE, 255))

def dropdown(cv, box, t, open_=False, lab=None, sz=13):
    x0, y0, x1, y1 = box; r = 11
    cv.rr(box, r, fill=(255, 255, 255, 22 if not open_ else 34), outline=A(BLUE, 170) if open_ else (255, 255, 255, 46), width=1)
    cv.text(x0 + 14, (y0 + y1) / 2, t, 'i:Medium', sz, TXT, 'lm')
    if lab: label(cv, x1 - 38 - cv.tw(lab, 'i:SemiBold', 10.5) - 18, (y0 + y1) / 2 - 10, lab, lab.lower())
    icon(cv, 'up' if open_ else 'down', x1 - 18, (y0 + y1) / 2, 15, TXT2, 2)

def chip(cv, x, y, t, active=False, h=26):
    w = cv.tw(t, 'i:SemiBold', 11.5) + 26
    if active: cv.grad((x, y, x + w, y + h), h / 2, (98, 140, 255), (52, 88, 230)); cv.text(x + w / 2, y + h / 2, t, 'i:SemiBold', 11.5, (255, 255, 255), 'mm')
    else: cv.rr((x, y, x + w, y + h), h / 2, fill=(255, 255, 255, 18), outline=(255, 255, 255, 40), width=1); cv.text(x + w / 2, y + h / 2, t, 'i:SemiBold', 11.5, TXT2, 'mm')
    return w

def avatar(cv, cx, cy, r, seed=1, ring=None, placeholder=True):
    """Placeholder slot: the Microsoft account profile picture goes here (no icon yet)."""
    cv.ell((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 22), outline=(255, 255, 255, 80), width=1)
    if ring: cv.ell((cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2), outline=ring, width=1.6)

def loader_tile(cv, x, y, kind, selected=False, sz=44):
    cv.rr((x, y, x + sz, y + sz), 11, fill=(255, 255, 255, 18 if not selected else 30), outline=A(GREEN, 230) if selected else (255, 255, 255, 36), width=1.6 if selected else 1)
    cx, cy = x + sz / 2, y + sz / 2
    if kind == 'bedrock':
        rnd = random.Random(7); n = 12; px = (sz - 12) / n
        for i in range(n):
            for j in range(n):
                v = rnd.choice([52, 64, 78, 92, 108, 124]) if rnd.random() > .15 else rnd.choice([28, 34])
                cv.rr((x + 6 + i * px, y + 6 + j * px, x + 6 + (i + 1) * px + .4, y + 6 + (j + 1) * px + .4), 0, fill=(v, v, v + 6, 255))
        cv.rr((x + 6, y + 6, x + sz - 6, y + sz - 6), 2, outline=(20, 20, 26, 255), width=1.5)
    elif kind == 'rust':
        for i in range(12):
            a = i * math.pi / 6; px, py = cx + 11 * math.cos(a), cy + 11 * math.sin(a); cv.ell((px - 2.4, py - 2.4, px + 2.4, py + 2.4), fill=(222, 165, 132, 255))
        cv.ell((cx - 10, cy - 10, cx + 10, cy + 10), fill=(222, 165, 132, 255)); cv.ell((cx - 7.2, cy - 7.2, cx + 7.2, cy + 7.2), fill=(34, 22, 18, 255))
        cv.text(cx, cy + .5, 'R', 'p:Bold', 12, (222, 165, 132), 'mm')
    elif kind == 'bolt':
        cv.ell((cx - 15, cy - 15, cx + 15, cy + 15), fill=(255, 208, 64, 38)); icon(cv, 'bolt', cx, cy, 26, YELLOW, 2)
    if selected:
        cv.ell((x - 5, y - 5, x + 9, y + 9), fill=A(GREEN, 255), outline=(10, 18, 40, 255), width=1.5); icon(cv, 'check', x + 2, y + 2, 9, (6, 36, 18), 3)

def pill(cv, box, fill=(255, 255, 255, 18), outline=(255, 255, 255, 40)):
    cv.rr(box, (box[3] - box[1]) / 2, fill=fill, outline=outline, width=1)

def section_title(cv, x, y, t, sub=None):
    cv.text(x, y, t, 'p:Medium', 15, TXT, 'lm')
    if sub: cv.text(x, y + 19, sub, 'i:Regular', 11.5, TXT2, 'lm')

def scrollbar(cv, x, y0, y1, pos=0.0, size=.35):
    cv.rr((x, y0, x + 4, y1), 2, fill=(255, 255, 255, 18)); h = (y1 - y0) * size; yy = y0 + (y1 - y0 - h) * pos; cv.rr((x, yy, x + 4, yy + h), 2, fill=(255, 255, 255, 90))

def apple(cv, x, y, w, alpha=1.0):
    cv.paste(Image.open(os.path.join(ROOT, 'assets', 'apple_logo.png')), x, y, w, w, alpha)

def wrap(cv, x, y, text, fn, sz, fill, maxw, lh, anchor='m'):
    lines, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if cv.tw(t, fn, sz) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    for i, l in enumerate(lines): cv.text(x, y + i * lh, l, fn, sz, fill, anchor + 'm')
    return len(lines)

def dashed(cv, box, col, dash=6, gap=4, width=1.5):
    x0, y0, x1, y1 = box
    for (ax, ay, bx, by) in [(x0, y0, x1, y0), (x0, y1, x1, y1), (x0, y0, x0, y1), (x1, y0, x1, y1)]:
        L = math.hypot(bx - ax, by - ay); n = int(L // (dash + gap)) + 1
        for i in range(n):
            t0 = i * (dash + gap) / L; t1 = min(1, (i * (dash + gap) + dash) / L)
            cv.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], col, width)
