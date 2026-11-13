package dev.caramel.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsHoveredAsState
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.unit.dp
import androidx.compose.foundation.hoverable
import dev.caramel.ui.theme.C
import dev.caramel.ui.theme.T

enum class Tone(val top: Color, val bottom: Color, val on: Color) {
    Green(C.GreenLight, C.GreenDark, C.OnGreen),
    Caramel(Color(0xFFFFBE5A), C.CaramelDark, Color.White),
    Blue(C.BlueLight, C.BlueDark, Color.White),
    Red(Color(0xFFFF6C7E), Color(0xFFD6344E), Color.White),
}

@Composable
fun PrimaryButton(text: String, onClick: () -> Unit, modifier: Modifier = Modifier, tone: Tone = Tone.Green, icon: ImageVector? = null, height: Int = 44) {
    val src = remember { MutableInteractionSource() }
    val hover by src.collectIsHoveredAsState()
    val shape = RoundedCornerShape((height / 2.6).dp)
    Box(
        modifier.height(height.dp)
            .shadow(if (hover) 16.dp else 10.dp, shape, ambientColor = tone.bottom, spotColor = tone.bottom)
            .clip(shape)
            .background(Brush.verticalGradient(listOf(tone.top, tone.bottom)))
            .background(Brush.verticalGradient(listOf(Color.White.copy(if (hover) 0.28f else 0.20f), Color.Transparent, Color.Transparent)))
            .border(1.dp, Color.White.copy(0.28f), shape)
            .hoverable(src).clickable(src, null, onClick = onClick),
        Alignment.Center,
    ) {
        Row(Modifier.padding(horizontal = 16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            if (icon != null) Icon(icon, null, Modifier.size(18.dp), tone.on)
            Text(text, style = T.Button.copy(color = tone.on))
        }
    }
}

@Composable
fun GlassButton(text: String?, onClick: () -> Unit, modifier: Modifier = Modifier, icon: ImageVector? = null, danger: Boolean = false, active: Boolean = false, height: Int = 40) {
    val src = remember { MutableInteractionSource() }
    val hover by src.collectIsHoveredAsState()
    val tint = when { danger -> C.Red; active -> C.Blue; else -> Color.White }
    val shape = RoundedCornerShape(12.dp)
    val fg = if (danger) C.Red else C.Text
    Box(
        modifier.height(height.dp).then(if (text == null) Modifier.width(height.dp) else Modifier)
            .clip(shape)
            .background(tint.copy(if (danger || active) 0.16f else if (hover) 0.14f else 0.08f))
            .border(1.dp, tint.copy(if (danger || active) 0.45f else if (hover) 0.28f else 0.17f), shape)
            .hoverable(src).clickable(src, null, onClick = onClick),
        Alignment.Center,
    ) {
        Row(Modifier.padding(horizontal = if (text == null) 0.dp else 16.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            if (icon != null) Icon(icon, null, Modifier.size(17.dp), fg)
            if (text != null) Text(text, style = T.Label.copy(color = fg))
        }
    }
}
