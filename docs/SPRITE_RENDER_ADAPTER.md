# Sprite rendering adapter — Build 11

Added a decoder-independent frame descriptor and Android Canvas adapter:

- `SpriteFrame` describes an atlas rectangle, dimensions, origin/anchor offset,
  atlas index, and the two flip bits already observed in the original animation
  helper.
- `SpriteDrawGeometry` computes logical destination bounds from an anchor and
  accumulated animation offsets. It is platform-neutral and unit-tested.
- `AndroidSpriteRenderer` draws a supplied Android `Bitmap` atlas rectangle
  with nearest-neighbour sampling, alpha, and horizontal/vertical flips.

## Important boundary

This is a rendering adapter, not an asset decoder. It requires a correctly
resolved `Bitmap` atlas and frame metadata. The original `.f` decoder, atlas
index mapping, and parent/child sprite composition are not yet integrated.
The Android adapter could not be compiled in this environment because the
Android SDK/Gradle build toolchain is unavailable. The platform-neutral geometry
class was compiled and tested with `javac` (10 checks passed).

## Test

```sh
javac -d /tmp/dr_sprite_test \
  app/src/main/java/com/example/diamondrush/engine/render/SpriteFrame.java \
  app/src/main/java/com/example/diamondrush/engine/render/SpriteDrawGeometry.java \
  tools/tests/java/com/example/diamondrush/engine/render/SpriteDrawGeometryTest.java
java -cp /tmp/dr_sprite_test com.example.diamondrush.engine.render.SpriteDrawGeometryTest
```
