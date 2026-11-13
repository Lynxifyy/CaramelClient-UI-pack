package dev.caramel.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Lock
import androidx.compose.material.icons.rounded.LockOpen
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import dev.caramel.ui.data.Channel
import dev.caramel.ui.data.ProfileMode
import dev.caramel.ui.theme.C
import dev.caramel.ui.theme.T

/** Tinted status pill. Release = green, Beta = orange, Locked = red, Unlocked = green. */
@Composable
fun StatusLabel(text: String, color: Color, modifier: Modifier = Modifier, icon: ImageVector? = null) {
    val shape = RoundedCornerShape(50)
    Row(modifier.height(20.dp).clip(shape).background(color.copy(0.16f)).border(1.dp, color.copy(0.5f), shape).padding(horizontal = 9.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
        if (icon != null) Icon(icon, null, Modifier.size(11.dp), color)
        Text(text, style = T.Chip.copy(color = color))
    }
}

@Composable fun ChannelLabel(channel: Channel, modifier: Modifier = Modifier) = StatusLabel(channel.label, channel.color, modifier)
@Composable fun ProfileLabel(mode: ProfileMode, modifier: Modifier = Modifier) =
    StatusLabel(mode.label, if (mode.locked) C.Red else C.Green, modifier, if (mode.locked) Icons.Rounded.Lock else Icons.Rounded.LockOpen)

@Composable
fun FilterChip(text: String, selected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val shape = RoundedCornerShape(50)
    Box(
        modifier.height(26.dp).clip(shape)
            .background(if (selected) Brush.verticalGradient(listOf(C.BlueLight, C.BlueDark)) else SolidColor(Color.White.copy(0.07f)))
            .border(1.dp, if (selected) Color.Transparent else Color.White.copy(0.16f), shape)
            .clickable(remember { MutableInteractionSource() }, null, onClick = onClick).padding(horizontal = 13.dp),
        Alignment.Center,
    ) { Text(text, style = T.Chip.copy(fontSize = 11.5.sp_, color = if (selected) Color.White else C.Text2)) }
}

@Composable
fun SegmentedTabs(items: List<String>, selected: Int, onSelect: (Int) -> Unit, modifier: Modifier = Modifier) {
    val shape = RoundedCornerShape(50)
    Row(modifier.height(36.dp).clip(shape).background(Color.White.copy(0.06f)).border(1.dp, Color.White.copy(0.14f), shape).padding(3.dp)) {
        items.forEachIndexed { i, t ->
            Box(
                Modifier.width(96.dp).fillMaxHeight().clip(shape)
                    .background(if (i == selected) Brush.verticalGradient(listOf(C.BlueLight, C.BlueDark)) else SolidColor(Color.Transparent))
                    .clickable(remember { MutableInteractionSource() }, null) { onSelect(i) },
                Alignment.Center,
            ) { Text(t.uppercase(), style = T.Chip.copy(letterSpacing = 1.sp_, color = if (i == selected) Color.White else C.Text2)) }
        }
    }
}

/** Placeholder slot. The Microsoft account profile picture goes here (no icon yet). */
@Composable
fun Avatar(size: Int = 36, online: Boolean = false) {
    Box(Modifier.size(size.dp).background(Color.White.copy(0.09f), CircleShape).border(if (online) 2.dp else 1.dp, if (online) C.Green else Color.White.copy(0.3f), CircleShape))
}

/** SERVER ICON slot. Used by Quick play (title bar) and the Servers tab; replace the inner square with the server's icon image. */
@Composable
fun ServerIcon(color: Color, size: Int = 26) {
    val shape = RoundedCornerShape((size * 0.3f).dp)
    Box(Modifier.size(size.dp).clip(shape).background(color.copy(0.22f)).border(1.dp, color.copy(0.6f), shape), Alignment.Center) { Box(Modifier.size((size * 0.4f).dp).background(color, RoundedCornerShape(2.dp))) }
}

/** Supported-versions label for servers, e.g. "1.21.132 – 26.62". */
@Composable
fun VersionRangeLabel(min: String, max: String, modifier: Modifier = Modifier) = StatusLabel("$min – $max", Color(0xFF78A0FF), modifier)

// local sp helpers so this file stays import-light
private val Int.sp_ get() = androidx.compose.ui.unit.TextUnit(this.toFloat(), androidx.compose.ui.unit.TextUnitType.Sp)
private val Double.sp_ get() = androidx.compose.ui.unit.TextUnit(this.toFloat(), androidx.compose.ui.unit.TextUnitType.Sp)
