# Development fake blueprint

A development fake is a small, runnable external system that a person can operate
and inspect while exercising the real application. Its UI should make three things
obvious: what state exists, what action can be taken, and what actually happened.
A protocol stub with a JSON dump alone does not provide this experience.

Use this blueprint when creating or reviewing a manually usable service fake.
Keep the same observable shape across languages; choose the repository's familiar
protocol libraries, web server, templates, storage and test tools. Server-rendered HTML with modest
JavaScript is sufficient. A frontend framework, shared UI package, Docker, SSE or
particular database is not required. For an explicitly headless test fixture,
retain the control, state, event and isolation semantics without building an
unrequested browser interface.

## Domain-neutral shape

The shared pattern is service behavior, scenario controls, readable state and an
event inspector. Derive entity names, actions, state fields and optional views from
the consumed service contract; the blueprint does not prescribe a business domain.
For example:

| External service | State and controls might expose | Optional domain view |
| --- | --- | --- |
| Object storage | Objects, revisions, conditional-write conflicts | Object contents |
| Payment processing | Synthetic transactions, settlement state, declined requests | Transaction history |
| Search | Indexed documents, query responses, indexing delays | Index contents |
| Job processing | Jobs, retries, completion and failure injection | Job output |
| Messaging | Queues, delivery attempts, acknowledgements | Captured messages |

These are alternatives, not capabilities every fake must implement. A fake may
have no users, accounts, messages, browser login or outgoing calls. Its service
protocol may be HTTP, RPC, a queue or another exchange; only the human inspector
necessarily needs a browser-facing surface.

## Runtime and boundary shape

Run the fake separately from the application under test. Keep its implementation
out of production binaries and deployment modules. Give each service a distinct
name and endpoint; `<service>4dev` is a useful naming convention, not a requirement.
Print the relevant service endpoints and inspector URLs on startup. A separate dashboard or landing
service is unnecessary when direct links suffice.

The fake provides four logical surfaces:

| Surface | Purpose |
| --- | --- |
| Service protocol | The actual exchange consumed by the application or client. |
| Test controls | Arrange external state, faults and reset through explicit operations. |
| Inspection | Read current state and bounded event history in machine-readable form. |
| Human interface | Operate the controls and inspect the same state and events. |

Routes such as `/__control`, `/__inspect` and `/healthz` are examples. Separate
these concerns from the simulated public contract; they need not be separate
servers. Manual and automated controls must act on the same model. Do not maintain
a cosmetic UI state independent of the service's behavior.

Keep application-owned logic, validation and persistence real. Fake controls change
external-system state; they do not seed the application's database or bypass its
public operations. Where a client is simulated, it uses actual protocol exchanges
and independently scoped credentials or sessions when applicable. Model only the
roles needed by the scenario; implementing one exchange does not imply support
for every capability of the service.

## Visual identity and page composition

Make the fake a polished developer tool, visually distinct from the product it
helps test. Use a persistent header with a short service name, one-letter or simple
symbol mark, concise role description, and a visible **FAKE · DEVELOPMENT** badge.
Use a matching favicon so several open service tabs are easy to distinguish.
Choose a different accent for each fake; pair colour with names and marks so
identity does not depend on colour alone. Do not impersonate the real provider's
branding or copy the production application's visual identity.

Use a quiet neutral background, white or subtly tinted cards, restrained borders,
consistent spacing and a readable system font. Reserve monospace for IDs, paths
and payloads. Keep primary actions visually prominent; secondary actions quieter;
reset/destructive controls clearly separated from ordinary scenario actions.
Avoid a large navigation sidebar, promotional artwork, dense dashboards or a raw
JSON wall as the main screen.

