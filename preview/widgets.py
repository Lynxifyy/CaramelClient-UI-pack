import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from launcher import VERSIONS, version_list, profile_list
OUT = os.path.join(ROOT, 'previews', 'widget_packs'); ICO = os.path.join(ROOT, 'previews', 'icon_pack'); os.makedirs(OUT, exist_ok=True); os.makedirs(ICO, exist_ok=True)
def sheet(w, h, title, sub):
    cv = Cv(w, h); navy_bg(cv); cv.text(40, 48, title, 'p:Bold', 24, TXT, 'lm'); cv.text(40, 78, sub, 'i:Regular', 12.5, TXT2, 'lm'); return cv
def cap(cv, x, y, t): cv.text(x, y, t, 'i:Medium', 11, TXT3, 'lm')

def buttons():
    cv = sheet(1000, 640, 'Buttons', 'Primary, glass, danger, icon and disabled states')
    cap(cv, 40, 120, 'Primary'); btn_primary(cv, (40, 134, 220, 186), 'Launch Game', 'green', 15, 'rocket'); btn_primary(cv, (240, 134, 400, 186), 'Caramel+', 'caramel', 14); btn_primary(cv, (420, 134, 580, 186), 'Continue', 'blue', 14); btn_primary(cv, (600, 134, 760, 186), 'Delete', 'red', 14)
    cap(cv, 40, 230, 'Primary, compact'); btn_primary(cv, (40, 244, 160, 280), 'Save', 'green', 12.5); btn_primary(cv, (176, 244, 296, 280), 'Install', 'blue', 12.5); btn_primary(cv, (312, 244, 472, 280), 'Get Caramel+', 'caramel', 12.5)
    cap(cv, 40, 324, 'Glass'); btn_glass(cv, (40, 338, 180, 378), 'Open folder', 'folder'); btn_glass(cv, (196, 338, 336, 378), 'Add friend', 'plus', active=True); btn_glass(cv, (352, 338, 492, 378), 'Delete', 'trash', danger=True); btn_glass(cv, (508, 338, 648, 378), 'Cancel')
    cap(cv, 40, 422, 'Icon buttons')
    for i, ic in enumerate(['gear', 'x', 'bell', 'search', 'plus', 'swap']): btn_glass(cv, (40 + i * 56, 436, 88 + i * 56, 484), '', ic)
    cap(cv, 40, 528, 'Disabled')
    cv.rr((40, 542, 200, 582), 12, fill=(255, 255, 255, 10), outline=(255, 255, 255, 22), width=1); cv.text(120, 562, 'Unavailable', 'i:SemiBold', 12.5, (255, 255, 255, 70), 'mm')
    cap(cv, 240, 528, 'Segmented / tabs')
    cv.rr((240, 542, 540, 580), 19, fill=(255, 255, 255, 16), outline=(255, 255, 255, 36), width=1)
    for i, t in enumerate(['Mods', 'Settings', 'Waypoints']):
        x0 = 244 + i * 98
        if i == 0: cv.grad((x0, 546, x0 + 96, 576), 15, (98, 140, 255), (52, 88, 230)); cv.text(x0 + 48, 561, t, 'i:Bold', 12, (255, 255, 255), 'mm')
        else: cv.text(x0 + 48, 561, t, 'i:Bold', 12, TXT2, 'mm')
    return cv

