package com.diamondrush.legacy

object Build242DynamicSpriteResourceOriginChecks {
    fun runAll() {
        val slot42 = LegacyDynamicSpriteResourceOriginCatalog.originForGlobalSlot(42)!!
        check(slot42.resourcePath == "/{aA}.f" && slot42.recordIndex == 2)
        val slot16 = LegacyDynamicSpriteResourceOriginCatalog.originForGlobalSlot(16)!!
        check(slot16.resourcePath == "/{aA}.f" && slot16.recordIndex == 1)
        val slot60 = LegacyDynamicSpriteResourceOriginCatalog.originForGlobalSlot(60)!!
        check(slot60.resourcePath == "/{aA}.f" && slot60.recordIndex == 0)

        val slot27 = LegacyDynamicSpriteResourceOriginCatalog.originForGlobalSlot(27)!!
        check(slot27.resourcePath == "/gen3.f")
        check(slot27.recordIndex == 34 && slot27.localRecordIndex == 4)
        check(slot27.lengthHeaderOffset == 37)

        val slot30 = LegacyDynamicSpriteResourceOriginCatalog.originForGlobalSlot(30)!!
        check(slot30.resourcePath == "/gen2.f")
        check(slot30.recordIndex == 23 && slot30.localRecordIndex == 3)
        check(slot30.lengthHeaderOffset == 29)

        val slot56 = LegacyDynamicSpriteResourceOriginCatalog.originForGlobalSlot(56)!!
        check(slot56.resourcePath == "/cm.f")
        check(slot56.recordIndex == 1 && slot56.lengthHeaderOffset == 13)
        check(slot56.condition.contains("aA==1-or-2"))

        check(LegacyDynamicSpriteResourceOriginCatalog.originForGlobalSlot(999) == null)
        check(LegacyDynamicSpriteResourceOriginCatalog.confirmedOrigins.size == 9)

        fun parseFixture(name: String) = javaClass.getResourceAsStream("/build242/$name")!!.use {
            LegacySpriteResourceBundleParser.parse(it.readBytes())
        }
        val parsed27 = parseFixture("slot27.bin")
        check(parsed27.sprites.size == 11 && parsed27.paletteCount == 1 && parsed27.colorsPerPalette == 9)
        check(parsed27.paletteFormat == 21781 && parsed27.pixelFormat == 5632 && parsed27.trailingBytes.isEmpty())
        val parsed30 = parseFixture("slot30.bin")
        check(parsed30.sprites.size == 11 && parsed30.paletteCount == 1 && parsed30.colorsPerPalette == 16)
        check(parsed30.paletteFormat == 21781 && parsed30.pixelFormat == 5632 && parsed30.trailingBytes.isEmpty())
        val parsed56 = parseFixture("slot56.bin")
        check(parsed56.sprites.size == 6 && parsed56.paletteCount == 3 && parsed56.colorsPerPalette == 15)
        check(parsed56.paletteFormat == 21781 && parsed56.pixelFormat == 5632 && parsed56.trailingBytes.isEmpty())
        println("BUILD242_DYNAMIC_DF03_FIXTURES_PARSED: f27=11 f30=11 f56=6")
        check(LegacyDynamicSpriteResourceOriginCatalog.canonicalCsv().lines().size == 11)
    }
}
