package com.diamondrush.legacy

/**
 * Build 224: logical canvas and gameplay viewport contract.
 *
 * Coordinates are logical pixels, not device pixels. The original paint path
 * clips the full canvas to 320x240, translates the gameplay origin by y=31,
 * then applies a local 320x178 clip.
 */
data class LegacyRect(val x: Int, val y: Int, val width: Int, val height: Int) {
    init {
        require(width >= 0 && height >= 0)
    }
    val rightExclusive: Int get() = x + width
    val bottomExclusive: Int get() = y + height
}

object LegacyGameplayViewport {
    const val CANVAS_WIDTH = 320
    const val CANVAS_HEIGHT = 240
    const val TILE_SIZE = 24
    const val VIEWPORT_TRANSLATE_Y = 31
    const val VIEWPORT_WIDTH = 320
    const val VIEWPORT_HEIGHT = 178

    val canvas = LegacyRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT)
    val gameplayClipInCanvas = LegacyRect(
        0, VIEWPORT_TRANSLATE_Y, VIEWPORT_WIDTH, VIEWPORT_HEIGHT
    )
}

/** Camera values are the original raw pixel offsets a and b, not normalized values. */
data class LegacyCameraOffset(val rawX: Int, val rawY: Int) {
    val tileX: Int get() = rawX / LegacyGameplayViewport.TILE_SIZE
    val tileY: Int get() = rawY / LegacyGameplayViewport.TILE_SIZE
    val pixelRemainderX: Int get() = rawX % LegacyGameplayViewport.TILE_SIZE
    val pixelRemainderY: Int get() = rawY % LegacyGameplayViewport.TILE_SIZE
}

/**
 * The source renderer has two independent switch selectors. Keep their values
 * separate: no combined enum or semantic aliases are inferred here.
 */
data class LegacyRenderDispatchSelectors(val bJ: Int, val bI: Int) {
    companion object {
        const val BJ_CASE_COUNT = 35
        const val BI_CASE_COUNT = 50
    }
}

/** One candidate in the statically observed -1..8 row, -1..14 column scan. */
data class LegacyVisibleCellCandidate(
    val row: Int,
    val column: Int,
    val mapFirst: Int,
    val mapSecond: Int,
    val screenX: Int,
    val screenY: Int,
    val inBounds: Boolean
)

/**
 * Build 215 proves candidate loop bounds and screen placement formula, but not
 * all wrap/semantic behavior. This iterator therefore reports bounded in-map
 * candidates only and preserves out-of-map candidates as explicit records.
 *
 * The first/second map dimensions follow the room model's original orientation.
 */
object LegacyVisibleCellTraversal {
    const val FIRST_ROW = -1
    const val LAST_ROW = 8
    const val FIRST_COLUMN = -1
    const val LAST_COLUMN = 14

    fun candidates(
        room: LegacyRoomMapPlanes,
        camera: LegacyCameraOffset
    ): List<LegacyVisibleCellCandidate> {
        val result = ArrayList<LegacyVisibleCellCandidate>(160)
        for (row in FIRST_ROW..LAST_ROW) {
            for (column in FIRST_COLUMN..LAST_COLUMN) {
                val mapFirst = camera.tileX + column
                val mapSecond = camera.tileY + row
                val inBounds = mapFirst in 0 until room.firstDimension &&
                    mapSecond in 0 until room.secondDimension
                result += LegacyVisibleCellCandidate(
                    row = row,
                    column = column,
                    mapFirst = mapFirst,
                    mapSecond = mapSecond,
                    screenX = column * LegacyGameplayViewport.TILE_SIZE - camera.pixelRemainderX,
                    screenY = row * LegacyGameplayViewport.TILE_SIZE - camera.pixelRemainderY,
                    inBounds = inBounds
                )
            }
        }
        return result
    }
}

/** Minimal deterministic logical pixel surface with viewport-clipped sprite blits. */
class LegacyLogicalSurface(
    val width: Int = LegacyGameplayViewport.CANVAS_WIDTH,
    val height: Int = LegacyGameplayViewport.CANVAS_HEIGHT
) {
    private val pixels: IntArray
    init {
        require(width > 0 && height > 0)
        pixels = IntArray(Math.multiplyExact(width, height))
    }

    fun clear(argb: Int = 0) { pixels.fill(argb) }

    fun blit(
        source: IntArray,
        sourceWidth: Int,
        sourceHeight: Int,
        destinationX: Int,
        destinationY: Int,
        clip: LegacyRect = LegacyGameplayViewport.canvas
    ) {
        require(sourceWidth > 0 && sourceHeight > 0)
        require(source.size == Math.multiplyExact(sourceWidth, sourceHeight))
        val left = maxOf(0, clip.x, destinationX)
        val top = maxOf(0, clip.y, destinationY)
        val right = minOf(width, clip.rightExclusive, destinationX + sourceWidth)
        val bottom = minOf(height, clip.bottomExclusive, destinationY + sourceHeight)
        if (left >= right || top >= bottom) return
        for (y in top until bottom) {
            val sy = y - destinationY
            for (x in left until right) {
                val sx = x - destinationX
                val color = source[sy * sourceWidth + sx]
                if ((color ushr 24) != 0) pixels[y * width + x] = color
            }
        }
    }

    fun pixelAt(x: Int, y: Int): Int {
        require(x in 0 until width && y in 0 until height)
        return pixels[y * width + x]
    }

    fun copyPixels(): IntArray = pixels.copyOf()
}
