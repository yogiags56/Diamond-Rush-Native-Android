package com.diamondrush.legacy

/**
 * Build 237: decoded pixels bound to a concrete draw operation and an explicit
 * palette row. This is still renderer-neutral: MIDP transforms, clipping and
 * target-surface writes are deliberately deferred to the raster execution stage.
 */
data class LegacyPaletteBoundSpriteDraw(
    val operation: LegacyConcreteSpriteDrawOperation,
    val paletteIndex: Int,
    val argbPixels: IntArray,
    val hasTransparency: Boolean
) {
    init {
        require(argbPixels.size == operation.spriteWidth * operation.spriteHeight) {
            "Pixel count does not match operation sprite dimensions"
        }
    }
}

object LegacyPaletteAwareSpriteDecoder {
    /** Decode every sprite in one parsed resource using the caller's proven palette state. */
    @JvmStatic
    fun decodeResource(
        parsed: LegacySpriteResourceBundleParser.ParsedDf03,
        globalArraySlot: Int,
        paletteIndex: Int
    ): List<LegacyDecodedSpriteRecord> {
        require(globalArraySlot >= 0) { "Global resource slot must be non-negative" }
        val paletteFormat = requireNotNull(parsed.paletteFormat) {
            "Resource f[$globalArraySlot] has no palette format"
        }
        val pixelFormat = requireNotNull(parsed.pixelFormat) {
            "Resource f[$globalArraySlot] has no pixel format"
        }
        require(paletteFormat in SUPPORTED_PALETTE_FORMATS) {
            "Unsupported palette format $paletteFormat in f[$globalArraySlot]"
        }
        require(paletteIndex in parsed.palettes.indices) {
            "Palette index $paletteIndex out of range for f[$globalArraySlot]"
        }
        val palette = LegacySpriteDecoder.decodePalette(parsed.palettes[paletteIndex], paletteFormat)
        return parsed.sprites.map { sprite ->
            require(sprite.width > 0 && sprite.height > 0) {
                "Invalid dimensions ${sprite.width}x${sprite.height} for f[$globalArraySlot] sprite ${sprite.index}"
            }
            val indices = LegacySpriteDecoder.decodeIndices(
                sprite.encodedPixels, sprite.width, sprite.height, pixelFormat
            )
            val pixels = IntArray(indices.size)
            for (pixelIndex in indices.indices) {
                val colorIndex = indices[pixelIndex]
                require(colorIndex in palette.indices) {
                    "Palette index $colorIndex at pixel $pixelIndex exceeds ${palette.size} colors " +
                        "in f[$globalArraySlot] palette $paletteIndex sprite ${sprite.index}"
                }
                pixels[pixelIndex] = palette[colorIndex]
            }
            LegacyDecodedSpriteRecord(
                globalArraySlot, sprite.index, sprite.width, sprite.height,
                pixelFormat, paletteFormat, paletteIndex, pixels,
                pixels.any { (it ushr 24) != 0xff }
            )
        }
    }

    /** Attach decoded pixels to operations without changing their geometry or flags. */
    @JvmStatic
    fun bindOperations(
        operations: List<LegacyConcreteSpriteDrawOperation>,
        decodedSprites: List<LegacyDecodedSpriteRecord>,
        paletteIndex: Int
    ): List<LegacyPaletteBoundSpriteDraw> {
        val byIdentity = decodedSprites.associateBy { it.globalArraySlot to it.spriteIndex }
        require(byIdentity.size == decodedSprites.size) { "Duplicate decoded sprite identity" }
        return operations.map { operation ->
            val decoded = byIdentity[operation.globalArraySlot to operation.spriteIndex]
                ?: throw IllegalArgumentException(
                    "No decoded pixels for f[${operation.globalArraySlot}] sprite ${operation.spriteIndex}"
                )
            require(decoded.paletteIndex == paletteIndex) {
                "Decoded palette ${decoded.paletteIndex} does not match requested palette $paletteIndex"
            }
            require(decoded.width == operation.spriteWidth && decoded.height == operation.spriteHeight) {
                "Decoded dimensions ${decoded.width}x${decoded.height} disagree with draw operation " +
                    "${operation.spriteWidth}x${operation.spriteHeight}"
            }
            LegacyPaletteBoundSpriteDraw(
                operation, paletteIndex, decoded.argbPixels.copyOf(), decoded.hasTransparency
            )
        }
    }

    private val SUPPORTED_PALETTE_FORMATS = setOf(-30584, 17476, 21781, 25861)
}

data class LegacyDecodedSpriteRecord(
    val globalArraySlot: Int,
    val spriteIndex: Int,
    val width: Int,
    val height: Int,
    val pixelFormat: Int,
    val paletteFormat: Int,
    val paletteIndex: Int,
    val argbPixels: IntArray,
    val hasTransparency: Boolean
) {
    init {
        require(globalArraySlot >= 0 && spriteIndex >= 0)
        require(width > 0 && height > 0)
        require(argbPixels.size == width * height)
    }
}
