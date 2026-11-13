# Caramel Client UI Pack

Navy glassmorphic UI for a Minecraft client, in the spirit of Lunar Client.

```
compose/              Jetpack Compose Desktop launcher (Haze blur). Open in IntelliJ, run `./gradlew run`
imgui/src/            Dear ImGui mod menu (C++17, CMake): cmake -B build && cmake --build build, run caramel_demo
imgui/optional/       Waypoints menu for a future waypoints mod. NOT part of the pack, not built by CMake
previews/             PNG previews (2560px wide launcher, smooth edges)
  launcher/ mod_menu/ widget_packs/ icon_pack/ app_icon/
preview/              Python scripts that regenerate every preview
assets/ fonts/        Transparent apple logo, Inter + Poppins (SIL OFL)
```

## Launcher (Compose)
Home, Mods (click a mod for its detail menu), Servers, Cosmetics, News, Store, Launcher settings, plus:
Caramel Client menu (title arrow, includes Quit), launch menu (version search, Release/Beta labels, 3 loaders, Open/Isolated profile),
Instance settings (General, Game, Performance, Mods, Advanced), Screenshots, Friends > View all, Add friend, Add account,
Account settings, account popup.

Code labels you asked for: QUICK PLAY tiles = SERVER ICON, INSTANCES COUNT, Microsoft account profile picture slot, 3D skin viewer slot, mod icon slot.
The window has no minimize/maximize/close buttons; quit from the Caramel Client menu.

## Mod menu (ImGui)
Tabs: Mods, Replay, Cosmetics (studio), VC, Settings, plus Edit HUD layout (its own overlay with draggable FPS, Example HUD and Coordinates).
One "Example" module: OPTIONS button and enable toggle share a row. Module settings menu included.

## Notes
- Version list is example data (26.62 down to 1.21.132). Replace it in `data/Models.kt`. Servers show a supported-version range from the same version numbers.
- The previews are drawn by `preview/` from the same tokens and layouts, not screenshots of the running apps. The apple art is pixel art on purpose; everything else is smooth.
- ImGui has no backdrop blur. Glass is layered fills; `ui::SetBlurHook` lets you add a real blur.
- The Kotlin and C++ were written without a build environment and have not been compiled. Pinned: Compose 1.7.3, Haze 1.3.1.
