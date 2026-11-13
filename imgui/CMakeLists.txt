cmake_minimum_required(VERSION 3.20)
project(caramel_modmenu CXX)
set(CMAKE_CXX_STANDARD 17)
include(FetchContent)
FetchContent_Declare(imgui GIT_REPOSITORY https://github.com/ocornut/imgui.git GIT_TAG v1.91.5)
FetchContent_Declare(glfw  GIT_REPOSITORY https://github.com/glfw/glfw.git  GIT_TAG 3.4)
FetchContent_MakeAvailable(imgui glfw)
find_package(OpenGL REQUIRED)

add_library(imgui_lib STATIC
  ${imgui_SOURCE_DIR}/imgui.cpp ${imgui_SOURCE_DIR}/imgui_draw.cpp ${imgui_SOURCE_DIR}/imgui_tables.cpp ${imgui_SOURCE_DIR}/imgui_widgets.cpp
  ${imgui_SOURCE_DIR}/backends/imgui_impl_glfw.cpp ${imgui_SOURCE_DIR}/backends/imgui_impl_opengl3.cpp)
target_include_directories(imgui_lib PUBLIC ${imgui_SOURCE_DIR} ${imgui_SOURCE_DIR}/backends)
target_link_libraries(imgui_lib PUBLIC glfw OpenGL::GL)

# CaramelMenu is renderer-agnostic: it only needs a Dear ImGui context. Reuse it from any backend (DX11, Vulkan, hook).
add_library(caramel_menu STATIC src/CaramelTheme.cpp src/CaramelWidgets.cpp src/CaramelMenu.cpp)
target_include_directories(caramel_menu PUBLIC src)
target_link_libraries(caramel_menu PUBLIC imgui_lib)

add_executable(caramel_demo src/demo_main.cpp)
target_link_libraries(caramel_demo PRIVATE caramel_menu)
# stb_image single header is fetched for the demo's logo texture
FetchContent_Declare(stb GIT_REPOSITORY https://github.com/nothings/stb.git GIT_TAG master)
FetchContent_MakeAvailable(stb)
target_include_directories(caramel_demo PRIVATE ${stb_SOURCE_DIR})
file(COPY ${CMAKE_SOURCE_DIR}/assets DESTINATION ${CMAKE_BINARY_DIR})
