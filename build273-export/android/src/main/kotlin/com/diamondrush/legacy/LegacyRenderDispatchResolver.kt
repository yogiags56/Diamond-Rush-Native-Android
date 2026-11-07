    package com.diamondrush.legacy

    /**
     * Build 227: typed interpretation of the raw selectors found in i.D().
     *
     * This layer resolves numeric control-flow and animation-frame requests only.
     * It intentionally does not assign gameplay names to cell IDs or resources.
     */
    enum class LegacyMainDispatchKind {
        EXPLICIT_SWITCH_CASE,
        DEFAULT_SHARED_TAIL,
        SIGNED_BYTE_BYPASS_TO_SHARED_TAIL,
        SKIP_CELL
    }

    data class LegacyMainDispatchDecision(
        val kind: LegacyMainDispatchKind,
        val rawSelector: Int,
        val branchTargetOffset: Int
    )

    data class LegacyRenderCellSample(
        /** Low 8 bits of the serialized integer map plane. */
        val integerPlaneLowByte: Int,
        /** Signed value read from the serialized byte map plane. */
        val signedBytePlaneValue: Int,
        /** Full packed integer-plane value, retained for metadata bits. */
        val packedIntegerPlaneValue: Int
    ) {
        init {
            require(integerPlaneLowByte in 0..255)
            require(signedBytePlaneValue in -128..127)
            require((packedIntegerPlaneValue and 0xff) == integerPlaneLowByte) {
                "integerPlaneLowByte must match packedIntegerPlaneValue & 255"
            }
        }
    }

    enum class LegacyOverlaySelectionKind {
        ANIMATION_SEQUENCE_FRAME,
        DIRECT_DRAW_ARGUMENT
    }

    data class LegacyOverlayFrameSelection(
        val resourceIndex: Int,
        val kind: LegacyOverlaySelectionKind,
        val sequenceIndex: Int?,
        val frameIndex: Int?,
        val directDrawArgument: Int?,
        val rawLowByte: Int,
        val rawPackedHighValue: Int
    )

    data class LegacyResolvedCompositeOverlay(
        val selection: LegacyOverlayFrameSelection,
        val placement: LegacySpriteAnimationFramePlacement,
        val leafCommands: List<CompositeSpriteObjectResolver.LeafDrawCommand>
    )

    object LegacyRenderDispatchResolver {
        private val bJByValue = LegacyRenderDispatchCatalog.bJCases.associateBy { it.rawValue }
        private val bIByValue = LegacyRenderDispatchCatalog.bICases.associateBy { it.rawValue }

        /**
         * First main switch: selector is the unsigned low byte of a:[[I.
         * Unknown values take the switch default at offset 1995.
         */
        fun selectFirstMainPass(unsignedSelector: Int): LegacyMainDispatchDecision {
            require(unsignedSelector in 0..255)
            val explicit = bJByValue[unsignedSelector]
            return if (explicit != null) {
                LegacyMainDispatchDecision(
                    LegacyMainDispatchKind.EXPLICIT_SWITCH_CASE,
                    unsignedSelector,
                    explicit.branchTargetOffset
                )
            } else {
                LegacyMainDispatchDecision(
                    LegacyMainDispatchKind.DEFAULT_SHARED_TAIL,
                    unsignedSelector,
                    LegacyRenderDispatchCatalog.MAIN_PASS_BJ_SHARED_TAIL_OFFSET
                )
            }
        }

        /**
         * Second main switch: selector is a signed JVM byte from a:[[B.
         * Bytecode checks -1 first, then tests i2b(selector - 80) >= 0.
         */
        fun selectSecondMainPass(signedSelector: Int): LegacyMainDispatchDecision {
            require(signedSelector in -128..127)
            if (signedSelector == -1) {
                return LegacyMainDispatchDecision(
                    LegacyMainDispatchKind.SKIP_CELL,
                    signedSelector,
                    5976
                )
            }
            val narrowedDifference = (signedSelector - 80).toByte().toInt()
            if (narrowedDifference >= 0) {
                return LegacyMainDispatchDecision(
                    LegacyMainDispatchKind.SIGNED_BYTE_BYPASS_TO_SHARED_TAIL,
                    signedSelector,
                    LegacyRenderDispatchCatalog.MAIN_PASS_BI_SHARED_TAIL_OFFSET
                )
            }
            val explicit = bIByValue[signedSelector]
            return if (explicit != null) {
                LegacyMainDispatchDecision(
                    LegacyMainDispatchKind.EXPLICIT_SWITCH_CASE,
                    signedSelector,
                    explicit.branchTargetOffset
                )
            } else {
                LegacyMainDispatchDecision(
                    LegacyMainDispatchKind.DEFAULT_SHARED_TAIL,
                    signedSelector,
                    LegacyRenderDispatchCatalog.MAIN_PASS_BI_SHARED_TAIL_OFFSET
                )
            }
        }

        /**
         * Applies the second traversal's bytecode filter before looking up a route.
         * The raw low byte is from a:[[I & 255; the other values remain opaque.
         */
        fun selectSecondaryOverlay(cell: LegacyRenderCellSample): LegacyRenderDispatchCatalog.OverlayRoute? {
            val raw = cell.integerPlaneLowByte
            if (!(raw < 38 || raw >= 80)) return null
            return LegacyRenderDispatchCatalog.overlayRoute(raw)
        }

        /**
         * Resolve the bytecode's sequence/frame expressions.
         *
         * animationClock is the original aS value. Kotlin's signed shift and
         * remainder are intentional matches for JVM ishl/ishr/irem behavior.
         * Resource 42 uses the six-int direct draw path, not the five-byte
         * animation-table path, so its first draw argument remains opaque.
         */
        fun resolveOverlayFrame(
            cell: LegacyRenderCellSample,
            animationClock: Int,
            animationTables: Map<Int, LegacySpriteAnimationTable>
        ): LegacyOverlayFrameSelection? {
            val route = selectSecondaryOverlay(cell) ?: return null
            val raw = cell.integerPlaneLowByte
            val packedHigh = cell.packedIntegerPlaneValue shr 8

            fun animated(resource: Int, sequence: Int, phase: Int): LegacyOverlayFrameSelection {
                val table = animationTables[resource]
                    ?: throw IllegalArgumentException("Missing animation table for resource f[$resource]")
                val sequenceData = table.sequence(sequence)
                require(sequenceData.frameCount > 0) {
                    "Animation sequence $sequence in resource f[$resource] has no frames"
                }
                val frame = phase % sequenceData.frameCount
                return LegacyOverlayFrameSelection(
                    resource, LegacyOverlaySelectionKind.ANIMATION_SEQUENCE_FRAME,
                    sequence, frame, null, raw, packedHigh
                )
            }

            return when (route.frameRule) {
                LegacyRenderDispatchCatalog.OverlayFrameRule.LOW_ID_MINUS_20_ANIMATED_BY_AS_SHIFT_2 ->
                    animated(route.resourceIndex, raw - 20, animationClock shr 2)
                LegacyRenderDispatchCatalog.OverlayFrameRule.PACKED_HIGH_BYTE_ANIMATED_BY_AS_SHIFT_1 ->
                    animated(route.resourceIndex, packedHigh, animationClock shr 1)
                LegacyRenderDispatchCatalog.OverlayFrameRule.PACKED_HIGH_BYTE_RAW ->
                    animated(route.resourceIndex, 0, packedHigh and 0xff)
                LegacyRenderDispatchCatalog.OverlayFrameRule.PACKED_HIGH_BYTE_MINUS_ONE_TIMES_7_DIV_16 ->
                    animated(route.resourceIndex, 0, (((packedHigh - 1) * 7) / 16))
                LegacyRenderDispatchCatalog.OverlayFrameRule.LOW_ID_MINUS_80_SIGNED_BYTE -> {
                    val directFrame = (raw - 80).toByte().toInt()
                    require(directFrame >= 0) { "Signed-byte direct frame index is negative" }
                    LegacyOverlayFrameSelection(
                        route.resourceIndex, LegacyOverlaySelectionKind.DIRECT_DRAW_ARGUMENT,
                        null, null, directFrame, raw, packedHigh
                    )
                }
            }
        }

        /**
         * Resolve an animation-table frame into the existing composite graph model.
         * The frame's 0xFF group sentinel yields an empty leaf-command list.
         */
        fun resolveCompositeOverlay(
            selection: LegacyOverlayFrameSelection,
            table: LegacySpriteAnimationTable,
            section: LegacySpriteCompositeSection,
            baseX: Int,
            baseY: Int,
            incomingFlags: Int = 0,
            inheritedOffsetX: Int = 0,
            inheritedOffsetY: Int = 0,
            opaqueArgumentA: Int = 0,
            opaqueArgumentB: Int = 0
        ): LegacyResolvedCompositeOverlay {
            require(selection.kind == LegacyOverlaySelectionKind.ANIMATION_SEQUENCE_FRAME) {
                "Direct-frame resource requests do not use the animation/composite path"
            }
            val sequence = selection.sequenceIndex
                ?: throw IllegalArgumentException("Animation selection has no sequence index")
            val frameIndex = selection.frameIndex
                ?: throw IllegalArgumentException("Animation selection has no frame index")
            val placement = table.placement(
                sequence, frameIndex, baseX, baseY, incomingFlags,
                inheritedOffsetX, inheritedOffsetY
            )
            val group = placement.frame.compositeGroupIndex
            val commands = if (group == null) emptyList() else {
                CompositeSpriteObjectResolver(section).resolve(
                    rootGroup = group,
                    x = placement.drawX,
                    y = placement.drawY,
                    incomingFlags = placement.drawFlags,
                    opaqueArgumentA = opaqueArgumentA,
                    opaqueArgumentB = opaqueArgumentB
                )
            }
            return LegacyResolvedCompositeOverlay(selection, placement, commands)
        }

        /** Exact supplemental conditions after the secondary overlay branch. */
        fun supplementalResources(cell: LegacyRenderCellSample): List<Int> =
            LegacyRenderDispatchCatalog.supplementalResourceIndices(
                cell.packedIntegerPlaneValue, cell.signedBytePlaneValue
            )
    }
