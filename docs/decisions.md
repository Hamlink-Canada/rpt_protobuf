# Current decisions

The `rpt_protobuf` repository owns shared schemas and generated bindings; consumers
do not copy schemas or generated code. Service builds follow this library's `main`
branch. CI resolves `main` once per workflow run so tests and image builds in that
run use the same revision. Separate builds can resolve newer commits, so deployments
should use a versioned service image or image digest when exact artifact identity is
needed. Editable sibling checkouts support coordinated local development.

Registrars authenticate node credentials locally after an authorized credential
lookup. The credential RPC contract lives in the shared schema; Central Auth owns
the server implementation and authorization policy.
