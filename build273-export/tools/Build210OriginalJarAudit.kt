import com.diamondrush.legacy.LegacySpriteFieldLayoutParser
import java.util.zip.ZipFile
import java.nio.file.Paths

private fun u32le(b: ByteArray, p: Int): Long =
    (b[p].toLong() and 255) or ((b[p+1].toLong() and 255) shl 8) or
    ((b[p+2].toLong() and 255) shl 16) or ((b[p+3].toLong() and 255) shl 24)

fun main(args: Array<String>) {
    require(args.size == 1) { "usage: Build210OriginalJarAudit <original.jar>" }
    var resources = 0
    var sprites = 0
    var groups = 0
    var components = 0
    var pixelBytes = 0
    ZipFile(Paths.get(args[0]).toFile()).use { zip ->
        val entries = zip.entries()
        while (entries.hasMoreElements()) {
            val entry = entries.nextElement()
            if (!entry.name.endsWith(".f")) continue
            val container = zip.getInputStream(entry).use { it.readBytes() }
            val count = container[0].toInt() and 255
            val directoryBase = 1 + count * 8
            repeat(count) { index ->
                val directory = 1 + index * 8
                val offset = u32le(container, directory)
                val length = u32le(container, directory + 4)
                val start = directoryBase.toLong() + offset
                require(start + length <= container.size.toLong()) { "Invalid ${entry.name}[$index] range" }
                val payload = container.copyOfRange(start.toInt(), (start + length).toInt())
                if (payload.size >= 4 && payload[0] == 0xDF.toByte() && payload[1] == 3.toByte() &&
                    payload[2] == 1.toByte() && payload[3] == 1.toByte()) {
                    val parsed = LegacySpriteFieldLayoutParser.parse(payload)
                    resources++
                    sprites += parsed.spriteCount
                    groups += parsed.groupCount
                    components += parsed.hComponents.size / 4
                    pixelBytes += parsed.concatenatedPixelBytes.size
                }
            }
        }
    }
    println("resources=$resources sprites=$sprites groups=$groups components=$components pixelBytes=$pixelBytes")
    check(resources == 94)
    check(sprites == 1372)
    check(groups == 1129)
    check(components == 10149)
}
