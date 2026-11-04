# Build 15 — Android-native menu prototype

Implemented the first real Android `Activity` menu screen using native Android
Views (`LinearLayout`, `TextView`, `Button`) and `GradientDrawable` surfaces.

Visual direction:
- deep stone/brown background
- warm gold outlines and highlights
- parchment-like light text
- centered Diamond Rush title treatment
- large touch-friendly menu rows

Current button actions are placeholders with Toast feedback. They do not yet
start gameplay, load levels, or persist settings. The original game logo art is
not yet integrated because the `.f` asset pipeline is still being traced.

Validation performed in this environment: source-level inspection only.
An Android SDK/Gradle build is not claimed here, and no APK is produced.
