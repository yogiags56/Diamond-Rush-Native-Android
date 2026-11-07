# GitHub repository maintenance — Build 273

## Upgrade policy

Build 273 is the current source checkpoint. Update the existing repository's default branch with a normal forward commit/merge. Do not force-push or delete the Build 60-era history. Tag the checkpoint as `build-273` after the update is verified.

## Public repository contents

Keep authored Kotlin/Python source, tests, documentation, and text/CSV evidence. Do not add the original game JAR, proprietary extracted assets, sprite PNG/RGBA previews, compiled `.class`/`.jar` outputs, or bundled prior-build ZIP archives unless redistribution rights have been confirmed. These are intentionally excluded from this source export and covered by `.gitignore`.

## Suggested upload sequence

1. Clone the existing GitHub repository and create a branch such as `upgrade/build-273`.
2. Back up the current default branch/tag before replacing tracked files.
3. Copy this source-export tree into the clone, preserving `.git/` and existing Git history.
4. Run `python -m pip install -r requirements-dev.txt` and `python -m pytest -q`.
5. Review `git status`, `git diff --stat`, and `git diff --check`; confirm no original game binaries or credentials are staged.
6. Commit with message `Advance Diamond Rush native port to Build 273`.
7. Push the branch, inspect the GitHub diff, then merge it into the existing default branch.
8. Create tag `build-273` on the merged commit.

Do not use `git push --force` for this upgrade. The original Build 60-era commits should remain in history.

## Current technical limitation

This is not yet a complete Gradle Android application. The next milestone is Build 274 (composite group and renderer argument binding), followed by geometry/transform proof and first-room raster validation.
