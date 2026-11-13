package dev.caramel.ui.launcher

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Popup
import dev.caramel.ui.components.*
import dev.caramel.ui.data.LauncherState
import dev.caramel.ui.theme.C
import dev.caramel.ui.theme.T

@Composable
fun HomeScreen(state: LauncherState) {
    Row(Modifier.fillMaxSize(), horizontalArrangement = Arrangement.spacedBy(20.dp)) {
        Column(Modifier.weight(1f).fillMaxHeight(), verticalArrangement = Arrangement.spacedBy(20.dp)) {
            Hero(state, Modifier.fillMaxWidth().height(320.dp))
            Row(Modifier.fillMaxWidth()) { Text("Latest news", style = T.Title, modifier = Modifier.weight(1f)); Text("View all news", style = T.Label.copy(color = C.Text2, fontSize = 11.5.sp_)) }
            Row(Modifier.fillMaxWidth().weight(1f), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                NewsCard("Caramel Client 26.2 is here", "Release notes · 2 days ago", listOf(Color(0xFF5A2818), Color(0xFFF5963C)), Modifier.weight(1f))
                NewsCard("Example mod updates", "Mods · 5 days ago", listOf(Color(0xFF182660), Color(0xFF4A5ABE)), Modifier.weight(1f))
                NewsCard("Cosmetics festival", "Store · 1 week ago", listOf(Color(0xFF541C4C), Color(0xFFF06EA0)), Modifier.weight(1f))
            }
        }
        Column(Modifier.width(374.dp).fillMaxHeight(), verticalArrangement = Arrangement.spacedBy(20.dp)) {
            FriendsCard(state, Modifier.fillMaxWidth().height(320.dp))
            PromoCard(Modifier.fillMaxWidth().weight(1f))
        }
    }
}

@Composable
private fun Hero(state: LauncherState, modifier: Modifier) {
    GlassPanel(modifier, RoundedCornerShape(24.dp)) {
        Canvas(Modifier.matchParentSize()) { drawCircle(Brush.radialGradient(listOf(C.Blue.copy(0.28f), Color.Transparent), Offset(size.width * .25f, size.height * .5f), size.width * .5f), center = Offset(size.width * .25f, size.height * .5f), radius = size.width * .5f) }
        Image(painterResource("drawable/apple_logo.png"), null, Modifier.align(Alignment.CenterStart).padding(start = 24.dp).size(210.dp))
        Column(Modifier.align(Alignment.Center).padding(start = 130.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(14.dp)) {
            Text("Ready when you are", style = T.Body)
            LaunchSplitButton(state)
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                GlassButton("Profiles", { state.launchMenu = true }, icon = Icons.Rounded.Folder, height = 32)
                GlassButton("Instances", { state.instanceSettings = true }, icon = Icons.Rounded.Tune, height = 32)
                GlassButton("Screenshots", { state.screenshots = true }, icon = Icons.Rounded.PhotoCamera, height = 32)
            }
            Text("Last played 2 hours ago · ${state.profile.title.substringBefore(" Instance").lowercase()} profile", style = T.Caption)
        }
    }
}

/** LAUNCH GAME with a split chevron that opens the launch menu. */
@Composable
fun LaunchSplitButton(state: LauncherState) {
    val shape = RoundedCornerShape(20.dp)
    Row(
        Modifier.width(340.dp).height(72.dp).clip(shape).background(Brush.verticalGradient(listOf(C.GreenLight, C.GreenDark))).background(Brush.verticalGradient(listOf(Color.White.copy(0.22f), Color.Transparent, Color.Transparent))).border(1.dp, Color.White.copy(0.3f), shape),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(Modifier.weight(1f).fillMaxHeight().clickable(remember { MutableInteractionSource() }, null) { }, Arrangement.Center, Alignment.CenterHorizontally) {
            Text("LAUNCH GAME", style = T.Display.copy(fontSize = 19.sp_, color = C.OnGreen))
            Text("Caramel Client ${state.version.id} · ${state.loader.title.removePrefix("Minecraft ")}", style = T.Chip.copy(color = C.OnGreen.copy(0.85f)))
        }
        Box(Modifier.width(1.dp).height(48.dp).background(C.OnGreen.copy(0.3f)))
        Box(Modifier.width(52.dp).fillMaxHeight().clickable(remember { MutableInteractionSource() }, null) { state.launchMenu = !state.launchMenu }, Alignment.Center) {
            Icon(if (state.launchMenu) Icons.Rounded.KeyboardArrowUp else Icons.Rounded.KeyboardArrowDown, null, Modifier.size(24.dp), C.OnGreen)
        }
    }
}

