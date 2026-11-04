public final class PreviewSceneModelTest {
    private static int checks;
    public static void main(String[] args) {
        int x = 2, y = 3;
        x = Math.max(1, x - 1);
        check(x == 1);
        x = Math.min(12, x + 1);
        check(x == 2);
        y = Math.max(1, y - 1);
        check(y == 2);
        y = Math.min(6, y + 1);
        check(y == 3);
        int gemX = 5, gemY = 2;
        check(!(x == gemX && y == gemY));
        x = gemX; y = gemY;
        check(x == gemX && y == gemY);
        System.out.println("PASS: " + checks + " preview-scene model checks");
    }
    private static void check(boolean value) {
        checks++;
        if (!value) throw new AssertionError("preview model check " + checks);
    }
}
