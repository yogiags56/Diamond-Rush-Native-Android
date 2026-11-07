# Applying Build 273 to the existing GitHub repository

This source export is designed to replace the tracked working-tree contents of
the existing Build 60-era repository while preserving its Git history.

1. Clone the existing repository to a computer with Git installed.
2. Create a backup branch and a feature branch:
   ```bash
   git switch main
   git pull --ff-only
   git branch backup/pre-build-273
   git switch -c upgrade/build-273
   ```
   Replace `main` if the repository uses a different default branch.
3. Extract this ZIP and copy its contents over the cloned repository root.
   Preserve the clone's `.git` directory. Do not copy a `.git` directory from
   this export (none is included).
4. Review the staged change set and run tests:
   ```bash
   python -m pip install -r requirements-dev.txt
   python -m pytest -q
   git status --short
   git diff --check
   git diff --stat
   ```
5. Confirm that no original game JAR, proprietary game assets, credentials, or
   local machine files are staged.
6. Commit and push the feature branch:
   ```bash
   git add -A
   git commit -m "Advance Diamond Rush native port to Build 273"
   git push -u origin upgrade/build-273
   ```
7. Review the GitHub diff, then merge the pull request into the default branch.
   Tag the merged commit as `build-273`.

Do not force-push. The previous Build 60-era commits remain in history and can
still be checked out. The backup branch provides an additional rollback point.

The export intentionally omits the original commercial game JAR, extracted
sprite images/raw buffers, compiled class/JAR outputs, and prior-build ZIPs.
Some historical tests are therefore skipped in a clean GitHub checkout. See
`GITHUB_SOURCE_EXPORT_TEST_RESULTS.txt`.
