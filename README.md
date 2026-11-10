# Repeater protobuf definitions

This library defines the messages used by the repeater DNS directory and registration
services. Service images include the bindings they need, so operators do not need
to install or run this project separately. There is no runtime container or PyPI
release for this library.

If you are deploying a service, start with its own instructions:

- [DNS directory](https://github.com/Hamlink-Canada/dnsserver): serve node lookups.
- [HTTP registrar](https://github.com/Hamlink-Canada/pyHTTP-Register): accept HTTP registrations.
- [IAX registrar](https://github.com/Hamlink-Canada/pyIAX-Register): accept IAX registrations.

## Choosing compatible service versions

Each service follows this library’s `main` branch when building from source.
CI resolves that branch once per run so tests and image builds use the same revision.
Use versioned service images or image digests for deployments. There is no
need to regenerate bindings on a running service.

The DNS messages describe when a registration was issued and the node's ID, IPv4
address, port, lifetime, and originating server. The node details are nested inside
the update. Producers and consumers must use this shared format; the old flat DNS
messages are not supported by the updated services.

The credential lookup interface allows an authorized registrar to retrieve a node's
generated password. The registrar verifies the client's credentials locally; IAX
challenge handling stays in the IAX project. A production central credential server
is a separate, future project.

Credential lookup requires an authenticated, authorized service connection. Clients
use verified TLS with a service token or mutual TLS. The server must enforce which
credentials each registrar may retrieve and never include passwords in logs or
error messages. Registrar caches can delay password changes until their configured
TTL expires; see the service documentation when planning a rotation.

## Schema reference

| Source | Purpose |
| --- | --- |
| `protos/node.proto` | Shared node details, including registration lifetime in seconds. |
| `protos/dns_update.proto` | Timestamped registration update containing a nested node. |
| `protos/auth_request.proto` | `rpt.auth.v1.CredentialService.GetNodeCredential` request and response. |
| `protos/monitor_dstar.proto` | D-Star event definitions used by other projects. |

The current generator targets the node, DNS, and credential lookup schemas. Other
projects' schema sources remain in this repository and are maintained separately.
The existing nested DNS schema is the source of truth; legacy definitions from
consumer repositories do not belong here.

## Development

Use Python 3.13+ and uv:

```sh
uv sync --locked
make check test build
```

Python bindings and type stubs are committed in `src/rpt_protobuf/`. After changing
a supported schema, regenerate them with the pinned compiler:

```sh
./build_proto.sh
git diff -- src/rpt_protobuf
```

Review the schema and generated-code changes together. Running the generator again
should produce no further diff. CI checks generation reproducibility and runs the
Python 3.13 and 3.14 tests. Consuming services do not need a protobuf compiler.

The Python package requires `protobuf`; gRPC users also install the `grpc` extra.
For example, application code imports `dns_update` from
`rpt_protobuf.dns_update_pb2` and accesses `entry.node.id`, `entry.node.ipaddress`,
`entry.node.port`, `entry.node.ttl`, and `entry.node.server`.

The credential RPC takes a numeric node ID and returns its shared password. A server
implementation must return `NOT_FOUND` for an absent node and `UNAVAILABLE` for a
backend outage. Service tokens use `authorization: Bearer …` metadata. Generated
32-character ASCII base64url passwords fit the AllStarLink client's 79-character
limit and avoid its configuration delimiters.

Install from the `main` branch, or use the editable sibling checkout supported by the
service repositories while developing changes together. Refresh the sibling checkout when adopting changes to `main`; update lockfiles
when dependency metadata changes. Keep application code,
configuration, and authentication implementations in their service projects.

The [dependency ADR](docs/adr/0001-shared-schema-dependency.md) and
[authentication ADR](docs/adr/0002-local-authentication-with-credential-lookup.md)
record the reasons for these choices.

## License

[AGPL-3.0-or-later](LICENSE).
