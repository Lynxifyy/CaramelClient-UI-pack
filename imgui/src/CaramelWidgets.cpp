#include "CaramelWidgets.h"
#include "imgui_internal.h"
#include <cmath>
#include <cstring>

namespace caramel::ui {

static BlurHook g_blur = nullptr;
void SetBlurHook(BlurHook h) { g_blur = h; }

static ImU32 Mul(ImU32 c, float a) { ImVec4 v = ImGui::ColorConvertU32ToFloat4(c); v.w *= a; return ImGui::ColorConvertFloat4ToU32(v); }
static ImDrawList* DL() { return ImGui::GetWindowDrawList(); }

float Anim(ImGuiID id, float target, float speed) {
    float* v = ImGui::GetStateStorage()->GetFloatRef(id, target);
    *v += (target - *v) * (1.f - std::exp(-speed * ImGui::GetIO().DeltaTime));
    return *v;
}

void TextAt(ImVec2 p, ImFont* f, ImU32 c, const char* t, bool cx, bool cy) {
    ImGui::PushFont(f ? f : ImGui::GetFont());
    ImVec2 s = ImGui::CalcTextSize(t);
    if (cx) p.x -= s.x * .5f;
    if (cy) p.y -= s.y * .5f;
    DL()->AddText(p, c, t);
    ImGui::PopFont();
}

void Glass(ImVec2 a, ImVec2 b, float r, bool shadow, ImU32 tint) {
    ImDrawList* d = DL();
    if (g_blur) d->AddCallback((ImDrawCallback)g_blur, nullptr);
    if (shadow) for (int i = 0; i < 7; ++i) { float e = 3.f + i * 4.f; d->AddRectFilled(ImVec2(a.x - e, a.y - e + 12), ImVec2(b.x + e, b.y + e + 12), IM_COL32(0, 0, 8, 16), r + e); }
    d->AddRectFilled(a, b, IM_COL32(12, 22, 56, g_blur ? 150 : 238), r);               // frosted navy base
    d->AddRectFilled(a, b, tint, r);                                                    // tint
    d->AddRectFilled(a, ImVec2(b.x, a.y + (b.y - a.y) * .42f), IM_COL32(255, 255, 255, 14), r, ImDrawFlags_RoundCornersTop);  // sheen
    d->AddRect(a, b, IM_COL32(255, 255, 255, 40), r, 0, 1.f);                           // hairline border
    d->AddLine(ImVec2(a.x + r, a.y + .5f), ImVec2(b.x - r, a.y + .5f), IM_COL32(255, 255, 255, 70));  // top light
}

void Hairline(float x0, float x1, float y) { DL()->AddLine(ImVec2(x0, y), ImVec2(x1, y), IM_COL32(255, 255, 255, 24)); }

void DrawIcon(Icon ic, ImVec2 c, float s, ImU32 col, float t) {
    ImDrawList* d = DL(); float h = s * .5f;
    switch (ic) {
        case Icon::Close: d->AddLine({c.x - h * .55f, c.y - h * .55f}, {c.x + h * .55f, c.y + h * .55f}, col, t); d->AddLine({c.x + h * .55f, c.y - h * .55f}, {c.x - h * .55f, c.y + h * .55f}, col, t); break;
        case Icon::Check: d->PathLineTo({c.x - h * .5f, c.y}); d->PathLineTo({c.x - h * .1f, c.y + h * .4f}); d->PathLineTo({c.x + h * .55f, c.y - h * .4f}); d->PathStroke(col, 0, t); break;
        case Icon::Search: d->AddCircle({c.x - h * .15f, c.y - h * .15f}, h * .5f, col, 0, t); d->AddLine({c.x + h * .22f, c.y + h * .22f}, {c.x + h * .6f, c.y + h * .6f}, col, t); break;
        case Icon::Down: d->PathLineTo({c.x - h * .5f, c.y - h * .22f}); d->PathLineTo({c.x, c.y + h * .28f}); d->PathLineTo({c.x + h * .5f, c.y - h * .22f}); d->PathStroke(col, 0, t); break;
        case Icon::Up: d->PathLineTo({c.x - h * .5f, c.y + h * .22f}); d->PathLineTo({c.x, c.y - h * .28f}); d->PathLineTo({c.x + h * .5f, c.y + h * .22f}); d->PathStroke(col, 0, t); break;
        case Icon::Left: d->PathLineTo({c.x + h * .22f, c.y - h * .5f}); d->PathLineTo({c.x - h * .28f, c.y}); d->PathLineTo({c.x + h * .22f, c.y + h * .5f}); d->PathStroke(col, 0, t); break;
        case Icon::Plus: d->AddLine({c.x - h * .55f, c.y}, {c.x + h * .55f, c.y}, col, t); d->AddLine({c.x, c.y - h * .55f}, {c.x, c.y + h * .55f}, col, t); break;
        case Icon::Sliders: d->AddLine({c.x - h * .7f, c.y - h * .3f}, {c.x + h * .7f, c.y - h * .3f}, col, t); d->AddLine({c.x - h * .7f, c.y + h * .3f}, {c.x + h * .7f, c.y + h * .3f}, col, t); d->AddCircleFilled({c.x - h * .25f, c.y - h * .3f}, h * .2f, col); d->AddCircleFilled({c.x + h * .25f, c.y + h * .3f}, h * .2f, col); break;
        case Icon::Hud: d->AddRect({c.x - h * .75f, c.y - h * .5f}, {c.x + h * .75f, c.y + h * .5f}, col, 3.f, 0, t); d->AddRectFilled({c.x - h * .5f, c.y - h * .25f}, {c.x, c.y}, col, 1.f); break;
        case Icon::Swap: d->AddLine({c.x - h * .7f, c.y - h * .25f}, {c.x + h * .7f, c.y - h * .25f}, col, t); d->AddLine({c.x - h * .7f, c.y + h * .25f}, {c.x + h * .7f, c.y + h * .25f}, col, t); break;
        case Icon::Puzzle: d->AddRect({c.x - h * .6f, c.y - h * .35f}, {c.x + h * .6f, c.y + h * .7f}, col, 3.f, 0, t); d->AddCircle({c.x, c.y - h * .5f}, h * .26f, col, 0, t); d->AddCircle({c.x + h * .62f, c.y + h * .15f}, h * .24f, col, 0, t); break;
        case Icon::Replay: d->PathArcTo(c, h * .65f, 0.7f, 5.5f); d->PathStroke(col, 0, t); d->AddTriangleFilled({c.x - h * .12f, c.y - h * .3f}, {c.x + h * .3f, c.y}, {c.x - h * .12f, c.y + h * .3f}, col); break;
        case Icon::Cube: { ImVec2 p[6] = {{c.x, c.y - h * .8f}, {c.x + h * .7f, c.y - h * .4f}, {c.x + h * .7f, c.y + h * .4f}, {c.x, c.y + h * .8f}, {c.x - h * .7f, c.y + h * .4f}, {c.x - h * .7f, c.y - h * .4f}}; d->AddPolyline(p, 6, col, ImDrawFlags_Closed, t); d->AddLine(p[5], {c.x, c.y}, col, t); d->AddLine(p[1], {c.x, c.y}, col, t); d->AddLine({c.x, c.y}, p[3], col, t); break; }
        case Icon::Mic: d->AddRect({c.x - h * .26f, c.y - h * .75f}, {c.x + h * .26f, c.y + h * .1f}, col, h * .26f, 0, t); d->PathArcTo({c.x, c.y - h * .05f}, h * .52f, 0.f, IM_PI, 16); d->PathStroke(col, 0, t); d->AddLine({c.x, c.y + h * .47f}, {c.x, c.y + h * .8f}, col, t); break;
        case Icon::Gear: for (int i = 0; i < 8; ++i) { float a = i * IM_PI / 4; d->AddLine({c.x + h * .62f * cosf(a), c.y + h * .62f * sinf(a)}, {c.x + h * .88f * cosf(a), c.y + h * .88f * sinf(a)}, col, t + .4f); } d->AddCircle(c, h * .5f, col, 0, t); d->AddCircle(c, h * .2f, col, 0, t); break;
        case Icon::Star: case Icon::StarFill: { ImVec2 p[11]; for (int i = 0; i < 10; ++i) { float a = -IM_PI / 2 + i * IM_PI / 5, r = (i % 2 == 0) ? h * .95f : h * .42f; p[i] = {c.x + r * cosf(a), c.y + h * .06f + r * sinf(a)}; } p[10] = p[0];
            if (ic == Icon::StarFill) for (int i = 0; i < 10; ++i) d->AddTriangleFilled(c, p[i], p[i + 1], col);
            d->AddPolyline(p, 11, col, 0, ic == Icon::StarFill ? t : t); break; }
        case Icon::Play: d->AddTriangleFilled({c.x - h * .4f, c.y - h * .6f}, {c.x + h * .6f, c.y}, {c.x - h * .4f, c.y + h * .6f}, col); break;
        case Icon::Map: d->AddCircle({c.x, c.y - h * .15f}, h * .45f, col, 0, t); d->AddLine({c.x - h * .3f, c.y + h * .15f}, {c.x, c.y + h * .8f}, col, t); d->AddLine({c.x + h * .3f, c.y + h * .15f}, {c.x, c.y + h * .8f}, col, t); break;
        case Icon::Dots: for (int i = -1; i <= 1; ++i) d->AddCircleFilled({c.x + i * h * .5f, c.y}, h * .12f, col); break;
    }
}

static bool Hit(const char* id, ImVec2 pos, ImVec2 size, bool* hovered, bool* held) {
    ImGui::SetCursorScreenPos(pos);
    bool pressed = ImGui::InvisibleButton(id, size);
    *hovered = ImGui::IsItemHovered(); *held = ImGui::IsItemActive();
    return pressed;
}

static void GradientRounded(ImVec2 a, ImVec2 b, float r, ImU32 top, ImU32 bottom) {
    ImDrawList* d = DL();
    d->AddRectFilled(a, b, bottom, r);
    d->AddRectFilled(a, ImVec2(b.x, a.y + (b.y - a.y) * .55f), top, r, ImDrawFlags_RoundCornersTop);
    d->AddRectFilledMultiColor(ImVec2(a.x, a.y + r), ImVec2(b.x, b.y - r), top, top, bottom, bottom);
}

bool PrimaryButton(const char* id, const char* label, ImVec2 size, Tone tone) {
    ImVec2 p = ImGui::GetCursorScreenPos(); bool hov, held; bool clicked = Hit(id, p, size, &hov, &held);
    float h = Anim(ImGui::GetID(id), hov ? 1.f : 0.f); ImDrawList* d = DL(); float r = size.y / 2.6f;
    ImU32 top, bot, on = col::White(255);
    switch (tone) {
        case Tone::Green:   top = col::GreenLight(); bot = col::GreenDark(); on = col::OnGreen(); break;
        case Tone::Caramel: top = IM_COL32(255, 190, 90, 255); bot = IM_COL32(222, 134, 36, 255); break;
        case Tone::Blue:    top = col::BlueLight(); bot = col::BlueDark(); break;
        default:            top = IM_COL32(255, 108, 126, 255); bot = IM_COL32(214, 52, 78, 255); break;
    }
    for (int i = 0; i < 4; ++i) d->AddRectFilled({p.x - i * 2, p.y - i * 2 + 5}, {p.x + size.x + i * 2, p.y + size.y + i * 2 + 5}, Mul(bot, (0.05f + 0.03f * h)), r + i * 2);
    GradientRounded(p, {p.x + size.x, p.y + size.y}, r, top, bot);
    d->AddRectFilled({p.x + 2, p.y + 2}, {p.x + size.x - 2, p.y + size.y * .5f}, col::White(int(36 + 30 * h)), r - 2, ImDrawFlags_RoundCornersTop);
    d->AddRect(p, {p.x + size.x, p.y + size.y}, col::White(72), r);
    TextAt({p.x + size.x * .5f, p.y + size.y * .5f}, GetFonts().title, on, label, true);
    return clicked;
}

bool GlassButton(const char* id, const char* label, ImVec2 size, bool danger, bool active, const Icon* icon) {
    ImVec2 p = ImGui::GetCursorScreenPos(); bool hov, held; bool clicked = Hit(id, p, size, &hov, &held);
    float h = Anim(ImGui::GetID(id), hov ? 1.f : 0.f); ImDrawList* d = DL(); float r = ImMin(12.f, size.y / 2.4f);
    ImU32 t = danger ? col::Red() : (active ? col::Blue() : col::White(255)); ImU32 fg = danger ? col::Red() : col::Text();
    d->AddRectFilled(p, {p.x + size.x, p.y + size.y}, Mul(t, (danger || active) ? .16f : .07f + .06f * h), r);
    d->AddRect(p, {p.x + size.x, p.y + size.y}, Mul(t, (danger || active) ? .5f : .17f + .12f * h), r);
    ImVec2 c{p.x + size.x * .5f, p.y + size.y * .5f};
    if (icon && label && *label) { float tw = ImGui::CalcTextSize(label).x; DrawIcon(*icon, {c.x - tw * .5f - 10, c.y}, 15, fg, 1.7f); TextAt({c.x + 9, c.y}, GetFonts().bodyMedium, fg, label, true); }
    else if (icon) DrawIcon(*icon, c, 17, fg, 1.8f);
    else TextAt(c, GetFonts().bodyMedium, fg, label, true);
    return clicked;
}

bool Toggle(const char* id, bool* v) {
    ImVec2 p = ImGui::GetCursorScreenPos(); ImVec2 size(40, 22); bool hov, held; bool clicked = Hit(id, p, size, &hov, &held);
    if (clicked) *v = !*v;
    float t = Anim(ImGui::GetID(id), *v ? 1.f : 0.f, 18.f); ImDrawList* d = DL();
    if (t > .01f) GradientRounded(p, {p.x + 40, p.y + 22}, 11, Mul(col::GreenLight(), t), Mul(col::GreenDark(), t));
    d->AddRectFilled(p, {p.x + 40, p.y + 22}, col::White(int(26 * (1 - t))), 11);
    d->AddRect(p, {p.x + 40, p.y + 22}, col::White(int(60 * (1 - t))), 11);
    d->AddCircleFilled({p.x + 11 + 18 * t, p.y + 11}, 8.f, *v ? IM_COL32(255, 255, 255, 255) : IM_COL32(190, 202, 235, 255));
    return clicked;
}

bool CheckBox(const char* id, const char* label, bool* v) {
    ImVec2 p = ImGui::GetCursorScreenPos(); ImVec2 size(ImGui::CalcTextSize(label).x + 32, 18); bool hov, held; bool clicked = Hit(id, p, size, &hov, &held);
    if (clicked) *v = !*v; ImDrawList* d = DL();
    if (*v) { GradientRounded(p, {p.x + 18, p.y + 18}, 5, col::BlueLight(), col::BlueDark()); DrawIcon(Icon::Check, {p.x + 9, p.y + 9}, 13, col::White(255), 2.2f); }
    else { d->AddRectFilled(p, {p.x + 18, p.y + 18}, col::White(14), 5); d->AddRect(p, {p.x + 18, p.y + 18}, col::White(72), 5); }
    TextAt({p.x + 28, p.y + 9}, GetFonts().body, col::Text(), label);
    return clicked;
}

bool Slider(const char* id, float* v, float lo, float hi) {
    float w = ImGui::GetContentRegionAvail().x; ImVec2 p = ImGui::GetCursorScreenPos(); ImVec2 size(w, 22); bool hov, held; Hit(id, p, size, &hov, &held);
    bool changed = false;
    if (held) { float n = ImClamp((ImGui::GetIO().MousePos.x - p.x) / w, 0.f, 1.f); float nv = lo + n * (hi - lo); if (nv != *v) { *v = nv; changed = true; } }
    float t = (*v - lo) / (hi - lo); float cy = p.y + 11; ImDrawList* d = DL();
    d->AddRectFilled({p.x, cy - 3}, {p.x + w, cy + 3}, col::White(30), 3.f);
    d->AddRectFilledMultiColor({p.x, cy - 3}, {p.x + w * t, cy + 3}, col::BlueLight(), IM_COL32(74, 190, 255, 255), IM_COL32(74, 190, 255, 255), col::BlueLight());
    d->AddCircleFilled({p.x + w * t, cy + 1.5f}, 9.f, IM_COL32(0, 0, 0, 80)); d->AddCircleFilled({p.x + w * t, cy}, 8.f, IM_COL32(255, 255, 255, 255)); d->AddCircleFilled({p.x + w * t, cy}, 3.f, col::Blue());
    return changed;
}

bool Chip(const char* label, bool active) {
    ImGui::PushFont(GetFonts().bodyBold); float tw = ImGui::CalcTextSize(label).x; ImGui::PopFont();
    ImVec2 p = ImGui::GetCursorScreenPos(); ImVec2 size(tw + 26, 26); bool hov, held; bool clicked = Hit(label, p, size, &hov, &held); ImDrawList* d = DL();
    if (active) GradientRounded(p, {p.x + size.x, p.y + 26}, 13, col::BlueLight(), col::BlueDark());
    else { d->AddRectFilled(p, {p.x + size.x, p.y + 26}, col::White(hov ? 26 : 18), 13); d->AddRect(p, {p.x + size.x, p.y + 26}, col::White(40), 13); }
    TextAt({p.x + size.x * .5f, p.y + 13}, GetFonts().bodyBold, active ? col::White(255) : col::Text2(), label, true);
    return clicked;
}

bool TextField(const char* id, char* buf, size_t cap, float w) {
    ImGui::SetNextItemWidth(w);
    return ImGui::InputText(id, buf, cap);
}

bool SearchField(const char* id, char* buf, size_t cap, float w, const char* hint) {
    ImVec2 p = ImGui::GetCursorScreenPos();
    ImGui::SetNextItemWidth(w); ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, ImVec2(38, 9));
    bool r = ImGui::InputTextWithHint(id, hint, buf, cap); ImGui::PopStyleVar();
    DrawIcon(Icon::Search, {p.x + 20, p.y + ImGui::GetFrameHeight() * .5f}, 15, col::Text3(), 1.8f); return r;
}

