package com.example.diamondrush.engine;

import java.util.Arrays;

/** Reads the indexed little-endian section table used by Diamond Rush .f resources. */
public final class ResourceSectionReader {
    private static final int HEADER_BYTES = 1;
    private static final int ENTRY_BYTES = 8;

    private ResourceSectionReader() { }

    public static int sectionCount(byte[] container) {
        validateHeader(container);
        return container[0] & 0xff;
    }

    /** Returns an independent copy of the requested payload, not the whole container. */
    public static byte[] readSection(byte[] container, int sectionIndex) {
        int count = sectionCount(container);
        if (sectionIndex < 0 || sectionIndex >= count) {
            throw new IndexOutOfBoundsException("section " + sectionIndex + " of " + count);
        }
        int tableEnd = HEADER_BYTES + count * ENTRY_BYTES;
        int entry = HEADER_BYTES + sectionIndex * ENTRY_BYTES;
        long offset = u32le(container, entry);
        long length = u32le(container, entry + 4);
        long start = (long) tableEnd + offset;
        long end = start + length;
        if (length == 0 || start < tableEnd || end < start || end > container.length) {
            throw new IllegalArgumentException("invalid section bounds at index " + sectionIndex);
        }
        return Arrays.copyOfRange(container, (int) start, (int) end);
    }

    private static void validateHeader(byte[] data) {
        if (data == null || data.length < HEADER_BYTES) {
            throw new IllegalArgumentException("empty resource container");
        }
        int count = data[0] & 0xff;
        long tableEnd = HEADER_BYTES + (long) count * ENTRY_BYTES;
        if (tableEnd > data.length) {
            throw new IllegalArgumentException("truncated resource section table");
        }
    }

    private static long u32le(byte[] data, int offset) {
        return (data[offset] & 0xffL)
                | ((data[offset + 1] & 0xffL) << 8)
                | ((data[offset + 2] & 0xffL) << 16)
                | ((data[offset + 3] & 0xffL) << 24);
    }
}
