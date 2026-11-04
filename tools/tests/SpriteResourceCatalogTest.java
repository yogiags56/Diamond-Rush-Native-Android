package com.example.diamondrush.engine;

public final class SpriteResourceCatalogTest {
    private static void check(boolean ok, String message) { if (!ok) throw new AssertionError(message); }
    public static void main(String[] args) {
        check(SpriteResourceCatalog.verifiedEntries().size() == 11, "entry count");
        check(SpriteResourceCatalog.groupsFor("cm.f", 2).length == 2, "cm section 2 groups");
        check(SpriteResourceCatalog.groupsFor("mmv.f", 5)[0] == 0, "mmv section 5 group");
        check(SpriteResourceCatalog.groupsFor("ui.f", 3)[0] == 0, "ui section 3 group");
        boolean rejected = false;
        try { SpriteResourceCatalog.groupsFor("snd.f", 0); } catch (IllegalArgumentException expected) { rejected = true; }
        check(rejected, "unverified audio section rejected");
        int[] groups = SpriteResourceCatalog.groupsFor("cm.f", 2);
        groups[0] = 99;
        check(SpriteResourceCatalog.groupsFor("cm.f", 2)[0] == 0, "groups defensive copy");
        System.out.println("SpriteResourceCatalogTest: 6 checks passed");
    }
}