For a concrete starting point, use a spacing scale of 4/8/12/16/24/32 pixels,
roughly 14–16px body text, 24–28px page titles, 8–12px card radii, and 24–32px desktop
page padding. These are adjustable proportions, not acceptance thresholds. Prefer
comfortable controls and whitespace over fitting every field above the fold.
Use explicit surface/text colours or a deliberate dark theme; browser dark-mode
preferences must not accidentally make inputs, labels or status badges unreadable.

The shared page shape is:

```text
[ S ] service4dev    External service simulator    [ FAKE · DEVELOPMENT ]

Current state       Optional domain view                 Events
──────────────────────────────────────────────────────────────────────────
Current state:
  [ Primary scenario action / state controls                          ]
  [ Immediate action feedback                                         ]
  [ Global counters and active faults                                 ]
  [ ▸ Entity A — status and summary                                    ]
  [ ▸ Entity B — status and summary                                    ]
  [ ▸ Advanced fault controls                                         ]

Events:
  Live · connected                          [✓ Follow latest] [JSON]
  [ newest events, ~one third ] [ selected event details, ~two thirds   ]
  [ operation · status        ] [ direction, time, duration             ]
  [ operation · status        ] [ exchange → result / error / acknowledgement ]
```

Use one compact main page with **Current state** selected initially. **Events** is
a separate tab, not a continuously growing log below the controls. Add a domain
view such as **Job output** or **Object contents** only when it helps operate
and understand that service.
Use stable deep links to tabs. On narrow screens, stack event list and detail,
keep controls reachable, and wrap long IDs/URLs without horizontal page overflow.

## Current state and manual controls

Present global settings and counters separately from entity-specific state. Use
readable labels, status summaries and expandable entity rows; place raw JSON in
an optional details panel or export. Entity rows should expose the useful causal
state: queued work, stored revisions, completion state, expiry or emitted effects,
as appropriate. Do not force every domain into the same entity model.

Use stable synthetic identifiers. If an identifier or system-generated value can
be overridden for testing, label that capability explicitly as a test control.
Retain selected entities and entered values after errors. Group advanced fault controls separately
and keep them collapsed initially, while summarising active faults visibly so a
forgotten outage switch does not look like an unexplained application failure.
Label whether a fault affects one entity, the next call, or the whole service.

Every action acknowledges immediately and shows progress. Prevent duplicate
submission for that action while keeping the rest of the page responsive. Show
completion or failure beside the action, based on its actual result; do not display
success when only submission has occurred. Avoid full-page reloads for routine
control changes. Redirect to protocol screens when the simulated flow requires it.

Where useful, give domain artifacts or external effects a dedicated, readable
view. Choose fields appropriate to the service: object key and revision, job status
and output, transaction amount and outcome, or message destination and contents.
Raw source can be optional. Label simulated effects explicitly; displaying them
must not imply a real payment, notification or other external action occurred.
If a manual journey needs a sensitive synthetic value, expose it only through a
purposeful, scoped test view, not through general event logging.

## Events and live updates

Capture both incoming and outgoing exchanges where the fake participates in both.
Use stable event identities so selection survives insertion, reordering and polling.
An event should contain enough information to follow the exchange:

- Time, direction, operation or method, and sanitised target/path.
- Pending/completed state, protocol result, duration or transport failure.
- Redacted exchange fields: requests/responses, published messages/acknowledgements,
  or other protocol-specific details as applicable. Keep action summaries distinct from actual wire-level exchanges.

Bound history and payload sizes. A few hundred events is a reasonable starting
point; choose and document the limit. Show newest events first in the UI. Exclude
inspector polling/assets, health probes and control traffic from protocol history
so the observer does not generate its own noise. Protocol calls caused by controls
remain visible; control changes still refresh state and action feedback.

Follow latest is initially enabled. Selecting an older event pauses following;
re-enabling it selects the latest event. Preserve the selected event by ID, not
its list index. If it ages out of retained history, say so explicitly rather than
silently showing a different event. Update pending events when they complete.

