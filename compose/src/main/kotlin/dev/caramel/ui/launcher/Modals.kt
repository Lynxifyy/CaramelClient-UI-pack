package dev.caramel.ui.launcher

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Popup
import androidx.compose.ui.window.PopupProperties
import dev.caramel.ui.components.*
import dev.caramel.ui.data.*
import dev.caramel.ui.theme.C
import dev.caramel.ui.theme.T

@Composable private fun ModalHeader(title: String, sub: String?, onClose: () -> Unit, actions: @Composable RowScope.() -> Unit = {}) =
    Row(Modifier.fillMaxWidth().padding(start = 32.dp, end = 24.dp, top = 24.dp, bottom = 16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        Column(Modifier.weight(1f)) { Text(title, style = T.Title.copy(fontSize = 20.sp_)); if (sub != null) Text(sub, style = T.Body) }
        actions(); GlassButton(null, onClose, icon = Icons.Rounded.Close, height = 32)
    }
@Composable private fun Rule() = Box(Modifier.fillMaxWidth().padding(horizontal = 24.dp).height(1.dp).background(Color.White.copy(0.09f)))

/** Caramel Client menu: opened by the arrow beside the title. Quit lives here because the window has no close button. */
@Composable
fun AppMenu(state: LauncherState, onQuit: () -> Unit) {
    if (!state.appMenu) return
    Popup(alignment = Alignment.TopStart, offset = IntOffset(14, 42), onDismissRequest = { state.appMenu = false }, properties = PopupProperties(focusable = true)) {
        GlassPanel(Modifier.width(262.dp), RoundedCornerShape(18.dp), popup = true, elevation = 36.dp) {
            Column(Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                MenuItem("Launcher settings", Icons.Rounded.Settings, true) { state.appMenu = false; state.launcherSettings = true }
                MenuItem("Check for updates", Icons.Rounded.RocketLaunch) { state.appMenu = false }
                MenuItem("Release notes", Icons.Rounded.Article) { state.appMenu = false; state.tab = Tab.News }
                MenuItem("Community", Icons.Rounded.Group) { state.appMenu = false }
                MenuItem("About Caramel Client", Icons.Rounded.Info) { state.appMenu = false }
                Box(Modifier.fillMaxWidth().padding(vertical = 6.dp, horizontal = 6.dp).height(1.dp).background(Color.White.copy(0.1f)))
                MenuItem("Quit Caramel Client", Icons.Rounded.Close, danger = true) { onQuit() }
            }
        }
    }
}

/** Opens when a mod card is clicked: icon, description, Remove, Edit config. */
@Composable
fun ModDetailModal(state: LauncherState) {
    val idx = state.selectedMod
    Modal(idx != null, { state.selectedMod = null }, Modifier.size(560.dp, 470.dp)) {
        val m = ExampleMods[idx ?: 0]; var enabled by remember(idx) { mutableStateOf(true) }
        Column(Modifier.fillMaxSize()) {
            Row(Modifier.fillMaxWidth().padding(start = 32.dp, end = 20.dp, top = 28.dp), horizontalArrangement = Arrangement.spacedBy(20.dp)) {
                // MOD ICON slot
                Box(Modifier.size(80.dp).background(C.Blue.copy(0.2f), RoundedCornerShape(22.dp)).border(1.2.dp, C.Blue.copy(0.6f), RoundedCornerShape(22.dp)), Alignment.Center) { Icon(Icons.Rounded.Extension, null, Modifier.size(38.dp), C.Blue) }
                Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    Text(m.name, style = T.Display.copy(fontSize = 21.sp_)); Text("by ${m.author} · v${m.version}", style = T.Body.copy(fontSize = 12.5.sp_))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) { StatusLabel("Utility", C.Text2); StatusLabel("Installed", C.Green) }
                }
                GlassButton(null, { state.selectedMod = null }, icon = Icons.Rounded.Close, height = 34)
            }
            Column(Modifier.weight(1f).padding(32.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
                Text("Description", style = T.Subtitle.copy(color = C.Text2)); Text(m.description, style = T.Label.copy(fontWeight = androidx.compose.ui.text.font.FontWeight.Normal, lineHeight = 21.sp_))
                Row(horizontalArrangement = Arrangement.spacedBy(12.dp)) { listOf("Size" to m.size, "Updated" to "3 days ago", "Author" to m.author).forEach { (a, b) -> Column(Modifier.width(154.dp).clip(RoundedCornerShape(14.dp)).background(Color.White.copy(0.06f)).border(1.dp, Color.White.copy(0.12f), RoundedCornerShape(14.dp)).padding(14.dp)) { Text(a, style = T.Caption); Text(b, style = T.Label) } } }
                SettingRow("Enabled") { CaramelToggle(enabled, { enabled = it }) }
            }
            Rule()
            Row(Modifier.fillMaxWidth().padding(24.dp, 18.dp), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                GlassButton("Remove", { state.selectedMod = null }, icon = Icons.Rounded.Delete, danger = true)
                Spacer(Modifier.weight(1f)); PrimaryButton("Edit config", {}, Modifier.width(180.dp), Tone.Blue, Icons.Rounded.Edit, 40)
            }
        }
    }
}