def inputs():
    cv = sheet(1000, 640, 'Inputs & controls', 'Toggles, checkboxes, radios, sliders, text fields')
    cap(cv, 40, 120, 'Toggle'); toggle(cv, 40, 134, True); toggle(cv, 100, 134, False)
    cap(cv, 220, 120, 'Checkbox'); checkbox(cv, 220, 134, True); checkbox(cv, 252, 134, False)
    cap(cv, 340, 120, 'Radio'); radio(cv, 340, 134, True); radio(cv, 372, 134, False)
    cap(cv, 40, 210, 'Slider (blue)'); slider(cv, 40, 244, 400, .55); cap(cv, 40, 290, 'Slider (caramel)'); slider(cv, 40, 324, 400, .3, col=CARAMEL)
    cap(cv, 40, 370, 'Text field'); field(cv, (40, 384, 340, 422), '', 'Instance name'); field(cv, (40, 436, 340, 474), 'Caramel Client', focus=True); field(cv, (40, 488, 340, 526), '', 'Search', 'search')
    cap(cv, 520, 120, 'Chips'); x = 520
    for i, t in enumerate(['All', 'New', 'HUD', 'Server']): x += chip(cv, x, 134, t, i == 0) + 8
    cap(cv, 520, 210, 'Avatars')
    for i in range(5): avatar(cv, 540 + i * 50, 258, 18, i, ring=A(GREEN, 255) if i == 0 else None)
    cap(cv, 520, 330, 'Scrollbar'); cv.rr((520, 344, 524, 444), 2, fill=(255, 255, 255, 18)); cv.rr((520, 360, 524, 400), 2, fill=(255, 255, 255, 90))
    cap(cv, 600, 330, 'Color swatches')
    for i, c in enumerate([CARAMEL, BLUE, GREEN, (150, 110, 255), RED]): cv.ell((606 + i * 40, 352, 632 + i * 40, 378), fill=(*c, 255), outline=(255, 255, 255, 230) if i == 0 else (255, 255, 255, 50), width=2)
    return cv

def dropdowns():
    cv = sheet(1000, 760, 'Dropdowns', 'Version list with search, profile picker, closed and open states')
    cap(cv, 40, 120, 'Closed'); dropdown(cv, (40, 134, 220, 172), '26.2'); dropdown(cv, (240, 134, 440, 172), 'Unlimited')
    cap(cv, 40, 210, 'Open version dropdown (search + labels)'); version_list(cv, 40, 224, 300, '26.60', '', 9)
    cap(cv, 380, 210, 'Filtered by search'); version_list(cv, 380, 224, 300, '1.21.132', '1.21', 3)
    cap(cv, 380, 440, 'Profile picker'); profile_list(cv, 380, 454, 330)
    return cv

def labels():
    cv = sheet(1000, 400, 'Labels', 'Status labels: release, beta, locked, unlocked and more')
    x = 40
    for t, k in [('Release', 'release'), ('Beta', 'beta'), ('Locked', 'locked'), ('Unlocked', 'unlocked'), ('New', 'new'), ('Online', 'online'), ('Caramel+', 'plus'), ('Utility', 'info'), ('1.21.132 – 26.62', 'ver')]: x += label(cv, x, 130, t, k) + 14
    cap(cv, 40, 190, 'Large'); x = 40
    for t, k in [('Release', 'release'), ('Beta', 'beta'), ('Locked', 'locked'), ('Unlocked', 'unlocked')]: x += label(cv, x, 206, t, k, h=26) + 14
    return cv

def loaders():
    cv = sheet(1000, 360, 'Loader pack', 'Bedrock, Rust and Lightning, unselected and selected')
    for i, k in enumerate(['bedrock', 'rust', 'bolt']): loader_tile(cv, 60 + i * 80, 140, k, False, 56); loader_tile(cv, 60 + i * 80, 230, k, True, 56)
    cap(cv, 330, 168, 'Unselected'); cap(cv, 330, 258, 'Selected')
    return cv

def toasts():
    cv = sheet(1000, 520, 'Tooltips, toasts & modals', 'Feedback surfaces')
    cv.glass((40, 130, 360, 190), 16); cv.rr((58, 148, 90, 172), 8, fill=A(GREEN, 50)); icon(cv, 'check', 74, 160, 14, GREEN, 2.6); cv.text(104, 160, 'Instance saved', 'i:SemiBold', 13, TXT, 'lm')
    cv.glass((40, 206, 360, 266), 16); icon(cv, 'x', 74, 236, 14, RED, 2.6); cv.text(104, 236, 'Could not reach server', 'i:SemiBold', 13, TXT, 'lm')
    cv.glass((40, 282, 200, 322), 12, tint=(120, 150, 255, 24)); cv.text(120, 302, 'Open instance folder', 'i:Medium', 11.5, TXT, 'mm')
    cv.glass((440, 130, 800, 340), 22); cv.text(468, 168, 'Delete instance?', 'p:Medium', 17, TXT, 'lm'); cv.text(468, 198, 'This removes all files for this instance.', 'i:Regular', 12.5, TXT2, 'lm')
    btn_glass(cv, (468, 270, 598, 308), 'Cancel'); btn_primary(cv, (610, 270, 772, 308), 'Delete', 'red', 13)
    return cv

