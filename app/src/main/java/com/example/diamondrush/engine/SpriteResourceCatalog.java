package com.example.diamondrush.engine;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Verified resource/section/group hand-offs observed in the original MIDlet loader. */
public final class SpriteResourceCatalog {
    public static final class Entry {
        public final String resource;
        public final int section;
        public final int[] groups;
        private Entry(String resource, int section, int... groups) {
            this.resource = resource;
            this.section = section;
            this.groups = groups.clone();
        }
    }

    private static final Entry[] ENTRIES = {
        new Entry("mmv.f", 0, 0), new Entry("mmv.f", 1, 0),
        new Entry("mmv.f", 2, 0), new Entry("mmv.f", 3, 0),
        new Entry("mmv.f", 4, 0), new Entry("mmv.f", 5, 0),
        new Entry("ui.f", 3, 0), new Entry("0.f", 3, 0),
        new Entry("cm.f", 2, 0, 1), new Entry("ms.f", 0, 0),
        new Entry("cm.f", 7, 0)
    };

    private SpriteResourceCatalog() { }

    public static List<Entry> verifiedEntries() {
        List<Entry> copy = new ArrayList<>();
        Collections.addAll(copy, ENTRIES);
        return Collections.unmodifiableList(copy);
    }

    /** Extracts a verified sprite payload from an already-loaded original .f container. */
    public static byte[] readPayload(String resource, int section, byte[] container) {
        for (Entry entry : ENTRIES) {
            if (entry.resource.equals(resource) && entry.section == section) {
                return ResourceSectionReader.readSection(container, section);
            }
        }
        throw new IllegalArgumentException("unverified sprite resource selection: " + resource + "#" + section);
    }

    public static int[] groupsFor(String resource, int section) {
        for (Entry entry : ENTRIES) {
            if (entry.resource.equals(resource) && entry.section == section) return entry.groups.clone();
        }
        throw new IllegalArgumentException("unverified sprite resource selection: " + resource + "#" + section);
    }
}
