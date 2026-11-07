package com.diamondrush.legacy

/**
 * Build 233: exact static bundle-directory entry -> global f[] slot
 * assignments observed in i.b(I)V.
 *
 * The entryIndex is the resource-table index passed to the original
 * a(String, int, int, int) loader. It is not a sprite ID or gameplay label.
 * Offsets identify the loader callsites; the following aastore commits the
 * returned f object into the stated global array slot.
 */
data class LegacyBundleSpriteSlotBinding(
    val globalArraySlot: Int,
    val bundlePath: String,
    val entryIndex: Int,
    val loaderCallOffset: Int,
    val assignmentMethod: String = "i.b(I)V"
)

object LegacyBundleSpriteSlotCatalog {
    @JvmField
    val staticBindings: List<LegacyBundleSpriteSlotBinding> = listOf(
        LegacyBundleSpriteSlotBinding(10, "/mmv.f", 0, 145),
        LegacyBundleSpriteSlotBinding(46, "/mmv.f", 5, 178),
        LegacyBundleSpriteSlotBinding(55, "/mmv.f", 4, 258),
        LegacyBundleSpriteSlotBinding(18, "/ui.f", 3, 314),
        LegacyBundleSpriteSlotBinding(54, "/mmv.f", 1, 348),
        LegacyBundleSpriteSlotBinding(53, "/mmv.f", 2, 417),
        LegacyBundleSpriteSlotBinding(52, "/mmv.f", 3, 451),
        LegacyBundleSpriteSlotBinding(59, "/cm.f", 2, 513),
        LegacyBundleSpriteSlotBinding(17, "/ms.f", 0, 584),
        LegacyBundleSpriteSlotBinding(9, "/cm.f", 7, 621)
    )

    @JvmStatic
    fun bindingForSlot(globalArraySlot: Int): LegacyBundleSpriteSlotBinding? =
        staticBindings.firstOrNull { it.globalArraySlot == globalArraySlot }

    @JvmStatic
    fun bindingsForBundle(bundlePath: String): List<LegacyBundleSpriteSlotBinding> =
        staticBindings.filter { it.bundlePath == bundlePath }
}
