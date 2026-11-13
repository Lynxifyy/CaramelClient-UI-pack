package dev.caramel.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.KeyboardArrowDown
import androidx.compose.material.icons.rounded.KeyboardArrowUp
import androidx.compose.material.icons.rounded.Folder
import androidx.compose.material.icons.rounded.SwapHoriz
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.DpOffset
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.window.Popup
import androidx.compose.ui.window.PopupProperties
import dev.caramel.ui.data.GameVersion
import dev.caramel.ui.data.ProfileMode
import dev.caramel.ui.data.Versions
import dev.caramel.ui.theme.C
import dev.caramel.ui.theme.T

/** Closed dropdown trigger + generic glass popup. */
@Composable
fun CaramelDropdown(value: String, modifier: Modifier = Modifier, width: Int = 180, panelWidth: Int = width, panel: @Composable (close: () -> Unit) -> Unit) {
    var open by remember { mutableStateOf(false) }
    Box(modifier) {
        DropdownField(value, open, Modifier.width(width.dp)) { open = !open }
        if (open) Popup(alignment = Alignment.TopStart, offset = IntOffset(0, 46), onDismissRequest = { open = false }, properties = PopupProperties(focusable = true)) {
            GlassPanel(Modifier.width(panelWidth.dp), RoundedCornerShape(16.dp), popup = true, elevation = 32.dp) { panel { open = false } }
        }
    }
}

@Composable
fun DropdownField(text: String, open: Boolean, modifier: Modifier = Modifier, onClick: () -> Unit) {
    val shape = RoundedCornerShape(11.dp)
    Row(
        modifier.height(38.dp).clip(shape).background(Color.White.copy(if (open) 0.13f else 0.08f))
            .border(1.dp, if (open) C.Blue.copy(0.7f) else Color.White.copy(0.18f), shape)
            .clickable(remember { MutableInteractionSource() }, null, onClick = onClick).padding(horizontal = 14.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(text, style = T.Label.copy(fontWeight = androidx.compose.ui.text.font.FontWeight.Medium), modifier = Modifier.weight(1f))
        Icon(if (open) Icons.Rounded.KeyboardArrowUp else Icons.Rounded.KeyboardArrowDown, null, Modifier.size(18.dp), C.Text2)
    }
}

@Composable
fun SimpleDropdown(value: String, options: List<String>, onSelect: (String) -> Unit, modifier: Modifier = Modifier, width: Int = 190) =
    CaramelDropdown(value, modifier, width) { close ->
        Column(Modifier.padding(8.dp)) {
            options.forEach { o ->
                Box(Modifier.fillMaxWidth().height(34.dp).clip(RoundedCornerShape(9.dp)).background(if (o == value) C.Blue.copy(0.24f) else Color.Transparent).clickable { onSelect(o); close() }.padding(horizontal = 12.dp), Alignment.CenterStart) { Text(o, style = T.Label) }
            }
        }
    }

/** Version picker: search box on top, scrolling list with Release (green) / Beta (orange) labels. */
@Composable
fun VersionDropdown(selected: GameVersion, onSelect: (GameVersion) -> Unit, modifier: Modifier = Modifier) =
    CaramelDropdown(selected.id, modifier, width = 124, panelWidth = 300) { close ->
        var q by remember { mutableStateOf("") }
        val list = remember(q) { Versions.all.filter { it.id.contains(q.trim()) } }
        Column(Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
            SearchField(q, { q = it }, "Search versions", Modifier.fillMaxWidth())
            LazyColumn(Modifier.heightIn(max = 252.dp)) {
                items(list, key = { it.id }) { v ->
                    Row(
                        Modifier.fillMaxWidth().height(36.dp).clip(RoundedCornerShape(9.dp)).background(if (v == selected) C.Blue.copy(0.26f) else Color.Transparent)
                            .clickable { onSelect(v); close() }.padding(horizontal = 12.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) { Text(v.id, style = T.Label, modifier = Modifier.weight(1f)); ChannelLabel(v.channel) }
                }
                if (list.isEmpty()) item { Text("No versions match", style = T.Body, modifier = Modifier.padding(12.dp)) }
            }
        }
    }

/** Profile picker: Open (green, unlocked) vs Isolated (red, locked). */
@Composable
fun ProfileDropdown(selected: ProfileMode, onSelect: (ProfileMode) -> Unit, modifier: Modifier = Modifier, width: Int = 328) {
    var open by remember { mutableStateOf(false) }
    Box(modifier) {
        val shape = RoundedCornerShape(11.dp)
        Row(
            Modifier.width(width.dp).height(38.dp).clip(shape).background(Color.White.copy(if (open) 0.13f else 0.08f)).border(1.dp, if (open) C.Blue.copy(0.7f) else Color.White.copy(0.18f), shape)
                .clickable(remember { MutableInteractionSource() }, null) { open = !open }.padding(horizontal = 14.dp),
            verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            Icon(Icons.Rounded.Folder, null, Modifier.size(17.dp), Color(0xFF50BEFF))
            Text(if (selected == ProfileMode.Open) "Open profile" else "Isolated profile", style = T.Label.copy(fontWeight = androidx.compose.ui.text.font.FontWeight.Medium), modifier = Modifier.weight(1f))
            Icon(Icons.Rounded.SwapHoriz, null, Modifier.size(16.dp), C.Text3)
        }
        if (open) Popup(alignment = Alignment.TopStart, offset = IntOffset(0, 46), onDismissRequest = { open = false }, properties = PopupProperties(focusable = true)) {
            GlassPanel(Modifier.width(width.dp), RoundedCornerShape(16.dp), popup = true, elevation = 32.dp) {
                Column(Modifier.padding(8.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                    ProfileMode.entries.forEach { m ->
                        Row(
                            Modifier.fillMaxWidth().clip(RoundedCornerShape(11.dp)).background(if (m == selected) C.Blue.copy(0.22f) else Color.Transparent).clickable { onSelect(m); open = false }.padding(12.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Column(Modifier.weight(1f)) { Text(m.title, style = T.Label); Text(m.desc, style = T.Body) }
                            ProfileLabel(m)
                        }
                    }
                }
            }
        }
    }
}
