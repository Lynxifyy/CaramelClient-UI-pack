import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from launcher import *
out = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'previews', 'launcher'); os.makedirs(out, exist_ok=True)
jobs = [('01_home', home), ('02_home_launch_menu', lambda: home_popup('main')), ('03_launch_menu_version_dropdown', lambda: home_popup('ver')), ('04_launch_menu_profile_dropdown', lambda: home_popup('prof')),
        ('05a_instance_settings_general', lambda: instance_settings(0)), ('05b_instance_settings_game', lambda: instance_settings(1)), ('05c_instance_settings_performance', lambda: instance_settings(2)),
        ('05d_instance_settings_mods', lambda: instance_settings(3)), ('05e_instance_settings_advanced', lambda: instance_settings(4)),
        ('06_tab_mods', mods_tab), ('06b_mod_detail', mod_detail), ('07_tab_servers', servers_tab), ('08_tab_cosmetics', cosmetics_tab), ('09_tab_news', news_tab),
        ('10_tab_store', store_tab), ('11_tab_settings', settings_tab), ('12_popup_account', account_popup), ('13_popup_add_friend', add_friend_modal),
        ('14_menu_app_dropdown', app_menu), ('15_screenshots', screenshots), ('16_friends_view_all', friends_modal), ('17_add_account', add_account), ('18_account_settings', account_settings)]
for n, f in jobs:
    cv = f(); cv.clip_round(None, 16); cv.save(os.path.join(out, n + '.png')); print(n)
