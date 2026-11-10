# Repeater protobuf definitions

The shared Python dependency for the repeater DNS directory and HTTP/IAX registrars.
Python 3.13+. Licensed AGPL-3.0-or-later. This project is not published to PyPI
and does not have a runtime Docker image.

## Schemas and ownership

`protos/dns_update.proto` is the DNS source of truth, importing `protos/node.proto`.
It contains a timestamp and a nested node with ID, address, port, lifetime in seconds,
and originating server. Consumers must use `entry.node.id`, `entry.node.ipaddress`,
`entry.node.port`, `entry.node.ttl`, and `entry.node.server`. The existing DNS/node
schema definitions were preserved; no legacy flat DNS definitions were imported.

`protos/auth_request.proto` defines `rpt.auth.v1.CredentialService.GetNodeCredential`.
An authorized registrar supplies a numeric node ID and receives its system-generated
shared password. The future credential server must authenticate service identities,
authorize lookup scope, return NOT_FOUND for absent nodes and UNAVAILABLE for backend
failures, and never log or reflect credentials into errors. Clients use TLS and either
mTLS or a service token in `authorization: Bearer …` metadata. IAX challenge-response
verification belongs entirely to the IAX registrar. HTTP compares supplied passwords
locally. Suggested generated credentials are 32-character ASCII base64url strings;
AllStarLink's client limits credentials to 79 characters and its configuration uses
colon and at-sign delimiters.

Other-project schemas, including `monitor_dstar.proto`, remain present and unchanged.
They are outside this cleanup; the generator deliberately targets only node, DNS,
and credential-lookup schemas. Do not migrate unrelated consumers as part of this work.

## Development

```sh
uv sync --locked
make check test build
./build_proto.sh
# Generated code must reproduce exactly:
git diff --exit-code -- src/rpt_protobuf
```

Bindings and type stubs are committed under `src/rpt_protobuf/`. Generation uses the
locked `grpcio-tools` version; runtime protobuf compatibility is declared in
`pyproject.toml`. The gRPC runtime is an optional `grpc` extra. No compiler is needed
by consuming services. Install normally from a full Git SHA, or use an editable
sibling checkout while developing coordinated changes.

See `docs/adr/` for the dependency and authentication decisions. Never add application
configuration, authentication implementations, or legacy DNS schema copies here.
