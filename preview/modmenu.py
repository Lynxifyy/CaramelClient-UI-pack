from lib import *
W, H = 1280, 720
MX, MY, MW, MH = 120, 70, 1040, 580

def hud(cv):
    cv.rr((14, 14, 112, 40), 6, fill=(0, 0, 0, 110)); cv.text(26, 27, '144 FPS', 'i:Bold', 12, (255, 255, 255), 'lm')
    cv.rr((14, 48, 150, 74), 6, fill=(0, 0, 0, 110)); cv.text(26, 61, 'Example HUD', 'i:Medium', 12, (255, 255, 255), 'lm')
    cv.rr((W - 168, 14, W - 14, 74), 6, fill=(0, 0, 0, 110)); cv.text(W - 156, 32, 'X: 128  Y: 64', 'i:Medium', 11.5, (255, 255, 255), 'lm'); cv.text(W - 156, 56, 'Z: -230', 'i:Medium', 11.5, (255, 255, 255), 'lm')
    cv.rr((W // 2 - 91, H - 62, W // 2 + 91, H - 22), 4, fill=(0, 0, 0, 120), outline=(255, 255, 255, 80), width=1)
    for i in range(9): cv.rr((W // 2 - 91 + i * 20 + 1, H - 61, W // 2 - 91 + i * 20 + 20, H - 23), 0, outline=(255, 255, 255, 36), width=1)

TABS = [('MODS', 'puzzle'), ('REPLAY', 'replay'), ('COSMETICS', 'cube'), ('VC', 'mic'), ('SETTINGS', 'gear')]

def shell(tab=0, tabs=TABS):
    cv = Cv(W, H); game_bg(cv); hud(cv); cv.rr((0, 0, W, H), 0, fill=(4, 9, 28, 120))
    cv.glass((MX, MY, MX + MW, MY + MH), 18, tint=(120, 150, 255, 14), blur=22, sh_alpha=190)
    apple(cv, MX + 18, MY + 10, 40); cv.text(MX + 66, MY + 31, 'CARAMEL CLIENT', 'p:Bold', 15, TXT, 'lm', track=1.6)
    iw = 112; tw_ = len(tabs) * iw + 8; tx = MX + MW / 2 - tw_ / 2 + 40
    cv.rr((tx, MY + 14, tx + tw_, MY + 48), 17, fill=(255, 255, 255, 16), outline=(255, 255, 255, 36), width=1)
    for i, (t, ic) in enumerate(tabs):
        x0 = tx + 4 + i * iw; on = i == tab; fg = (255, 255, 255) if on else TXT2
        if on: cv.grad((x0, MY + 18, x0 + iw - 2, MY + 44), 13, (98, 140, 255), (52, 88, 230))
        wt = cv.tw(t, 'i:Bold', 10.5) + 20 + 0; st = x0 + (iw - 2) / 2 - wt / 2
        icon(cv, ic, st + 7, MY + 31, 14, fg, 1.9); cv.text(st + 20, MY + 31, t, 'i:Bold', 10.5, fg, 'lm', track=.6)
    btn_glass(cv, (MX + MW - 52, MY + 16, MX + MW - 18, MY + 48), '', 'x')
    cv.rr((MX + 18, MY + 62, MX + MW - 18, MY + 63), 0, fill=(255, 255, 255, 24))
    return cv

def mods_tab():
    cv = shell(0); sx = MX + 18
    cv.text(sx, MY + 86, 'Profiles', 'p:Medium', 13, TXT2, 'lm')
    for i, (t, a) in enumerate([('Default', True), ('PvP', False), ('Survival', False)]):
        y = MY + 104 + i * 42
        cv.rr((sx, y, sx + 200, y + 36), 10, fill=(74, 120, 255, 56) if a else (255, 255, 255, 12), outline=(74, 120, 255, 130) if a else (255, 255, 255, 30), width=1)
        cv.text(sx + 14, y + 18, t, 'i:SemiBold', 12.5, TXT if a else TXT2, 'lm'); icon(cv, 'dots', sx + 180, y + 18, 14, TXT3, 2)
    btn_glass(cv, (sx, MY + 240, sx + 200, MY + 276), 'Save new profile', 'plus', 11.5)
    btn_primary(cv, (sx, MY + MH - 76, sx + 200, MY + MH - 32), 'Edit HUD layout', 'blue', 12.5, 'hud')
    cv.rr((sx + 214, MY + 78, sx + 215, MY + MH - 24), 0, fill=(255, 255, 255, 20))
    x = sx + 238
    for i, t in enumerate(['All', 'New', 'HUD', 'Server', 'Mechanic']): x += chip(cv, x, MY + 78, t, i == 0) + 6
    field(cv, (MX + MW - 18 - 230, MY + 74, MX + MW - 18, MY + 110), '', 'Search modules', 'search')
    gx, gy = sx + 238, MY + 130; w, h = 214, 158
    cv.glass((gx, gy, gx + w, gy + h), 16, sh_alpha=60, blur=10)
    cv.rr((gx + w / 2 - 26, gy + 16, gx + w / 2 + 26, gy + 68), 14, fill=A(BLUE, 46), outline=A(BLUE, 140), width=1); icon(cv, 'hud', gx + w / 2, gy + 42, 26, (140, 175, 255), 1.9)
    cv.text(gx + w / 2, gy + 88, 'Example', 'p:Medium', 14, TXT, 'mm')
    btn_glass(cv, (gx + 14, gy + 110, gx + w - 14 - 52, gy + 142), 'OPTIONS', 'sliders', 10.5)     # OPTIONS button + toggle share one row, same height
    toggle(cv, gx + w - 14 - 40, gy + 115, True)
    return cv

def module_settings():
    cv = mods_tab(); cv.rr((0, 0, W, H), 0, fill=(3, 7, 20, 150))
    x, y, w, h = 380 + 40, 50, 520, 620; cv.glass((x, y, x + w, y + h), 20, tint=(120, 150, 255, 18), sh_alpha=200)
    btn_glass(cv, (x + 18, y + 16, x + 52, y + 50), '', 'left'); cv.text(x + 68, y + 33, 'Example', 'p:Medium', 17, TXT, 'lm'); label(cv, x + w - 78, y + 23, 'HUD', 'new', anchor='r'); toggle(cv, x + w - 66, y + 22, True)
    cv.rr((x + 18, y + 64, x + w - 18, y + 65), 0, fill=(255, 255, 255, 24))
    def row(yy, t, d=None): cv.text(x + 28, yy, t, 'i:SemiBold', 12.5, TXT, 'lm'); d and cv.text(x + 28, yy + 17, d, 'i:Regular', 11, TXT2, 'lm')
    cv.text(x + 28, y + 90, 'Appearance', 'p:Medium', 13, TXT2, 'lm')
    row(y + 126, 'Scale'); cv.text(x + w - 28, y + 126, '1.00x', 'i:SemiBold', 12, BLUE, 'rm'); slider(cv, x + 28, y + 154, w - 56, .45)
    row(y + 190, 'Opacity'); cv.text(x + w - 28, y + 190, '80%', 'i:SemiBold', 12, BLUE, 'rm'); slider(cv, x + 28, y + 218, w - 56, .8)
    row(y + 258, 'Text color')
    for i, c in enumerate([(255, 255, 255), CARAMEL, BLUE, GREEN, RED, (150, 110, 255)]): cx = x + w - 28 - 17 - (5 - i) * 34; cv.ell((cx - 11, y + 248, cx + 11, y + 270), fill=(*c, 255), outline=(255, 255, 255, 230) if i == 0 else (255, 255, 255, 50), width=2)
    row(y + 300, 'Position'); dropdown(cv, (x + w - 28 - 190, y + 284, x + w - 28, y + 318), 'Top left', sz=12)
    cv.text(x + 28, y + 352, 'Behavior', 'p:Medium', 13, TXT2, 'lm')
    for i, (t, on) in enumerate([('Show background', True), ('Text shadow', True), ('Compact mode', False)]):
        yy = y + 386 + i * 36; checkbox(cv, x + 28, yy - 9, on); cv.text(x + 58, yy, t, 'i:Medium', 12.5, TXT, 'lm')
    row(y + 500, 'Keybind'); field(cv, (x + w - 28 - 190, y + 484, x + w - 28, y + 518), 'Right Shift', mono=True)
    cv.rr((x + 18, y + h - 70, x + w - 18, y + h - 69), 0, fill=(255, 255, 255, 24))
    btn_glass(cv, (x + 24, y + h - 54, x + 184, y + h - 18), 'Reset defaults', 'swap', 11.5); btn_primary(cv, (x + w - 164, y + h - 54, x + w - 24, y + h - 18), 'Done', 'green', 12.5)
    return cv

def settings_tab():
    cv = shell(4); x0 = MX + 28; cw = (MW - 84) / 2
    for c in range(2): cv.glass((x0 + c * (cw + 28), MY + 84, x0 + c * (cw + 28) + cw, MY + MH - 28), 16, sh_alpha=30, blur=10)
    L = x0 + 22; R = x0 + cw + 28 + 22; iw = cw - 44
    cv.text(L, MY + 114, 'General', 'p:Medium', 14, TXT, 'lm')
    for i, (t, on) in enumerate([('Auto-join last server', False), ('Show module toggles in chat', True), ('Notifications', True), ('Smooth camera', False)]):
        yy = MY + 160 + i * 46; cv.text(L, yy, t, 'i:Medium', 12.5, TXT, 'lm'); toggle(cv, L + iw - 40, yy - 11, on)
    cv.text(L, MY + 360, 'Menu scale', 'i:Medium', 12.5, TXT, 'lm'); cv.text(L + iw, MY + 360, '100%', 'i:SemiBold', 12, BLUE, 'rm'); slider(cv, L, MY + 388, iw, .4)
    cv.text(L, MY + 430, 'Open menu key', 'i:Medium', 12.5, TXT, 'lm'); field(cv, (L + iw - 150, MY + 414, L + iw, MY + 448), 'Right Shift')
    cv.text(R, MY + 114, 'Appearance', 'p:Medium', 14, TXT, 'lm'); cv.text(R, MY + 160, 'Accent color', 'i:Medium', 12.5, TXT, 'lm')
    for i, c in enumerate([BLUE, CARAMEL, GREEN, (150, 110, 255), RED]): cx = R + iw - 17 - (4 - i) * 38; cv.ell((cx - 13, MY + 148, cx + 13, MY + 174), fill=(*c, 255), outline=(255, 255, 255, 230) if i == 0 else (255, 255, 255, 50), width=2)
    cv.text(R, MY + 206, 'Blur strength', 'i:Medium', 12.5, TXT, 'lm'); cv.text(R + iw, MY + 206, '60%', 'i:SemiBold', 12, BLUE, 'rm'); slider(cv, R, MY + 234, iw, .6)
    cv.text(R, MY + 276, 'Language', 'i:Medium', 12.5, TXT, 'lm'); dropdown(cv, (R + iw - 190, MY + 258, R + iw, MY + 294), 'English (US)', sz=12)
    cv.text(R, MY + 330, 'Font', 'i:Medium', 12.5, TXT, 'lm'); dropdown(cv, (R + iw - 190, MY + 312, R + iw, MY + 348), 'Inter', sz=12)
    for i, (t, on) in enumerate([('Rounded corners', True), ('Animations', True)]): yy = MY + 392 + i * 44; checkbox(cv, R, yy - 9, on); cv.text(R + 30, yy, t, 'i:Medium', 12.5, TXT, 'lm')
    btn_glass(cv, (R, MY + 456, R + 160, MY + 492), 'Reset client', 'swap', 11.5, danger=True)
    return cv


def replay_tab():
    cv = shell(1); x0 = MX + 28; lw = 600
    cv.glass((x0, MY + 84, x0 + lw, MY + MH - 28), 16, sh_alpha=30, blur=10); cv.glass((x0 + lw + 24, MY + 84, MX + MW - 28, MY + MH - 28), 16, sh_alpha=30, blur=10)
    cv.text(x0 + 22, MY + 114, 'Recordings', 'p:Medium', 14, TXT, 'lm'); btn_primary(cv, (x0 + lw - 178, MY + 98, x0 + lw - 18, MY + 130), 'Start recording', 'red', 11.5)
    for i, th in enumerate(['sky', 'ember', 'mint']):
        y = MY + 150 + i * 100; cv.rr((x0 + 16, y, x0 + lw - 16, y + 88), 14, fill=(255, 255, 255, 14), outline=(255, 255, 255, 30), width=1)
        art = news_art(120, 68, i + 31, th); art.putalpha(ImageChops.multiply(art.getchannel('A'), cv.mask((0, 0, 120, 68), 10).resize(art.size))); cv.paste(art, x0 + 26, y + 10)
        cv.text(x0 + 164, y + 28, f'Example replay {i + 1}', 'i:SemiBold', 13.5, TXT, 'lm'); cv.text(x0 + 164, y + 50, f'0{i + 2}:14 · {1.2 + i * .4:.1f} GB · Today', 'i:Regular', 11.5, TXT2, 'lm')
        btn_glass(cv, (x0 + lw - 214, y + 26, x0 + lw - 132, y + 62), 'Play', 'play', 11.5); btn_glass(cv, (x0 + lw - 122, y + 26, x0 + lw - 82, y + 62), '', 'copy'); btn_glass(cv, (x0 + lw - 72, y + 26, x0 + lw - 32, y + 62), '', 'trash', danger=True)
    rx = x0 + lw + 46; rw = MX + MW - 28 - rx - 22
    cv.text(rx, MY + 114, 'Recording', 'p:Medium', 14, TXT, 'lm')
    cv.text(rx, MY + 160, 'Record automatically', 'i:Medium', 12.5, TXT, 'lm'); toggle(cv, rx + rw - 40, MY + 149, False)
    cv.text(rx, MY + 210, 'Buffer length', 'i:Medium', 12.5, TXT, 'lm'); cv.text(rx + rw, MY + 210, '2 min', 'i:SemiBold', 12, BLUE, 'rm'); slider(cv, rx, MY + 238, rw, .3)
    cv.text(rx, MY + 288, 'Quality', 'i:Medium', 12.5, TXT, 'lm'); dropdown(cv, (rx + rw - 150, MY + 270, rx + rw, MY + 306), 'High', sz=12)
    cv.text(rx, MY + 338, 'Hotkey', 'i:Medium', 12.5, TXT, 'lm'); field(cv, (rx + rw - 150, MY + 320, rx + rw, MY + 356), 'F8')
    return cv

def studio_tab():
    cv = shell(2); x0 = MX + 28
    cv.glass((x0, MY + 84, x0 + 300, MY + MH - 28), 16, sh_alpha=30, blur=10)
    cv.rr((x0 + 22, MY + 106, x0 + 278, MY + 400), 20, fill=(255, 255, 255, 240))         # 3D skin viewer slot
    wrap(cv, x0 + 150, MY + 252, 'Where the skin of the 3d skin goes', 'p:Medium', 14, (28, 40, 84), 180, 22)
    cv.text(x0 + 22, MY + 432, 'Rotation', 'i:Medium', 12.5, TXT, 'lm'); slider(cv, x0 + 22, MY + 458, 256, .35)
    btn_glass(cv, (x0 + 22, MY + 484, x0 + 278, MY + 520), 'Reset view', 'swap', 11.5)
    gx = x0 + 324; x = gx
    for i, t in enumerate(['All', 'Capes', 'Wings', 'Hats']): x += chip(cv, x, MY + 84, t, i == 0) + 6
    w_ = cv.tw('Favorites', 'i:SemiBold', 11.5) + 44; cv.rr((x, MY + 84, x + w_, MY + 110), 13, fill=(255, 255, 255, 18), outline=(255, 255, 255, 40), width=1); icon(cv, 'star_fill', x + 17, MY + 97, 13, CARAMEL, 1.6); cv.text(x + 30, MY + 97, 'Favorites', 'i:SemiBold', 11.5, TXT2, 'lm')
    for i in range(6):
        cx, cy = gx + (i % 3) * 218, MY + 126 + (i // 3) * 160; w, h = 208, 148; on = i in (0, 4)
        cv.glass((cx, cy, cx + w, cy + h), 16, sh_alpha=30, blur=8, border=90 if i == 1 else 70)
        if i == 1: cv.rr((cx, cy, cx + w, cy + h), 16, outline=A(BLUE, 230), width=2)
        c = [BLUE, CARAMEL, GREEN][i % 3]; cv.grad((cx + 8, cy + 8, cx + w - 8, cy + 92), 11, A(c, 80), A(c, 12)); cv.rr((cx + w / 2 - 18, cy + 20, cx + w / 2 + 18, cy + 80), 4, fill=A(c, 230), outline=(255, 255, 255, 80), width=1)
        cv.ell((cx + w - 40, cy + 14, cx + w - 14, cy + 40), fill=(8, 14, 36, 150), outline=A(CARAMEL, 200) if on else (255, 255, 255, 60), width=1); icon(cv, 'star_fill' if on else 'star', cx + w - 27, cy + 27, 14, CARAMEL if on else (230, 236, 255), 1.7)
        cv.text(cx + 14, cy + 112, f'Example {["Cape", "Wings", "Hat"][i % 3]}', 'i:SemiBold', 12.5, TXT, 'lm'); cv.text(cx + 14, cy + 132, 'Equipped' if i == 1 else 'Owned', 'i:Regular', 11, GREEN if i == 1 else TXT2, 'lm')
    sx = gx; sy = MY + 456
    cv.glass((sx, sy, MX + MW - 28, MY + MH - 28), 16, sh_alpha=0, blur=8)
    cv.text(sx + 18, sy + 24, 'Editing: Example Wings', 'i:SemiBold', 13, TXT, 'lm'); cv.text(sx + 18, sy + 62, 'Scale', 'i:Medium', 12, TXT2, 'lm'); slider(cv, sx + 70, sy + 62, 250, .5)
    cv.text(sx + 350, sy + 62, 'Tint', 'i:Medium', 12, TXT2, 'lm')
    for i, c in enumerate([(255, 255, 255), CARAMEL, BLUE, GREEN, RED]): cx = sx + 394 + i * 30; cv.ell((cx - 10, sy + 52, cx + 10, sy + 72), fill=(*c, 255), outline=(255, 255, 255, 230) if i == 0 else (255, 255, 255, 50), width=2)
    btn_primary(cv, (MX + MW - 28 - 150, sy + 12, MX + MW - 28 - 14, sy + 46), 'Equip', 'green', 12)
    return cv

def vc_tab():
    cv = shell(3); x0 = MX + 28; cw = (MW - 84) / 2
    for c in range(2): cv.glass((x0 + c * (cw + 28), MY + 84, x0 + c * (cw + 28) + cw, MY + MH - 28), 16, sh_alpha=30, blur=10)
    L = x0 + 22; R = x0 + cw + 28 + 22; iw = cw - 44
    cv.text(L, MY + 114, 'Devices', 'p:Medium', 14, TXT, 'lm')
    cv.text(L, MY + 160, 'Input device', 'i:Medium', 12.5, TXT, 'lm'); dropdown(cv, (L + iw - 230, MY + 142, L + iw, MY + 178), 'Default microphone', sz=12)
    cv.text(L, MY + 210, 'Output device', 'i:Medium', 12.5, TXT, 'lm'); dropdown(cv, (L + iw - 230, MY + 192, L + iw, MY + 228), 'Default speakers', sz=12)
    cv.text(L, MY + 268, 'Microphone volume', 'i:Medium', 12.5, TXT, 'lm'); cv.text(L + iw, MY + 268, '80%', 'i:SemiBold', 12, BLUE, 'rm'); slider(cv, L, MY + 296, iw, .8)
    cv.text(L, MY + 340, 'Output volume', 'i:Medium', 12.5, TXT, 'lm'); cv.text(L + iw, MY + 340, '65%', 'i:SemiBold', 12, BLUE, 'rm'); slider(cv, L, MY + 368, iw, .65)
    cv.text(L, MY + 414, 'Mic test', 'i:Medium', 12.5, TXT, 'lm')
    for i in range(28): c = GREEN if i < 16 else (ORANGE if i < 23 else RED); cv.rr((L + i * (iw / 28), MY + 430, L + i * (iw / 28) + iw / 28 - 3, MY + 450), 2, fill=A(c, 255 if i < 14 else 50))
    cv.text(R, MY + 114, 'Voice chat', 'p:Medium', 14, TXT, 'lm')
    for i, (t, d, on) in enumerate([('Push to talk', 'Hold a key to speak', True), ('Noise suppression', 'Filter background sound', True), ('Proximity chat', 'Hear players near you', True)]):
        yy = MY + 160 + i * 52; cv.text(R, yy, t, 'i:Medium', 12.5, TXT, 'lm'); cv.text(R, yy + 17, d, 'i:Regular', 11, TXT2, 'lm'); toggle(cv, R + iw - 40, yy - 11, on)
    cv.text(R, MY + 330, 'Push to talk key', 'i:Medium', 12.5, TXT, 'lm'); field(cv, (R + iw - 150, MY + 312, R + iw, MY + 348), 'V')
    cv.text(R, MY + 380, 'Proximity range', 'i:Medium', 12.5, TXT, 'lm'); cv.text(R + iw, MY + 380, '24 blocks', 'i:SemiBold', 12, BLUE, 'rm'); slider(cv, R, MY + 408, iw, .45)
    btn_glass(cv, (R, MY + 450, R + 150, MY + 486), 'Mute', 'mic', 11.5); btn_glass(cv, (R + 160, MY + 450, R + 310, MY + 486), 'Deafen', 'x', 11.5, danger=True)
    return cv

def hud_editor():
    cv = Cv(W, H); game_bg(cv); cv.rr((0, 0, W, H), 0, fill=(4, 9, 28, 90))
    for gx_ in range(0, W, 40): cv.line([(gx_, 0), (gx_, H)], (255, 255, 255, 14), 1)
    for gy_ in range(0, H, 40): cv.line([(0, gy_), (W, gy_)], (255, 255, 255, 14), 1)
    els = [('FPS', (14, 14, 112, 40), '144 FPS'), ('Example HUD', (14, 48, 150, 74), 'Example HUD'), ('Coordinates', (W - 168, 14, W - 14, 74), 'X: 128  Y: 64\nZ: -230')]
    for i, (n, b, t) in enumerate(els):
        cv.rr(b, 6, fill=(0, 0, 0, 110)); lines = t.split('\n')
        for j, l in enumerate(lines): cv.text(b[0] + 12, b[1] + 13 + j * 24, l, 'i:Bold' if i == 0 else 'i:Medium', 12, (255, 255, 255), 'lm')
        sel = i == 2; col = A(BLUE, 255) if sel else (255, 255, 255, 150); dashed(cv, (b[0] - 3, b[1] - 3, b[2] + 3, b[3] + 3), col)
        for hx, hy in [(b[0] - 3, b[1] - 3), (b[2] + 3, b[1] - 3), (b[0] - 3, b[3] + 3), (b[2] + 3, b[3] + 3)]: cv.rr((hx - 4, hy - 4, hx + 4, hy + 4), 2, fill=(255, 255, 255, 255), outline=A(BLUE, 255) if sel else (0, 0, 0, 0), width=1.5)
        tx_, ty_ = (b[2] + 14, (b[1] + b[3]) / 2 - 12) if i < 2 else (b[0], b[3] + 10)
        cv.glass((tx_, ty_, tx_ + cv.tw(n, 'i:SemiBold', 11) + 22, ty_ + 24), 8, sh_alpha=0, blur=6); cv.text(tx_ + 11, ty_ + 12, n, 'i:SemiBold', 11, TXT, 'lm')
    cv.glass((W // 2 - 330, 20, W // 2 + 330, 84), 20, sh_alpha=150)
    apple(cv, W // 2 - 318, 26, 34); cv.text(W // 2 - 276, 52, 'Edit HUD layout', 'p:Medium', 14, TXT, 'lm')
    checkbox(cv, W // 2 - 140, 43, True); cv.text(W // 2 - 114, 52, 'Snap to grid', 'i:Medium', 12, TXT, 'lm'); checkbox(cv, W // 2 - 20, 43, True); cv.text(W // 2 + 6, 52, 'Show grid', 'i:Medium', 12, TXT, 'lm')
    btn_glass(cv, (W // 2 + 100, 34, W // 2 + 170, 70), 'Reset', None, 11.5); btn_glass(cv, (W // 2 + 178, 34, W // 2 + 248, 70), 'Cancel', None, 11.5); btn_primary(cv, (W // 2 + 256, 34, W // 2 + 320, 70), 'Save', 'green', 12)
    px, py = W - 290, H - 250; cv.glass((px, py, px + 262, py + 222), 20, sh_alpha=150)
    cv.text(px + 20, py + 28, 'Coordinates', 'p:Medium', 14, TXT, 'lm'); cv.text(px + 20, py + 62, 'X', 'i:Medium', 12, TXT2, 'lm'); field(cv, (px + 38, py + 46, px + 116, py + 78), '1112'); cv.text(px + 134, py + 62, 'Y', 'i:Medium', 12, TXT2, 'lm'); field(cv, (px + 152, py + 46, px + 230, py + 78), '14')
    cv.text(px + 20, py + 110, 'Scale', 'i:Medium', 12, TXT2, 'lm'); cv.text(px + 242, py + 110, '1.00x', 'i:SemiBold', 12, BLUE, 'rm'); slider(cv, px + 20, py + 136, 222, .45)
    btn_glass(cv, (px + 20, py + 164, px + 130, py + 200), 'Hide', 'eye', 11.5); btn_glass(cv, (px + 140, py + 164, px + 242, py + 200), 'Reset', 'swap', 11.5)
    return cv
