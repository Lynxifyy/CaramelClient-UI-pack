#include "WaypointsMenu.h"
#include <cstdio>
namespace caramel::optional {
using namespace caramel::ui;
void RenderWaypointsPage(ImVec2 o, ImVec2 size, WaypointsState& s) {
    ImVec2 l{o.x, o.y}; Glass(l, {l.x + 600, o.y + size.y}, 16, false); ImVec2 f{l.x + 624, l.y}; Glass(f, {o.x + size.x, o.y + size.y}, 16, false);
    TextAt({l.x + 22, l.y + 30}, GetFonts().title, col::Text(), "Waypoints"); static const Icon plus = Icon::Plus;
    ImGui::SetCursorScreenPos({l.x + 600 - 170, l.y + 14}); GlassButton("addwp", "Add waypoint", {152, 32}, false, true, &plus);
    static const char* names[] = {"Example base", "Example mine", "Example portal"};
    for (int i = 0; i < 3; ++i) {
        ImVec2 a{l.x + 16, l.y + 66 + i * 62}; ImGui::GetWindowDrawList()->AddRectFilled(a, {a.x + 568, a.y + 54}, IM_COL32(255, 255, 255, 14), 13);
        TextAt({a.x + 16, a.y + 20}, GetFonts().bodyMedium, col::Text(), names[i]); TextAt({a.x + 16, a.y + 38}, GetFonts().body, col::Text2(), "X 128  Y 64  Z -230  -  Overworld");
        ImGui::SetCursorScreenPos({a.x + 514, a.y + 16}); char id[16]; snprintf(id, 16, "wp%d", i); Toggle(id, &s.enabled[i]);
    }
    float fw = o.x + size.x - f.x - 44; TextAt({f.x + 22, f.y + 30}, GetFonts().title, col::Text(), "New waypoint");
    ImGui::SetCursorScreenPos({f.x + 22, f.y + 70}); ImGui::SetNextItemWidth(fw); ImGui::InputText("##wpn", s.name, sizeof s.name);
    char* fields[] = {s.x, s.y, s.z}; for (int i = 0; i < 3; ++i) { ImGui::SetCursorScreenPos({f.x + 22 + i * (fw / 3 + 2), f.y + 126}); ImGui::SetNextItemWidth(fw / 3 - 8); char id[8]; snprintf(id, 8, "##c%d", i); ImGui::InputText(id, fields[i], 12); }
    ImGui::SetCursorScreenPos({f.x + 22, f.y + 190}); CheckBox("beam", "Show beam in world", &s.beam);
    ImGui::SetCursorScreenPos({f.x + 22, o.y + size.y - 64}); PrimaryButton("savewp", "Save waypoint", {fw, 42}, Tone::Green);
}
}
