package dev.caramel.ui.launcher

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import dev.caramel.ui.data.*
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.*
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import dev.caramel.ui.components.*
import dev.caramel.ui.theme.C
import dev.caramel.ui.theme.T

private val accents = listOf(C.Blue, C.Caramel, C.Green, Color(0xFF966EFF))

@Composable
private fun Page(title: String, sub: String, actions: @Composable RowScope.() -> Unit = {}, body: @Composable ColumnScope.() -> Unit) {
    Column(Modifier.fillMaxSize(), verticalArrangement = Arrangement.spacedBy(18.dp)) {
        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
            Column(Modifier.weight(1f)) { Text(title, style = T.Display); Text(sub, style = T.Body.copy(fontSize = 12.5.sp_)) }; actions()
        }
        body()
    }
}

@Composable
private fun IconTile(icon: ImageVector, color: Color, size: Int = 48) =
    Box(Modifier.size(size.dp).background(color.copy(0.2f), RoundedCornerShape(14.dp)).border(1.dp, color.copy(0.55f), RoundedCornerShape(14.dp)), Alignment.Center) { Icon(icon, null, Modifier.size((size / 2).dp), color) }

@Composable
fun ModsScreen(state: LauncherState) = Page("Mods", "Browse, install and toggle mods for this instance", {
    var q by remember { mutableStateOf("") }; SearchField(q, { q = it }, "Search mods", Modifier.width(300.dp)); GlassButton("Open mods folder", {}, icon = Icons.Rounded.Folder)
}) {
    var chip by remember { mutableStateOf(0) }
    Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) { listOf("All", "Installed", "Performance", "Visual", "Utility", "Fun").forEachIndexed { i, t -> FilterChip(t, chip == i, { chip = i }) } }
    LazyVerticalGrid(GridCells.Adaptive(270.dp), horizontalArrangement = Arrangement.spacedBy(14.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        items((0 until 8).toList()) { i ->
            var on by remember { mutableStateOf(i % 3 != 1) }
            GlassPanel(Modifier.fillMaxWidth().height(218.dp).clickable(remember { MutableInteractionSource() }, null) { state.selectedMod = i }, RoundedCornerShape(20.dp), elevation = 8.dp) {   // click opens ModDetailModal
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Row(horizontalArrangement = Arrangement.spacedBy(14.dp), verticalAlignment = Alignment.CenterVertically) {
                        IconTile(listOf(Icons.Rounded.Extension, Icons.Rounded.Bolt, Icons.Rounded.Place, Icons.Rounded.Dashboard)[i % 4], accents[i % 4])
                        Column { Text(ExampleMods[i].name, style = T.Subtitle); Text("by ${ExampleMods[i].author}", style = T.Body) }
                    }
                    Text("A short example description of what this mod does inside the game.", style = T.Body)
                    StatusLabel(if (i == 0) "New" else "Utility", if (i == 0) C.Blue else C.Text2)
                    Spacer(Modifier.weight(1f))
                    Row(verticalAlignment = Alignment.CenterVertically) { Text(if (on) "Enabled" else "Disabled", style = T.Label.copy(color = if (on) C.Text else C.Text3), modifier = Modifier.weight(1f)); CaramelToggle(on, { on = it }) }
                }
            }
        }
    }
}

