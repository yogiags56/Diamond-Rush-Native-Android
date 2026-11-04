package com.example.diamondrush;

import android.util.SparseIntArray;
import android.view.MotionEvent;
import java.util.HashMap;
import java.util.Map;

/**
 * Multi-pointer input bridge. UI hit-testing supplies a bit mask for each
 * pointer; this class guarantees that one finger cannot release an action
 * still held by another finger.
 *
 * The masks deliberately have no gameplay meaning here. Map them to the
 * original MIDP key masks only after the original state-specific controls
 * have been traced.
 */
public final class TouchInput {
    public interface Listener { void onMaskChanged(int heldMask); }

    private final Listener listener;
    private final SparseIntArray pointerMasks = new SparseIntArray();
    private final Map<Integer, Integer> maskCounts = new HashMap<>();
    private int heldMask;

    public TouchInput(Listener listener) { this.listener = listener; }

    /** Update one pointer's currently hit-tested action mask. */
    public void setPointerMask(int pointerId, int newMask) {
        int oldMask = pointerMasks.get(pointerId, 0);
        if (oldMask == newMask) return;
        int changed = oldMask ^ newMask;
        for (int bit = 0; bit < 32; bit++) {
            int flag = 1 << bit;
            if ((changed & flag) == 0) continue;
            int count = maskCounts.containsKey(flag) ? maskCounts.get(flag) : 0;
            if ((newMask & flag) != 0) {
                count++;
                maskCounts.put(flag, count);
                heldMask |= flag;
            } else {
                count = Math.max(0, count - 1);
                if (count == 0) { maskCounts.remove(flag); heldMask &= ~flag; }
                else maskCounts.put(flag, count);
            }
        }
        if (newMask == 0) pointerMasks.delete(pointerId);
        else pointerMasks.put(pointerId, newMask);
        listener.onMaskChanged(heldMask);
    }

    public void releasePointer(int pointerId) { setPointerMask(pointerId, 0); }
    public void releaseAll() {
        if (heldMask == 0 && pointerMasks.size() == 0) return;
        pointerMasks.clear(); maskCounts.clear(); heldMask = 0;
        listener.onMaskChanged(0);
    }
    public int getHeldMask() { return heldMask; }

    /** Call when the view loses focus or receives ACTION_CANCEL. */
    public void onCancel() { releaseAll(); }

    /** Utility for hit-test code to locate a pointer in a MotionEvent. */
    public static int pointerId(MotionEvent event, int pointerIndex) {
        return event.getPointerId(pointerIndex);
    }
}