bool Segmented(const char* id, const char* const* items, int n, int* sel, float iw) {
    ImVec2 p = ImGui::GetCursorScreenPos(); ImDrawList* d = DL(); bool changed = false; float w = n * iw + 8;
    d->AddRectFilled(p, {p.x + w, p.y + 34}, col::White(16), 17); d->AddRect(p, {p.x + w, p.y + 34}, col::White(36), 17);
    for (int i = 0; i < n; ++i) {
        ImVec2 a{p.x + 4 + i * iw, p.y + 4}; bool hov, held; char key[64]; snprintf(key, sizeof key, "%s_%d", id, i);
        if (Hit(key, a, {iw, 26}, &hov, &held)) { *sel = i; changed = true; }
        if (i == *sel) GradientRounded(a, {a.x + iw, a.y + 26}, 13, col::BlueLight(), col::BlueDark());
        TextAt({a.x + iw * .5f, a.y + 13}, GetFonts().bodyBold, i == *sel ? col::White(255) : col::Text2(), items[i], true);
    }
    ImGui::SetCursorScreenPos({p.x, p.y + 38}); return changed;
}

bool TabBar(const char* id, const char* const* labels, const Icon* icons, int n, int* sel, float iw) {
    ImVec2 p = ImGui::GetCursorScreenPos(); ImDrawList* d = DL(); bool changed = false; float w = n * iw + 8;
    d->AddRectFilled(p, {p.x + w, p.y + 34}, col::White(16), 17); d->AddRect(p, {p.x + w, p.y + 34}, col::White(36), 17);
    for (int i = 0; i < n; ++i) {
        ImVec2 a{p.x + 4 + i * iw, p.y + 4}; bool hov, held; char key[64]; snprintf(key, sizeof key, "%s_%d", id, i);
        if (Hit(key, a, {iw - 2, 26}, &hov, &held)) { *sel = i; changed = true; }
        if (i == *sel) GradientRounded(a, {a.x + iw - 2, a.y + 26}, 13, col::BlueLight(), col::BlueDark());
        ImU32 fg = i == *sel ? col::White(255) : col::Text2();
        ImGui::PushFont(GetFonts().bodyBold); float tw = ImGui::CalcTextSize(labels[i]).x; ImGui::PopFont();
        float start = a.x + (iw - 2) * .5f - (tw + 22) * .5f;
        DrawIcon(icons[i], {start + 7, a.y + 13}, 14, fg, 1.7f); TextAt({start + 22, a.y + 13}, GetFonts().bodyBold, fg, labels[i]);
    }
    ImGui::SetCursorScreenPos({p.x, p.y + 38}); return changed;
}

