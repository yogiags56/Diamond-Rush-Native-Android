# Build 25 — Verified sprite resource catalog

Build 25 turns the partial original MIDlet call trace into a small, explicit native-side registry. The registry contains only resource/section pairs observed being sent to the original `f` sprite loader, and records the group indices requested at those call sites.

## Registered selections

- `mmv.f`: sections 0–5, group 0 each
- `ui.f`: section 3, group 0
- `0.f`: section 3, group 0
- `cm.f`: section 2, groups 0 and 1; section 7, group 0
- `ms.f`: section 0, group 0

`SpriteResourceCatalog.readPayload` accepts the original resource filename, section number, and container bytes, then delegates extraction to `ResourceSectionReader`. `groupsFor` returns a defensive copy. Unknown pairs are rejected rather than guessed. This intentionally excludes `/cr.f` because its observed call site consumes raw bytes rather than invoking the sprite decoder; audio and other untraced resources are also excluded.

## Verification boundary

The catalog is a faithful call-site registry, not a semantic label map: it does not yet claim which entry is the player, a tile set, a menu element, or an effect. It also does not parse the remaining sprite metadata or create Android Bitmaps. The next stage is to decode a specific registered payload end-to-end and compare its dimensions/pixels against a reproducible reference.
