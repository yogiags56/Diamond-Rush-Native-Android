# Diamond Rush Native Android — Build268

Build268 corrects switch-table parsing in the cross-class abstract operand interpreter and adds conservative exception-handler state propagation using the original classfile exception table.

See:
- `docs/BUILD268_EXCEPTION_AWARE_OPERAND_INTERPRETER.md`
- `docs/ROADMAP_THROUGH_BUILD268.md`
- `research/build268_callsite_operand_results.csv`
- `research/build268_phi_provenance.csv`
- `research/build268_renderer_operand_states.csv`
- `research/build268_exception_state_transfers.csv`
- `BUILD268_TEST_RESULTS.txt`

Full test suite: 315 passed, 4 existing Pillow deprecation warnings.

This build is still reverse-engineering and engine research. It does not claim a completed Android application or playable APK.
