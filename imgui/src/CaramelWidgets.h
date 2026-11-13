#pragma once
#include "CaramelTheme.h"

namespace caramel::ui {

enum class Tone { Green, Caramel, Blue, Red };
enum class Icon { Close, Check, Search, Down, Up, Left, Plus, Sliders, Hud, Swap, Dots, Puzzle, Replay, Cube, Mic, Gear, Star, StarFill, Play, Map };

// Surfaces
void Glass(ImVec2 a, ImVec2 b, float radius = 18.f, bool shadow = true, ImU32 tint = IM_COL32(150, 175, 255, 14));
void Hairline(float x0, float x1, float y);
// Optional: set a callback that draws a real backdrop blur (copy of the framebuffer) before a Glass surface.
using BlurHook = void (*)(const ImDrawList* parent, const ImDrawCmd* cmd);
void SetBlurHook(BlurHook hook);

// Drawing helpers
void DrawIcon(Icon icon, ImVec2 center, float size, ImU32 color, float thickness = 1.8f);
float Anim(ImGuiID id, float target, float speed = 14.f);
void TextAt(ImVec2 pos, ImFont* font, ImU32 color, const char* text, bool centerX = false, bool centerY = true);

// Controls (all draw with the foreground list and return true on change/click)
bool PrimaryButton(const char* id, const char* label, ImVec2 size, Tone tone = Tone::Green);
bool GlassButton(const char* id, const char* label, ImVec2 size, bool danger = false, bool active = false, const Icon* icon = nullptr);
bool Toggle(const char* id, bool* value);
bool CheckBox(const char* id, const char* label, bool* value);
bool Slider(const char* id, float* v, float lo, float hi);
bool Chip(const char* label, bool active);
bool SearchField(const char* id, char* buf, size_t cap, float width, const char* hint);
bool TextField(const char* id, char* buf, size_t cap, float width);
bool Segmented(const char* id, const char* const* items, int count, int* selected, float itemWidth);
// Segmented tab bar with an icon + label per tab.
bool TabBar(const char* id, const char* const* labels, const Icon* icons, int count, int* selected, float itemWidth);
void DashedRect(ImVec2 a, ImVec2 b, ImU32 color, float dash = 6.f, float gap = 4.f, float thickness = 1.5f);
bool ColorSwatches(const char* id, const ImU32* colors, int count, int* selected);
bool Dropdown(const char* id, const char* const* items, int count, int* selected, float width);
void StatusLabel(const char* text, ImU32 color);

}  // namespace caramel::ui
