package dev.caramel.ui.components

import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.onFocusChanged

fun Modifier.onFocusChangedCompat(block: (Boolean) -> Unit): Modifier = onFocusChanged { block(it.isFocused) }
