# Source and build integrity

NCSC Code theme 2 concerns build access and traceable changes; theme 3.1 addresses
distribution integrity. See [sources](sources.md).

Trace the path from reviewed source and dependencies to the artifact actually
consumed. Identify identities, credentials and mutable inputs that can alter it.
Pay particular attention when untrusted contributions can influence privileged
jobs, caches, release metadata or deployment inputs.

Use the repository's established review, dependency and release conventions.
Check that permissions and secret exposure fit the job's purpose, and that evidence
can relate the released artifact to its inputs. Logging should support investigation
without exposing credentials or protected data.

Choose verification for the actual boundary: for example, demonstrate that a
contribution check cannot publish an artifact, or that a consumer verifies the
artifact it will execute. Configuration inspection and observed execution provide
different evidence; describe which was obtained.

Provider-specific CI permissions, cloud identities and signing mechanisms belong
in local or explicitly adopted specialist skills. Adding this guidance does not
authorize changing repository protections, credentials or deployment access.
