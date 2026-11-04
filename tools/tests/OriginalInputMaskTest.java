import com.example.diamondrush.engine.OriginalInputMask;
import com.example.diamondrush.ui.DiamondRushKeyMap;

public final class OriginalInputMaskTest {
    private static int checks;
    public static void main(String[] args) {
        OriginalInputMask input = new OriginalInputMask(0);
        input.keyPressed(DiamondRushKeyMap.UP);
        input.keyPressed(DiamondRushKeyMap.RIGHT);
        check(input.snapshot() == (1 | 8));
        check(input.isDown(1));
        check(input.isDown(8));
        check(!input.isDown(2));

        input.keyReleased(DiamondRushKeyMap.UP);
        check(input.snapshot() == 8);
        input.keyReleased(DiamondRushKeyMap.RIGHT);
        check(input.snapshot() == 0);

        input.keyPressed(DiamondRushKeyMap.IGNORED_KEY);
        check(input.snapshot() == 0);

        OriginalInputMask state30 = new OriginalInputMask(30);
        state30.keyPressed(999); // original special fallback maps unknown key to 53
        check(state30.snapshot() == 32768);
        state30.keyReleased(999);
        check(state30.snapshot() == 0);

        input.keyPressed(48);
        input.keyPressed(49);
        check(input.snapshot() == (1024 | 2048));
        input.clear();
        check(input.snapshot() == 0);

        System.out.println("PASS: " + checks + " original input-mask checks");
    }
    private static void check(boolean ok) {
        checks++;
        if (!ok) throw new AssertionError("input mask mismatch at " + checks);
    }
}
