package dev.caramel.ui.launcher

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
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Popup
import androidx.compose.ui.window.PopupProperties
import dev.caramel.ui.components.*
import dev.caramel.ui.data.LauncherState
import dev.caramel.ui.theme.C
import dev.caramel.ui.theme.T

@Composable
fun AccountMenu(state: LauncherState) {
    if (!state.accountMenu) return
    Popup(alignment = Alignment.TopEnd, offset = IntOffset(-150, 44), onDismissRequest = { state.accountMenu = false }, properties = PopupProperties(focusable = true)) {
        GlassPanel(Modifier.width(238.dp), RoundedCornerShape(20.dp), popup = true, elevation = 36.dp) {
            Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                Row(Modifier.padding(bottom = 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Avatar(44, online = true) // Microsoft account profile picture goes here
                    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) { Text("Example_Player", style = T.Subtitle); StatusLabel("Online", C.Green) }
                }
                MenuItem("Switch account", Icons.Rounded.SwapHoriz, true); MenuItem("Add account", Icons.Rounded.Add) { state.accountMenu = false; state.addAccount = true }; MenuItem("Skin & cosmetics", Icons.Rounded.ViewInAr); MenuItem("Account settings", Icons.Rounded.Settings) { state.accountMenu = false; state.accountSettings = true }; MenuItem("Sign out", Icons.Rounded.Close, danger = true)
            }
        }
    }
}

@Composable
fun MenuItem(text: String, icon: ImageVector, active: Boolean = false, danger: Boolean = false, onClick: () -> Unit = {}) {
    val shape = RoundedCornerShape(10.dp)
    Row(Modifier.fillMaxWidth().height(34.dp).clip(shape).background(if (active) C.Blue.copy(0.2f) else Color.Transparent).clickable(remember { MutableInteractionSource() }, null, onClick = onClick).padding(horizontal = 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        Icon(icon, null, Modifier.size(16.dp), if (danger) C.Red else C.Text2); Text(text, style = T.Label.copy(color = if (danger) C.Red else C.Text, fontWeight = androidx.compose.ui.text.font.FontWeight.Medium))
    }
}

@Composable
fun AddFriendModal(state: LauncherState) = Modal(state.addFriend, { state.addFriend = false }, Modifier.size(400.dp, 300.dp)) {
    var user by remember { mutableStateOf("Example_Friend") }
    Column(Modifier.fillMaxSize().padding(28.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) { Column(Modifier.weight(1f)) { Text("Add a friend", style = T.Title.copy(fontSize = 18.sp_)); Text("Enter their Caramel or Minecraft username", style = T.Body) }; GlassButton(null, { state.addFriend = false }, icon = Icons.Rounded.Close, height = 32) }
        CaramelTextField(user, { user = it }, Modifier.fillMaxWidth(), "Username", Icons.Rounded.Person)
        Row(Modifier.fillMaxWidth().height(40.dp).clip(RoundedCornerShape(12.dp)).background(C.Green.copy(0.11f)).border(1.dp, C.Green.copy(0.4f), RoundedCornerShape(12.dp)).padding(horizontal = 16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            Icon(Icons.Rounded.Check, null, Modifier.size(15.dp), C.Green); Text("$user found", style = T.Label.copy(fontWeight = androidx.compose.ui.text.font.FontWeight.Medium, fontSize = 12.5.sp_))
        }
        Spacer(Modifier.weight(1f))
        Row(horizontalArrangement = Arrangement.spacedBy(14.dp)) { GlassButton("Cancel", { state.addFriend = false }, Modifier.width(140.dp), height = 38); PrimaryButton("Send request", { state.addFriend = false }, Modifier.weight(1f), height = 38) }
    }
}

@Composable
fun LauncherSettingsPanel(close: () -> Unit) {
    var blur by remember { mutableStateOf(0.6f) }; var scale by remember { mutableStateOf(0.4f) }; var lang by remember { mutableStateOf("English (US)") }
    var accent by remember { mutableStateOf(0) }; var a by remember { mutableStateOf(false) }; var b by remember { mutableStateOf(true) }; var c by remember { mutableStateOf(true) }
    Column(Modifier.fillMaxSize().padding(28.dp), verticalArrangement = Arrangement.spacedBy(20.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically) { Text("Settings", style = T.Display, modifier = Modifier.weight(1f)); GlassButton(null, close, icon = Icons.Rounded.Close, height = 32) }
        Text("Appearance", style = T.Title)
        Row(horizontalArrangement = Arrangement.spacedBy(14.dp)) { listOf(C.Caramel, C.Blue, C.Green, Color(0xFF966EFF), C.Red, Color(0xFF4AC8E6)).forEachIndexed { i, col -> Box(Modifier.size(34.dp).background(col, androidx.compose.foundation.shape.CircleShape).border(2.dp, if (i == accent) Color.White else Color.White.copy(0.15f), androidx.compose.foundation.shape.CircleShape).clickable { accent = i }) } }
        SliderRow("Glass blur strength", "${(blur * 40).toInt()}", blur, { blur = it }); SliderRow("Interface scale", "${(80 + scale * 50).toInt()}%", scale, { scale = it })
        SettingRow("Language") { SimpleDropdown(lang, listOf("English (US)", "Español", "Français", "Deutsch"), { lang = it }) }
        SettingRow("Reduce motion", "Turn off launcher animations") { CaramelToggle(a, { a = it }) }
        SettingRow("Open on startup", "Start Caramel Client with your computer") { CaramelToggle(b, { b = it }) }
        SettingRow("Check for updates", "Notify me about new versions") { CaramelToggle(c, { c = it }) }
        Spacer(Modifier.weight(1f))
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) { GlassButton("Check for updates", {}, icon = Icons.Rounded.RocketLaunch); Spacer(Modifier.weight(1f)); PrimaryButton("Save", close, Modifier.width(140.dp), height = 40) }
    }
}
