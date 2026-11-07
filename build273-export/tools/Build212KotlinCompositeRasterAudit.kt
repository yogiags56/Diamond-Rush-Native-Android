package com.diamondrush.audit

import com.diamondrush.legacy.*
import java.io.File
import java.util.zip.ZipFile

private fun le32(b: ByteArray, p: Int): Int =
    (b[p].toInt() and 255) or ((b[p+1].toInt() and 255) shl 8) or
    ((b[p+2].toInt() and 255) shl 16) or ((b[p+3].toInt() and 255) shl 24)

fun main(args: Array<String>) {
    val jarFile = File(args[0])
    val outDir = File(args[1]).apply { mkdirs() }
    var done = 0
    ZipFile(jarFile).use { zip ->
        val entries = zip.entries()
        while (entries.hasMoreElements()) {
            val ze = entries.nextElement()
            if (!ze.name.endsWith(".f")) continue
            val container = zip.getInputStream(ze).use { it.readBytes() }
            if (container.isEmpty()) continue
            val count = container[0].toInt() and 255
            val base = 1 + count * 8
            for (entry in 0 until count) {
                val offset = le32(container, 1 + entry * 8)
                val length = le32(container, 5 + entry * 8)
                val payload = container.copyOfRange(base + offset, base + offset + length)
                if (payload.size < 4 || payload[0] != 0xDF.toByte() ||
                    payload[1] != 3.toByte() || payload[2] != 1.toByte() ||
                    payload[3] != 1.toByte()) continue
                val layout = LegacySpriteFieldLayoutParser.parse(payload)
                if (layout.groupCount == 0) continue
                val section = LegacySpriteCompositeSection.fromFieldLayout(layout)
                val palette = layout.palettesArgb.firstOrNull() ?: continue
                val sprites = layout.spritePayloads.mapIndexed { i, bytes ->
                    val w = layout.fDimensions[i * 2].toInt() and 255
                    val h = layout.fDimensions[i * 2 + 1].toInt() and 255
                    val indices = LegacySpriteDecoder.decodeIndices(bytes, w, h, layout.pixelFormat)
                    val pixels = IntArray(indices.size) { palette[indices[it]] }
                    LegacySpriteDecoder.DecodedSprite(w, h, pixels, pixels.any { (it ushr 24) != 255 })
                }
                val resolver = CompositeSpriteObjectResolver(section)
                for (group in 0 until section.groupCount) {
                    val commands = resolver.resolve(group, 0, 0, 0)
                    if (commands.size < 3 || commands.any { it.drawFlags != 0 }) continue
                    val raster = CompositeSpriteRasterizer.rasterize(commands, sprites)
                    val stem = "${ze.name.replace('.', '_')}_e${entry}_g${group}"
                    val raw = File(outDir, "$stem.rgba")
                    raw.outputStream().buffered().use { os ->
                        for (pixel in raster.argb) {
                            os.write((pixel ushr 16) and 255)
                            os.write((pixel ushr 8) and 255)
                            os.write(pixel and 255)
                            os.write(pixel ushr 24)
                        }
                    }
                    File(outDir, "$stem.meta").writeText("${raster.width},${raster.height},${raster.originX},${raster.originY},${raster.drawnSprites}\n")
                    done++
                }
            }
        }
    }
    println("KOTLIN_COMPOSITE_RASTER_AUDIT composites=$done")
}
