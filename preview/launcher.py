from lib import *
W, H = 1280, 800
VERSIONS = [('26.62', 'Beta'), ('26.61', 'Beta'), ('26.60', 'Release'), ('26.50', 'Release'), ('26.40', 'Release'), ('26.30', 'Release'), ('26.20', 'Release'),
            ('26.10', 'Release'), ('26.0', 'Release'), ('1.21.140', 'Release'), ('1.21.139', 'Beta'), ('1.21.132', 'Release')]
NAV = ['gamepad', 'puzzle', 'globe', 'cube', 'news', 'cart']

def titlebar(cv, logged=False, running=0, app_menu=False):
    apple(cv, 14, 8, 30); cv.text(52, 22, 'Caramel Client', 'p:Medium', 13.5, TXT, 'lm')
    # Caramel Client menu button (opens the app dropdown)
    cv.rr((168, 11, 190, 33), 8, fill=(255, 255, 255, 34 if app_menu else 14), outline=(255, 255, 255, 46), width=1); icon(cv, 'up' if app_menu else 'down', 179, 22, 13, TXT2, 2)
    pill(cv, (206, 10, 300, 34)); icon(cv, 'rocket', 222, 22, 13, TXT2, 2); cv.text(232, 22, 'Launchpad', 'i:Medium', 11.5, TXT2, 'lm')
    # QUICK PLAY: each tile is a SERVER ICON (replace with the server's icon image)
    cv.text(332, 22, 'Quick play', 'i:Medium', 11, TXT3, 'lm')
    cols = [(245, 167, 66), (74, 120, 255), (47, 211, 107), (255, 84, 104), (150, 110, 255), (74, 200, 230), (255, 140, 60), (120, 130, 255), (240, 110, 160), (90, 220, 170)]
    for i, c in enumerate(cols):
        x = 398 + i * 32; cv.rr((x, 11, x + 26, 37), 8, fill=A(c, 60), outline=A(c, 150), width=1); cv.rr((x + 8, 19, x + 18, 29), 2, fill=A(c, 255))
    # INSTANCES COUNT (number of running instances)
    cv.text(1118, 22, f'{running} instances', 'i:Regular', 11, TXT3, 'rm')
    pill(cv, (1132, 8, 1264, 36)); avatar(cv, 1150, 22, 9)   # <- Microsoft account profile picture goes here
    cv.text(1168, 22, 'Sign in' if not logged else 'Example_Player', 'i:SemiBold', 11.5, TXT, 'lm'); icon(cv, 'down', 1248, 22, 12, TXT3, 2)

def sidebar(cv, active=0):
    cv.glass((14, 52, 70, H - 14), 18, tint=(150, 175, 255, 10), blur=16, sh_alpha=70)
    for i, n in enumerate(NAV):
        cy = 90 + i * 54
        if i == active:
            cv.rr((20, cy - 20, 64, cy + 20), 13, fill=(255, 255, 255, 30), outline=(255, 255, 255, 54), width=1); cv.rr((14, cy - 11, 17, cy + 11), 2, fill=A(CARAMEL, 255))
        icon(cv, n, 42, cy, 22, TXT if i == active else TXT3, 1.8)
    icon(cv, 'gear', 42, H - 48, 22, TXT3, 1.8)

def frame(active=0, logged=False, running=0, app_menu=False):
    cv = Cv(W, H); navy_bg(cv); titlebar(cv, logged, running, app_menu); sidebar(cv, active); return cv

def finish(cv, path):
    cv.clip_round(None, 16); cv.save(path)

def news_card(cv, x, y, w, h, i, title, meta, theme):
    cv.glass((x, y, x + w, y + h), 18, sh_alpha=70, blur=14)
    art = news_art(int(w - 12), 150, i + 2, theme); m = cv.mask((x + 6, y + 6, x + w - 6, y + 156), 13); cv_art = art; cv_art.putalpha(ImageChops.multiply(cv_art.getchannel('A'), m.resize(cv_art.size)))
    cv.paste(cv_art, x + 6, y + 6)
    cv.text(x + 16, y + 176, title, 'p:Medium', 13.5, TXT, 'lm'); cv.text(x + 16, y + 198, meta, 'i:Regular', 11.5, TXT2, 'lm')
    label(cv, x + w - 16, y + 164 - 22 + 8, 'New' if i == 0 else 'Update', 'new' if i == 0 else 'info', anchor='r') if False else None

