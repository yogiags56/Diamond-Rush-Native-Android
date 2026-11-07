import com.diamondrush.legacy.LegacyBundleSpriteSlotCatalog
import com.diamondrush.legacy.LegacyPaletteAwareSpriteDecoder
import com.diamondrush.legacy.LegacySpriteResourceBundleParser
import java.io.File
import java.security.MessageDigest
import java.util.zip.ZipFile

/** Reproducible Build237 audit of all statically mapped original-JAR sprite resources. */
fun main(args: Array<String>) {
    require(args.size == 2) { "Usage: <original.jar> <output.csv>" }
    val jar = File(args[0])
    val output = File(args[1])
    val rows = mutableListOf(
        "global_slot,bundle,entry,palette_index,sprite_count,pixel_count,transparent_sprites,sha256_pixel_stream"
    )
    var paletteVariants = 0
    var spriteInstances = 0
    var pixelsTotal = 0L

    ZipFile(jar).use { zip ->
        for (binding in LegacyBundleSpriteSlotCatalog.staticBindings) {
            val bundleName = binding.bundlePath.removePrefix("/")
            val bundleEntry = requireNotNull(zip.getEntry(bundleName)) { "Missing bundle $bundleName" }
            val bundleBytes = zip.getInputStream(bundleEntry).use { it.readBytes() }
            val entry = LegacySpriteResourceBundleParser.readBundleEntries(bundleBytes)
                .firstOrNull { it.index == binding.entryIndex }
                ?: error("Missing $bundleName directory entry ${binding.entryIndex}")
            val parsed = LegacySpriteResourceBundleParser.parse(entry.payload)

            for (paletteIndex in parsed.palettes.indices) {
                val decoded = LegacyPaletteAwareSpriteDecoder.decodeResource(
                    parsed, binding.globalArraySlot, paletteIndex
                )
                val digest = MessageDigest.getInstance("SHA-256")
                var pixelCount = 0L
                decoded.forEach { sprite ->
                    spriteInstances++
                    pixelsTotal += sprite.argbPixels.size
                    pixelCount += sprite.argbPixels.size
                    sprite.argbPixels.forEach { argb ->
                        digest.update((argb ushr 24).toByte())
                        digest.update((argb ushr 16).toByte())
                        digest.update((argb ushr 8).toByte())
                        digest.update(argb.toByte())
                    }
                }
                paletteVariants++
                rows += listOf(
                    binding.globalArraySlot, bundleName, binding.entryIndex, paletteIndex,
                    decoded.size, pixelCount, decoded.count { it.hasTransparency },
                    digest.digest().joinToString("") { "%02x".format(it) }
                ).joinToString(",")
            }
        }
    }

    output.writeText(rows.joinToString("\n") + "\n")
    println("mapped_resources=${LegacyBundleSpriteSlotCatalog.staticBindings.size}")
    println("decoded_palette_variants=$paletteVariants")
    println("decoded_sprite_instances=$spriteInstances")
    println("decoded_pixels=$pixelsTotal")
    println("audit_csv=${output.absolutePath}")
}