void DashedRect(ImVec2 a, ImVec2 b, ImU32 col, float dash, float gap, float th) {
    ImDrawList* d = DL(); ImVec2 q[4][2] = {{a, {b.x, a.y}}, {{a.x, b.y}, b}, {a, {a.x, b.y}}, {{b.x, a.y}, b}};
    for (auto& s : q) { float dx = s[1].x - s[0].x, dy = s[1].y - s[0].y, L = sqrtf(dx * dx + dy * dy); for (float t = 0; t < L; t += dash + gap) { float e = ImMin(t + dash, L); d->AddLine({s[0].x + dx * t / L, s[0].y + dy * t / L}, {s[0].x + dx * e / L, s[0].y + dy * e / L}, col, th); } }
}

bool ColorSwatches(const char* id, const ImU32* colors, int n, int* sel) {
    ImVec2 p = ImGui::GetCursorScreenPos(); bool changed = false; ImDrawList* d = DL();
    for (int i = 0; i < n; ++i) {
        ImVec2 c{p.x + 11 + i * 32, p.y + 11}; bool hov, held; char key[64]; snprintf(key, sizeof key, "%s_%d", id, i);
        if (Hit(key, {c.x - 11, c.y - 11}, {22, 22}, &hov, &held)) { *sel = i; changed = true; }
        d->AddCircleFilled(c, 10.f, colors[i]); d->AddCircle(c, 11.f, i == *sel ? col::White(235) : col::White(50), 0, 2.f);
    }
    return changed;
}

