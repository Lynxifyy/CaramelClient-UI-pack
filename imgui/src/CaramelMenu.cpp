#include "CaramelMenu.h"
#include <cstdio>
#include <cmath>

namespace caramel {
using namespace ui;

static const ImVec2 kSize(1040, 580);
static ImDrawList* DL() { return ImGui::GetWindowDrawList(); }
static void At(ImVec2 o, float x, float y) { ImGui::SetCursorScreenPos({o.x + x, o.y + y}); }
static void Txt(ImVec2 o, float x, float y, const char* t, bool strong = true) { TextAt({o.x + x, o.y + y}, strong ? GetFonts().bodyMedium : GetFonts().body, strong ? col::Text() : col::Text2(), t); }
static void Title(ImVec2 o, float x, float y, const char* t) { TextAt({o.x + x, o.y + y}, GetFonts().title, col::Text(), t); }
static void Rule(ImVec2 a, float x0, float x1, float y) { Hairline(a.x + x0, a.x + x1, a.y + y); }
static ImU32 kSwatches[] = {IM_COL32(255, 255, 255, 255), col::Caramel(), col::Blue(), col::Green(), col::Red(), IM_COL32(150, 110, 255, 255)};

// ---- game HUD (stand-in overlays; your real modules draw these) -------------------------------------------------
static void DrawHud(MenuState& s) {
    ImDrawList* d = ImGui::GetBackgroundDrawList();
    for (int i = 0; i < 3; ++i) {
        HudElement& e = s.hud[i]; if (!e.visible) continue; ImVec2 b{e.pos.x + e.size.x * e.scale, e.pos.y + e.size.y * e.scale};
        d->AddRectFilled(e.pos, b, IM_COL32(0, 0, 0, 110), 6.f);
        const char* t = i == 0 ? "144 FPS" : i == 1 ? "Example HUD" : "X: 128  Y: 64";
        d->AddText(GetFonts().bodyBold, 14.f * e.scale, {e.pos.x + 12, e.pos.y + 5}, IM_COL32(255, 255, 255, 255), t);
        if (i == 2) d->AddText(GetFonts().body, 14.f * e.scale, {e.pos.x + 12, e.pos.y + 30}, IM_COL32(255, 255, 255, 255), "Z: -230");
    }
}

// ---- Edit HUD layout: its own overlay with the FPS / Example HUD / Coordinates elements draggable ------------------
static void RenderHudEditor(MenuState& s, ImVec2 display) {
    ImDrawList* d = DL(); d->AddRectFilled({0, 0}, display, IM_COL32(4, 9, 28, 90));
    if (s.showGrid) { for (float x = 0; x < display.x; x += 40) d->AddLine({x, 0}, {x, display.y}, IM_COL32(255, 255, 255, 14)); for (float y = 0; y < display.y; y += 40) d->AddLine({0, y}, {display.x, y}, IM_COL32(255, 255, 255, 14)); }
    for (int i = 0; i < 3; ++i) {
        HudElement& e = s.hud[i]; ImVec2 size{e.size.x * e.scale, e.size.y * e.scale};
        ImGui::SetCursorScreenPos(e.pos); char id[24]; snprintf(id, sizeof id, "hud%d", i); ImGui::InvisibleButton(id, size);
        if (ImGui::IsItemActive()) { ImVec2 dl = ImGui::GetIO().MouseDelta; e.pos.x += dl.x; e.pos.y += dl.y; s.hudSel = i; }
        if (ImGui::IsItemDeactivated() && s.snap) { e.pos.x = roundf(e.pos.x / 20) * 20; e.pos.y = roundf(e.pos.y / 20) * 20; }
        bool sel = s.hudSel == i; ImU32 c = sel ? col::Blue() : col::White(150);
        DashedRect({e.pos.x - 3, e.pos.y - 3}, {e.pos.x + size.x + 3, e.pos.y + size.y + 3}, c);
        ImVec2 corners[4] = {{e.pos.x - 3, e.pos.y - 3}, {e.pos.x + size.x + 3, e.pos.y - 3}, {e.pos.x - 3, e.pos.y + size.y + 3}, {e.pos.x + size.x + 3, e.pos.y + size.y + 3}};
        for (auto& k : corners) { d->AddRectFilled({k.x - 4, k.y - 4}, {k.x + 4, k.y + 4}, IM_COL32(255, 255, 255, 255), 2.f); if (sel) d->AddRect({k.x - 4, k.y - 4}, {k.x + 4, k.y + 4}, col::Blue(), 2.f, 0, 1.5f); }
        // name tag
        ImVec2 tag = i < 2 ? ImVec2(e.pos.x + size.x + 14, e.pos.y + size.y * .5f - 12) : ImVec2(e.pos.x, e.pos.y + size.y + 10);
        ImGui::PushFont(GetFonts().bodyBold); float tw = ImGui::CalcTextSize(e.name).x; ImGui::PopFont();
        Glass(tag, {tag.x + tw + 22, tag.y + 24}, 8, false); TextAt({tag.x + 11, tag.y + 12}, GetFonts().bodyBold, col::Text(), e.name);
    }
    // toolbar
    float cx = display.x * .5f; ImVec2 a{cx - 330, 20}; Glass(a, {a.x + 660, a.y + 64}, 20, true);
    TextAt({a.x + 54, a.y + 32}, GetFonts().title, col::Text(), "Edit HUD layout");
    ImGui::SetCursorScreenPos({a.x + 190, a.y + 23}); CheckBox("snap", "Snap to grid", &s.snap); ImGui::SetCursorScreenPos({a.x + 310, a.y + 23}); CheckBox("grid", "Show grid", &s.showGrid);
    ImGui::SetCursorScreenPos({a.x + 430, a.y + 14}); if (GlassButton("hreset", "Reset", {70, 36})) { s.hud[0].pos = {14, 14}; s.hud[1].pos = {14, 48}; s.hud[2].pos = {display.x - 168, 14}; }
    ImGui::SetCursorScreenPos({a.x + 508, a.y + 14}); if (GlassButton("hcancel", "Cancel", {70, 36})) s.hudEditing = false;
    ImGui::SetCursorScreenPos({a.x + 586, a.y + 14}); if (PrimaryButton("hsave", "Save", {64, 36}, Tone::Green)) s.hudEditing = false;
    // selected element panel
    HudElement& e = s.hud[s.hudSel]; ImVec2 p{display.x - 290, display.y - 250}; Glass(p, {p.x + 262, p.y + 222}, 20, true);
    TextAt({p.x + 20, p.y + 28}, GetFonts().title, col::Text(), e.name);
    char buf[48]; snprintf(buf, sizeof buf, "X %d    Y %d", (int)e.pos.x, (int)e.pos.y); TextAt({p.x + 20, p.y + 66}, GetFonts().bodyMedium, col::Text2(), buf);
    TextAt({p.x + 20, p.y + 110}, GetFonts().body, col::Text2(), "Scale"); ImGui::SetCursorScreenPos({p.x + 20, p.y + 126}); ImGui::PushItemWidth(222); float sc = (e.scale - .5f) / 1.5f; if (Slider("hscale", &sc, 0, 1)) e.scale = .5f + sc * 1.5f; ImGui::PopItemWidth();
    ImGui::SetCursorScreenPos({p.x + 20, p.y + 164}); if (GlassButton("hhide", e.visible ? "Hide" : "Show", {110, 36})) e.visible = !e.visible;
}

// ---- header ---------------------------------------------------------------------------------------------------
static void Header(ImVec2 o, MenuState& s, ImTextureID logo) {
    if (logo) DL()->AddImage(logo, {o.x + 18, o.y + 10}, {o.x + 58, o.y + 50});
    float x = o.x + 66; for (const char* c = "CARAMEL CLIENT"; *c; ++c) { char ch[2] = {*c, 0}; TextAt({x, o.y + 31}, GetFonts().display, col::Text(), ch); ImGui::PushFont(GetFonts().display); x += ImGui::CalcTextSize(ch).x + 1.6f; ImGui::PopFont(); }
    static const char* labels[] = {"MODS", "REPLAY", "COSMETICS", "VC", "SETTINGS"};
    static const Icon icons[] = {Icon::Puzzle, Icon::Replay, Icon::Cube, Icon::Mic, Icon::Gear};
    At(o, kSize.x * .5f - 280 + 40, 14); TabBar("tabs", labels, icons, 5, &s.tab, 112);
    At(o, kSize.x - 52, 16); static const Icon x_ = Icon::Close; if (GlassButton("close", nullptr, {34, 32}, false, false, &x_)) s.open = false;
    Rule(o, 18, kSize.x - 18, 62);
}

// ---- Mods -------------------------------------------------------------------------------------------------------
static void ModsTab(ImVec2 o, MenuState& s) {
    Txt(o, 18, 86, "Profiles", false);
    static const char* profiles[] = {"Default", "PvP", "Survival"};
    for (int i = 0; i < 3; ++i) {
        ImVec2 a{o.x + 18, o.y + 104 + i * 42}; At(o, 18, 104 + i * 42); char id[16]; snprintf(id, sizeof id, "prof%d", i);
        if (GlassButton(id, nullptr, {200, 36}, false, s.profile == i)) s.profile = i;
        TextAt({a.x + 14, a.y + 18}, GetFonts().bodyMedium, s.profile == i ? col::Text() : col::Text2(), profiles[i]); DrawIcon(Icon::Dots, {a.x + 180, a.y + 18}, 14, col::Text3());
    }
    At(o, 18, 240); static const Icon plus = Icon::Plus; GlassButton("saveprof", "Save new profile", {200, 36}, false, false, &plus);
    At(o, 18, kSize.y - 76); if (PrimaryButton("hud", "Edit HUD layout", {200, 44}, Tone::Blue)) s.hudEditing = true;
    DL()->AddLine({o.x + 232, o.y + 78}, {o.x + 232, o.y + kSize.y - 24}, IM_COL32(255, 255, 255, 20));
    static const char* cats[] = {"All", "New", "HUD", "Server", "Mechanic"};
    At(o, 256, 78); for (int i = 0; i < 5; ++i) { if (Chip(cats[i], s.category == i)) s.category = i; ImGui::SameLine(0, 6); }
    At(o, kSize.x - 18 - 230, 74); SearchField("##search", s.search, sizeof s.search, 230, "Search modules");

    // The single Example module card: OPTIONS and the enable toggle share one row.
    ImVec2 a{o.x + 256, o.y + 130}, b{a.x + 214, a.y + 158}; Glass(a, b, 16, true);
    ImVec2 ic{(a.x + b.x) * .5f, a.y + 42};
    DL()->AddRectFilled({ic.x - 26, ic.y - 26}, {ic.x + 26, ic.y + 26}, IM_COL32(74, 120, 255, 46), 14); DL()->AddRect({ic.x - 26, ic.y - 26}, {ic.x + 26, ic.y + 26}, IM_COL32(74, 120, 255, 140), 14);
    DrawIcon(Icon::Hud, ic, 26, IM_COL32(140, 175, 255, 255));
    TextAt({ic.x, a.y + 88}, GetFonts().title, col::Text(), "Example", true);
    ImGui::SetCursorScreenPos({a.x + 14, a.y + 110}); static const Icon sl = Icon::Sliders;
    if (GlassButton("opts", "OPTIONS", {214 - 28 - 52, 32}, false, false, &sl)) s.moduleSettingsOpen = true;
    ImGui::SetCursorScreenPos({b.x - 14 - 40, a.y + 115}); Toggle("mod_on", &s.example.enabled);
}

static void ModuleSettings(ImVec2 o, ImVec2 display, MenuState& s) {
    DL()->AddRectFilled({0, 0}, display, IM_COL32(3, 7, 20, 150));
    ImVec2 a{o.x + (kSize.x - 520) * .5f, o.y - 20}, b{a.x + 520, a.y + 620}; Glass(a, b, 20, true, IM_COL32(120, 150, 255, 18));
    auto at = [&](float x, float y) { ImGui::SetCursorScreenPos({a.x + x, a.y + y}); };
    ModuleExample& m = s.example; static const Icon left = Icon::Left;
    at(18, 16); if (GlassButton("back", nullptr, {34, 34}, false, false, &left)) s.moduleSettingsOpen = false;
    TextAt({a.x + 68, a.y + 33}, GetFonts().title, col::Text(), "Example");
    at(520 - 66, 22); Toggle("mod_on2", &m.enabled); Hairline(a.x + 18, b.x - 18, a.y + 64);
    TextAt({a.x + 28, a.y + 90}, GetFonts().bodyMedium, col::Text2(), "Appearance");
    TextAt({a.x + 28, a.y + 126}, GetFonts().bodyMedium, col::Text(), "Scale"); at(28, 144); ImGui::PushItemWidth(464); float sc = (m.scale - .5f) / 1.5f; if (Slider("scale", &sc, 0.f, 1.f)) m.scale = .5f + sc * 1.5f;
    TextAt({a.x + 28, a.y + 190}, GetFonts().bodyMedium, col::Text(), "Opacity"); at(28, 208); Slider("opacity", &m.opacity, 0.f, 1.f); ImGui::PopItemWidth();
    TextAt({a.x + 28, a.y + 258}, GetFonts().bodyMedium, col::Text(), "Text color"); at(520 - 28 - 190, 247); ColorSwatches("tc", kSwatches, 6, &m.textColor);
    TextAt({a.x + 28, a.y + 300}, GetFonts().bodyMedium, col::Text(), "Position"); at(520 - 28 - 190, 282); static const char* pos[] = {"Top left", "Top right", "Bottom left", "Bottom right"}; Dropdown("pos", pos, 4, &m.position, 190);
    TextAt({a.x + 28, a.y + 352}, GetFonts().bodyMedium, col::Text2(), "Behavior");
    at(28, 377); CheckBox("bg", "Show background", &m.background); at(28, 413); CheckBox("sh", "Text shadow", &m.textShadow); at(28, 449); CheckBox("cp", "Compact mode", &m.compact);
    TextAt({a.x + 28, a.y + 500}, GetFonts().bodyMedium, col::Text(), "Keybind"); at(520 - 28 - 190, 482); ImGui::SetNextItemWidth(190); ImGui::InputText("##kb", m.keybind, sizeof m.keybind);
    Hairline(a.x + 18, b.x - 18, b.y - 70);
    static const Icon sw = Icon::Swap; at(24, 620 - 54); if (GlassButton("reset", "Reset defaults", {160, 36}, false, false, &sw)) m = ModuleExample{};
    at(520 - 164, 620 - 54); if (PrimaryButton("done", "Done", {140, 36}, Tone::Green)) s.moduleSettingsOpen = false;
}

// ---- Replay -------------------------------------------------------------------------------------------------------
static void ReplayTab(ImVec2 o, MenuState& s) {
    ImVec2 l{o.x + 28, o.y + 84}; float lw = 600; Glass(l, {l.x + lw, o.y + kSize.y - 28}, 16, false); ImVec2 r{l.x + lw + 24, l.y}; Glass(r, {o.x + kSize.x - 28, o.y + kSize.y - 28}, 16, false);
    Title(l, 22, 30, "Recordings"); ImGui::SetCursorScreenPos({l.x + lw - 178, l.y + 14}); PrimaryButton("rec", "Start recording", {160, 32}, Tone::Red);
    for (int i = 0; i < 3; ++i) {
        ImVec2 a{l.x + 16, l.y + 66 + i * 100}; DL()->AddRectFilled(a, {a.x + lw - 32, a.y + 88}, IM_COL32(255, 255, 255, 14), 14); DL()->AddRect(a, {a.x + lw - 32, a.y + 88}, IM_COL32(255, 255, 255, 30), 14);
        DL()->AddRectFilled({a.x + 10, a.y + 10}, {a.x + 130, a.y + 78}, IM_COL32(74, 120, 255, 70), 10.f);   // thumbnail slot
        char t[48]; snprintf(t, sizeof t, "Example replay %d", i + 1); TextAt({a.x + 148, a.y + 28}, GetFonts().bodyMedium, col::Text(), t);
        snprintf(t, sizeof t, "0%d:14  -  %.1f GB  -  Today", i + 2, 1.2f + i * .4f); TextAt({a.x + 148, a.y + 50}, GetFonts().body, col::Text2(), t);
        static const Icon play = Icon::Play, plus = Icon::Plus; char id[16];
        ImGui::SetCursorScreenPos({a.x + lw - 32 - 200, a.y + 26}); snprintf(id, 16, "play%d", i); GlassButton(id, "Play", {82, 36}, false, false, &play);
        ImGui::SetCursorScreenPos({a.x + lw - 32 - 108, a.y + 26}); snprintf(id, 16, "exp%d", i); GlassButton(id, "Export", {76, 36});
        ImGui::SetCursorScreenPos({a.x + lw - 32 - 56, a.y + 26}); snprintf(id, 16, "del%d", i); static const Icon x_ = Icon::Close; GlassButton(id, nullptr, {40, 36}, true, false, &x_);
    }
    float rw = o.x + kSize.x - 28 - r.x - 44; Title(r, 22, 30, "Recording");
    TextAt({r.x + 22, r.y + 76}, GetFonts().body, col::Text(), "Record automatically"); ImGui::SetCursorScreenPos({r.x + 22 + rw - 40, r.y + 65}); Toggle("auto", &s.autoRecord);
    TextAt({r.x + 22, r.y + 126}, GetFonts().body, col::Text(), "Buffer length"); ImGui::SetCursorScreenPos({r.x + 22, r.y + 142}); ImGui::PushItemWidth(rw); Slider("buf", &s.buffer, 0, 1); ImGui::PopItemWidth();
    TextAt({r.x + 22, r.y + 204}, GetFonts().body, col::Text(), "Quality"); ImGui::SetCursorScreenPos({r.x + 22 + rw - 150, r.y + 186}); static const char* q[] = {"Low", "High", "Ultra"}; Dropdown("q", q, 3, &s.quality, 150);
    TextAt({r.x + 22, r.y + 254}, GetFonts().body, col::Text(), "Hotkey"); ImGui::SetCursorScreenPos({r.x + 22 + rw - 150, r.y + 236}); ImGui::SetNextItemWidth(150); ImGui::InputText("##rk", s.replayKey, sizeof s.replayKey);
}

// ---- Cosmetics studio ---------------------------------------------------------------------------------------------
static void StudioTab(ImVec2 o, MenuState& s) {
    ImVec2 l{o.x + 28, o.y + 84}; Glass(l, {l.x + 300, o.y + kSize.y - 28}, 16, false);
    // 3D SKIN VIEWER slot: render the 3D skin into this white rounded square.
    DL()->AddRectFilled({l.x + 22, l.y + 22}, {l.x + 278, l.y + 316}, IM_COL32(255, 255, 255, 240), 20.f);
    const char* msg = "Where the skin of the 3d skin goes"; ImGui::PushFont(GetFonts().title); ImVec2 ts = ImGui::CalcTextSize(msg, nullptr, false, 180); ImGui::PopFont();
    DL()->AddText(GetFonts().title, GetFonts().title->FontSize, {l.x + 150 - ts.x * .5f, l.y + 169 - ts.y * .5f}, IM_COL32(28, 40, 84, 255), msg, nullptr, 180);
    Txt(l, 22, 348, "Rotation"); ImGui::SetCursorScreenPos({l.x + 22, l.y + 364}); ImGui::PushItemWidth(256); Slider("rot", &s.rotation, 0, 1); ImGui::PopItemWidth();
    static const Icon sw = Icon::Swap; ImGui::SetCursorScreenPos({l.x + 22, l.y + 400}); GlassButton("rview", "Reset view", {256, 36}, false, false, &sw);
    float gx = l.x + 324; ImGui::SetCursorScreenPos({gx, l.y}); static const char* cats[] = {"All", "Capes", "Wings", "Hats"};
    for (int i = 0; i < 4; ++i) { if (Chip(cats[i], s.cosCategory == i)) s.cosCategory = i; ImGui::SameLine(0, 6); }
    static const char* names[] = {"Example Cape", "Example Wings", "Example Hat"}; static ImU32 cols[] = {col::Blue(), col::Caramel(), col::Green()};
    for (int i = 0; i < 6; ++i) {
        ImVec2 a{gx + (i % 3) * 218, l.y + 42 + (i / 3) * 160}; ImVec2 b{a.x + 208, a.y + 148}; Glass(a, b, 16, false);
        char id[16]; snprintf(id, 16, "tile%d", i); ImGui::SetCursorScreenPos(a); if (ImGui::InvisibleButton(id, {208, 148})) s.cosSelected = i;
        if (i == s.cosSelected) DL()->AddRect(a, b, col::Blue(), 16, 0, 2.f);
        ImU32 c = cols[i % 3]; DL()->AddRectFilled({a.x + 8, a.y + 8}, {b.x - 8, a.y + 92}, (c & 0x00FFFFFF) | (60u << 24), 11.f); DL()->AddRectFilled({a.x + 86, a.y + 20}, {a.x + 122, a.y + 80}, c, 4.f);
        // favorite star button
        ImVec2 sc{b.x - 28, a.y + 28}; ImGui::SetCursorScreenPos({sc.x - 13, sc.y - 13}); snprintf(id, 16, "fav%d", i); if (ImGui::InvisibleButton(id, {26, 26})) s.fav[i] = !s.fav[i];
        DL()->AddCircleFilled(sc, 13, IM_COL32(8, 14, 36, 150)); DL()->AddCircle(sc, 13, s.fav[i] ? col::Caramel() : col::White(60));
        DrawIcon(s.fav[i] ? Icon::StarFill : Icon::Star, sc, 15, s.fav[i] ? col::Caramel() : IM_COL32(230, 236, 255, 255), 1.6f);
        TextAt({a.x + 14, a.y + 112}, GetFonts().bodyMedium, col::Text(), names[i % 3]); TextAt({a.x + 14, a.y + 132}, GetFonts().body, i == 1 ? col::Green() : col::Text2(), i == 1 ? "Equipped" : "Owned");
    }
    ImVec2 e{gx, l.y + 372}; Glass(e, {o.x + kSize.x - 28, o.y + kSize.y - 28}, 16, false);
    TextAt({e.x + 18, e.y + 24}, GetFonts().bodyMedium, col::Text(), "Editing: Example Wings"); TextAt({e.x + 18, e.y + 62}, GetFonts().body, col::Text2(), "Scale");
    ImGui::SetCursorScreenPos({e.x + 70, e.y + 51}); ImGui::PushItemWidth(250); Slider("cs", &s.cosScale, 0, 1); ImGui::PopItemWidth();
    TextAt({e.x + 350, e.y + 62}, GetFonts().body, col::Text2(), "Tint"); ImGui::SetCursorScreenPos({e.x + 384, e.y + 51}); ColorSwatches("tint", kSwatches, 5, &s.tint);
    ImGui::SetCursorScreenPos({o.x + kSize.x - 28 - 164, e.y + 12}); PrimaryButton("equip", "Equip", {136, 34}, Tone::Green);
}

// ---- Voice chat ---------------------------------------------------------------------------------------------------
static void VoiceTab(ImVec2 o, MenuState& s) {
    float cw = (kSize.x - 84) * .5f; ImVec2 l{o.x + 28, o.y + 84}, r{l.x + cw + 28, l.y};
    Glass(l, {l.x + cw, o.y + kSize.y - 28}, 16, false); Glass(r, {r.x + cw, o.y + kSize.y - 28}, 16, false); float iw = cw - 44;
    Title(l, 22, 30, "Devices");
    static const char* in[] = {"Default microphone", "USB microphone"}; static const char* out[] = {"Default speakers", "Headphones"};
    TextAt({l.x + 22, l.y + 76}, GetFonts().body, col::Text(), "Input device"); ImGui::SetCursorScreenPos({l.x + 22 + iw - 230, l.y + 58}); Dropdown("in", in, 2, &s.inDevice, 230);
    TextAt({l.x + 22, l.y + 126}, GetFonts().body, col::Text(), "Output device"); ImGui::SetCursorScreenPos({l.x + 22 + iw - 230, l.y + 108}); Dropdown("out", out, 2, &s.outDevice, 230);
    TextAt({l.x + 22, l.y + 184}, GetFonts().body, col::Text(), "Microphone volume"); ImGui::SetCursorScreenPos({l.x + 22, l.y + 200}); ImGui::PushItemWidth(iw); Slider("mic", &s.micVol, 0, 1);
    TextAt({l.x + 22, l.y + 256}, GetFonts().body, col::Text(), "Output volume"); ImGui::SetCursorScreenPos({l.x + 22, l.y + 272}); Slider("vol", &s.outVol, 0, 1); ImGui::PopItemWidth();
    TextAt({l.x + 22, l.y + 330}, GetFonts().body, col::Text(), "Mic test"); float level = 0.5f + 0.15f * sinf((float)ImGui::GetTime() * 4.f);   // replace with the real input level
    for (int i = 0; i < 28; ++i) { ImU32 c = i < 16 ? col::Green() : (i < 23 ? col::Orange() : col::Red()); float x = l.x + 22 + i * (iw / 28); DL()->AddRectFilled({x, l.y + 346}, {x + iw / 28 - 3, l.y + 366}, i < level * 28 ? c : (c & 0x00FFFFFF) | (50u << 24), 2.f); }
    Title(r, 22, 30, "Voice chat");
    struct { const char* t; const char* d; bool* v; } rows[] = {{"Push to talk", "Hold a key to speak", &s.ptt}, {"Noise suppression", "Filter background sound", &s.noiseSuppression}, {"Proximity chat", "Hear players near you", &s.proximity}};
    for (int i = 0; i < 3; ++i) { TextAt({r.x + 22, r.y + 76 + i * 52}, GetFonts().body, col::Text(), rows[i].t); TextAt({r.x + 22, r.y + 94 + i * 52}, GetFonts().body, col::Text2(), rows[i].d); ImGui::SetCursorScreenPos({r.x + 22 + iw - 40, r.y + 65 + i * 52}); char id[8]; snprintf(id, 8, "v%d", i); Toggle(id, rows[i].v); }
    TextAt({r.x + 22, r.y + 246}, GetFonts().body, col::Text(), "Push to talk key"); ImGui::SetCursorScreenPos({r.x + 22 + iw - 150, r.y + 228}); ImGui::SetNextItemWidth(150); ImGui::InputText("##ptk", s.pttKey, sizeof s.pttKey);
    TextAt({r.x + 22, r.y + 296}, GetFonts().body, col::Text(), "Proximity range"); ImGui::SetCursorScreenPos({r.x + 22, r.y + 312}); ImGui::PushItemWidth(iw); Slider("range", &s.range, 0, 1); ImGui::PopItemWidth();
    static const Icon mic = Icon::Mic, x_ = Icon::Close; ImGui::SetCursorScreenPos({r.x + 22, r.y + 366}); GlassButton("mute", "Mute", {150, 36}, false, false, &mic); ImGui::SetCursorScreenPos({r.x + 182, r.y + 366}); GlassButton("deaf", "Deafen", {150, 36}, true, false, &x_);
}

// ---- Settings ---------------------------------------------------------------------------------------------------
static void SettingsTab(ImVec2 o, MenuState& s) {
    float cw = (kSize.x - 84) * .5f; ImVec2 l{o.x + 28, o.y + 84}, r{l.x + cw + 28, l.y};
    Glass(l, {l.x + cw, o.y + kSize.y - 28}, 16, false); Glass(r, {r.x + cw, o.y + kSize.y - 28}, 16, false);
    Title(l, 22, 30, "General");
    struct { const char* t; bool* v; } rows[] = {{"Auto-join last server", &s.autoJoin}, {"Show module toggles in chat", &s.chatToggles}, {"Notifications", &s.notifications}, {"Smooth camera", &s.smoothCamera}};
    for (int i = 0; i < 4; ++i) { TextAt({l.x + 22, l.y + 76 + i * 46}, GetFonts().body, col::Text(), rows[i].t); ImGui::SetCursorScreenPos({l.x + cw - 62, l.y + 65 + i * 46}); char id[16]; snprintf(id, 16, "g%d", i); Toggle(id, rows[i].v); }
    TextAt({l.x + 22, l.y + 276}, GetFonts().body, col::Text(), "Menu scale"); ImGui::SetCursorScreenPos({l.x + 22, l.y + 293}); ImGui::PushItemWidth(cw - 44); Slider("ms", &s.menuScale, 0, 1); ImGui::PopItemWidth();
    Title(r, 22, 30, "Appearance");
    TextAt({r.x + 22, r.y + 76}, GetFonts().body, col::Text(), "Accent color"); ImGui::SetCursorScreenPos({r.x + cw - 22 - 160, r.y + 64}); ColorSwatches("ac", kSwatches + 1, 5, &s.accent);
    TextAt({r.x + 22, r.y + 122}, GetFonts().body, col::Text(), "Blur strength"); ImGui::SetCursorScreenPos({r.x + 22, r.y + 140}); ImGui::PushItemWidth(cw - 44); Slider("bl", &s.blur, 0, 1); ImGui::PopItemWidth();
    TextAt({r.x + 22, r.y + 192}, GetFonts().body, col::Text(), "Language"); ImGui::SetCursorScreenPos({r.x + cw - 22 - 190, r.y + 174}); static const char* langs[] = {"English (US)", "Espanol", "Francais", "Deutsch"}; Dropdown("lang", langs, 4, &s.language, 190);
    ImGui::SetCursorScreenPos({r.x + 22, r.y + 250}); CheckBox("rc", "Rounded corners", &s.rounded); ImGui::SetCursorScreenPos({r.x + 22, r.y + 290}); CheckBox("an", "Animations", &s.animations);
    ImGui::SetCursorScreenPos({r.x + 22, r.y + 340}); GlassButton("rst", "Reset client", {160, 36}, true);
}

void RenderMenu(MenuState& s, ImTextureID logo, ImVec2 display) {
    if (!s.open) return;
    ImGui::SetNextWindowPos({0, 0}); ImGui::SetNextWindowSize(display);
    ImGui::PushStyleVar(ImGuiStyleVar_WindowPadding, ImVec2(0, 0));
    ImGui::Begin("##caramel", nullptr, ImGuiWindowFlags_NoDecoration | ImGuiWindowFlags_NoBackground | ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoSavedSettings | ImGuiWindowFlags_NoBringToFrontOnFocus);
    if (s.hudEditing) { RenderHudEditor(s, display); ImGui::End(); ImGui::PopStyleVar(); return; }   // own overlay: draggable HUD elements
    DrawHud(s);
    ImGui::GetWindowDrawList()->AddRectFilled({0, 0}, display, IM_COL32(4, 9, 28, 120));              // game dim
    ImVec2 o{(display.x - kSize.x) * .5f, (display.y - kSize.y) * .5f};
    Glass(o, {o.x + kSize.x, o.y + kSize.y}, 18, true, IM_COL32(120, 150, 255, 14));
    Header(o, s, logo);
    switch (s.tab) { case TabMods: ModsTab(o, s); break; case TabReplay: ReplayTab(o, s); break; case TabCosmetics: StudioTab(o, s); break; case TabVoice: VoiceTab(o, s); break; default: SettingsTab(o, s); }
    if (s.tab == TabMods && s.moduleSettingsOpen) ModuleSettings(o, display, s);
    ImGui::End(); ImGui::PopStyleVar();
}

}  // namespace caramel
