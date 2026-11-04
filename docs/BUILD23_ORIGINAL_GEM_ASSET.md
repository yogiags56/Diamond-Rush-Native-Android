# Build 23 — First original Diamond Rush artwork integrated

Recovered `icon.png` directly from the bundled original JAR:
- Dimensions: 46 x 48 pixels
- PNG palette-mode artwork with its original palette/transparency
- Artwork: original purple diamond gem icon

Integrated byte-for-byte as `res/drawable-nodpi/diamond_rush_gem.png`:
- Android application icon (`android:icon`)
- Menu header image
- Gem artwork in the interactive gameplay preview

The renderer disables bitmap filtering to retain the original pixel-art look.
The cave, player, collision, and level data remain preview placeholders.
This is the first confirmed original visual asset used by the Android UI.
No Android SDK/Gradle build or APK is claimed.
