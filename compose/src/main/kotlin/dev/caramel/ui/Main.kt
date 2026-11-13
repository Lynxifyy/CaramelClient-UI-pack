package dev.caramel.ui

import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.DpSize
import androidx.compose.ui.unit.dp
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.FrameWindowScope
import androidx.compose.ui.window.WindowDraggableArea
import androidx.compose.ui.window.application
import androidx.compose.ui.window.rememberWindowState
import dev.caramel.ui.launcher.CaramelApp

fun main() = application {
    val state = rememberWindowState(size = DpSize(1280.dp, 800.dp))
    Window(
        onCloseRequest = ::exitApplication, state = state, title = "Caramel Client",
        undecorated = true, transparent = true, icon = painterResource("drawable/app_icon.png"),
    ) {
        // No minimize/maximize/close buttons on purpose. Quit lives in the Caramel Client menu (title bar arrow).
        CaramelApp(onQuit = ::exitApplication, dragArea = { content -> WindowDragArea(content) })
    }
}

@Composable
private fun FrameWindowScope.WindowDragArea(content: @Composable () -> Unit) = WindowDraggableArea { content() }
