package dev.caramel.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import dev.caramel.ui.data.Loader
import dev.caramel.ui.theme.C
import dev.caramel.ui.theme.T
import kotlin.math.PI
import kotlin.math.cos
import kotlin.math.sin
import kotlin.random.Random

/** The three loader icons: Minecraft Bedrock block, Rust cog, yellow lightning bolt. */
@Composable
fun LoaderGlyph(loader: Loader, modifier: Modifier = Modifier.size(28.dp)) {
    when (loader) {
        Loader.Bedrock -> Canvas(modifier) {
            val n = 12; val px = size.width / n; val rnd = Random(7)
            for (i in 0 until n) for (j in 0 until n) {
                val v = if (rnd.nextFloat() > .15f) listOf(52, 64, 78, 92, 108, 124).random(rnd) else listOf(28, 34).random(rnd)
                drawRect(Color(v, v, v + 6), Offset(i * px, j * px), Size(px + .5f, px + .5f))
            }
            drawRoundRect(Color(0xFF14141A), Offset.Zero, size, CornerRadius(2.dp.toPx()), Stroke(1.5.dp.toPx()))
        }
        Loader.Rust -> Box(modifier, Alignment.Center) {
            Canvas(Modifier.matchParentSizeCompat()) {
                val c = Offset(size.width / 2, size.height / 2); val r = size.width * .36f; val rust = Color(0xFFDEA584)
                for (i in 0 until 12) { val a = i * PI / 6; drawCircle(rust, size.width * .085f, Offset(c.x + (r + size.width * .1f) * cos(a).toFloat(), c.y + (r + size.width * .1f) * sin(a).toFloat())) }
                drawCircle(rust, r + size.width * .04f, c); drawCircle(Color(0xFF221612), r * .72f, c)
            }
            Text("R", style = T.Title.copy(color = Color(0xFFDEA584), fontSize = 12.sp_))
        }
        Loader.Lightning -> Canvas(modifier) {
            val w = size.width; val h = size.height
            val p = Path().apply { moveTo(.56f * w, .06f * h); lineTo(.19f * w, .56f * h); lineTo(.46f * w, .56f * h); lineTo(.40f * w, .94f * h); lineTo(.81f * w, .40f * h); lineTo(.54f * w, .40f * h); close() }
            drawPath(p, C.Yellow)
        }
    }
}

@Composable
fun LoaderTile(loader: Loader, selected: Boolean, onClick: () -> Unit, modifier: Modifier = Modifier) {
    val shape = RoundedCornerShape(11.dp)
    Box(modifier.size(44.dp)) {
        Box(
            Modifier.size(44.dp).background(Color.White.copy(if (selected) 0.12f else 0.07f), shape)
                .border(if (selected) 1.6.dp else 1.dp, if (selected) C.Green else Color.White.copy(0.14f), shape)
                .clickable(remember { MutableInteractionSource() }, null, onClick = onClick),
            Alignment.Center,
        ) { LoaderGlyph(loader, Modifier.size(28.dp)) }
        if (selected) Box(Modifier.offset((-5).dp, (-5).dp).size(14.dp).background(C.Green, CircleShape).border(1.5.dp, C.Navy, CircleShape), Alignment.Center) { Icon(Icons.Rounded.Check, null, Modifier.size(9.dp), C.OnGreen) }
    }
}

private fun Modifier.matchParentSizeCompat() = this.then(Modifier.size(28.dp))
private val Int.sp_ get() = androidx.compose.ui.unit.TextUnit(this.toFloat(), androidx.compose.ui.unit.TextUnitType.Sp)
