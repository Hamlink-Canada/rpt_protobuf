# Follow protobuf main for service builds

Services declare `rpt_protobuf` from its `main` branch instead of a fixed commit,
as requested on 2026-11-10. CI resolves that branch once per workflow run and uses
the resulting revision for both Python test jobs and the image job; editable sibling
checkouts remain available for local development. This supersedes the fixed-revision
choice in decision 0001 and reduces manual dependency updates, while allowing later
builds of the same service revision to use newer protobuf code; deploy published
images by digest when exact artifact identity matters.
