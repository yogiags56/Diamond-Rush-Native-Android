package com.diamondrush.legacy

object Build245RenderCallsiteProvenanceChecks {
    fun runAll() {
        check(LegacyRenderCallsiteProvenance.validate())
        check(LegacyRenderCallsiteProvenance.verifiedCallsites.size == 25)
        check(LegacyRenderCallsiteProvenance.verifiedCallsites.count { it.integerArgumentCount == 7 } == 16)
        check(LegacyRenderCallsiteProvenance.verifiedCallsites.count { it.integerArgumentCount == 6 } == 9)
        check(LegacyRenderCallsiteProvenance.verifiedCallsites.none { it.receiverSlotProven || it.compositeGroupProven })
    }
}