@Composable
private fun NewsCard(title: String, meta: String, art: List<Color>, modifier: Modifier) {
    GlassPanel(modifier, RoundedCornerShape(18.dp), elevation = 10.dp) {
        Column(Modifier.padding(6.dp)) {
            Box(Modifier.fillMaxWidth().height(150.dp).clip(RoundedCornerShape(13.dp)).background(Brush.verticalGradient(art))) {
                Canvas(Modifier.fillMaxSize()) { // blocky skyline
                    val u = 12.dp.toPx(); var x = 0f; var i = 0
                    while (x < size.width) { val h = size.height * .36f + (kotlin.math.sin(i * .5) * 18.dp.toPx()).toFloat(); drawRect(Color.Black.copy(0.45f), Offset(x, size.height - h), androidx.compose.ui.geometry.Size(u, h)); drawRect(Color.White.copy(0.25f), Offset(x, size.height - h), androidx.compose.ui.geometry.Size(u, 3.dp.toPx())); x += u; i++ }
                }
            }
            Column(Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) { Text(title, style = T.Subtitle.copy(fontSize = 13.5.sp_)); Text(meta, style = T.Body) }
        }
    }
}

@Composable
private fun FriendsCard(state: LauncherState, modifier: Modifier) {
    GlassPanel(modifier, RoundedCornerShape(24.dp)) {
        Column(Modifier.fillMaxSize().padding(22.dp)) {
            Row { Text("Friends", style = T.Title, modifier = Modifier.weight(1f)); Text("View all", style = T.Label.copy(color = C.Text2, fontSize = 11.5.sp_), modifier = Modifier.clickable(remember { MutableInteractionSource() }, null) { state.friendsAll = true }) }
            Column(Modifier.weight(1f).fillMaxWidth(), Arrangement.Center, Alignment.CenterHorizontally) {
                Box(Modifier.size(60.dp).clip(RoundedCornerShape(50)).background(Color.White.copy(0.07f)).border(1.dp, Color.White.copy(0.17f), RoundedCornerShape(50)), Alignment.Center) { Icon(Icons.Rounded.Group, null, Modifier.size(28.dp), C.Text2) }
                Spacer(Modifier.height(16.dp))
                Text("Chat with friends, send game invites, and more.", style = T.Body.copy(fontSize = 12.5.sp_, textAlign = androidx.compose.ui.text.style.TextAlign.Center), modifier = Modifier.width(200.dp))
                Spacer(Modifier.height(16.dp))
                GlassButton("Add your first friend", { state.addFriend = true }, icon = Icons.Rounded.Add)
            }
        }
    }
}

@Composable
private fun PromoCard(modifier: Modifier) {
    GlassPanel(modifier, RoundedCornerShape(24.dp)) {
        Box(Modifier.matchParentSize().background(Brush.verticalGradient(listOf(C.Caramel.copy(0.26f), Color.Transparent))))
        Column(Modifier.fillMaxSize().padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Image(painterResource("drawable/apple_logo.png"), null, Modifier.size(130.dp))
            Text("Become a", style = T.Title.copy(fontSize = 19.sp_))
            Text("Caramel+", style = T.Display.copy(fontSize = 25.sp_, color = C.Caramel))
            Spacer(Modifier.height(8.dp)); Text("Get access to HoneyLoader, The preloader that Honeyclient uses but for Glowberryclient!", style = T.Body.copy(fontSize = 12.5.sp_, textAlign = androidx.compose.ui.text.style.TextAlign.Center), modifier = Modifier.width(310.dp))
            Spacer(Modifier.weight(1f))
            PrimaryButton("Get Caramel+", {}, Modifier.fillMaxWidth(), Tone.Caramel)
        }
    }
}

/** Anchored under the launch button. Chevron toggles it; the gear closes it and opens Instance settings. */
@Composable
fun LaunchMenuOverlay(state: LauncherState) {
    Popup(alignment = Alignment.TopStart, offset = IntOffset(470, 290), onDismissRequest = { state.launchMenu = false }, properties = androidx.compose.ui.window.PopupProperties(focusable = true)) { LaunchMenu(state) }
}

@Composable
fun LaunchMenu(state: LauncherState) {
    GlassPanel(Modifier.width(372.dp), RoundedCornerShape(22.dp), popup = true, elevation = 40.dp) {
        Column(Modifier.padding(22.dp), verticalArrangement = Arrangement.spacedBy(18.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) { Text("Version", style = T.Title.copy(fontSize = 15.sp_), modifier = Modifier.weight(1f)); VersionDropdown(state.version, { state.version = it }) }
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text("Loaders", style = T.Title.copy(fontSize = 15.sp_), modifier = Modifier.weight(1f))
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) { dev.caramel.ui.data.Loader.entries.forEach { LoaderTile(it, state.loader == it, { state.loader = it }) } }
            }
            ProfileDropdown(state.profile, { state.profile = it }, width = 328)
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                GlassButton(null, { state.launchMenu = false; state.instanceSettings = true }, icon = Icons.Rounded.Settings, height = 44)
                PrimaryButton("Launch Game", { state.launchMenu = false }, Modifier.weight(1f), icon = Icons.Rounded.RocketLaunch)
            }
        }
    }
}
