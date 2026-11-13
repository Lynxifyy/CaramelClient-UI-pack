package dev.caramel.ui.launcher

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import dev.caramel.ui.components.*
import dev.caramel.ui.data.LauncherState
import dev.caramel.ui.data.Tab
import dev.caramel.ui.theme.*
import dev.chrisbanes.haze.HazeState
import dev.chrisbanes.haze.hazeSource

@Composable
fun CaramelApp(onQuit: () -> Unit, dragArea: @Composable (@Composable () -> Unit) -> Unit) {
    val backdrop = remember { HazeState() }
    val window = remember { HazeState() }
    val state = remember { LauncherState() }
    CompositionLocalProvider(LocalHaze provides backdrop, LocalWindowHaze provides window) {
        Box(Modifier.fillMaxSize().clip(RoundedCornerShape(16.dp)).background(C.Abyss)) {
            Box(Modifier.fillMaxSize().hazeSource(window)) {
                Box(Modifier.fillMaxSize().hazeSource(backdrop)) { Backdrop() }
                Column(Modifier.fillMaxSize()) {
                    dragArea { TitleBar(state) }
                    Row(Modifier.fillMaxSize().padding(start = 14.dp, end = 14.dp, bottom = 14.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        Sidebar(state)
                        Box(Modifier.weight(1f).fillMaxHeight()) {
                            when (state.tab) {
                                Tab.Home -> HomeScreen(state)
                                Tab.Mods -> ModsScreen(state)
                                Tab.Servers -> ServersScreen()
                                Tab.Cosmetics -> CosmeticsScreen()
                                Tab.News -> NewsScreen()
                                Tab.Store -> StoreScreen()
                            }
                        }
                    }
                }
            }
            // Overlays live outside the window blur source so they can sample it.
            if (state.launchMenu) LaunchMenuOverlay(state)
            AccountMenu(state)
            AppMenu(state, onQuit)
            ModDetailModal(state); ScreenshotsModal(state); FriendsModal(state); AddAccountModal(state); AccountSettingsModal(state)
            InstanceSettingsModal(state)
            AddFriendModal(state)
            Modal(state.launcherSettings, { state.launcherSettings = false }, Modifier.size(900.dp, 640.dp)) { LauncherSettingsPanel { state.launcherSettings = false } }
        }
    }
}

@Composable
private fun TitleBar(state: LauncherState) {
    Row(Modifier.fillMaxWidth().height(44.dp).padding(horizontal = 14.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Image(painterResource("drawable/apple_logo.png"), null, Modifier.size(30.dp))
        Text("Caramel Client", style = T.Subtitle)
        // Opens the Caramel Client menu (AppMenu)
        val menuShape = RoundedCornerShape(8.dp)
        Box(Modifier.size(22.dp).clip(menuShape).background(Color.White.copy(if (state.appMenu) 0.14f else 0.06f)).border(1.dp, Color.White.copy(0.18f), menuShape).clickable(remember { MutableInteractionSource() }, null) { state.appMenu = !state.appMenu }, Alignment.Center) {
            Icon(if (state.appMenu) Icons.Rounded.KeyboardArrowUp else Icons.Rounded.KeyboardArrowDown, null, Modifier.size(15.dp), C.Text2)
        }
        Pill { Icon(Icons.Rounded.RocketLaunch, null, Modifier.size(13.dp), C.Text2); Text("Launchpad", style = T.Label.copy(fontSize = 11.5.sp_, color = C.Text2)) }
        Spacer(Modifier.width(12.dp)); Text("Quick play", style = T.Caption)
        // QUICK PLAY: every tile here is a SERVER ICON (swap the placeholder for the server's icon image).
        listOf(C.Caramel, C.Blue, C.Green, C.Red, Color(0xFF966EFF), Color(0xFF4AC8E6), Color(0xFFFF8C3C), Color(0xFF7882FF)).forEach { ServerIcon(it, 26) }
        Spacer(Modifier.weight(1f))
        // INSTANCES COUNT: number of game instances currently running.
        Text("${state.runningInstances} instances", style = T.Caption)
        Pill(Modifier.clickable(remember { MutableInteractionSource() }, null) { state.accountMenu = !state.accountMenu }) {
            Avatar(18) // <- Microsoft account profile picture goes here
            Text("Sign in", style = T.Label.copy(fontSize = 11.5.sp_)); Icon(Icons.Rounded.KeyboardArrowDown, null, Modifier.size(14.dp), C.Text3)
        }
    }
}

@Composable
fun Pill(modifier: Modifier = Modifier, content: @Composable RowScope.() -> Unit) {
    val shape = RoundedCornerShape(50)
    Row(modifier.height(26.dp).clip(shape).background(Color.White.copy(0.07f)).border(1.dp, Color.White.copy(0.16f), shape).padding(horizontal = 10.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(7.dp), content = content)
}

private val nav = listOf(Tab.Home to Icons.Rounded.SportsEsports, Tab.Mods to Icons.Rounded.Extension, Tab.Servers to Icons.Rounded.Public, Tab.Cosmetics to Icons.Rounded.ViewInAr, Tab.News to Icons.Rounded.Article, Tab.Store to Icons.Rounded.ShoppingCart)

@Composable
private fun Sidebar(state: LauncherState) {
    GlassPanel(Modifier.width(56.dp).fillMaxHeight(), RoundedCornerShape(18.dp), elevation = 12.dp) {
        Column(Modifier.fillMaxSize().padding(vertical = 14.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(10.dp)) {
            nav.forEach { (tab, icon) -> NavItem(icon, state.tab == tab) { state.tab = tab } }
            Spacer(Modifier.weight(1f))
            NavItem(Icons.Rounded.Settings, state.launcherSettings) { state.launcherSettings = true }
        }
    }
}

@Composable
private fun NavItem(icon: ImageVector, active: Boolean, onClick: () -> Unit) {
    Box(Modifier.size(44.dp), Alignment.Center) {
        Box(Modifier.size(44.dp).clip(RoundedCornerShape(13.dp)).background(if (active) Color.White.copy(0.12f) else Color.Transparent).then(if (active) Modifier.border(1.dp, Color.White.copy(0.2f), RoundedCornerShape(13.dp)) else Modifier).clickable(remember { MutableInteractionSource() }, null, onClick = onClick), Alignment.Center) {
            Icon(icon, null, Modifier.size(22.dp), if (active) C.Text else C.Text3)
        }
        if (active) Box(Modifier.align(Alignment.CenterStart).offset((-14).dp).size(3.dp, 22.dp).background(C.Caramel, RoundedCornerShape(2.dp)))
    }
}

internal val Int.sp_ get() = androidx.compose.ui.unit.TextUnit(this.toFloat(), androidx.compose.ui.unit.TextUnitType.Sp)
internal val Double.sp_ get() = androidx.compose.ui.unit.TextUnit(this.toFloat(), androidx.compose.ui.unit.TextUnitType.Sp)
