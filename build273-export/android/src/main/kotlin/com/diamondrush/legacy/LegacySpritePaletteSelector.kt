package com.diamondrush.legacy

/**
 * Decodes one sprite set using the palette row selected by the original class f.a(IIII).
 *
 * The original first int argument is the palette index stored in field a:I.
 * The second and fourth arguments are not read by that method; the third argument
 * is the highest sprite index to preload. Palette choice is therefore explicit
 * state and must be supplied by the caller.
 */
object LegacySpritePaletteSelector {
    fun decodeSprites(
        layout: LegacySpriteFieldLayout,
        paletteIndex: Int
    ): List<LegacySpriteDecoder.DecodedSprite> {
        require(paletteIndex in layout.palettesArgb.indices) {
            "Palette index $paletteIndex out of range 0 until ${layout.palettesArgb.size}"
        }
        val palette = layout.palettesArgb[paletteIndex]
        return layout.spritePayloads.mapIndexed { index, payload ->
            val width = layout.fDimensions[index * 2].toInt() and 0xff
            val height = layout.fDimensions[index * 2 + 1].toInt() and 0xff
            val indices = LegacySpriteDecoder.decodeIndices(payload, width, height, layout.pixelFormat)
            val pixels = IntArray(indices.size)
            for (i in indices.indices) {
                val colorIndex = indices[i]
                require(colorIndex in palette.indices) {
                    "Palette index $colorIndex out of range for palette row $paletteIndex, sprite $index"
                }
                pixels[i] = palette[colorIndex]
            }
            LegacySpriteDecoder.DecodedSprite(
                width, height, pixels, pixels.any { (it ushr 24) != 0xff }
            )
        }
    }
}
