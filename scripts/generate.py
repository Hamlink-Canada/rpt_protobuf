"""Generate only the schemas used by registration and DNS. Run from any directory."""

import re
import subprocess
import sys
from pathlib import Path

import grpc_tools

root = Path(__file__).resolve().parents[1]
out = root / "src" / "rpt_protobuf"
include = Path(grpc_tools.__file__).parent / "_proto"
names = ["node", "dns_update", "auth_request"]
subprocess.run(
    [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"-I{root / 'protos'}",
        f"-I{include}",
        f"--python_out={out}",
        f"--pyi_out={out}",
        *[str(root / "protos" / f"{n}.proto") for n in names],
    ],
    check=True,
)
subprocess.run(
    [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"-I{root / 'protos'}",
        f"-I{include}",
        f"--grpc_python_out={out}",
        str(root / "protos/auth_request.proto"),
    ],
    check=True,
)
for path in out.glob("*_pb2*.py*"):
    text = re.sub(
        r"^import (\w+_pb2) as",
        r"from rpt_protobuf import \1 as",
        path.read_text(),
        flags=re.MULTILINE,
    )
    if path.suffix == ".py" and path.stem.endswith("_pb2"):
        text = text.replace(f"DESCRIPTOR, '{path.stem}'", f"DESCRIPTOR, 'rpt_protobuf.{path.stem}'")
    path.write_text(text)
