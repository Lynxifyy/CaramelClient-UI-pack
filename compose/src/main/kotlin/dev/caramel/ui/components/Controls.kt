package dev.caramel.ui.components

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.spring
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.unit.dp
import dev.caramel.ui.theme.C
import dev.caramel.ui.theme.T

@Composable
fun CaramelToggle(checked: Boolean, onChange: (Boolean) -> Unit, modifier: Modifier = Modifier) {
    val x by animateDpAsState(if (checked) 21.dp else 3.dp, spring(stiffness = 600f))
    val shape = RoundedCornerShape(50)
    Box(
        modifier.size(40.dp, 22.dp).clip(shape)
            .background(if (checked) Brush.horizontalGradient(listOf(C.GreenLight, C.GreenDark)) else SolidColor(Color.White.copy(0.10f)))
            .border(1.dp, if (checked) Color.Transparent else Color.White.copy(0.24f), shape)
            .clickable(remember { MutableInteractionSource() }, null) { onChange(!checked) },
    ) {
        Box(Modifier.offset(x, 3.dp).size(16.dp).shadow(3.dp, CircleShape).background(if (checked) Color.White else Color(0xFFBECAEB), CircleShape))
    }
}

@Composable
fun CaramelCheckbox(checked: Boolean, onChange: (Boolean) -> Unit, modifier: Modifier = Modifier) {
    val shape = RoundedCornerShape(5.dp)
    Box(
        modifier.size(18.dp).clip(shape)
            .background(if (checked) Brush.verticalGradient(listOf(C.BlueLight, C.BlueDark)) else SolidColor(Color.White.copy(0.06f)))
            .border(1.dp, if (checked) Color.Transparent else Color.White.copy(0.28f), shape)
            .clickable(remember { MutableInteractionSource() }, null) { onChange(!checked) },
        Alignment.Center,
    ) { if (checked) Icon(Icons.Rounded.Check, null, Modifier.size(13.dp), Color.White) }
}

@Composable
fun CaramelRadio(selected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Box(modifier.size(18.dp).clip(CircleShape).background(Color.White.copy(0.06f)).border(1.4.dp, if (selected) C.Blue else Color.White.copy(0.28f), CircleShape).clickable(remember { MutableInteractionSource() }, null, onClick = onClick), Alignment.Center) {
        if (selected) Box(Modifier.size(8.dp).background(C.Blue, CircleShape))
    }
}

/** Custom slider: gradient track, white knob with accent core. */
@Composable
fun CaramelSlider(value: Float, onChange: (Float) -> Unit, modifier: Modifier = Modifier, accent: Color = C.Blue, accentEnd: Color = Color(0xFF4ABEFF)) {
    var w by remember { mutableStateOf(1) }
    Canvas(
        modifier.fillMaxWidth().height(22.dp).onSizeChanged { w = it.width.coerceAtLeast(1) }
            .pointerInput(Unit) { detectTapGestures { onChange((it.x / w).coerceIn(0f, 1f)) } }
            .pointerInput(Unit) { detectDragGestures { c, _ -> onChange((c.position.x / w).coerceIn(0f, 1f)) } },
    ) {
        val cy = size.height / 2; val th = 6.dp.toPx(); val kx = size.width * value
        drawRoundRect(Color.White.copy(0.12f), Offset(0f, cy - th / 2), Size(size.width, th), CornerRadius(th))
        drawRoundRect(Brush.horizontalGradient(listOf(accent, accentEnd)), Offset(0f, cy - th / 2), Size(kx, th), CornerRadius(th))
        drawCircle(Color.Black.copy(0.35f), 9.dp.toPx(), Offset(kx, cy + 1.5.dp.toPx()))
        drawCircle(Color.White, 8.dp.toPx(), Offset(kx, cy))
        drawCircle(accent, 3.dp.toPx(), Offset(kx, cy))
    }
}

@Composable
fun CaramelTextField(value: String, onChange: (String) -> Unit, modifier: Modifier = Modifier, placeholder: String = "", leading: ImageVector? = null) {
    var focused by remember { mutableStateOf(false) }
    val border by animateColorAsState(if (focused) C.Blue.copy(0.8f) else Color.White.copy(0.16f))
    val shape = RoundedCornerShape(11.dp)
    BasicTextField(
        value, onChange, Modifier.height(38.dp).then(modifier).clip(shape).background(Color(0x6E040A1A)).border(1.dp, border, shape).onFocusChangedCompat { focused = it },
        singleLine = true, textStyle = T.Label.copy(fontWeight = androidx.compose.ui.text.font.FontWeight.Normal), cursorBrush = SolidColor(C.Blue),
        decorationBox = { inner ->
            Row(Modifier.padding(horizontal = 14.dp).fillMaxHeight(), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                if (leading != null) Icon(leading, null, Modifier.size(16.dp), C.Text3)
                Box(Modifier.weight(1f)) { if (value.isEmpty()) Text(placeholder, style = T.Label.copy(color = C.Text3, fontWeight = androidx.compose.ui.text.font.FontWeight.Normal)); inner() }
            }
        },
    )
}

@Composable
fun SearchField(value: String, onChange: (String) -> Unit, placeholder: String, modifier: Modifier = Modifier) =
    CaramelTextField(value, onChange, modifier, placeholder, Icons.Rounded.Search)

/** Row: title + description on the left, control on the right. */
@Composable
fun SettingRow(title: String, desc: String? = null, modifier: Modifier = Modifier, control: @Composable () -> Unit) {
    Row(modifier.fillMaxWidth(), verticalAlignment = Alignment.CenterVertically) {
        Column(Modifier.weight(1f)) { Text(title, style = T.Label); if (desc != null) Text(desc, style = T.Body) }
        control()
    }
}

@Composable
fun SliderRow(title: String, valueText: String, value: Float, onChange: (Float) -> Unit, accent: Color = C.Blue, accentEnd: Color = Color(0xFF4ABEFF)) {
    Column(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        Row { Text(title, style = T.Label, modifier = Modifier.weight(1f)); Text(valueText, style = T.Label.copy(color = accent)) }
        CaramelSlider(value, onChange, accent = accent, accentEnd = accentEnd)
    }
}