@Composable
fun ServersScreen() = Page("Servers", "Featured and saved servers") {
    GlassPanel(Modifier.fillMaxWidth().height(180.dp), RoundedCornerShape(24.dp)) {
        Box(Modifier.matchParentSize().background(Brush.horizontalGradient(listOf(C.Blue.copy(0.28f), C.Caramel.copy(0.16f)))))
        Row(Modifier.fillMaxSize().padding(36.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                Text("Featured: Example Network", style = T.Display.copy(fontSize = 26.sp_)); Text("Minigames, survival and community events", style = T.Body.copy(fontSize = 13.sp_))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) { StatusLabel("12,408 playing", C.Green); VersionRangeLabel("1.21.132", "26.62") }
            }
            PrimaryButton("Join server", {}, Modifier.width(176.dp), icon = Icons.Rounded.PlayArrow)
        }
    }
    ExampleServers.forEachIndexed { i, s ->
        GlassPanel(Modifier.fillMaxWidth().height(80.dp), RoundedCornerShape(20.dp), elevation = 6.dp) {
            Row(Modifier.fillMaxSize().padding(horizontal = 22.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(18.dp)) {
                ServerIcon(accents[i % 4], 52)   // SERVER ICON
                Column(Modifier.weight(1f)) { Text(s.name, style = T.Subtitle.copy(fontSize = 15.sp_)); Text(s.address, style = T.Body) }
                Text("${s.online} online", style = T.Label); Icon(Icons.Rounded.Wifi, null, Modifier.size(18.dp), C.Green); Text("${s.ping} ms", style = T.Body)
                VersionRangeLabel(s.minVersion, s.maxVersion)   // supported Bedrock versions (not Release/Beta)
                GlassButton("Join", {}, icon = Icons.Rounded.PlayArrow, height = 36)
            }
        }
    }
}

