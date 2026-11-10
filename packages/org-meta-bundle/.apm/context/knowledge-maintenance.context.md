# Maintained knowledge and references

Give each topic one authoritative maintained home. Link to another owner's
material rather than creating competing definitions. Product context and component
implementation details can live in different repositories while remaining connected
through explicit references. Actual repository roles belong in local context.

## Move, distill and archive

A move changes the authoritative location; inspect callers and update affected
references. A distillation produces an accurate current document from source
material while preserving the historical evidence behind it. Archiving retains
material in its historical context instead of presenting it as current guidance.

Preserve reviewed meaning, rationale, uncertainty and source attribution during
these operations. Do not turn an observation or an unaccepted proposal into a
current decision simply because it was copied into a maintained document.

Update references directly rather than introducing a permanent transfer register,
forwarding stubs, automatic redirects or a global document-ID service solely for
the move. Verification artifacts used to perform a move can remain disposable.
Respect existing identity and routing mechanisms where the project already has
an explicit need for them. Moving packaged guidance does not update consumers:
retain usable local guidance until a published replacement is adopted.

## Current navigation and historical citations

Current references answer where maintained guidance lives. Use repository-qualified
links to its maintained location; avoid links that depend on a sibling checkout on
one developer's machine.

Historical citations answer exactly which content informed a decision. Identify
the repository, file path and commit revision, with an observation date where
useful. A date alone does not identify content. A release label can aid navigation,
but an unpublished design can still be cited by its exact commit.

For example, citation metadata could record:

```yaml
repository: example-org/catalog
path: docs/design/search.md
revision: <full-commit-sha>
observed_on: YYYY-MM-DD
```

This illustrates the information, not a required schema. Current navigation and
historical evidence can coexist: cite the revision relied on and link to today's
maintained guidance separately. Binding assignments and contracts still use exact
published baselines under the [specification rules](specifications.context.md);
a moving navigation link is not a substitute for that baseline.

## Staleness and availability

A target changing does not make a historical citation false, although conclusions
based on it may need reassessment. A renamed document needs a reference update
where current navigation should follow it. A new commit elsewhere in a repository
does not establish that the cited document changed.

A deleted or inaccessible revision means the evidence cannot currently be retrieved.
Preserve needed evidence through the agreed archive rather than assuming rewritten
source history will remain recoverable. Do not restore purged material or old Git
history merely to repair a reference.

Links convey location, not permission. Access to a referring repository does not
grant access to its target. Report unavailable evidence without inventing content,
access rights or an implemented retrieval capability.
