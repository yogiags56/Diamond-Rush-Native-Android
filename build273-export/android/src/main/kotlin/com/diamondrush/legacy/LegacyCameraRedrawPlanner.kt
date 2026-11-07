package com.diamondrush.legacy

/**
 * Build 225 camera/redraw reconstruction from the original i.D() bytecode.
 * Coordinates are world pixels. The map pixel extents are cC (X) and cD (Y).
 */
enum class LegacyRedrawAxis { INITIAL, X_STRIP, Y_STRIP }

data class LegacyMapRedrawRegion(
    val axis: LegacyRedrawAxis,
    val startX: Int,
    val startY: Int,
    val endXInclusive: Int,
    val endYInclusive: Int
) {
    init {
        require(startX <= endXInclusive)
        require(startY <= endYInclusive)
        require(startX % LegacyGameplayViewport.TILE_SIZE == 0)
        require(startY % LegacyGameplayViewport.TILE_SIZE == 0)
        require(endXInclusive % LegacyGameplayViewport.TILE_SIZE == 0)
        require(endYInclusive % LegacyGameplayViewport.TILE_SIZE == 0)
    }

    val columns: Int get() =
        (endXInclusive - startX) / LegacyGameplayViewport.TILE_SIZE + 1
    val rows: Int get() =
        (endYInclusive - startY) / LegacyGameplayViewport.TILE_SIZE + 1
}

/** Tile-aligned boundaries calculated by D() before calling a(IIIIZ). */
data class LegacyCameraAlignedBounds(
    val left: Int,
    val top: Int,
    val right: Int,
    val bottom: Int
) {
    init {
        require(left <= right && top <= bottom)
    }
}

/**
 * Stateful counterpart of cE/cF/cG/cH cache in D().
 *
 * The first call paints the complete aligned region. Later calls paint only
 * newly exposed X and/or Y strips. The planner emits source helper arguments;
 * it does not render tiles or infer their semantics.
 */
class LegacyCameraRedrawPlanner {
    private var previous: LegacyCameraAlignedBounds? = null

    fun reset() { previous = null }

    fun alignedBounds(
        cameraX: Int,
        cameraY: Int,
        mapPixelWidth: Int,
        mapPixelHeight: Int
    ): LegacyCameraAlignedBounds {
        require(mapPixelWidth > 0 && mapPixelHeight > 0)
        val tile = LegacyGameplayViewport.TILE_SIZE
        val left = cameraX - cameraX % tile
        val top = cameraY - cameraY % tile
        val rightEdge = cameraX + mapPixelWidth - tile
        val bottomEdge = cameraY + mapPixelHeight - tile
        val right = rightEdge - rightEdge % tile
        val bottom = bottomEdge - bottomEdge % tile
        return LegacyCameraAlignedBounds(left, top, right, bottom)
    }

    fun plan(
        cameraX: Int,
        cameraY: Int,
        mapPixelWidth: Int,
        mapPixelHeight: Int
    ): List<LegacyMapRedrawRegion> {
        val current = alignedBounds(cameraX, cameraY, mapPixelWidth, mapPixelHeight)
        val old = previous
        val result = ArrayList<LegacyMapRedrawRegion>(2)

        if (old == null) {
            result += LegacyMapRedrawRegion(
                LegacyRedrawAxis.INITIAL,
                current.left, current.top, current.right, current.bottom
            )
            previous = current
            return result
        }

        if (old.left != current.left) {
            val startX: Int
            val endX: Int
            if (old.left < current.left) {
                startX = old.right + LegacyGameplayViewport.TILE_SIZE
                endX = current.right
            } else {
                startX = current.left
                endX = old.left - LegacyGameplayViewport.TILE_SIZE
            }
            if (startX <= endX) {
                result += LegacyMapRedrawRegion(
                    LegacyRedrawAxis.X_STRIP,
                    startX, current.top, endX, current.bottom
                )
            }
        }

        if (old.top != current.top) {
            val startY: Int
            val endY: Int
            if (old.top < current.top) {
                startY = old.bottom + LegacyGameplayViewport.TILE_SIZE
                endY = current.bottom
            } else {
                startY = current.top
                endY = old.top - LegacyGameplayViewport.TILE_SIZE
            }
            if (startY <= endY) {
                result += LegacyMapRedrawRegion(
                    LegacyRedrawAxis.Y_STRIP,
                    current.left, startY, current.right, endY
                )
            }
        }

        previous = current
        return result
    }
}

/**
 * Exact integer expression at D() offsets 48–109.
 * It computes a frame-dependent vertical camera step from bj and aS,
 * clamps the step to the current b value, then subtracts it from b.
 */
data class LegacyVerticalCameraStep(
    val resultingOffset: Int,
    val appliedDelta: Int
)

object LegacyCameraMotion {
    fun applyVerticalStep(
        currentOffset: Int,
        smoothingParameterBj: Int,
        frameCounter: Int
    ): LegacyVerticalCameraStep {
        var delta = 0
        if (smoothingParameterBj > 0) {
            delta = ((smoothingParameterBj * frameCounter) %
                ((smoothingParameterBj shr 1) + 1)) % 12
        }
        if (delta > currentOffset) delta = currentOffset
        return LegacyVerticalCameraStep(
            resultingOffset = currentOffset - delta,
            appliedDelta = delta
        )
    }
}