bool Dropdown(const char* id, const char* const* items, int n, int* sel, float w) {
    ImVec2 p = ImGui::GetCursorScreenPos(); bool hov, held; bool open = Hit(id, p, {w, 36}, &hov, &held); ImDrawList* d = DL(); bool changed = false;
    d->AddRectFilled(p, {p.x + w, p.y + 36}, col::White(hov ? 30 : 22), 11); d->AddRect(p, {p.x + w, p.y + 36}, col::White(46), 11);
    TextAt({p.x + 14, p.y + 18}, GetFonts().bodyMedium, col::Text(), items[*sel]); DrawIcon(Icon::Down, {p.x + w - 18, p.y + 18}, 15, col::Text2(), 1.8f);
    char pid[64]; snprintf(pid, sizeof pid, "%s_popup", id);
    if (open) ImGui::OpenPopup(pid);
    ImGui::SetNextWindowPos({p.x, p.y + 42}); ImGui::SetNextWindowSize({w, n * 34.f + 12});
    ImGui::PushStyleVar(ImGuiStyleVar_WindowPadding, ImVec2(6, 6)); ImGui::PushStyleVar(ImGuiStyleVar_ItemSpacing, ImVec2(0, 0));
    if (ImGui::BeginPopup(pid)) {
        for (int i = 0; i < n; ++i) if (ImGui::Selectable(items[i], i == *sel, 0, {0, 34})) { *sel = i; changed = true; }
        ImGui::EndPopup();
    }
    ImGui::PopStyleVar(2); return changed;
}

void StatusLabel(const char* text, ImU32 c) {
    ImVec2 p = ImGui::GetCursorScreenPos(); ImGui::PushFont(GetFonts().bodyBold); ImVec2 s = ImGui::CalcTextSize(text); ImGui::PopFont();
    ImDrawList* d = DL(); ImVec2 b{p.x + s.x + 18, p.y + 20};
    d->AddRectFilled(p, b, Mul(c, .16f), 10); d->AddRect(p, b, Mul(c, .5f), 10); TextAt({p.x + 9, p.y + 10}, GetFonts().bodyBold, c, text);
    ImGui::Dummy({s.x + 18, 20});
}

}  // namespace caramel::ui
