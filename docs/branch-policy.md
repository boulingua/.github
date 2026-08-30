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

## Branches cleaned up — 2026-08-30

All eight are gone. `main` is now the only branch in every repository in the org.

The seven that shared **no common ancestor** with `main` were tagged before deletion,
because a branch with no merge base is a record of something and deleting it is a
decision, not tidying:

| repo | branch | commits | archive tag |
|---|---|---|---|
| `fle` | `phase4/kl06e` | 65 | `archive/phase4-kl06e` |
| `fle` | `phase4/kl07e` | 77 | `archive/phase4-kl07e` |
| `fle` | `phase4/kl07gm` | 29 | `archive/phase4-kl07gm` |
| `fle` | `phase4/kl08e` | 151 | `archive/phase4-kl08e` |
| `fle` | `phase4/kl09gm` | 41 | `archive/phase4-kl09gm` |
| `fle` | `phase4/kl10gm` | 53 | `archive/phase4-kl10gm` |
| `ressources` | `add-prompt-docs` | 4 | `archive/add-prompt-docs` |

Those tips hold the **pre-migration Quarto `.qmd` sources**. The unit content survived
into `main` as converted `.md` leaf bundles — spot-checked page by page — but the `.qmd`
files themselves exist nowhere else, which is why the tags were pushed and each verified
to resolve to the same SHA on the remote before anything was deleted.

`efl`'s `migration/hugo-coder` was merged in substance and 0 commits ahead of `main`; it
was deleted without a tag because nothing was only there.

## Protection — configured 2026-08-30

Written here since the policy was drafted and configured on **zero of 27 repositories**
until now: the API returned 404 for every one. A policy nobody applied is a document, and
this one had been describing a setting that did not exist.

Now set on all 27: linear history, no force-push, no branch deletion, and the `course`
job required on every repository that runs it. Admin enforcement is **on**, which means
`main` no longer accepts a direct push from anyone, including the author — work reaches it
through a pull request, and the battery has to be green first.

That is the policy as written. If the PR round-trip proves too heavy for a
single-author repository, the one thing to relax is admin enforcement, not the required
check:

```
gh api -X DELETE repos/boulingua/<repo>/branches/main/protection/enforce_admins
```
