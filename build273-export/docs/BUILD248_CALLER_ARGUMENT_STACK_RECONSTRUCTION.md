# Build 248 — Caller Argument Producer Reconstruction

## Scope

Build247 established the callee semantics for the 7-, 6-, and 4-integer overloads. Build248 revisits all 25 sprite draw callsites in `i.D()V` and classifies the bytecode producer evidence visible in the Build246 callsite slices.

## Results

`research/build248_caller_argument_provenance.csv` contains all 25 callsites, preserving the original bytecode excerpt and recording:
- explicit or unresolved receiver slot;
- visible constant producers;
- visible primitive field producers;
- visible arithmetic/array operations;
- unresolved composite group status.

The 13 explicitly identified receivers and 12 unresolved receivers agree with Build246. Producer evidence is partial: a local slice around an invoke is not a complete JVM operand-stack proof, especially across branches and local-variable merges. Consequently, every row is marked `PARTIAL_PRODUCER_EVIDENCE_NOT_FULL_STACK_PROOF`, and all composite groups remain `UNKNOWN`.

## Validation

Three focused Python tests validate 25 unique callsites, preservation of unresolved group values, and receiver-count consistency. Full regression results are recorded in `BUILD248_PYTEST_OUTPUT.txt`.

## Next

Build249 should implement a worklist-based operand-stack/local-variable provenance analysis over the exact method CFG, with explicit branch merge states and JVM category/type handling. Only a unique, consistent value at every predecessor may be promoted to a proven call argument. Do not infer group indices from constants alone.

## Limitations

No runtime room render, Android Gradle build, device execution, screenshot parity, or APK packaging is claimed.
