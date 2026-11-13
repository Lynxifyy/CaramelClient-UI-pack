// OPTIONAL: UI for a future Waypoints mod. Not part of the core Caramel UI pack and not built by CMakeLists.txt.
// To use it, add WaypointsMenu.cpp to your target and call RenderWaypointsPage() from your own mod menu tab.
#pragma once
#include "../src/CaramelWidgets.h"

namespace caramel::optional {
struct WaypointsState {
    char name[48] = "Example waypoint"; char x[12] = "128", y[12] = "64", z[12] = "-230"; bool beam = true; bool enabled[3] = {true, true, false};
};
// Draws inside the rectangle [origin, origin + size]. Parent is responsible for the surrounding menu chrome.
void RenderWaypointsPage(ImVec2 origin, ImVec2 size, WaypointsState& s);
}
