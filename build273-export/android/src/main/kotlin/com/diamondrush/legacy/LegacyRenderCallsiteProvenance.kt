package com.diamondrush.legacy

/** Exact invocation shape observed in original i.D()V bytecode. Runtime arguments remain opaque. */
data class LegacyRenderCallsiteDescriptor(
    val bytecodeOffset: Int,
    val descriptor: String,
    val integerArgumentCount: Int,
    val receiverSlotProven: Boolean = false,
    val compositeGroupProven: Boolean = false
)

object LegacyRenderCallsiteProvenance {
    const val SPRITE_DRAW_7_INT_DESCRIPTOR = "(Ljavax/microedition/lcdui/Graphics;IIIIIII)V"
    const val SPRITE_DRAW_6_INT_DESCRIPTOR = "(Ljavax/microedition/lcdui/Graphics;IIIIII)V"

    val verifiedCallsites = listOf(
        LegacyRenderCallsiteDescriptor(960, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(1057, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(1526, SPRITE_DRAW_6_INT_DESCRIPTOR, 6),
        LegacyRenderCallsiteDescriptor(1950, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(2054, SPRITE_DRAW_6_INT_DESCRIPTOR, 6),
        LegacyRenderCallsiteDescriptor(2178, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(3984, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(4284, SPRITE_DRAW_6_INT_DESCRIPTOR, 6),
        LegacyRenderCallsiteDescriptor(4393, SPRITE_DRAW_6_INT_DESCRIPTOR, 6),
        LegacyRenderCallsiteDescriptor(5735, SPRITE_DRAW_6_INT_DESCRIPTOR, 6),
        LegacyRenderCallsiteDescriptor(5912, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(5953, SPRITE_DRAW_6_INT_DESCRIPTOR, 6),
        LegacyRenderCallsiteDescriptor(6130, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(6313, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(6426, SPRITE_DRAW_6_INT_DESCRIPTOR, 6),
        LegacyRenderCallsiteDescriptor(6748, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(6813, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(6853, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(6887, SPRITE_DRAW_6_INT_DESCRIPTOR, 6),
        LegacyRenderCallsiteDescriptor(6928, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(6972, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(7259, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(7672, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(7992, SPRITE_DRAW_7_INT_DESCRIPTOR, 7),
        LegacyRenderCallsiteDescriptor(8017, SPRITE_DRAW_6_INT_DESCRIPTOR, 6)
    )

    fun validate(): Boolean = verifiedCallsites.all {
        it.bytecodeOffset >= 0 &&
            ((it.descriptor == SPRITE_DRAW_7_INT_DESCRIPTOR && it.integerArgumentCount == 7) ||
             (it.descriptor == SPRITE_DRAW_6_INT_DESCRIPTOR && it.integerArgumentCount == 6)) &&
            !it.receiverSlotProven && !it.compositeGroupProven
    }
}