def home(popup=None, app_menu=False):
    cv = frame(0, app_menu=app_menu)
    X0, X1 = 90, 872
    cv.glass((X0, 52, X1, 372), 24)
    # hero art
    lay = Image.new('RGBA', cv.im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.ellipse((X0 * S + 40, 60 * S, X0 * S + 560, 380 * S), fill=(74, 120, 255, 70)); lay = lay.filter(ImageFilter.GaussianBlur(60 * S)); lay.putalpha(ImageChops.multiply(lay.getchannel('A'), cv.mask((0, 0, W, H), 0)))
    m = Image.new('L', cv.im.size, 0); ImageDraw.Draw(m).rounded_rectangle((X0 * S, 52 * S, X1 * S, 372 * S), 24 * S, fill=255); lay.putalpha(ImageChops.multiply(lay.getchannel('A'), m)); cv.im.alpha_composite(lay)
    apple(cv, X0 + 28, 98, 210, .96)
    rnd = random.Random(4)
    for i in range(9):
        bx, by = X0 + 560 + rnd.randint(0, 200), 80 + rnd.randint(0, 250); s_ = rnd.choice([14, 18, 24]); c = rnd.choice([BLUE, CARAMEL, (110, 200, 255)])
        cv.rr((bx, by, bx + s_, by + s_), 3, fill=A(c, 90), outline=A(c, 190), width=1)
    cx = (X0 + X1) / 2 + 40
    cv.text(cx, 118, 'Ready when you are', 'i:Medium', 12, TXT2, 'mm')
    # launch split button
    bx0, bx1, by0, by1 = cx - 170, cx + 170, 142, 214
    btn_primary(cv, (bx0, by0, bx1, by1), '', 'green', 19)
    cv.text(cx - 26, 169, 'LAUNCH GAME', 'p:Bold', 19, (6, 36, 18), 'mm')
    cv.text(cx - 26, 194, 'Caramel Client 26.2 · Bedrock', 'i:Medium', 10.5, (8, 60, 30, 230), 'mm')
    cv.rr((bx1 - 52, by0 + 10, bx1 - 51, by1 - 10), 0, fill=(6, 60, 30, 110)); icon(cv, 'up' if popup else 'down', bx1 - 26, (by0 + by1) / 2, 18, (6, 44, 22), 2.6)
    x = cx - 179
    for t, ic, w_ in [('Profiles', 'folder', 104), ('Instances', 'sliders', 116), ('Screenshots', 'camera', 130)]:
        btn_glass(cv, (x, 236, x + w_, 270), t, ic, 11.5); x += w_ + 8
    cv.text(cx, 306, 'Last played 2 hours ago · Isolated profile', 'i:Regular', 11.5, TXT3, 'mm')
    # news
    cv.text(X0 + 4, 396, 'Latest news', 'p:Medium', 16, TXT, 'lm'); cv.text(X1 - 4, 396, 'View all news', 'i:SemiBold', 11.5, TXT2, 'rm')
    for i, (t, m_, th) in enumerate([('Caramel Client 26.2 is here', 'Release notes · 2 days ago', 'ember'), ('Example mod updates', 'Mods · 5 days ago', 'night'), ('Cosmetics festival', 'Store · 1 week ago', 'rose')]):
        news_card(cv, X0 + i * 266, 418, 250, 370, i, t, m_, th)
    # friends
    FX = 892; cv.glass((FX, 52, 1266, 372), 24)
    cv.text(FX + 22, 82, 'Friends', 'p:Medium', 16, TXT, 'lm'); cv.text(1244, 82, 'View all', 'i:SemiBold', 11.5, TXT2, 'rm')
    cv.ell((FX + 157, 120, FX + 217, 180), fill=(255, 255, 255, 18), outline=(255, 255, 255, 44), width=1); icon(cv, 'users', FX + 187, 150, 28, TXT2, 1.8)
    cv.text(FX + 187, 214, 'Chat with friends, send game', 'i:Regular', 12.5, TXT2, 'mm'); cv.text(FX + 187, 232, 'invites, and more.', 'i:Regular', 12.5, TXT2, 'mm')
    btn_glass(cv, (FX + 107, 262, FX + 267, 298), 'Add your first friend', 'plus', 12)
    cv.text(FX + 187, 336, 'Friend requests will show up here', 'i:Regular', 11, TXT3, 'mm')
    # promo
    cv.glass((FX, 392, 1266, 788), 24)
    cv.grad((FX + 6, 398, 1260, 640), 20, (245, 167, 66, 70), (74, 120, 255, 10))
    apple(cv, FX + 122, 410, 130, .95)
    cv.text(FX + 187, 568, 'Become a', 'p:Medium', 19, TXT, 'mm'); cv.text(FX + 187, 598, 'Caramel+', 'p:Bold', 24, CARAMEL, 'mm')
    wrap(cv, FX + 187, 642, 'Get access to HoneyLoader, The preloader that Honeyclient uses but for Glowberryclient!', 'i:Regular', 12.5, TXT2, 310, 19)
    btn_primary(cv, (FX + 36, 712, FX + 338, 756), 'Get Caramel+', 'caramel', 13)
    return cv

def launch_card(cv, x, y, version='26.2', loader=0, profile='Isolated profile', open_ver=False, open_prof=False):
    w, h = 372, 250
    cv.glass((x, y, x + w, y + h), 22, sh_alpha=150)
    cv.text(x + 22, y + 38, 'Version', 'p:Medium', 15, TXT, 'lm'); dropdown(cv, (x + w - 22 - 124, y + 20, x + w - 22, y + 56), version, open_ver)
    cv.text(x + 22, y + 98, 'Loaders', 'p:Medium', 15, TXT, 'lm')
    for i, k in enumerate(['bedrock', 'rust', 'bolt']): loader_tile(cv, x + w - 22 - 3 * 44 - 2 * 10 + i * 54, y + 76, k, i == loader)
    cv.rr((x + 22, y + 134, x + w - 22, y + 172), 11, fill=(255, 255, 255, 34 if open_prof else 20), outline=A(BLUE, 170) if open_prof else (255, 255, 255, 40), width=1)
    icon(cv, 'folder', x + 42, y + 153, 16, (80, 190, 255), 2); cv.text(x + 60, y + 153, profile, 'i:Medium', 13, TXT, 'lm'); icon(cv, 'swap', x + w - 44, y + 153, 16, TXT3, 2)
    btn_glass(cv, (x + 22, y + 190, x + 66, y + 234), '', 'gear'); btn_primary(cv, (x + 76, y + 190, x + w - 22, y + 234), 'Launch Game', 'green', 15, 'rocket')

def version_list(cv, x, y, w=300, sel='26.2', query='', rows=7):
    items = [v for v in VERSIONS if query in v[0]][:rows]; h = 64 + len(items) * 36 + 8
    cv.glass((x, y, x + w, y + h), 16, tint=(120, 150, 255, 22), sh_alpha=170)
    field(cv, (x + 12, y + 12, x + w - 12, y + 48), query, 'Search versions', 'search', True)
    for i, (v, l) in enumerate(items):
        ry = y + 58 + i * 36
        if v == sel or (not sel and i == 2): cv.rr((x + 8, ry, x + w - 16, ry + 32), 9, fill=(74, 120, 255, 60), outline=(74, 120, 255, 120), width=1)
        cv.text(x + 22, ry + 16, v, 'i:SemiBold', 13, TXT, 'lm'); label(cv, x + w - 30, ry + 6, l, l.lower(), anchor='r')
    scrollbar(cv, x + w - 10, y + 62, y + h - 10, 0, .3)
    return h

def profile_list(cv, x, y, w=330):
    cv.glass((x, y, x + w, y + 138), 16, tint=(120, 150, 255, 22), sh_alpha=170)
    for i, (t, d, k) in enumerate([('Open Instance Profile', 'Shares worlds and settings', 'unlocked'), ('Isolated Instance Profile', 'Separate files and mods', 'locked')]):
        ry = y + 10 + i * 62
        if i == 1: cv.rr((x + 8, ry, x + w - 8, ry + 56), 11, fill=(74, 120, 255, 46), outline=(74, 120, 255, 110), width=1)
        cv.text(x + 22, ry + 20, t, 'i:SemiBold', 13, TXT, 'lm'); cv.text(x + 22, ry + 40, d, 'i:Regular', 11, TXT2, 'lm'); label(cv, x + w - 20, ry + 8, k.capitalize(), k, anchor='r')

def home_popup(stage):
    cv = home(popup=True); cx = (90 + 872) / 2 + 40
    px, py = cx + 170 - 372 + 20, 216
    cv.shadow((px, py, px + 372, py + 250), 22, alpha=60)
    launch_card(cv, px, py, open_ver=(stage == 'ver'), open_prof=(stage == 'prof'))
    if stage == 'ver': version_list(cv, px + 372 - 22 - 300, py + 60, 300, '26.2', '')
    if stage == 'prof': profile_list(cv, px + 21, py + 178)
    return cv

def field_row(cv, x, y, w, t, d=None):
    cv.text(x, y, t, 'i:SemiBold', 13, TXT, 'lm')
    if d: cv.text(x, y + 18, d, 'i:Regular', 11.5, TXT2, 'lm')

def instance_settings(tab=0):
    cv = home(); cv.rr((0, 0, W, H), 0, fill=(3, 7, 20, 170))
    x, y, w, h = 190, 50, 900, 700; cv.glass((x, y, x + w, y + h), 26, tint=(120, 150, 255, 14), sh_alpha=200)
    cv.text(x + 32, y + 40, 'Instance settings', 'p:Medium', 20, TXT, 'lm'); cv.text(x + 32, y + 64, 'Caramel Client 26.60 · Bedrock · Isolated profile', 'i:Regular', 12, TXT2, 'lm')
    label(cv, x + w - 90, y + 30, 'Locked', 'locked', anchor='r'); btn_glass(cv, (x + w - 64, y + 24, x + w - 24, y + 56), '', 'x')
    cv.rr((x + 24, y + 92, x + w - 24, y + 93), 0, fill=(255, 255, 255, 24))
    for i, (t, ic) in enumerate([('General', 'sliders'), ('Game', 'gamepad'), ('Performance', 'bolt'), ('Mods', 'puzzle'), ('Advanced', 'gear')]):
        ty = y + 112 + i * 46
        if i == tab: cv.rr((x + 20, ty, x + 200, ty + 38), 11, fill=(74, 120, 255, 60), outline=(74, 120, 255, 120), width=1); cv.rr((x + 20, ty + 9, x + 23, ty + 29), 2, fill=A(CARAMEL, 255))
        icon(cv, ic, x + 44, ty + 19, 17, TXT if i == tab else TXT3, 1.9); cv.text(x + 64, ty + 19, t, 'i:SemiBold', 13, TXT if i == tab else TXT2, 'lm')
    cv.rr((x + 216, y + 108, x + 217, y + h - 96), 0, fill=(255, 255, 255, 20))
    cx = x + 244; cw = w - 244 - 32; yy = y + 120
    def title(t, d=None):
        cv.text(cx, yy, t, 'i:SemiBold', 13, TXT, 'lm'); d and cv.text(cx, yy + 18, d, 'i:Regular', 11.5, TXT2, 'lm')
    def toggle_row(t, d, on):
        nonlocal yy
        title(t, d); toggle(cv, cx + cw - 40, yy - 8, on); yy += 54
    def slider_row(t, vt, v, col=BLUE):
        nonlocal yy
        title(t); cv.text(cx + cw, yy, vt, 'i:SemiBold', 13, col, 'rm'); slider(cv, cx, yy + 28, cw, v, col=col); yy += 70
    def dd_row(t, v, lab=None):
        nonlocal yy
        title(t); dropdown(cv, (cx + cw - 220, yy - 18, cx + cw, yy + 20), v, lab=lab); yy += 60
    def field_r(t, v, ph=''):
        nonlocal yy
        title(t); field(cv, (cx, yy + 16, cx + cw, yy + 54), v, ph); yy += 84
    if tab == 0:
        field_r('Instance name', 'Caramel Client 26.60 (example)')
        dd_row('Game version', '26.60', 'Release')
        title('Loader'); [loader_tile(cv, cx + cw - 3 * 44 - 20 + i * 54, yy - 14, k, i == 0) for i, k in enumerate(['bedrock', 'rust', 'bolt'])]; yy += 62
        title('Profile mode', 'Separate files, worlds and mods'); label(cv, cx + cw, yy - 8, 'Locked', 'locked', anchor='r'); yy += 62
        toggle_row('Close launcher on start', 'Hide the launcher while the game runs', True); toggle_row('Show console output', 'Open a log window next to the game', False)
    elif tab == 1:
        slider_row('Render distance', '12 chunks', .55); slider_row('Simulation distance', '8 chunks', .35)
        dd_row('FPS limit', 'Unlimited'); toggle_row('Fullscreen', 'Start in exclusive fullscreen', False); toggle_row('VSync', 'Match your display refresh rate', True)
    elif tab == 2:
        slider_row('Allocated memory', '4 GB', .42, CARAMEL); dd_row('Process priority', 'Normal')
        title('Memory preset'); xx = cx + cw - 250
        for i, t in enumerate(['Low', 'Balanced', 'High']): xx += chip(cv, xx, yy - 13, t, i == 1) + 8
        yy += 54; toggle_row('Use dedicated GPU', 'Prefer your faster graphics card', True); toggle_row('Reduce background tasks', 'Pause downloads while playing', True)
    elif tab == 3:
        btn_glass(cv, (cx, yy - 8, cx + 150, yy + 28), 'Update all', 'rocket', 12); btn_glass(cv, (cx + 160, yy - 8, cx + 330, yy + 28), 'Open mods folder', 'folder', 12); yy += 52
        for i in range(5):
            c = [BLUE, CARAMEL, GREEN, (150, 110, 255), (74, 200, 230)][i]; cv.rr((cx, yy - 8, cx + cw, yy + 42), 13, fill=(255, 255, 255, 14), outline=(255, 255, 255, 30), width=1)
            cv.rr((cx + 12, yy + 2, cx + 40, yy + 30), 8, fill=A(c, 60), outline=A(c, 160), width=1); icon(cv, 'puzzle', cx + 26, yy + 16, 15, c, 2)
            cv.text(cx + 54, yy + 8, f'Example mod {chr(65 + i)}', 'i:SemiBold', 13, TXT, 'lm'); cv.text(cx + 54, yy + 26, 'v1.0.' + str(i), 'i:Regular', 11, TXT2, 'lm'); toggle(cv, cx + cw - 54, yy + 6, i != 3); yy += 58
    else:
        field_r('Launch arguments', '--example-flag', 'Extra launch arguments'); field_r('Pre-launch command', '', 'Runs before the game starts'); field_r('Environment variables', 'KEY=value', '')
        toggle_row('Verbose logging', 'Write detailed logs for troubleshooting', False)
    cv.rr((x + 24, y + h - 84, x + w - 24, y + h - 83), 0, fill=(255, 255, 255, 24))
    by = y + h - 66
    btn_glass(cv, (x + 28, by, x + 168, by + 40), 'Open folder', 'folder'); btn_glass(cv, (x + 178, by, x + 298, by + 40), 'Repair', 'gear'); btn_glass(cv, (x + 308, by, x + 428, by + 40), 'Delete', 'trash', danger=True)
    btn_glass(cv, (x + w - 330, by, x + w - 192, by + 40), 'Reset'); btn_primary(cv, (x + w - 176, by, x + w - 28, by + 40), 'Save changes', 'green', 13)
    return cv

def page_title(cv, t, sub):
    cv.text(100, 86, t, 'p:Bold', 24, TXT, 'lm'); cv.text(100, 114, sub, 'i:Regular', 12.5, TXT2, 'lm')

def mods_tab():
    cv = frame(1); page_title(cv, 'Mods', 'Browse, install and toggle mods for this instance')
    field(cv, (780, 66, 1086, 104), '', 'Search mods', 'search'); btn_glass(cv, (1098, 66, 1262, 104), 'Open mods folder', 'folder', 11.5)
    x = 100
    for i, t in enumerate(['All', 'Installed', 'Performance', 'Visual', 'Utility', 'Fun']): x += chip(cv, x, 134, t, i == 0) + 8
    for i in range(8):
        cx, cy = 100 + (i % 4) * 292, 184 + (i // 4) * 232; w, h = 280, 218
        cv.glass((cx, cy, cx + w, cy + h), 20, sh_alpha=60, blur=14)
        c = [BLUE, CARAMEL, GREEN, (150, 110, 255)][i % 4]; cv.rr((cx + 18, cy + 18, cx + 66, cy + 66), 14, fill=A(c, 50), outline=A(c, 150), width=1)
        icon(cv, ['puzzle', 'bolt', 'map', 'hud'][i % 4], cx + 42, cy + 42, 24, c, 1.9)
        cv.text(cx + 80, cy + 34, f'Example mod {chr(65 + i)}', 'p:Medium', 14, TXT, 'lm'); cv.text(cx + 80, cy + 56, 'by Caramel Team', 'i:Regular', 11.5, TXT2, 'lm')
        cv.text(cx + 18, cy + 92, 'A short example description of what this', 'i:Regular', 12, TXT2, 'lm'); cv.text(cx + 18, cy + 110, 'mod does inside the game.', 'i:Regular', 12, TXT2, 'lm')
        label(cv, cx + 18, cy + 134, 'New' if i == 0 else 'Utility', 'new' if i == 0 else 'info'); cv.rr((cx + 18, cy + 164, cx + w - 18, cy + 165), 0, fill=(255, 255, 255, 22))
        cv.text(cx + 18, cy + 190, 'Enabled' if i % 3 != 1 else 'Disabled', 'i:SemiBold', 12, TXT if i % 3 != 1 else TXT3, 'lm'); toggle(cv, cx + w - 58, cy + 179, i % 3 != 1)
    return cv

def servers_tab():
    cv = frame(2); page_title(cv, 'Servers', 'Featured and saved servers')
    cv.glass((100, 140, 1262, 330), 24); cv.grad((106, 146, 1256, 324), 20, (74, 120, 255, 70), (245, 167, 66, 40), vertical=False)
    cv.text(140, 206, 'Featured: Example Network', 'p:Bold', 24, TXT, 'lm'); cv.text(140, 238, 'Minigames, survival and community events', 'i:Regular', 13, TXT2, 'lm')
    label(cv, 140, 262, '12,408 playing', 'online'); label(cv, 270, 262, '1.21.132 – 26.62', 'ver'); btn_primary(cv, (1040, 216, 1216, 262), 'Join server', 'green', 14, 'play')
    sup = ['1.21.132 – 26.62', '26.0 – 26.62', '1.21.140 – 26.20', '1.21.132 – 26.40']
    for i in range(4):
        y = 354 + i * 100; cv.glass((100, y, 1262, y + 88), 20, sh_alpha=50, blur=12); c = [BLUE, CARAMEL, GREEN, (150, 110, 255)][i]
        # SERVER ICON slot (the colored tile is a placeholder for the server's icon image)
        cv.rr((122, y + 16, 178, y + 72), 14, fill=A(c, 60), outline=A(c, 160), width=1); cv.rr((138, y + 32, 162, y + 56), 3, fill=A(c, 255))
        cv.text(200, y + 34, f'Example Server {i + 1}', 'p:Medium', 15, TXT, 'lm'); cv.text(200, y + 58, f'play.example{i + 1}.net', 'i:Regular', 12, TXT2, 'lm')
        cv.text(560, y + 44, f'{1204 - i * 211:,} online', 'i:SemiBold', 13, TXT, 'lm'); icon(cv, 'wifi', 730, y + 44, 18, GREEN, 2); cv.text(752, y + 44, f'{24 + i * 13} ms', 'i:Medium', 12, TXT2, 'lm')
        label(cv, 860, y + 34, sup[i], 'ver'); btn_glass(cv, (1100, y + 26, 1240, y + 62), 'Join', 'play', 12)
    return cv

def figure(cv, cx, y, s=10):
    for (dx, dy, w, h, c) in [(-2, 0, 4, 4, (250, 214, 180)), (-2, 0, 4, 1.4, (70, 44, 28)), (-2, 4, 4, 6, (245, 167, 66)), (-4, 4, 2, 6, (250, 214, 180)), (2, 4, 2, 6, (250, 214, 180)), (-2, 10, 2, 6, (60, 80, 160)), (0, 10, 2, 6, (60, 80, 160))]:
        cv.rr((cx + dx * s, y + dy * s, cx + (dx + w) * s, y + (dy + h) * s), 0, fill=(*c, 255))
    cv.rr((cx - 2 * s, y + 1.4 * s, cx - 1 * s, y + 2.2 * s), 0, fill=(255, 255, 255, 255)); cv.rr((cx + 0 * s, y + 1.4 * s, cx + 1 * s, y + 2.2 * s), 0, fill=(255, 255, 255, 255))

def cosmetics_tab():
    cv = frame(3); page_title(cv, 'Cosmetics', 'Capes, wings, hats and more')
    cv.glass((100, 140, 420, 788), 24)
    cv.rr((128, 168, 392, 650), 22, fill=(255, 255, 255, 240))       # 3D skin viewer slot
    wrap(cv, 260, 400, 'Where the skin of the 3d skin goes', 'p:Medium', 15, (28, 40, 84), 190, 24)
    btn_glass(cv, (128, 676, 392, 716), 'Save outfit', 'check'); btn_glass(cv, (128, 726, 392, 766), 'Reset view', 'swap')
    x = 444
    for i, t in enumerate(['All', 'Capes', 'Wings', 'Hats', 'Pets']): x += chip(cv, x, 138, t, i == 0) + 8
    w_ = cv.tw('Favorites', 'i:SemiBold', 11.5) + 44; cv.rr((x, 138, x + w_, 164), 13, fill=(255, 255, 255, 18), outline=(255, 255, 255, 40), width=1); icon(cv, 'star_fill', x + 17, 151, 13, CARAMEL, 1.6); cv.text(x + 30, 151, 'Favorites', 'i:SemiBold', 11.5, TXT2, 'lm')
    field(cv, (1000, 132, 1262, 168), '', 'Search cosmetics', 'search')
    favs = {1, 5}
    for i in range(12):
        cx, cy = 444 + (i % 4) * 205, 190 + (i // 4) * 200; w, h = 193, 188; cv.glass((cx, cy, cx + w, cy + h), 18, sh_alpha=40, blur=10)
        c = [BLUE, CARAMEL, GREEN, (150, 110, 255), RED, (74, 200, 230)][i % 6]; cv.grad((cx + 8, cy + 8, cx + w - 8, cy + 120), 12, A(c, 80), A(c, 14))
        cv.rr((cx + w / 2 - 20, cy + 30, cx + w / 2 + 20, cy + 98), 4, fill=A(c, 230), outline=(255, 255, 255, 80), width=1)
        # favorite star button
        on = i in favs; cv.ell((cx + w - 40, cy + 14, cx + w - 12, cy + 42), fill=(8, 14, 36, 150), outline=A(CARAMEL, 200) if on else (255, 255, 255, 60), width=1)
        icon(cv, 'star_fill' if on else 'star', cx + w - 26, cy + 28.5, 15, CARAMEL if on else (230, 236, 255), 1.7)
        cv.text(cx + 14, cy + 144, f'Example {["Cape", "Wings", "Hat"][i % 3]}', 'i:SemiBold', 13, TXT, 'lm')
        if i == 1: label(cv, cx + 14, cy + 156, 'Equipped', 'release', 18)
        elif i % 4 == 3: label(cv, cx + 14, cy + 156, 'Caramel+', 'plus', 18)
        else: cv.text(cx + 14, cy + 166, 'Owned', 'i:Regular', 11.5, TXT2, 'lm')
    return cv

def news_tab():
    cv = frame(4); page_title(cv, 'News', 'Updates, events and community posts')
    cv.glass((100, 140, 760, 560), 24); a = news_art(648, 260, 3, 'ember'); a.putalpha(ImageChops.multiply(a.getchannel('A'), cv.mask((0, 0, 648, 260), 18).resize(a.size))); cv.paste(a, 106, 146)
    label(cv, 128, 428, 'Featured', 'plus'); cv.text(128, 472, 'Caramel Client 26.2 is here', 'p:Bold', 24, TXT, 'lm'); cv.text(128, 506, 'New launcher, faster startup and the redesigned mod menu.', 'i:Regular', 13, TXT2, 'lm'); cv.text(128, 536, 'Read more', 'i:SemiBold', 12.5, CARAMEL, 'lm')
    for i, (t, th) in enumerate([('Example patch notes', 'night'), ('Community spotlight', 'mint'), ('Server of the week', 'sky')]):
        y = 140 + i * 142; cv.glass((780, y, 1262, y + 130), 20, sh_alpha=50, blur=12); a = news_art(150, 106, i + 7, th); a.putalpha(ImageChops.multiply(a.getchannel('A'), cv.mask((0, 0, 150, 106), 12).resize(a.size))); cv.paste(a, 792, y + 12)
        cv.text(966, y + 38, t, 'p:Medium', 15, TXT, 'lm'); cv.text(966, y + 64, 'A short example summary of this post that', 'i:Regular', 12, TXT2, 'lm'); cv.text(966, y + 82, 'wraps onto two lines at most.', 'i:Regular', 12, TXT2, 'lm'); cv.text(966, y + 110, f'{i + 1} day{"s" if i else ""} ago', 'i:Regular', 11, TXT3, 'lm')
    for i in range(3):
        x = 100 + i * 222; cv.glass((x, 580, x + 210, 788), 18, sh_alpha=40, blur=10); a = news_art(198, 100, i + 11, ['rose', 'sky', 'mint'][i]); a.putalpha(ImageChops.multiply(a.getchannel('A'), cv.mask((0, 0, 198, 100), 12).resize(a.size))); cv.paste(a, x + 6, 586)
        cv.text(x + 14, 712, f'Example article {i + 1}', 'i:SemiBold', 13, TXT, 'lm'); cv.text(x + 14, 734, 'Short summary text', 'i:Regular', 11.5, TXT2, 'lm'); cv.text(x + 14, 764, 'Read more', 'i:SemiBold', 11.5, CARAMEL, 'lm')
    return cv

def store_tab():
    cv = frame(5); page_title(cv, 'Store', 'Cosmetics, bundles and Caramel+')
    cv.glass((100, 140, 1262, 300), 24); cv.grad((106, 146, 1256, 294), 20, (245, 167, 66, 90), (74, 120, 255, 20), vertical=False); apple(cv, 130, 150, 140)
    cv.text(300, 206, 'Caramel+', 'p:Bold', 28, TXT, 'lm'); wrap(cv, 300, 240, 'Get access to HoneyLoader, The preloader that Honeyclient uses but for Glowberryclient!', 'i:Regular', 13.5, TXT2, 600, 22, 'l'); btn_primary(cv, (1000, 202, 1230, 250), 'Get Caramel+ · $4.99/mo', 'caramel', 13)
    for i in range(8):
        cx, cy = 100 + (i % 4) * 292, 324 + (i // 4) * 232; w, h = 280, 218; cv.glass((cx, cy, cx + w, cy + h), 20, sh_alpha=50, blur=12)
        c = [BLUE, CARAMEL, GREEN, (150, 110, 255)][i % 4]; cv.grad((cx + 8, cy + 8, cx + w - 8, cy + 120), 14, A(c, 90), A(c, 14)); cv.rr((cx + w / 2 - 28, cy + 26, cx + w / 2 + 28, cy + 96), 6, fill=A(c, 235), outline=(255, 255, 255, 90), width=1)
        cv.text(cx + 18, cy + 144, f'Example bundle {i + 1}', 'p:Medium', 14, TXT, 'lm'); cv.text(cx + 18, cy + 166, '3 items included', 'i:Regular', 11.5, TXT2, 'lm')
        cv.text(cx + 18, cy + 194, '$' + str(4 + i) + '.99', 'p:Bold', 15, CARAMEL, 'lm'); btn_glass(cv, (cx + w - 108, cy + 180, cx + w - 18, cy + 208), 'Add to cart', None, 11)
    return cv

def settings_tab():
    cv = frame(0); sidebar(cv, -1); cv.glass((14, 52, 70, H - 14), 18, tint=(150, 175, 255, 10), blur=16, sh_alpha=70)
    for i, n in enumerate(NAV): icon(cv, n, 42, 90 + i * 54, 22, TXT3, 1.8)
    cv.rr((20, H - 68, 64, H - 28), 13, fill=(255, 255, 255, 30), outline=(255, 255, 255, 54), width=1); cv.rr((14, H - 59, 17, H - 37), 2, fill=A(CARAMEL, 255)); icon(cv, 'gear', 42, H - 48, 22, TXT, 1.8)
    page_title(cv, 'Settings', 'Launcher preferences')
    cv.glass((100, 140, 640, 788), 24); cv.glass((660, 140, 1262, 788), 24)
    cv.text(128, 176, 'Appearance', 'p:Medium', 16, TXT, 'lm'); cv.text(128, 214, 'Accent color', 'i:SemiBold', 13, TXT, 'lm')
    for i, c in enumerate([CARAMEL, BLUE, GREEN, (150, 110, 255), RED, (74, 200, 230)]):
        cx = 138 + i * 52; cv.ell((cx - 17, 240, cx + 17, 274), fill=A(c, 255), outline=(255, 255, 255, 230) if i == 0 else (255, 255, 255, 40), width=2)
    cv.text(128, 318, 'Glass blur strength', 'i:SemiBold', 13, TXT, 'lm'); cv.text(612, 318, '24', 'i:SemiBold', 13, BLUE, 'rm'); slider(cv, 128, 348, 484, .6)
    cv.text(128, 392, 'Interface scale', 'i:SemiBold', 13, TXT, 'lm'); cv.text(612, 392, '100%', 'i:SemiBold', 13, BLUE, 'rm'); slider(cv, 128, 422, 484, .4)
    cv.text(128, 466, 'Language', 'i:SemiBold', 13, TXT, 'lm'); dropdown(cv, (392, 448, 612, 486), 'English (US)')
    for i, (t, d, on) in enumerate([('Reduce motion', 'Turn off launcher animations', False), ('Transparent window', 'Let the desktop show through', True), ('Show news on home', 'Latest news row on Home', True)]):
        y = 530 + i * 70; cv.text(128, y, t, 'i:SemiBold', 13, TXT, 'lm'); cv.text(128, y + 19, d, 'i:Regular', 11.5, TXT2, 'lm'); toggle(cv, 572, y - 8, on)
    cv.text(688, 176, 'Launcher', 'p:Medium', 16, TXT, 'lm')
    for i, (t, d, on) in enumerate([('Open on startup', 'Start Caramel Client with your computer', False), ('Keep launcher open', 'Stay open while the game runs', True), ('Check for updates', 'Notify me about new versions', True), ('Share crash reports', 'Help us fix problems faster', True)]):
        y = 220 + i * 66; cv.text(688, y, t, 'i:SemiBold', 13, TXT, 'lm'); cv.text(688, y + 19, d, 'i:Regular', 11.5, TXT2, 'lm'); toggle(cv, 1196, y - 8, on)
    cv.text(688, 500, 'Game directory', 'i:SemiBold', 13, TXT, 'lm'); field(cv, (688, 518, 1176, 556), 'C:\\Users\\Example\\.caramel', 'Path', 'folder'); btn_glass(cv, (1186, 518, 1236, 556), '', 'folder')
    cv.text(688, 590, 'Download threads', 'i:SemiBold', 13, TXT, 'lm'); cv.text(1236, 590, '8', 'i:SemiBold', 13, CARAMEL, 'rm'); slider(cv, 688, 620, 548, .5, col=CARAMEL)
    btn_glass(cv, (688, 700, 848, 740), 'Check for updates', 'rocket'); btn_glass(cv, (858, 700, 1018, 740), 'Open logs', 'news'); btn_primary(cv, (1090, 700, 1236, 740), 'Save', 'green', 13)
    return cv

def account_popup():
    cv = home(); cv.shadow((926, 44, 1124, 330), 18, alpha=80)
    x, y, w = 888, 44, 238; cv.glass((x, y, x + w, y + 286), 20, tint=(120, 150, 255, 22), sh_alpha=170)
    avatar(cv, x + 38, y + 40, 22, 0, ring=A(GREEN, 255)); cv.text(x + 72, y + 32, 'Example_Player', 'p:Medium', 14, TXT, 'lm'); label(cv, x + 72, y + 46, 'Online', 'online', 18)
    cv.rr((x + 16, y + 78, x + w - 16, y + 79), 0, fill=(255, 255, 255, 26))
    for i, (t, ic, c) in enumerate([('Switch account', 'swap', TXT), ('Add account', 'plus', TXT), ('Skin & cosmetics', 'cube', TXT), ('Account settings', 'gear', TXT), ('Sign out', 'x', RED)]):
        ry = y + 90 + i * 38
        if i == 0: cv.rr((x + 8, ry, x + w - 8, ry + 34), 10, fill=(74, 120, 255, 46), outline=(74, 120, 255, 100), width=1)
        icon(cv, ic, x + 30, ry + 17, 16, c if c == RED else TXT2, 1.9); cv.text(x + 52, ry + 17, t, 'i:Medium', 13, c, 'lm')
    return cv

def add_friend_modal():
    cv = home(); cv.rr((0, 0, W, H), 0, fill=(3, 7, 20, 170)); x, y, w, h = 440, 220, 400, 300; cv.glass((x, y, x + w, y + h), 24, sh_alpha=190)
    cv.text(x + 28, y + 40, 'Add a friend', 'p:Medium', 18, TXT, 'lm'); cv.text(x + 28, y + 64, 'Enter their Caramel or Minecraft username', 'i:Regular', 12, TXT2, 'lm'); btn_glass(cv, (x + w - 60, y + 22, x + w - 22, y + 54), '', 'x')
    field(cv, (x + 28, y + 100, x + w - 28, y + 140), 'Example_Friend', 'Username', 'user', True)
    cv.rr((x + 28, y + 156, x + w - 28, y + 196), 12, fill=A(GREEN, 28), outline=A(GREEN, 100), width=1); icon(cv, 'check', x + 50, y + 176, 15, GREEN, 2.4); cv.text(x + 70, y + 176, 'Example_Friend found', 'i:Medium', 12.5, TXT, 'lm')
    btn_glass(cv, (x + 28, y + 234, x + 168, y + 272), 'Cancel'); btn_primary(cv, (x + 182, y + 234, x + w - 28, y + 272), 'Send request', 'green', 13)
    return cv


# ---------------------------------------------------------------- new menus
def scrim(cv): cv.rr((0, 0, W, H), 0, fill=(3, 7, 20, 170))

def app_menu():
    cv = home(app_menu=True); x, y, w = 14, 42, 262; cv.glass((x, y, x + w, y + 268), 18, tint=(120, 150, 255, 22), sh_alpha=170)
    items = [('Launcher settings', 'gear', TXT2), ('Check for updates', 'rocket', TXT2), ('Release notes', 'news', TXT2), ('Community', 'users', TXT2), ('About Caramel Client', 'info', TXT2)]
    for i, (t, ic, c) in enumerate(items):
        ry = y + 10 + i * 38
        if i == 0: cv.rr((x + 8, ry, x + w - 8, ry + 34), 10, fill=(74, 120, 255, 46), outline=(74, 120, 255, 100), width=1)
        icon(cv, ic, x + 30, ry + 17, 16, c, 1.9); cv.text(x + 52, ry + 17, t, 'i:Medium', 13, TXT, 'lm')
    cv.rr((x + 16, y + 206, x + w - 16, y + 207), 0, fill=(255, 255, 255, 26)); icon(cv, 'x', x + 30, y + 236, 16, RED, 1.9); cv.text(x + 52, y + 236, 'Quit Caramel Client', 'i:Medium', 13, RED, 'lm')
    return cv

def mod_detail():
    cv = mods_tab(); scrim(cv); x, y, w, h = 360, 170, 560, 470; cv.glass((x, y, x + w, y + h), 26, tint=(120, 150, 255, 14), sh_alpha=200)
    btn_glass(cv, (x + w - 56, y + 18, x + w - 20, y + 52), '', 'x')
    cv.rr((x + 32, y + 36, x + 112, y + 116), 22, fill=A(BLUE, 50), outline=A(BLUE, 150), width=1.2); icon(cv, 'puzzle', x + 72, y + 76, 38, BLUE, 1.9)     # mod icon
    cv.text(x + 132, y + 62, 'Example mod A', 'p:Bold', 21, TXT, 'lm'); cv.text(x + 132, y + 90, 'by Caramel Team · v1.0.0', 'i:Regular', 12.5, TXT2, 'lm'); label(cv, x + 132, y + 104, 'Utility', 'info', 18); label(cv, x + 206, y + 104, 'Installed', 'release', 18)
    cv.text(x + 32, y + 150, 'Description', 'p:Medium', 14, TXT2, 'lm')
    wrap(cv, x + 32, y + 184, 'A short example description of what this mod does inside the game. It can run to a few lines, so people know what they are installing before they enable it.', 'i:Regular', 13, TXT, w - 64, 21, 'l')
    for i, (a_, b_) in enumerate([('Size', '1.2 MB'), ('Updated', '3 days ago'), ('Author', 'Caramel Team')]):
        xx = x + 32 + i * 166; cv.rr((xx, y + 262, xx + 154, y + 316), 14, fill=(255, 255, 255, 14), outline=(255, 255, 255, 30), width=1); cv.text(xx + 14, y + 280, a_, 'i:Regular', 11, TXT2, 'lm'); cv.text(xx + 14, y + 300, b_, 'i:SemiBold', 13, TXT, 'lm')
    cv.text(x + 32, y + 346, 'Enabled', 'i:SemiBold', 13, TXT, 'lm'); toggle(cv, x + w - 72, y + 335, True)
    cv.rr((x + 24, y + h - 84, x + w - 24, y + h - 83), 0, fill=(255, 255, 255, 24))
    btn_glass(cv, (x + 32, y + h - 66, x + 192, y + h - 26), 'Remove', 'trash', danger=True); btn_primary(cv, (x + w - 212, y + h - 66, x + w - 32, y + h - 26), 'Edit config', 'blue', 13, 'edit')
    return cv

def screenshots():
    cv = home(); scrim(cv); x, y, w, h = 150, 50, 980, 700; cv.glass((x, y, x + w, y + h), 26, tint=(120, 150, 255, 14), sh_alpha=200)
    cv.text(x + 32, y + 40, 'Screenshots', 'p:Medium', 20, TXT, 'lm'); cv.text(x + 32, y + 64, '12 screenshots · Isolated profile', 'i:Regular', 12, TXT2, 'lm')
    btn_glass(cv, (x + w - 64, y + 24, x + w - 24, y + 56), '', 'x'); btn_glass(cv, (x + w - 214, y + 24, x + w - 76, y + 56), 'Open folder', 'folder', 11.5)
    xx = x + 32
    for i, t in enumerate(['All', 'Today', 'This week']): xx += chip(cv, xx, y + 84, t, i == 0) + 8
    themes = ['sky', 'ember', 'mint', 'night', 'rose', 'sky', 'mint', 'ember', 'night', 'rose', 'sky', 'mint']
    for i in range(12):
        cx, cy = x + 32 + (i % 4) * 232, y + 130 + (i // 4) * 156; art = news_art(216, 118, i + 20, themes[i]); art.putalpha(ImageChops.multiply(art.getchannel('A'), cv.mask((0, 0, 216, 118), 14).resize(art.size))); cv.paste(art, cx, cy)
        if i == 1: cv.rr((cx - 2, cy - 2, cx + 218, cy + 120), 15, outline=A(BLUE, 255), width=2); cv.ell((cx + 186, cy + 10, cx + 208, cy + 32), fill=A(BLUE, 255)); icon(cv, 'check', cx + 197, cy + 21, 12, (255, 255, 255), 2.6)
        else: cv.rr((cx, cy, cx + 216, cy + 118), 14, outline=(255, 255, 255, 40), width=1)
        cv.text(cx + 4, cy + 134, f'2026-11-{10 - i // 2:02d}_21.{10 + i}.12.png', 'i:Regular', 11, TXT2, 'lm')
    cv.rr((x + 24, y + h - 84, x + w - 24, y + h - 83), 0, fill=(255, 255, 255, 24))
    cv.text(x + 32, y + h - 44, '1 selected', 'i:SemiBold', 13, TXT, 'lm'); btn_glass(cv, (x + w - 462, y + h - 64, x + w - 322, y + h - 24), 'Copy', 'copy'); btn_glass(cv, (x + w - 312, y + h - 64, x + w - 172, y + h - 24), 'Open', 'folder'); btn_glass(cv, (x + w - 162, y + h - 64, x + w - 32, y + h - 24), 'Delete', 'trash', danger=True)
    return cv

def friends_modal():
    cv = home(); scrim(cv); x, y, w, h = 330, 50, 620, 700; cv.glass((x, y, x + w, y + h), 26, tint=(120, 150, 255, 14), sh_alpha=200)
    cv.text(x + 32, y + 40, 'Friends', 'p:Medium', 20, TXT, 'lm'); btn_glass(cv, (x + w - 64, y + 24, x + w - 24, y + 56), '', 'x'); btn_primary(cv, (x + w - 222, y + 24, x + w - 76, y + 56), 'Add friend', 'blue', 12, 'plus')
    xx = x + 32
    for i, t in enumerate(['All', 'Requests', 'Blocked']): xx += chip(cv, xx, y + 84, t, i == 0) + 8
    field(cv, (x + 32, y + 124, x + w - 32, y + 162), '', 'Search friends', 'search')
    def sect(t, yy): cv.text(x + 32, yy, t, 'i:SemiBold', 12, TXT2, 'lm')
    def row(yy, n, st, online):
        cv.rr((x + 24, yy, x + w - 24, yy + 62), 14, fill=(255, 255, 255, 12), outline=(255, 255, 255, 26), width=1)
        avatar(cv, x + 58, yy + 31, 17, ring=A(GREEN, 255) if online else None); cv.text(x + 88, yy + 24, n, 'i:SemiBold', 13.5, TXT, 'lm'); cv.text(x + 88, yy + 43, st, 'i:Regular', 11.5, GREEN if online else TXT3, 'lm')
        if online: btn_glass(cv, (x + w - 188, yy + 14, x + w - 84, yy + 48), 'Invite', 'plus', 11.5)
        btn_glass(cv, (x + w - 70, yy + 14, x + w - 38, yy + 48), '', 'dots')
    sect('Online · 2', y + 192)
    row(y + 208, 'Example_Friend1', 'Playing Caramel Client 26.60', True); row(y + 278, 'Example_Friend2', 'In the launcher', True)
    sect('Offline · 3', y + 372)
    for i in range(3): row(y + 388 + i * 70, f'Example_Friend{i + 3}', f'Last seen {i + 1}h ago', False)
    return cv

def add_account():
    cv = home(); scrim(cv); x, y, w, h = 410, 130, 460, 520; cv.glass((x, y, x + w, y + h), 26, tint=(120, 150, 255, 14), sh_alpha=200)
    cv.text(x + 32, y + 40, 'Add account', 'p:Medium', 20, TXT, 'lm'); cv.text(x + 32, y + 64, 'Sign in with the Microsoft account that owns Minecraft', 'i:Regular', 12, TXT2, 'lm'); btn_glass(cv, (x + w - 64, y + 24, x + w - 24, y + 56), '', 'x')
    cv.rr((x + 32, y + 100, x + w - 32, y + 156), 16, fill=(255, 255, 255, 240))
    for i, c in enumerate([(242, 80, 34), (127, 186, 0), (0, 164, 239), (255, 185, 0)]): cv.rr((x + 120 + (i % 2) * 12, y + 117 + (i // 2) * 12, x + 130 + (i % 2) * 12, y + 127 + (i // 2) * 12), 1, fill=(*c, 255))
    cv.text(x + 160, y + 128, 'Sign in with Microsoft', 'i:SemiBold', 14.5, (28, 36, 70), 'lm')
    cv.rr((x + 32, y + 186, x + 150, y + 187), 0, fill=(255, 255, 255, 30)); cv.text(x + w / 2, y + 186, 'or use a device code', 'i:Regular', 11.5, TXT3, 'mm'); cv.rr((x + w - 150, y + 186, x + w - 32, y + 187), 0, fill=(255, 255, 255, 30))
    cv.rr((x + 32, y + 218, x + w - 32, y + 318), 18, fill=(4, 9, 26, 120), outline=(255, 255, 255, 40), width=1); cv.text(x + w / 2, y + 258, 'ABCD-1234', 'p:Bold', 30, TXT, 'mm', track=3); cv.text(x + w / 2, y + 296, 'Code expires in 14:52', 'i:Regular', 11.5, TXT2, 'mm')
    wrap(cv, x + w / 2, y + 346, 'Open microsoft.com/link on any device and enter this code.', 'i:Regular', 12.5, TXT2, 360, 19); btn_glass(cv, (x + w / 2 - 80, y + 384, x + w / 2 + 80, y + 422), 'Copy code', 'copy')
    cv.rr((x + 24, y + h - 84, x + w - 24, y + h - 83), 0, fill=(255, 255, 255, 24)); btn_glass(cv, (x + 32, y + h - 62, x + 172, y + h - 24), 'Cancel'); cv.text(x + w - 32, y + h - 43, 'Waiting for sign-in…', 'i:Medium', 12, TXT2, 'rm')
    return cv

def account_settings():
    cv = home(); scrim(cv); x, y, w, h = 280, 60, 720, 680; cv.glass((x, y, x + w, y + h), 26, tint=(120, 150, 255, 14), sh_alpha=200)
    cv.text(x + 32, y + 40, 'Account settings', 'p:Medium', 20, TXT, 'lm'); btn_glass(cv, (x + w - 64, y + 24, x + w - 24, y + 56), '', 'x'); cv.rr((x + 24, y + 80, x + w - 24, y + 81), 0, fill=(255, 255, 255, 24))
    avatar(cv, x + 84, y + 150, 44)      # Microsoft account profile picture goes here
    cv.text(x + 150, y + 134, 'Example_Player', 'p:Bold', 19, TXT, 'lm'); cv.text(x + 150, y + 160, 'example@outlook.com', 'i:Regular', 12.5, TXT2, 'lm'); label(cv, x + 150, y + 176, 'Microsoft account linked', 'online', 20)
    btn_glass(cv, (x + w - 244, y + 130, x + w - 32, y + 168), 'Manage on Microsoft', 'globe', 11.5)
    cv.text(x + 32, y + 250, 'Privacy', 'p:Medium', 14, TXT2, 'lm')
    for i, (t, d, on) in enumerate([('Show my online status', 'Friends can see when you are playing', True), ('Allow friend requests', 'Anyone can send you a request', True), ('Share what I am playing', 'Show your server and version', False)]):
        yy = y + 296 + i * 58; cv.text(x + 32, yy, t, 'i:SemiBold', 13, TXT, 'lm'); cv.text(x + 32, yy + 18, d, 'i:Regular', 11.5, TXT2, 'lm'); toggle(cv, x + w - 72, yy - 8, on)
    cv.text(x + 32, y + 490, 'Default account', 'i:SemiBold', 13, TXT, 'lm'); dropdown(cv, (x + w - 252, y + 472, x + w - 32, y + 510), 'Example_Player')
    cv.rr((x + 24, y + h - 84, x + w - 24, y + h - 83), 0, fill=(255, 255, 255, 24)); btn_glass(cv, (x + 32, y + h - 66, x + 172, y + h - 26), 'Sign out', 'x', danger=True); btn_primary(cv, (x + w - 180, y + h - 66, x + w - 32, y + h - 26), 'Save', 'green', 13)
    return cv
