import com.example.diamondrush.engine.ResourceSectionReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;

public final class ResourceSectionReaderTest {
    private static void check(boolean value, String message) {
        if (!value) throw new AssertionError(message);
    }
    private static void rejects(Runnable action, String message) {
        try { action.run(); } catch (RuntimeException expected) { return; }
        throw new AssertionError("expected rejection: " + message);
    }
    public static void main(String[] args) throws Exception {
        byte[] fixture = new byte[] {2, 0,0,0,0, 2,0,0,0, 2,0,0,0, 3,0,0,0,
                10,11,20,21,22};
        check(ResourceSectionReader.sectionCount(fixture) == 2, "section count");
        check(Arrays.equals(ResourceSectionReader.readSection(fixture, 0), new byte[]{10,11}), "first section");
        check(Arrays.equals(ResourceSectionReader.readSection(fixture, 1), new byte[]{20,21,22}), "second section");
        byte[] copy = ResourceSectionReader.readSection(fixture, 0); copy[0] = 0;
        check(fixture[17] == 10, "payload must be copied");
        rejects(() -> ResourceSectionReader.readSection(fixture, -1), "negative index");
        rejects(() -> ResourceSectionReader.readSection(fixture, 2), "past final index");
        rejects(() -> ResourceSectionReader.sectionCount(new byte[0]), "empty container");
        rejects(() -> ResourceSectionReader.sectionCount(new byte[]{2,0}), "truncated table");
        byte[] badBounds = fixture.clone(); badBounds[5] = (byte) 0xff;
        rejects(() -> ResourceSectionReader.readSection(badBounds, 0), "out-of-range payload");
        int verified = 0;
        for (String name : args) {
            byte[] bytes = Files.readAllBytes(Paths.get(name));
            int n = ResourceSectionReader.sectionCount(bytes);
            for (int i = 0; i < n; i++) {
                byte[] payload = ResourceSectionReader.readSection(bytes, i);
                check(payload.length > 0, name + " section " + i + " empty");
                verified++;
            }
        }
        System.out.println("PASS: 8 behavioral checks; " + verified + " real sections read from source JAR containers");
    }
}
