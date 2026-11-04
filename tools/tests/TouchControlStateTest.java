import com.example.diamondrush.ui.TouchControlState;

public final class TouchControlStateTest {
    private static int passed;
    public static void main(String[] args) {
        TouchControlState s = new TouchControlState();
        check(s.horizontalAxis() == 0);
        s.setPressed(TouchControlState.LEFT, true);
        check(s.horizontalAxis() == -1);
        s.setPressed(TouchControlState.RIGHT, true);
        check(s.horizontalAxis() == 0);
        s.setPressed(TouchControlState.LEFT, false);
        check(s.horizontalAxis() == 1);
        s.setPressed(TouchControlState.UP, true);
        check(s.verticalAxis() == -1);
        s.setPressed(TouchControlState.ACTION, true);
        check(s.isPressed(TouchControlState.ACTION));
        s.releaseAll();
        check(s.horizontalAxis() == 0 && s.verticalAxis() == 0
                && !s.isPressed(TouchControlState.ACTION));
        System.out.println("PASS: " + passed + " touch control state checks");
    }
    private static void check(boolean ok) {
        passed++;
        if (!ok) throw new AssertionError("touch control state check failed");
    }
}
