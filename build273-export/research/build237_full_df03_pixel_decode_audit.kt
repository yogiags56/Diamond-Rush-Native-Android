import com.diamondrush.legacy.LegacySpriteDecoder
import com.diamondrush.legacy.LegacySpriteResourceBundleParser
import java.io.File
import java.util.zip.ZipFile

/** Full Kotlin parser+pixel decoder audit across every DF03 entry in the original JAR. */
fun main(args: Array<String>) {
    require(args.size == 2) { "Usage: <original.jar> <output.csv>" }
    val output = File(args[1])
    val rows = mutableListOf(
        "bundle,entry,sprite_count,palette_index,pixel_format,palette_format,pixel_count,transparent_sprites"
    )
    var bundleCount = 0
    var resourceCount = 0
    var spriteCount = 0
    var paletteVariants = 0
    var decodedVariants = 0
    var pixelCountTotal = 0L

    ZipFile(File(args[0])).use { zip ->
        val names = zip.entries().asSequence().map { it.name }
            .filter { it.endsWith(".f") }.sorted().toList()
        bundleCount = names.size
        for (name in names) {
            val bytes = zip.getInputStream(zip.getEntry(name)).use { it.readBytes() }
            for (entry in LegacySpriteResourceBundleParser.readBundleEntries(bytes)) {
                if (entry.payload.size < 4 || entry.payload[0] != 0xDF.toByte() ||
                    entry.payload[1] != 3.toByte() || entry.payload[2] != 1.toByte() ||
                    entry.payload[3] != 1.toByte()) continue
                val parsed = LegacySpriteResourceBundleParser.parse(entry.payload)
                resourceCount++
                spriteCount += parsed.sprites.size
                val paletteFormat = requireNotNull(parsed.paletteFormat)
                val pixelFormat = requireNotNull(parsed.pixelFormat)
                for (paletteIndex in parsed.palettes.indices) {
                    val palette = LegacySpriteDecoder.decodePalette(parsed.palettes[paletteIndex], paletteFormat)
                    var resourcePixels = 0L
                    var transparentSprites = 0
                    for (sprite in parsed.sprites) {
                        require(sprite.width > 0 && sprite.height > 0) {
                            "Invalid dimensions in $name entry ${entry.index} sprite ${sprite.index}"
                        }
                        val indices = LegacySpriteDecoder.decodeIndices(
                            sprite.encodedPixels, sprite.width, sprite.height, pixelFormat
                        )
                        val pixels = IntArray(indices.size) { pixel ->
                            val index = indices[pixel]
                            require(index in palette.indices) {
                                "Palette index $index out of range in $name entry ${entry.index} " +
                                    "sprite ${sprite.index}, palette $paletteIndex"
                            }
                            palette[index]
                        }
                        if (pixels.any { (it ushr 24) != 0xff }) transparentSprites++
                        resourcePixels += pixels.size
                    }
                    paletteVariants++
                    decodedVariants += parsed.sprites.size
                    pixelCountTotal += resourcePixels
                    rows += listOf(
                        name, entry.index, parsed.sprites.size, paletteIndex, pixelFormat,
                        paletteFormat, resourcePixels, transparentSprites
                    ).joinToString(",")
                }
            }
        }
    }
    output.writeText(rows.joinToString("\n") + "\n")
    println("bundles=$bundleCount")
    println("df03_resources=$resourceCount")
    println("sprite_records=$spriteCount")
    println("palette_variants=$paletteVariants")
    println("decoded_sprite_palette_variants=$decodedVariants")
    println("decoded_pixels=$pixelCountTotal")
    println("audit_csv=${output.absolutePath}")
}