def tokens():
    cv = sheet(1000, 620, 'Design tokens', 'Colors and type used across launcher and mod menu')
    for i, (n, c) in enumerate([('Abyss', BG0), ('Navy', BG1), ('Deep blue', BG2), ('Accent blue', BLUE), ('Caramel', CARAMEL), ('Go green', GREEN), ('Danger', RED), ('Beta orange', ORANGE)]):
        x = 40 + (i % 4) * 236; y = 120 + (i // 4) * 120; cv.rr((x, y, x + 220, y + 70), 14, fill=(*c, 255), outline=(255, 255, 255, 40), width=1); cv.text(x, y + 88, n, 'i:SemiBold', 12.5, TXT, 'lm'); cv.text(x + 220, y + 88, '#%02X%02X%02X' % c, 'i:Regular', 12, TXT2, 'rm')
    cv.text(40, 400, 'Poppins Bold 28', 'p:Bold', 28, TXT, 'lm'); cv.text(40, 444, 'Poppins Medium 16 for titles', 'p:Medium', 16, TXT, 'lm'); cv.text(40, 484, 'Inter SemiBold 13 for controls', 'i:SemiBold', 13, TXT, 'lm'); cv.text(40, 512, 'Inter Regular 12 for supporting text', 'i:Regular', 12, TXT2, 'lm')
    cv.text(560, 400, 'Radii 8 / 11 / 14 / 20 / 24', 'i:Medium', 13, TXT2, 'lm'); cv.text(560, 430, 'Glass: blur 20, tint 6%, hairline top light', 'i:Medium', 13, TXT2, 'lm'); cv.text(560, 460, 'Spacing grid: 4 / 8 / 12 / 16 / 24', 'i:Medium', 13, TXT2, 'lm')
    return cv

def icons():
    names = ['gamepad', 'puzzle', 'globe', 'cube', 'news', 'cart', 'gear', 'user', 'users', 'search', 'down', 'up', 'right', 'left', 'lock', 'unlock', 'bolt', 'x', 'check', 'plus', 'minus', 'square', 'bell', 'swap', 'folder', 'rocket', 'play', 'star', 'dots', 'sliders', 'trash', 'map', 'hud', 'wifi', 'camera', 'mic', 'replay', 'edit', 'copy', 'star_fill', 'info', 'eye']
    cv = sheet(1000, 700, 'Icon pack', f'{len(names)} stroke icons on a 24px grid')
    for i, n in enumerate(names):
        x = 40 + (i % 9) * 106; y = 110 + (i // 9) * 108; cv.rr((x, y, x + 92, y + 92), 16, fill=(255, 255, 255, 14), outline=(255, 255, 255, 34), width=1); icon(cv, n, x + 46, y + 36, 30, TXT, 1.8); cv.text(x + 46, y + 74, n, 'i:Medium', 10.5, TXT2, 'mm')
        c = Cv(128, 128); icon(c, n, 64, 64, 96, (255, 255, 255), 1.8); c.save(os.path.join(ICO, n + '.png'), 2)
    for k in ('bedrock', 'rust', 'bolt'):
        c = Cv(128, 128); loader_tile(c, 8, 8, k, False, 112); c.save(os.path.join(ICO, 'loader_' + k + '.png'))
    return cv

for n, f in [('01_buttons', buttons), ('02_inputs_controls', inputs), ('03_dropdowns', dropdowns), ('04_labels', labels), ('05_loaders', loaders), ('06_toasts_modals', toasts), ('07_design_tokens', tokens), ('08_icon_pack', icons)]:
    f().save(os.path.join(OUT, n + '.png')); print(n)
# app icons
from PIL import Image
a = Image.open(os.path.join(ROOT, 'assets', 'apple_logo.png')); d = os.path.join(ROOT, 'previews', 'app_icon'); os.makedirs(d, exist_ok=True)
for s in (1024, 512, 256, 128, 64, 32): a.resize((s, s), Image.NEAREST if s >= 512 else Image.LANCZOS).save(os.path.join(d, f'caramel_apple_{s}.png'))
