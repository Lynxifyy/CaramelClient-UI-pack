package dev.caramel.ui.data

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.compose.ui.graphics.Color
import dev.caramel.ui.theme.C

enum class Channel(val label: String, val color: Color) { Release("Release", C.Green), Beta("Beta", C.Orange) }
data class GameVersion(val id: String, val channel: Channel)
enum class Loader(val title: String) { Bedrock("Minecraft Bedrock"), Rust("Rust"), Lightning("Lightning") }
enum class ProfileMode(val title: String, val desc: String, val label: String, val locked: Boolean) {
    Open("Open Instance Profile", "Shares worlds and settings", "Unlocked", false),
    Isolated("Isolated Instance Profile", "Separate files and mods", "Locked", true),
}

/** Example list, newest to oldest. Swap for your real Bedrock manifest (26.62 down to 1.21.132). */
object Versions {
    val all: List<GameVersion> = buildList {
        add(GameVersion("26.62", Channel.Beta)); add(GameVersion("26.61", Channel.Beta))
        listOf("26.60", "26.50", "26.40", "26.30", "26.20", "26.10", "26.0").forEach { add(GameVersion(it, Channel.Release)) }
        add(GameVersion("1.21.140", Channel.Release)); add(GameVersion("1.21.139", Channel.Beta))
        for (n in 138 downTo 132) add(GameVersion("1.21.$n", if (n % 3 == 0) Channel.Beta else Channel.Release))
    }
}

class LauncherState {
    var tab by mutableStateOf(Tab.Home)
    var version by mutableStateOf(Versions.all.first { it.id == "26.60" })
    var loader by mutableStateOf(Loader.Bedrock)
    var profile by mutableStateOf(ProfileMode.Isolated)
    var launchMenu by mutableStateOf(false)
    var instanceSettings by mutableStateOf(false)
    var accountMenu by mutableStateOf(false)
    var addFriend by mutableStateOf(false)
    var launcherSettings by mutableStateOf(false)
    var appMenu by mutableStateOf(false)            // dropdown by the "Caramel Client" title
    var screenshots by mutableStateOf(false)
    var friendsAll by mutableStateOf(false)         // Friends > View all
    var addAccount by mutableStateOf(false)
    var accountSettings by mutableStateOf(false)
    var selectedMod by mutableStateOf<Int?>(null)   // index into ExampleMods, opens the mod detail modal
    var runningInstances by mutableStateOf(0)       // INSTANCES COUNT shown top right
}

enum class Tab { Home, Mods, Servers, Cosmetics, News, Store }

data class ModInfo(val name: String, val author: String, val version: String, val description: String, val size: String)
val ExampleMods = (0 until 8).map { ModInfo("Example mod ${'A' + it}", "Caramel Team", "1.0.$it", "A short example description of what this mod does inside the game. It can run to a few lines so people know what they are installing before they enable it.", "1.2 MB") }

/** Servers show the Bedrock versions they support, from [min] to [max] (1.21.132 up to 26.62). */
data class ServerInfo(val name: String, val address: String, val online: Int, val ping: Int, val minVersion: String, val maxVersion: String)
val ExampleServers = listOf(
    ServerInfo("Example Server 1", "play.example1.net", 1204, 24, "1.21.132", "26.62"),
    ServerInfo("Example Server 2", "play.example2.net", 993, 37, "26.0", "26.62"),
    ServerInfo("Example Server 3", "play.example3.net", 782, 50, "1.21.140", "26.20"),
    ServerInfo("Example Server 4", "play.example4.net", 571, 63, "1.21.132", "26.40"),
)
