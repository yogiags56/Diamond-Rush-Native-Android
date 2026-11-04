import com.example.diamondrush.ui.MidpInputAdapter;
import com.example.diamondrush.ui.TouchControlState;
import java.util.ArrayList;
import java.util.List;

public final class MidpInputAdapterTest {
    private static int checks;
    public static void main(String[] args) {
        final List<String> events = new ArrayList<>();
        MidpInputAdapter adapter = new MidpInputAdapter(new MidpInputAdapter.Sink() {
            public void keyPressed(int key) { events.add("+" + key); }
            public void keyReleased(int key) { events.add("-" + key); }
            public void pauseRequested() { events.add("PAUSE"); }
        });
        TouchControlState state = new TouchControlState();

        state.setPressed(TouchControlState.RIGHT, true);
        state.setPressed(TouchControlState.ACTION, true);
        adapter.update(state);
        check(events.size() == 2);
        check(events.contains("+" + MidpInputAdapter.KEY_RIGHT));
        check(events.contains("+" + MidpInputAdapter.KEY_FIRE));

        adapter.update(state);
        check(events.size() == 2); // held state must not repeat press events

        state.setPressed(TouchControlState.RIGHT, false);
        adapter.update(state);
        check(events.contains("-" + MidpInputAdapter.KEY_RIGHT));

        state.setPressed(TouchControlState.PAUSE, true);
        adapter.update(state);
        adapter.update(state);
        check(events.stream().filter("PAUSE"::equals).count() == 1);

        adapter.releaseAll();
        check(events.contains("-" + MidpInputAdapter.KEY_FIRE));
        System.out.println("PASS: " + checks + " MIDP input adapter checks");
    }
    private static void check(boolean value) {
        checks++;
        if (!value) throw new AssertionError("adapter check failed");
    }
}
