# Sprite animation state port — Build 10

Inspected `javap -c -p b` from the original JAR and added
`app/src/main/java/com/example/diamondrush/engine/SpriteAnimationState.java`.

## Bytecode behavior represented

- `setAnimation` mirrors original `b.a(int)`: changing animation resets frame,
  elapsed tick counter, and accumulated x/y offsets.
- `tick` mirrors original `b.b()`: negative animation indices do not advance;
  the frame duration comes from the sprite data provider; on expiry the frame
  advances and wraps to zero, clearing accumulated offsets.
- `accumulateFrameOffset` mirrors original `b.a()`: frame records are addressed
  as `(animationRecordOffsets[animation] + frame) * 5`; signed deltas are read
  from record bytes 2 and 3; transform bit 0 negates x and bit 1 negates y.

## Deliberate boundary

This is a state/timing port, not the image decoder or complete sprite renderer.
`SequenceData` must be backed by correctly decoded original `f` metadata before
real game assets can use it. Rendering overloads and parent-sprite chain drawing
remain unimplemented. The class is platform-neutral Java and has no Android
SDK dependency.

## Test

Compile and run the standalone test:

```sh
javac -d /tmp/dr_anim_test \
  app/src/main/java/com/example/diamondrush/engine/SpriteAnimationState.java \
  tools/tests/java/com/example/diamondrush/engine/SpriteAnimationStateTest.java
java -cp /tmp/dr_anim_test com.example.diamondrush.engine.SpriteAnimationStateTest
```

Result in this environment: `SpriteAnimationStateTest: 6 checks passed`.
The existing Python regression suite also passes 12 tests.
