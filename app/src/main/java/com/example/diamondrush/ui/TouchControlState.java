package com.example.diamondrush.ui;

/**
 * Platform-neutral state model for the Diamond Rush touch HUD.
 * Android MotionEvent coordinates are mapped into these logical controls by
 * the view/controller layer; this class owns no Android dependencies.
 */
public final class TouchControlState {
    public static final int NONE = 0;
    public static final int LEFT = 1;
    public static final int RIGHT = 2;
    public static final int UP = 3;
    public static final int DOWN = 4;
    public static final int ACTION = 5;
    public static final int PAUSE = 6;

    private boolean left, right, up, down, action, pausePressed;

    public void setPressed(int control, boolean pressed) {
        switch (control) {
            case LEFT: left = pressed; break;
            case RIGHT: right = pressed; break;
            case UP: up = pressed; break;
            case DOWN: down = pressed; break;
            case ACTION: action = pressed; break;
            case PAUSE: pausePressed = pressed; break;
            case NONE: break;
            default: throw new IllegalArgumentException("unknown control: " + control);
        }
    }

    public boolean isPressed(int control) {
        switch (control) {
            case LEFT: return left;
            case RIGHT: return right;
            case UP: return up;
            case DOWN: return down;
            case ACTION: return action;
            case PAUSE: return pausePressed;
            case NONE: return false;
            default: throw new IllegalArgumentException("unknown control: " + control);
        }
    }

    /** Releases all held controls, e.g. when Android cancels a touch sequence. */
    public void releaseAll() {
        left = right = up = down = action = pausePressed = false;
    }

    /** Returns -1, 0, or 1; opposite directions cancel each other. */
    public int horizontalAxis() {
        return (right ? 1 : 0) - (left ? 1 : 0);
    }

    /** Returns -1, 0, or 1; up is negative, down is positive. */
    public int verticalAxis() {
        return (down ? 1 : 0) - (up ? 1 : 0);
    }
}