@Composable
fun CosmeticsScreen() = Page("Cosmetics", "Capes, wings, hats and more") {
    Row(Modifier.fillMaxSize(), horizontalArrangement = Arrangement.spacedBy(20.dp)) {
        GlassPanel(Modifier.width(320.dp).fillMaxHeight(), RoundedCornerShape(24.dp)) {
            Column(Modifier.fillMaxSize().padding(28.dp), horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(12.dp)) {
                // 3D SKIN VIEWER slot: render the 3D skin inside this white rounded square.
                Box(Modifier.fillMaxWidth().weight(1f).background(Color.White, RoundedCornerShape(22.dp)), Alignment.Center) {
                    Text("Where the skin of the 3d skin goes", style = T.Title.copy(color = Color(0xFF1C2854), fontSize = 15.sp_, textAlign = androidx.compose.ui.text.style.TextAlign.Center), modifier = Modifier.width(190.dp))
                }
                GlassButton("Save outfit", {}, Modifier.fillMaxWidth(), icon = Icons.Rounded.Check); GlassButton("Reset view", {}, Modifier.fillMaxWidth(), icon = Icons.Rounded.SwapHoriz)
            }
        }
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(16.dp)) {
            var chip by remember { mutableStateOf(0) }
            val favorites = remember { mutableStateListOf(1, 5) }
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                listOf("All", "Capes", "Wings", "Hats", "Pets").forEachIndexed { i, t -> FilterChip(t, chip == i, { chip = i }) }
                FilterChip("★ Favorites", chip == 5, { chip = 5 })
            }
            LazyVerticalGrid(GridCells.Adaptive(190.dp), horizontalArrangement = Arrangement.spacedBy(12.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                items((0 until 12).toList()) { i ->
                    val fav = i in favorites
                    GlassPanel(Modifier.fillMaxWidth().height(188.dp), RoundedCornerShape(18.dp), elevation = 6.dp) {
                        Column(Modifier.padding(8.dp)) {
                            Box(Modifier.fillMaxWidth().height(112.dp).background(Brush.verticalGradient(listOf(accents[i % 4].copy(0.32f), accents[i % 4].copy(0.05f))), RoundedCornerShape(12.dp)), Alignment.Center) {
                                Box(Modifier.size(40.dp, 68.dp).background(accents[i % 4], RoundedCornerShape(4.dp)))
                                // Favorite (star) button
                                Box(Modifier.align(Alignment.TopEnd).padding(8.dp).size(28.dp).clip(androidx.compose.foundation.shape.CircleShape).background(Color(0x96081024)).border(1.dp, if (fav) C.Caramel else Color.White.copy(0.25f), androidx.compose.foundation.shape.CircleShape)
                                    .clickable(remember { MutableInteractionSource() }, null) { if (fav) favorites.remove(i) else favorites.add(i) }, Alignment.Center) {
                                    Icon(if (fav) Icons.Rounded.Star else Icons.Rounded.StarBorder, null, Modifier.size(16.dp), if (fav) C.Caramel else C.Text)
                                }
                            }
                            Column(Modifier.padding(8.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                                Text("Example ${listOf("Cape", "Wings", "Hat")[i % 3]}", style = T.Label)
                                when { i == 1 -> StatusLabel("Equipped", C.Green); i % 4 == 3 -> StatusLabel("Caramel+", C.Caramel); else -> Text("Owned", style = T.Body) }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun NewsScreen() = Page("News", "Updates, events and community posts") {
    Row(Modifier.fillMaxWidth().weight(1f), horizontalArrangement = Arrangement.spacedBy(20.dp)) {
        GlassPanel(Modifier.weight(1.3f).fillMaxHeight(), RoundedCornerShape(24.dp)) {
            Column(Modifier.padding(6.dp)) {
                Box(Modifier.fillMaxWidth().height(260.dp).background(Brush.verticalGradient(listOf(Color(0xFF5A2818), Color(0xFFF5963C))), RoundedCornerShape(18.dp)))
                Column(Modifier.padding(22.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) { StatusLabel("Featured", C.Caramel); Text("Caramel Client 26.2 is here", style = T.Display); Text("New launcher, faster startup and the redesigned mod menu.", style = T.Body.copy(fontSize = 13.sp_)); Text("Read more", style = T.Label.copy(color = C.Caramel)) }
            }
        }
        Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            listOf("Example patch notes", "Community spotlight", "Server of the week").forEachIndexed { i, t ->
                GlassPanel(Modifier.fillMaxWidth().height(130.dp), RoundedCornerShape(20.dp), elevation = 6.dp) {
                    Row(Modifier.padding(12.dp), horizontalArrangement = Arrangement.spacedBy(14.dp)) {
                        Box(Modifier.size(150.dp, 106.dp).background(Brush.verticalGradient(listOf(accents[i].copy(0.5f), accents[i].copy(0.1f))), RoundedCornerShape(12.dp)))
                        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) { Text(t, style = T.Subtitle.copy(fontSize = 15.sp_)); Text("A short example summary of this post that wraps onto two lines at most.", style = T.Body); Text("${i + 1} day${if (i > 0) "s" else ""} ago", style = T.Caption) }
                    }
                }
            }
        }
    }
}

@Composable
fun StoreScreen() = Page("Store", "Cosmetics, bundles and Caramel+") {
    GlassPanel(Modifier.fillMaxWidth().height(160.dp), RoundedCornerShape(24.dp)) {
        Box(Modifier.matchParentSize().background(Brush.horizontalGradient(listOf(C.Caramel.copy(0.3f), C.Blue.copy(0.08f)))))
        Row(Modifier.fillMaxSize().padding(horizontal = 36.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(6.dp)) { Text("Caramel+", style = T.Display.copy(fontSize = 28.sp_)); Text("Get access to HoneyLoader, The preloader that Honeyclient uses but for Glowberryclient!", style = T.Body.copy(fontSize = 13.5.sp_)) }
            PrimaryButton("Get Caramel+ · $4.99/mo", {}, Modifier.width(240.dp), Tone.Caramel)
        }
    }
    LazyVerticalGrid(GridCells.Adaptive(270.dp), horizontalArrangement = Arrangement.spacedBy(14.dp), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        items((0 until 8).toList()) { i ->
            GlassPanel(Modifier.fillMaxWidth().height(218.dp), RoundedCornerShape(20.dp), elevation = 8.dp) {
                Column(Modifier.padding(8.dp)) {
                    Box(Modifier.fillMaxWidth().height(112.dp).background(Brush.verticalGradient(listOf(accents[i % 4].copy(0.36f), accents[i % 4].copy(0.05f))), RoundedCornerShape(14.dp)), Alignment.Center) { Box(Modifier.size(56.dp, 70.dp).background(accents[i % 4], RoundedCornerShape(6.dp))) }
                    Column(Modifier.padding(10.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                        Text("Example bundle ${i + 1}", style = T.Subtitle); Text("3 items included", style = T.Body)
                        Row(verticalAlignment = Alignment.CenterVertically) { Text("$${4 + i}.99", style = T.Title.copy(color = C.Caramel, fontSize = 15.sp_), modifier = Modifier.weight(1f)); GlassButton("Add to cart", {}, height = 30) }
                    }
                }
            }
        }
    }
}
