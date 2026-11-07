# Roadmap through Build251

Fixed invariants: native Android port; 320×240 logical canvas; 320×178 gameplay viewport at y=31; 24×24 tile target; preserve original assets and proven bytecode behavior; unknown values remain opaque.

Completed foundations: Builds198–250 as documented in prior roadmap files. Build251 adds descriptor-aware JVM operand-slot contracts for all 25 render callsites.

Build251: 25/25 invocation descriptor contracts valid; six-int overload consumes 8 JVM slots including receiver, seven-int overload consumes 9. Three new tests cover both overloads and category-2 slots.

Next Build252: focused symbolic execution of straight-line bytecode slices with a whitelist of modeled opcodes; explicit TOP/UNKNOWN values; stack merges require compatible heights; unsupported opcodes poison only affected values. Validate invocation stack shape before attempting argument attribution. Do not promote values to draw commands unless every producer and branch merge is proven.

Still outstanding: full-room rasterization, Android Gradle/device runtime, screenshot parity, APK packaging.