@Composable
fun ScreenshotsModal(state: LauncherState) = Modal(state.screenshots, { state.screenshots = false }, Modifier.size(980.dp, 700.dp)) {
    var selected by remember { mutableStateOf(1) }; var chip by remember { mutableStateOf(0) }
    Column(Modifier.fillMaxSize()) {
        ModalHeader("Screenshots", "12 screenshots · ${state.profile.title.substringBefore(" Instance")} profile", { state.screenshots = false }) { GlassButton("Open folder", {}, icon = Icons.Rounded.Folder, height = 32) }
        Row(Modifier.padding(start = 32.dp, bottom = 12.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) { listOf("All", "Today", "This week").forEachIndexed { i, t -> FilterChip(t, chip == i, { chip = i }) } }
        val tints = listOf(C.Blue, C.Caramel, C.Green, Color(0xFF966EFF), C.Red, Color(0xFF4AC8E6))
        LazyVerticalGrid(GridCells.Fixed(4), Modifier.weight(1f).padding(horizontal = 32.dp), horizontalArrangement = Arrangement.spacedBy(16.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
            items((0 until 12).toList()) { i ->
                Column(Modifier.clickable(remember { MutableInteractionSource() }, null) { selected = i }, verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    // Thumbnail slot: show the screenshot image here.
                    Box(Modifier.fillMaxWidth().height(118.dp).clip(RoundedCornerShape(14.dp)).background(Brush.verticalGradient(listOf(tints[i % 6].copy(0.55f), Color(0xFF0A1330)))).border(if (i == selected) 2.dp else 1.dp, if (i == selected) C.Blue else Color.White.copy(0.16f), RoundedCornerShape(14.dp)))
                    Text("2026-11-${10 - i / 2}_21.${10 + i}.12.png", style = T.Caption)
                }
            }
        }
        Rule()
        Row(Modifier.fillMaxWidth().padding(24.dp, 18.dp), horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.CenterVertically) {
            Text("1 selected", style = T.Label, modifier = Modifier.weight(1f)); GlassButton("Copy", {}, icon = Icons.Rounded.ContentCopy); GlassButton("Open", {}, icon = Icons.Rounded.Folder); GlassButton("Delete", {}, icon = Icons.Rounded.Delete, danger = true)
        }
    }
}

@Composable
fun FriendsModal(state: LauncherState) = Modal(state.friendsAll, { state.friendsAll = false }, Modifier.size(620.dp, 700.dp)) {
    var tab by remember { mutableStateOf(0) }; var q by remember { mutableStateOf("") }
    Column(Modifier.fillMaxSize()) {
        ModalHeader("Friends", null, { state.friendsAll = false }) { PrimaryButton("Add friend", { state.friendsAll = false; state.addFriend = true }, Modifier.width(146.dp), Tone.Blue, Icons.Rounded.Add, 34) }
        Row(Modifier.padding(start = 32.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) { listOf("All", "Requests", "Blocked").forEachIndexed { i, t -> FilterChip(t, tab == i, { tab = i }) } }
        SearchField(q, { q = it }, "Search friends", Modifier.fillMaxWidth().padding(32.dp, 14.dp))
        LazyColumn(Modifier.weight(1f).padding(horizontal = 24.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            item { Text("Online · 2", style = T.Label.copy(color = C.Text2, fontSize = 12.sp_), modifier = Modifier.padding(start = 8.dp, top = 6.dp)) }
            items(listOf("Example_Friend1" to "Playing Caramel Client 26.60", "Example_Friend2" to "In the launcher")) { (n, s) -> FriendRow(n, s, true) }
            item { Text("Offline · 3", style = T.Label.copy(color = C.Text2, fontSize = 12.sp_), modifier = Modifier.padding(start = 8.dp, top = 14.dp)) }
            items((3..5).toList()) { FriendRow("Example_Friend$it", "Last seen ${it - 2}h ago", false) }
        }
    }
}

@Composable
private fun FriendRow(name: String, status: String, online: Boolean) {
    val shape = RoundedCornerShape(14.dp)
    Row(Modifier.fillMaxWidth().clip(shape).background(Color.White.copy(0.05f)).border(1.dp, Color.White.copy(0.1f), shape).padding(14.dp, 12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(14.dp)) {
        Avatar(36, online) // Microsoft profile picture of the friend goes here
        Column(Modifier.weight(1f)) { Text(name, style = T.Label); Text(status, style = T.Caption.copy(color = if (online) C.Green else C.Text3)) }
        if (online) GlassButton("Invite", {}, icon = Icons.Rounded.Add, height = 34)
        GlassButton(null, {}, icon = Icons.Rounded.MoreHoriz, height = 34)
    }
}

/** Microsoft sign-in: browser button plus a device code fallback. */
@Composable
fun AddAccountModal(state: LauncherState) = Modal(state.addAccount, { state.addAccount = false }, Modifier.size(460.dp, 520.dp)) {
    Column(Modifier.fillMaxSize()) {
        ModalHeader("Add account", "Sign in with the Microsoft account that owns Minecraft", { state.addAccount = false })
        Column(Modifier.weight(1f).padding(horizontal = 32.dp), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            Row(Modifier.fillMaxWidth().height(56.dp).clip(RoundedCornerShape(16.dp)).background(Color.White).clickable {}, verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.Center) {
                Text("Sign in with Microsoft", style = T.Label.copy(color = Color(0xFF1C2446), fontSize = 14.5.sp_))
            }
            Text("or use a device code", style = T.Caption, modifier = Modifier.align(Alignment.CenterHorizontally))
            Column(Modifier.fillMaxWidth().clip(RoundedCornerShape(18.dp)).background(Color(0x78040A1A)).border(1.dp, Color.White.copy(0.16f), RoundedCornerShape(18.dp)).padding(20.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                Text("ABCD-1234", style = T.Display.copy(fontSize = 30.sp_, letterSpacing = 3.sp_)); Text("Code expires in 14:52", style = T.Body)
            }
            Text("Open microsoft.com/link on any device and enter this code.", style = T.Body.copy(fontSize = 12.5.sp_, textAlign = TextAlign.Center), modifier = Modifier.fillMaxWidth())
            GlassButton("Copy code", {}, Modifier.align(Alignment.CenterHorizontally), icon = Icons.Rounded.ContentCopy)
        }
        Rule()
        Row(Modifier.fillMaxWidth().padding(24.dp, 18.dp), verticalAlignment = Alignment.CenterVertically) { GlassButton("Cancel", { state.addAccount = false }); Spacer(Modifier.weight(1f)); Text("Waiting for sign-in…", style = T.Body) }
    }
}

@Composable
fun AccountSettingsModal(state: LauncherState) = Modal(state.accountSettings, { state.accountSettings = false }, Modifier.size(720.dp, 680.dp)) {
    var status by remember { mutableStateOf(true) }; var requests by remember { mutableStateOf(true) }; var activity by remember { mutableStateOf(false) }; var default by remember { mutableStateOf("Example_Player") }
    Column(Modifier.fillMaxSize()) {
        ModalHeader("Account settings", null, { state.accountSettings = false }); Rule()
        Column(Modifier.weight(1f).padding(32.dp), verticalArrangement = Arrangement.spacedBy(22.dp)) {
            Row(horizontalArrangement = Arrangement.spacedBy(18.dp), verticalAlignment = Alignment.CenterVertically) {
                Avatar(88) // Microsoft account profile picture goes here
                Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(4.dp)) { Text("Example_Player", style = T.Display.copy(fontSize = 19.sp_)); Text("example@outlook.com", style = T.Body.copy(fontSize = 12.5.sp_)); StatusLabel("Microsoft account linked", C.Green) }
                GlassButton("Manage on Microsoft", {}, icon = Icons.Rounded.Public)
            }
            Text("Privacy", style = T.Subtitle.copy(color = C.Text2))
            SettingRow("Show my online status", "Friends can see when you are playing") { CaramelToggle(status, { status = it }) }
            SettingRow("Allow friend requests", "Anyone can send you a request") { CaramelToggle(requests, { requests = it }) }
            SettingRow("Share what I am playing", "Show your server and version") { CaramelToggle(activity, { activity = it }) }
            SettingRow("Default account") { SimpleDropdown(default, listOf("Example_Player"), { default = it }, width = 220) }
        }
        Rule()
        Row(Modifier.fillMaxWidth().padding(24.dp, 18.dp)) { GlassButton("Sign out", {}, icon = Icons.Rounded.Close, danger = true); Spacer(Modifier.weight(1f)); PrimaryButton("Save", { state.accountSettings = false }, Modifier.width(148.dp), height = 40) }
    }
}
