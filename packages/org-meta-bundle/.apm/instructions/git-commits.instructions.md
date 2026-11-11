---
description: Require Conventional Commit subjects, explanatory bodies, and relevant issue references.
applyTo: "**"
---

# Git Commit Messages

Use Conventional Commits to drive Semantic Versioning: `feat` advances minor,
`fix` or `perf` advances patch, and incompatible changes use `!` and a
`BREAKING CHANGE:` footer to advance major. Follow the shared release policy,
including its `0.x` rule. Classify by consumer impact: shipped skills and
instructions are functionality; `docs` is for explanatory documentation.

Every message needs a concise subject and a body explaining what changed and why.
Use this template, omitting optional parts that do not apply:

```text
<type>(<optional scope>)[optional !]: <description>

<What changed and why.>

Fixes #<completed issue>
Refs #<related or partially addressed issue>
BREAKING CHANGE: <incompatibility and required consumer action>
```

Close each issue fully resolved by the commit with `Fixes #<number>` in the
footer. Use `Refs` only for related or partial work, and state what remains for
partial work. For another repository, use `owner/repository#<number>`. Closing
keywords take effect when the commit reaches the default branch.

Append `[no ci]` to the subject for documentation-only or administrative changes
that do not affect shipped behavior, tests, dependencies, builds, workflows or
releases. Shipped skills and instructions count as behavior, regardless of file
extension. For mixed changes or uncertainty, run CI. Check the repository's
workflows first: the marker skips GitHub `push` and `pull_request` workflows,
including releases, and can leave required checks pending. Do not skip required
checks. See [GitHub's skip rules](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs).

Before suggesting or creating a commit, check its type, body, closing references
and whether CI should run.

After completing a coherent piece of work, suggest a suitable Conventional
Commit message and wait for human review before creating the commit, unless a
human explicitly asks you to commit.

When suggesting a commit message for review, show the complete subject, body,
and any issue footer together in one top-level `text` code block. Do not indent
the block or nest it inside a list or quotation. Put these exact lowercase
separator lines outside the block, with a blank line between each separator
and the block:

--- suggested commit message ---

```text
fix: correct test path

Resolve fixture paths relative to the test file so the suite can run from
any working directory.

Fixes #123
```

--- end of message ---

Put any explanation or verification notes before the suggested message. End
the response with the closing separator so the copyable message stays clearly
separated from commentary.
