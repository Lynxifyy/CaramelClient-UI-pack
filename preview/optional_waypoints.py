"""OPTIONAL: preview of a future Waypoints mod menu. Not part of the core UI pack."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from modmenu import *
cv = shell(0, [('WAYPOINTS', 'map')]); x0 = MX + 28
cv.glass((x0, MY + 84, x0 + 600, MY + MH - 28), 16, sh_alpha=30, blur=10); cv.text(x0 + 22, MY + 114, 'Waypoints', 'p:Medium', 14, TXT, 'lm'); btn_primary(cv, (x0 + 430, MY + 98, x0 + 582, MY + 130), 'Add waypoint', 'blue', 11.5, 'plus')
for i, (n, c) in enumerate([('Example base', CARAMEL), ('Example mine', BLUE), ('Example portal', (150, 110, 255))]):
    y = MY + 150 + i * 62; cv.rr((x0 + 16, y, x0 + 584, y + 54), 13, fill=(255, 255, 255, 14), outline=(255, 255, 255, 32), width=1); cv.rr((x0 + 28, y + 12, x0 + 58, y + 42), 9, fill=A(c, 60), outline=A(c, 170), width=1); icon(cv, 'map', x0 + 43, y + 27, 16, c, 2)
    cv.text(x0 + 70, y + 20, n, 'i:SemiBold', 13, TXT, 'lm'); cv.text(x0 + 70, y + 38, 'X 128  Y 64  Z -230 · Overworld', 'i:Regular', 11, TXT2, 'lm'); toggle(cv, x0 + 528, y + 16, i != 2)
out = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'imgui', 'optional', 'waypoints_preview'); os.makedirs(out, exist_ok=True); cv.save(os.path.join(out, 'waypoints_menu.png'))
