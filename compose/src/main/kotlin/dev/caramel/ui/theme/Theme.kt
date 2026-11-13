package dev.caramel.ui.theme

import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp
import dev.chrisbanes.haze.HazeState

/** Design tokens for Caramel Client. Mirrors previews/widget_packs/07_design_tokens.png */
object C {
    val Abyss = Color(0xFF060B1A)
    val Navy = Color(0xFF0A1330)
    val DeepBlue = Color(0xFF0F1B44)
    val Blue = Color(0xFF4A78FF)
    val BlueLight = Color(0xFF628CFF)
    val BlueDark = Color(0xFF3458E6)
    val Caramel = Color(0xFFF5A742)
    val CaramelDark = Color(0xFFDE8624)
    val Green = Color(0xFF2FD36B)
    val GreenLight = Color(0xFF3EE27A)
    val GreenDark = Color(0xFF18A050)
    val Red = Color(0xFFFF5468)
    val Orange = Color(0xFFFF9F2E)
    val Yellow = Color(0xFFFFD040)
    val Text = Color(0xFFEAF0FF)
    val Text2 = Color(0xFF9AA8D0)
    val Text3 = Color(0xFF66749E)
    val OnGreen = Color(0xFF062412)
    val Hairline = Color.White.copy(alpha = 0.14f)
    val Fill = Color.White.copy(alpha = 0.07f)
    val FillStrong = Color.White.copy(alpha = 0.12f)
}

private val Inter = FontFamily(
    Font(resource = "fonts/Inter-Regular.otf", weight = FontWeight.Normal),
    Font(resource = "fonts/Inter-Medium.otf", weight = FontWeight.Medium),
    Font(resource = "fonts/Inter-SemiBold.otf", weight = FontWeight.SemiBold),
    Font(resource = "fonts/Inter-Bold.otf", weight = FontWeight.Bold),
)
private val Poppins = FontFamily(
    Font(resource = "fonts/Poppins-Regular.ttf", weight = FontWeight.Normal),
    Font(resource = "fonts/Poppins-Medium.ttf", weight = FontWeight.Medium),
    Font(resource = "fonts/Poppins-Bold.ttf", weight = FontWeight.Bold),
)

/** Poppins for display/titles, Inter for controls and body. */
object T {
    val Display = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.Bold, fontSize = 24.sp, color = C.Text)
    val Title = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.Medium, fontSize = 16.sp, color = C.Text)
    val Subtitle = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.Medium, fontSize = 14.sp, color = C.Text)
    val Button = TextStyle(fontFamily = Poppins, fontWeight = FontWeight.Medium, fontSize = 14.sp, color = C.Text)
    val Label = TextStyle(fontFamily = Inter, fontWeight = FontWeight.SemiBold, fontSize = 13.sp, color = C.Text)
    val Body = TextStyle(fontFamily = Inter, fontWeight = FontWeight.Normal, fontSize = 12.sp, color = C.Text2)
    val Caption = TextStyle(fontFamily = Inter, fontWeight = FontWeight.Normal, fontSize = 11.sp, color = C.Text3)
    val Chip = TextStyle(fontFamily = Inter, fontWeight = FontWeight.SemiBold, fontSize = 10.5.sp)
}

/** Backdrop blur source (wallpaper only) and whole-window blur source (for popups and modals). */
val LocalHaze = staticCompositionLocalOf<HazeState> { error("No HazeState provided") }
val LocalWindowHaze = staticCompositionLocalOf<HazeState> { error("No window HazeState provided") }
