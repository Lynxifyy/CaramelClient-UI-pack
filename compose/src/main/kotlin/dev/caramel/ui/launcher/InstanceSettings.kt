package dev.caramel.ui.launcher

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
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
import androidx.compose.ui.unit.dp
import dev.caramel.ui.components.*
import dev.caramel.ui.data.*
import dev.caramel.ui.theme.C
import dev.caramel.ui.theme.T

/** Bigger modal opened by the gear in the launch menu. */
@Composable
fun InstanceSettingsModal(state: LauncherState) =
    Modal(state.instanceSettings, { state.instanceSettings = false }, Modifier.size(900.dp, 670.dp)) { InstanceSettingsPanel(state) { state.instanceSettings = false } }

private val sections = listOf("General" to Icons.Rounded.Tune, "Game" to Icons.Rounded.SportsEsports, "Performance" to Icons.Rounded.Bolt, "Mods" to Icons.Rounded.Extension, "Advanced" to Icons.Rounded.Settings)

@Composable
private fun InstanceSettingsPanel(state: LauncherState, close: () -> Unit) {
    var section by remember { mutableStateOf(0) }
    var name by remember { mutableStateOf("Caramel Client ${state.version.id} (example)") }
    var memory by remember { mutableStateOf(0.42f) }; var render by remember { mutableStateOf(0.55f) }
    var closeLauncher by remember { mutableStateOf(true) }; var console by remember { mutableStateOf(false) }; var fullscreen by remember { mutableStateOf(false) }
    var fps by remember { mutableStateOf("Unlimited") }; var sim by remember { mutableStateOf(0.35f) }; var vsync by remember { mutableStateOf(true) }
    var priority by remember { mutableStateOf("Normal") }; var preset by remember { mutableStateOf(1) }; var gpu by remember { mutableStateOf(true) }; var bg by remember { mutableStateOf(true) }
    var args by remember { mutableStateOf("--example-flag") }; var pre by remember { mutableStateOf("") }; var env by remember { mutableStateOf("") }; var verbose by remember { mutableStateOf(false) }
    Column(Modifier.fillMaxSize()) {
        Row(Modifier.fillMaxWidth().padding(start = 32.dp, end = 24.dp, top = 24.dp, bottom = 18.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f)) { Text("Instance settings", style = T.Display.copy(fontSize = 20.sp_, fontWeight = androidx.compose.ui.text.font.FontWeight.Medium)); Text("Caramel Client ${state.version.id} · ${state.loader.title.removePrefix("Minecraft ")} · ${state.profile.title.substringBefore(" Instance")} profile", style = T.Body) }
            ProfileLabel(state.profile); Spacer(Modifier.width(12.dp)); GlassButton(null, close, icon = Icons.Rounded.Close, height = 32)
        }
        Divider()
        Row(Modifier.weight(1f)) {
            Column(Modifier.width(216.dp).padding(20.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                sections.forEachIndexed { i, (t, ic) -> SideItem(t, ic, i == section) { section = i } }
            }
            Box(Modifier.width(1.dp).fillMaxHeight().background(Color.White.copy(0.08f)))
            Column(Modifier.weight(1f).verticalScroll(rememberScrollState()).padding(28.dp), verticalArrangement = Arrangement.spacedBy(22.dp)) {
                when (section) {
                    0 -> { // General
                        Field("Instance name") { CaramelTextField(name, { name = it }, Modifier.fillMaxWidth()) }
                        SettingRow("Game version") { VersionDropdown(state.version, { state.version = it }) }
                        SettingRow("Loader") { Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) { Loader.entries.forEach { LoaderTile(it, state.loader == it, { state.loader = it }) } } }
                        SettingRow("Profile mode", "Separate files, worlds and mods") { ProfileLabel(state.profile) }
                        SettingRow("Close launcher on start", "Hide the launcher while the game runs") { CaramelToggle(closeLauncher, { closeLauncher = it }) }
                        SettingRow("Show console output", "Open a log window next to the game") { CaramelToggle(console, { console = it }) }
                    }
                    1 -> { // Game (window size was removed on purpose)
                        SliderRow("Render distance", "${(2 + render * 20).toInt()} chunks", render, { render = it })
                        SliderRow("Simulation distance", "${(4 + sim * 12).toInt()} chunks", sim, { sim = it })
                        SettingRow("FPS limit") { SimpleDropdown(fps, listOf("30", "60", "144", "Unlimited"), { fps = it }, width = 200) }
                        SettingRow("Fullscreen", "Start in exclusive fullscreen") { CaramelToggle(fullscreen, { fullscreen = it }) }
                        SettingRow("VSync", "Match your display refresh rate") { CaramelToggle(vsync, { vsync = it }) }
                    }
                    2 -> { // Performance
                        SliderRow("Allocated memory", "${(1 + memory * 7).toInt()} GB", memory, { memory = it }, C.Caramel, C.CaramelDark)
                        SettingRow("Process priority") { SimpleDropdown(priority, listOf("Low", "Normal", "High"), { priority = it }, width = 200) }
                        SettingRow("Memory preset") { Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) { listOf("Low", "Balanced", "High").forEachIndexed { i, t -> FilterChip(t, preset == i, { preset = i }) } } }
                        SettingRow("Use dedicated GPU", "Prefer your faster graphics card") { CaramelToggle(gpu, { gpu = it }) }
                        SettingRow("Reduce background tasks", "Pause downloads while playing") { CaramelToggle(bg, { bg = it }) }
                    }
                    3 -> { // Mods for this instance
                        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) { GlassButton("Update all", {}, icon = Icons.Rounded.RocketLaunch); GlassButton("Open mods folder", {}, icon = Icons.Rounded.Folder) }
                        ExampleMods.take(5).forEachIndexed { i, m ->
                            var on by remember { mutableStateOf(i != 3) }
                            Row(Modifier.fillMaxWidth().clip(RoundedCornerShape(13.dp)).background(Color.White.copy(0.06f)).border(1.dp, Color.White.copy(0.12f), RoundedCornerShape(13.dp)).padding(12.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                Box(Modifier.size(28.dp).background(C.Blue.copy(0.25f), RoundedCornerShape(8.dp)), Alignment.Center) { Icon(Icons.Rounded.Extension, null, Modifier.size(15.dp), C.Blue) }
                                Column(Modifier.weight(1f)) { Text(m.name, style = T.Label); Text("v${m.version}", style = T.Caption) }
                                CaramelToggle(on, { on = it })
                            }
                        }
                    }
                    else -> { // Advanced
                        Field("Launch arguments") { CaramelTextField(args, { args = it }, Modifier.fillMaxWidth(), "Extra launch arguments") }
                        Field("Pre-launch command") { CaramelTextField(pre, { pre = it }, Modifier.fillMaxWidth(), "Runs before the game starts") }
                        Field("Environment variables") { CaramelTextField(env, { env = it }, Modifier.fillMaxWidth(), "KEY=value") }
                        SettingRow("Verbose logging", "Write detailed logs for troubleshooting") { CaramelToggle(verbose, { verbose = it }) }
                    }
                }
            }
        }
        Divider()
        Row(Modifier.fillMaxWidth().padding(24.dp, 16.dp), horizontalArrangement = Arrangement.spacedBy(10.dp), verticalAlignment = Alignment.CenterVertically) {
            GlassButton("Open folder", {}, icon = Icons.Rounded.Folder); GlassButton("Repair", {}, icon = Icons.Rounded.Build); GlassButton("Delete", {}, icon = Icons.Rounded.Delete, danger = true)
            Spacer(Modifier.weight(1f)); GlassButton("Reset", {}); PrimaryButton("Save changes", close, Modifier.width(148.dp), height = 40)
        }
    }
}

@Composable private fun Divider() = Box(Modifier.fillMaxWidth().padding(horizontal = 24.dp).height(1.dp).background(Color.White.copy(0.09f)))
@Composable private fun Field(title: String, content: @Composable () -> Unit) = Column(verticalArrangement = Arrangement.spacedBy(8.dp)) { Text(title, style = T.Label); content() }
@Composable
private fun SideItem(text: String, icon: ImageVector, active: Boolean, onClick: () -> Unit) {
    val shape = RoundedCornerShape(11.dp)
    Row(Modifier.fillMaxWidth().height(38.dp).clip(shape).background(if (active) C.Blue.copy(0.24f) else Color.Transparent).then(if (active) Modifier.border(1.dp, C.Blue.copy(0.45f), shape) else Modifier).clickable(remember { MutableInteractionSource() }, null, onClick = onClick).padding(horizontal = 14.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
        Icon(icon, null, Modifier.size(17.dp), if (active) C.Text else C.Text3); Text(text, style = T.Label.copy(color = if (active) C.Text else C.Text2))
    }
}
