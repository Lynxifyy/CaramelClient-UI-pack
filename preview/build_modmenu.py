import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from modmenu import *
out = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'previews', 'mod_menu'); os.makedirs(out, exist_ok=True)
for n, f in [('01_mods', mods_tab), ('02_module_settings', module_settings), ('03_replay', replay_tab), ('04_cosmetics_studio', studio_tab), ('05_vc', vc_tab), ('06_settings', settings_tab), ('07_edit_hud_layout', hud_editor)]:
    f().save(os.path.join(out, n + '.png')); print(n)
