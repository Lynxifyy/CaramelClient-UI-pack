// Minimal GLFW + OpenGL3 host. In a real client, call caramel::RenderMenu() from your own ImGui frame.
#define GL_SILENCE_DEPRECATION
#include <GLFW/glfw3.h>
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include "CaramelMenu.h"

static ImTextureID LoadTexture(const char* path) {
    int w, h, n; unsigned char* px = stbi_load(path, &w, &h, &n, 4); if (!px) return 0;
    GLuint t; glGenTextures(1, &t); glBindTexture(GL_TEXTURE_2D, t);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST); glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, px); stbi_image_free(px);
    return (ImTextureID)(intptr_t)t;
}

int main() {
    if (!glfwInit()) return 1;
    glfwWindowHint(GLFW_SAMPLES, 4);
    GLFWwindow* win = glfwCreateWindow(1280, 720, "Caramel Client - Mod Menu", nullptr, nullptr);
    glfwMakeContextCurrent(win); glfwSwapInterval(1);
    IMGUI_CHECKVERSION(); ImGui::CreateContext();
    ImGui_ImplGlfw_InitForOpenGL(win, true); ImGui_ImplOpenGL3_Init("#version 130");
    caramel::LoadFonts("assets"); caramel::ApplyStyle();
    ImTextureID logo = LoadTexture("assets/logo.png"); caramel::MenuState state;
    while (!glfwWindowShouldClose(win)) {
        glfwPollEvents(); ImGui_ImplOpenGL3_NewFrame(); ImGui_ImplGlfw_NewFrame(); ImGui::NewFrame();
        caramel::RenderMenu(state, logo, ImGui::GetIO().DisplaySize); if (!state.open) glfwSetWindowShouldClose(win, 1);
        ImGui::Render(); int w, h; glfwGetFramebufferSize(win, &w, &h);
        glViewport(0, 0, w, h); glClearColor(0.49f, 0.69f, 0.96f, 1); glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData()); glfwSwapBuffers(win);
    }
    ImGui_ImplOpenGL3_Shutdown(); ImGui_ImplGlfw_Shutdown(); ImGui::DestroyContext(); glfwDestroyWindow(win); glfwTerminate();
}
