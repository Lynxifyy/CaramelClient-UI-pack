#pragma once
#include "imgui.h"

namespace caramel {

// Design tokens (match previews/widget_packs/07_design_tokens.png)
namespace col {
inline ImU32 Abyss()     { return IM_COL32(6, 11, 26, 255); }
inline ImU32 Navy()      { return IM_COL32(10, 19, 48, 255); }
inline ImU32 Blue()      { return IM_COL32(74, 120, 255, 255); }
inline ImU32 BlueLight() { return IM_COL32(98, 140, 255, 255); }
inline ImU32 BlueDark()  { return IM_COL32(52, 88, 230, 255); }
inline ImU32 Caramel()   { return IM_COL32(245, 167, 66, 255); }
inline ImU32 Green()     { return IM_COL32(47, 211, 107, 255); }
inline ImU32 GreenLight(){ return IM_COL32(62, 226, 122, 255); }
inline ImU32 GreenDark() { return IM_COL32(24, 160, 80, 255); }
inline ImU32 Red()       { return IM_COL32(255, 84, 104, 255); }
inline ImU32 Orange()    { return IM_COL32(255, 159, 46, 255); }
inline ImU32 Text()      { return IM_COL32(234, 240, 255, 255); }
inline ImU32 Text2()     { return IM_COL32(154, 168, 208, 255); }
inline ImU32 Text3()     { return IM_COL32(102, 116, 158, 255); }
inline ImU32 OnGreen()   { return IM_COL32(6, 36, 18, 255); }
inline ImU32 White(int a){ return IM_COL32(255, 255, 255, a); }
}

struct Fonts { ImFont* body = nullptr; ImFont* bodyMedium = nullptr; ImFont* bodyBold = nullptr; ImFont* title = nullptr; ImFont* display = nullptr; };

// Loads Inter + Poppins from `assetDir` (call before the first frame, before building the font atlas).
Fonts LoadFonts(const char* assetDir);
// Applies Caramel style colors, rounding and spacing to the current ImGui context.
void ApplyStyle();
Fonts& GetFonts();

}  // namespace caramel
