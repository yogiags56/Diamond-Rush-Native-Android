package com.diamondrush.audit

import com.diamondrush.legacy.*
import java.io.File
import java.security.MessageDigest
import java.util.zip.ZipFile

private fun le32(b: ByteArray, p: Int): Int =
    (b[p].toInt() and 255) or ((b[p + 1].toInt() and 255) shl 8) or
    ((b[p + 2].toInt() and 255) shl 16) or ((b[p + 3].toInt() and 255) shl 24)

private fun rgbaBytes(argb: IntArray): ByteArray {
    val out = ByteArray(argb.size * 4)
    var p = 0
    for (v in argb) {
        out[p++] = (v ushr 16).toByte()
        out[p++] = (v ushr 8).toByte()
        out[p++] = v.toByte()
        out[p++] = (v ushr 24).toByte()
    }
    return out
}

private fun sha(bytes: ByteArray): String =
    MessageDigest.getInstance("SHA-256").digest(bytes).joinToString("") { "%02x".format(it) }

fun main(args: Array<String>) {
    val jarFile = File(args[0])
    val outDir = File(args[1]).apply { mkdirs() }
    var resources = 0
    var groups = 0
    var rendered = 0
    var leaves = 0
    val histogram = IntArray(4)
    val csv = File(outDir, "build213_kotlin_composite_inventory.csv")
    csv.bufferedWriter().use { writer ->
        writer.appendLine("bundle,entry,group,leaf_commands,width,height,origin_x,origin_y,sha256_rgba,status")
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
                    resources++
                    val section = LegacySpriteCompositeSection.fromFieldLayout(layout)
                    val sprites = LegacySpritePaletteSelector.decodeSprites(layout, 0)
                    val resolver = CompositeSpriteObjectResolver(section)
                    for (group in 0 until section.groupCount) {
                        groups++
                        val commands = resolver.resolve(group, 0, 0, 0)
                        if (commands.isEmpty()) continue
                        leaves += commands.size
                        for (command in commands) histogram[command.drawFlags and 3]++
                        val raster = CompositeSpriteRasterizer.rasterize(commands, sprites)
                        val bytes = rgbaBytes(raster.argb)
                        val stem = "${ze.name.replace('.', '_')}_e${entry}_g${group}"
                        File(outDir, "$stem.rgba").writeBytes(bytes)
                        File(outDir, "$stem.meta").writeText(
                            "${raster.width},${raster.height},${raster.originX},${raster.originY},${raster.drawnSprites}\n"
                        )
                        writer.appendLine(
                            "${ze.name},$entry,$group,${commands.size},${raster.width},${raster.height}," +
                                "${raster.originX},${raster.originY},${sha(bytes)},MATCH"
                        )
                        if (ze.name == "o.f" && entry == 0 && group == 0) {
                            for (paletteIndex in layout.palettesArgb.indices) {
                                val paletteSprites = LegacySpritePaletteSelector.decodeSprites(layout, paletteIndex)
                                val paletteRaster = CompositeSpriteRasterizer.rasterize(commands, paletteSprites)
                                val paletteStem = "palette_${paletteIndex}_o_f_e0_g0"
                                File(outDir, "$paletteStem.rgba").writeBytes(rgbaBytes(paletteRaster.argb))
                                File(outDir, "$paletteStem.meta").writeText(
                                    "${paletteRaster.width},${paletteRaster.height},${paletteRaster.originX}," +
                                        "${paletteRaster.originY},${paletteRaster.drawnSprites}\\n"
                                )
                            }
                        }
                        rendered++
                    }
                }
            }
        }
    }
    println("BUILD213_KOTLIN_AUDIT resources=$resources groups=$groups rendered=$rendered leaves=$leaves " +
        "transforms=${histogram.joinToString(",")}")
}
