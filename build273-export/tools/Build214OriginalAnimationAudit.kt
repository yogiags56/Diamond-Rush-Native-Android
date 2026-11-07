package com.diamondrush.audit

import com.diamondrush.legacy.LegacySpriteAnimationFrame
import com.diamondrush.legacy.LegacySpriteAnimationTable
import com.diamondrush.legacy.LegacySpriteFieldLayoutParser
import java.io.File
import java.util.zip.ZipFile

private fun le32(b: ByteArray, p: Int): Int =
    (b[p].toInt() and 255) or ((b[p + 1].toInt() and 255) shl 8) or
    ((b[p + 2].toInt() and 255) shl 16) or ((b[p + 3].toInt() and 255) shl 24)

fun main(args: Array<String>) {
    val jarFile = File(args[0])
    var resources = 0
    var sequences = 0
    var records = 0
    var validGroups = 0
    var noGroupFrames = 0
    var invalidGroups = 0
    val durations = IntArray(256)
    val controlFlags = IntArray(256)
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
                val table = LegacySpriteAnimationTable.fromFieldLayout(layout)
                if (table.recordCount == 0 && table.sequenceCount == 0) continue
                resources++
                sequences += table.sequenceCount
                records += table.recordCount
                for (sequenceIndex in 0 until table.sequenceCount) {
                    val sequence = table.sequence(sequenceIndex)
                    for (frameIndex in 0 until sequence.frameCount) {
                        val frame = table.frame(sequenceIndex, frameIndex)
                        durations[frame.durationUnits]++
                        controlFlags[frame.controlFlags]++
                        when {
                            frame.compositeGroupIndex == null -> noGroupFrames++
                            frame.compositeGroupIndex in 0 until layout.groupCount -> validGroups++
                            else -> invalidGroups++
                        }
                    }
                }
                check(table.validateGroupReferences().isEmpty()) {
                    "Invalid animation group reference in ${ze.name} entry $entry"
                }
            }
        }
    }
    check(invalidGroups == 0)
    check(validGroups == records - noGroupFrames)
    println("BUILD214_ANIMATION_AUDIT resources=$resources sequences=$sequences records=$records " +
        "validGroups=$validGroups noGroupFrames=$noGroupFrames invalidGroups=$invalidGroups")
    println("DURATION_HIST=" + durations.withIndex().filter { it.value > 0 }.joinToString(",") { "${it.index}:${it.value}" })
    println("CONTROL_HIST=" + controlFlags.withIndex().filter { it.value > 0 }.joinToString(",") { "${it.index}:${it.value}" })
}
