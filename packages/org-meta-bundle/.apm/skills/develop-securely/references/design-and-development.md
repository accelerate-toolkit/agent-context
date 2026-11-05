# Design and development

NCSC Code theme 1 addresses development methods, third-party composition, testing
and secure defaults. See [sources](sources.md) for the edition and scope.

For the current change, follow data and authority across its boundaries: who can
provide input, what they can influence, what becomes trusted, and what harm could
follow. Identify sensitive state and the assumptions supplied by other components.
Use this to choose relevant controls and acceptance observations, rather than
starting with a universal checklist.

Inspect dependency origin, privileges and update paths along with application
code. Prefer established mechanisms and understandable boundaries. A new dependency
or custom security mechanism needs a reason tied to the actual requirement and
maintenance constraints.

Exercise the consequential failures: unauthorized use, malformed input, unintended
disclosure, loss of integrity or unavailable dependencies, as applicable. Record
which assumptions were tested and which remain external. For domain-specific
mechanisms, consult or develop a local technical skill before recommending exact
settings. Preserve current contracts; return proposed boundary changes to their owner.

For a tiny library, a concise misuse example and focused tests may be sufficient.
For infrastructure, consider both the provisioned resources and the authority of
the provisioning process. Do not introduce a formal register solely to use this skill.
