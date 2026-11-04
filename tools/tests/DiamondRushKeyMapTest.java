import com.example.diamondrush.ui.DiamondRushKeyMap;

public final class DiamondRushKeyMapTest {
    private static int checks;
    public static void main(String[] args) {
        check(DiamondRushKeyMap.toInputBit(DiamondRushKeyMap.UP) == 1);
        check(DiamondRushKeyMap.toInputBit(DiamondRushKeyMap.DOWN) == 2);
        check(DiamondRushKeyMap.toInputBit(DiamondRushKeyMap.LEFT) == 4);
        check(DiamondRushKeyMap.toInputBit(DiamondRushKeyMap.RIGHT) == 8);
        check(DiamondRushKeyMap.toInputBit(DiamondRushKeyMap.FIRE) == 16);
        check(DiamondRushKeyMap.toInputBit(23) == 128);
        check(DiamondRushKeyMap.toInputBit(42) == 256);
        check(DiamondRushKeyMap.toInputBit(53) == 32768);
        check(DiamondRushKeyMap.toInputBit(57) == 524288);
        check(DiamondRushKeyMap.toInputBit(-10) == -10);
        check(DiamondRushKeyMap.toInputBit(999) == 0);
        System.out.println("PASS: " + checks + " original key-map checks");
    }
    private static void check(boolean ok) {
        checks++;
        if (!ok) throw new AssertionError("key map mismatch at check " + checks);
    }
}