Update without manual reloads, using SSE, polling, WebSockets or the simplest
suitable mechanism. Preserve dirty forms, focused inputs, expanded entity rows,
selected tabs and event selection during updates. Show disconnected/reconnecting
state; stale data must not masquerade as a live connection. Reconnect automatically
without replaying mutations or clearing scenario setup.

## Accessibility and safe inspection

Use semantic buttons, labels, forms and headings. Tabs need selected/focus state,
keyboard arrows and Home/End navigation. Provide visible focus, keyboard-operable
entity expansion, readable contrast and status text alongside colour. Announce
action results without moving focus unnecessarily or flooding assistive technology
with every incoming event.

Redact before storage/export/streaming, not only during rendering. Prefer explicit
allowlists for visible fields and redact unknown values by default, recursively.
Never log passwords, tokens, session cookies, authorization codes or unfiltered
headers, URLs and errors. Bound nested structures. Display external text safely;
do not insert provider HTML into the inspector. Purposeful synthetic-value views may
have a deliberate scoped exception, separate from general event logging.

Keep test controls in local or explicitly isolated development environments.
Apply origin/CSRF protections to browser mutations as appropriate, and do not
ship the inspector in the production service. Separate browser origins, sessions
and client credentials where those boundaries are part of the scenario. For
HTTPS-sensitive flows, use explicit local CA trust rather than disabling TLS
validation; document trust setup and removal without silently changing host trust.

## Lifecycle and repeatable use

First startup has no scenario data and is usable without a pre-seeded business
fixture. Required protocol/bootstrap configuration is distinct from scenario data.
Tests arrange only the required synthetic external state. Ordinary startup must
not unexpectedly erase a person's manual work. Define exactly what survives
restart, stop/down and reset, including application data, fake state, events,
captured effects, certificates and browser state. Do not assume resetting server
state clears browser cookies or storage.

Manual environments can be retained; automated runs use isolated names, ports,
storage and fixtures, with cleanup limited to their own resources. Failures retain
diagnostic evidence, with an explicit option to retain the failing isolated stack
when useful. Automated tests must never reset the manual environment.

Provide discoverable start, stop, reset, logs and test actions using repository
conventions. Document prerequisites, direct URLs, persistence, initial scenario
steps and limitations. State whether reset is per-fake or coordinated across the
stack so inconsistent partial resets are diagnosable.

## Observable acceptance checklist

Review the actual running UI in addition to protocol tests. Use synthetic data and
record executed versus unrun checks. At minimum, exercise the applicable cases:

- Open a clean fake: its identity and development status are unmistakable, Current
  state is useful, and the next manual action is clear without inspecting JSON.
- Arrange an entity manually and through test controls; both affect the same
  protocol-visible state. Complete a real application exchange through the fake.
- Trigger a delayed action, failure and retry: feedback is immediate, duplicate
  submission is prevented, and entered values and prior setup survive.
- Inspect incoming/outgoing exchanges, pending completion and redacted details.
  Select an older event while new events arrive; selection stays fixed until
  Follow latest is restored. Exercise history eviction and reconnect behavior.
- Edit a control while updates arrive: focus, unsaved changes and expanded rows
  survive. Disconnect observation and verify the stale/reconnecting indicator.
- Inspect representative synthetic captured effects, if supported, without
  exposing their sensitive content through the general event stream.
- Check desktop and narrow layouts, long text, empty and populated states, keyboard
  tabs/actions, focus visibility, contrast and the chosen colour-scheme behavior.
- Verify redaction in stored/exported/streamed data, not merely screenshots. Check
  that inspector and health traffic do not pollute the protocol history.
- Verify documented restart/reset semantics and two isolated test runs, including
  that their cleanup leaves the retained manual environment untouched.

Keep screenshots for human look-and-feel review and structured/text events for
exchange assertions. Screenshots alone do not establish protocol fidelity. Compare
selected fake behavior with the real dependency separately; report discrepancies
and unobserved behavior instead of treating successful fake tests as parity.
