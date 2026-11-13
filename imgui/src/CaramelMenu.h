#pragma once
#include "CaramelWidgets.h"

namespace caramel {

// One module. The pack ships a single "Example" module on purpose: copy this struct per feature.
struct ModuleExample {
    bool enabled = true;
    float scale = 1.0f, opacity = 0.8f;
    int textColor = 0, position = 0;
    bool background = true, textShadow = true, compact = false;
    char keybind[24] = "Right Shift";
};

// HUD overlays the player can move in "Edit HUD layout" (FPS, Example HUD, Coordinates).
struct HudElement { const char* name; ImVec2 pos; ImVec2 size; float scale = 1.f; bool visible = true; };

enum Tab { TabMods, TabReplay, TabCosmetics, TabVoice, TabSettings };

struct MenuState {
    bool open = true;
    int tab = TabMods;
    int profile = 0, category = 0;
    char search[64] = {};
    bool moduleSettingsOpen = false;
    ModuleExample example;
    // Replay
    bool autoRecord = false; float buffer = 0.3f; int quality = 1; char replayKey[8] = "F8";
    // Cosmetics studio
    int cosCategory = 0, cosSelected = 1; bool fav[6] = {true, false, false, false, true, false}; float rotation = 0.35f, cosScale = 0.5f; int tint = 0;
    // Voice chat
    int inDevice = 0, outDevice = 0; float micVol = 0.8f, outVol = 0.65f, range = 0.45f; bool ptt = true, noiseSuppression = true, proximity = true; char pttKey[8] = "V";
    // Settings
    bool autoJoin = false, chatToggles = true, notifications = true, smoothCamera = false;
    float menuScale = 0.4f, blur = 0.6f; int language = 0, accent = 0; bool rounded = true, animations = true;
    // HUD layout editor
    bool hudEditing = false, snap = true, showGrid = true; int hudSel = 2;
    HudElement hud[3] = {{"FPS", {14, 14}, {98, 26}}, {"Example HUD", {14, 48}, {136, 26}}, {"Coordinates", {1112, 14}, {154, 60}}};
};

// Draws the whole mod menu centered in `display` (or the HUD editor when state.hudEditing). `logo` may be 0.
void RenderMenu(MenuState& s, ImTextureID logo, ImVec2 display);

}  // namespace caramel
