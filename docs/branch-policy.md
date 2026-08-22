# Branch policy

`main` is the only long-lived branch in every repository.

- Protected, linear history, no force-push.
- The required check is the `course` job — that is, `kit check`.
- **No workflow writes to `main`.** Enforced by the org audit, not by
  convention: `contents: write`, `git push`, and the two common auto-commit
  actions are all a failure anywhere in the org. The rule exists because a
  `workflow_dispatch` job with write access once stood one click away from
  overwriting 156 committed branded worksheet PDFs with placeholders.

Work branches are `fix/…`, `feat/…` or `content/…`, deleted on merge, and none
should outlive 90 days.

## Branches to clean up

Three repositories carry stale branches, and one of them is worth understanding
rather than simply deleting:

- **`fle`** — six `phase4/*` branches whose tips predate the Quarto→Hugo
  migration and which share **no common ancestor** with `main`. `fle/main` was
  rebuilt from scratch, so the repository stores two unrelated histories. That
  is also most of why its `.git` is 136 MB. Anyone planning URL-affecting work
  there should know the history has already been orphaned once.
- **`efl`** — `migration/hugo-coder`, merged in substance, 45 behind.
- **`ressources`** — `add-prompt-docs`, 4 ahead and 26 behind.

None is deleted automatically. A branch with no common ancestor is a record of
something, and deleting it is a decision, not tidying.
