# Android multi-touch input bridge

`TouchInput` accepts hit-tested action masks per Android pointer ID. It tracks
how many pointers hold each bit, so lifting one finger cannot release a bit
that another finger still holds. `releaseAll()` is intended for focus loss,
activity pause, and `MotionEvent.ACTION_CANCEL`.

The bridge deliberately does not assign gameplay meaning to masks. The
original MIDP key mapping must be connected only after each key's use in the
original game states is traced. This avoids guessing that a key means the same
thing in menus, gameplay, dialogs, and password/name entry.

The standalone regression test is in `tools/tests/TouchInputLogicTest.java`.
It validates the reference-count transition rules independently of Android.
