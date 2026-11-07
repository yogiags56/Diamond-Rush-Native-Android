package com.diamondrush.audit

import com.diamondrush.legacy.LegacySpriteFieldLayoutParser
import com.diamondrush.legacy.LegacySpriteDecoder
import java.io.File
import java.security.MessageDigest
import java.util.zip.ZipFile

fun le32(b: ByteArray, p: Int): Long =
    (b[p].toLong() and 255) or ((b[p+1].toLong() and 255) shl 8) or
    ((b[p+2].toLong() and 255) shl 16) or ((b[p+3].toLong() and 255) shl 24)

fun sha(bytes: ByteArray): String = MessageDigest.getInstance("SHA-256")
    .digest(bytes).joinToString("") { "%02x".format(it) }

fun main(args: Array<String>) {
    val jarPath = args[0]
    val out = File(args[1])
    var resources = 0
    var sprites = 0
    out.bufferedWriter().use { w ->
        w.appendLine("bundle,entry,sprite,width,height,pixel_format,payload_bytes,decoded_pixels,max_index,sha256_indices,status")
        ZipFile(jarPath).use { zip ->
            val entries = zip.entries()
            while (entries.hasMoreElements()) {
                val ze = entries.nextElement()
                if (!ze.name.endsWith(".f")) continue
                val c = zip.getInputStream(ze).use { it.readBytes() }
                if (c.isEmpty()) continue
                val n = c[0].toInt() and 255
                val base = 1 + n * 8
                for (i in 0 until n) {
                    val off = le32(c, 1 + i * 8).toInt()
                    val len = le32(c, 5 + i * 8).toInt()
                    val payload = c.copyOfRange(base + off, base + off + len)
                    if (payload.size < 4 || payload[0] != 0xDF.toByte() ||
                        payload[1] != 0x03.toByte() || payload[2] != 1.toByte() ||
                        payload[3] != 1.toByte()) continue
                    val layout = LegacySpriteFieldLayoutParser.parse(payload)
                    resources++
                    for (si in 0 until layout.spriteCount) {
                        val width = layout.fDimensions[si * 2].toInt() and 255
                        val height = layout.fDimensions[si * 2 + 1].toInt() and 255
                        val pixels = LegacySpriteDecoder.decodeIndices(
                            layout.spritePayloads[si], width, height, layout.pixelFormat
                        )
                        val maxIndex = pixels.maxOrNull() ?: 0
                        require(maxIndex < layout.colorsPerPalette) {
                            "Palette overflow ${ze.name}:$i:$si $maxIndex/${layout.colorsPerPalette}"
                        }
                        val bytes = ByteArray(pixels.size) { pixels[it].toByte() }
                        val format = "0x%04X".format(layout.pixelFormat)
                        w.appendLine("${ze.name},$i,$si,$width,$height,$format,${layout.spritePayloads[si].size},${pixels.size},$maxIndex,${sha(bytes)},PASS")
                        sprites++
                    }
                }
            }
        }
    }
    println("KOTLIN_AUDIT resources=$resources sprites=$sprites output=${out.absolutePath}")
}
