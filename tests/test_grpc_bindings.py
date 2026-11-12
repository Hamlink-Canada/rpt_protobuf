from rpt_protobuf.auth_request_pb2 import CredentialRequest, CredentialResponse
from rpt_protobuf.auth_request_pb2_grpc import CredentialServiceStub


def test_stub_binds_unary_method_and_serializers():
    observed = {}

    def rpc(request, **kwargs):
        observed["request"] = request
        observed["kwargs"] = kwargs
        return CredentialResponse(password="secret-from-test")

    class Channel:
        def unary_unary(self, path, **kwargs):
            observed["path"] = path
            observed["binding"] = kwargs
            return rpc

    stub = CredentialServiceStub(Channel())
    request = CredentialRequest(node_id=42)
    result = stub.GetNodeCredential(request, timeout=0.25)

    assert observed["path"] == "/rpt.auth.v1.CredentialService/GetNodeCredential"
    assert observed["binding"]["request_serializer"] is CredentialRequest.SerializeToString
    assert observed["binding"]["response_deserializer"] == CredentialResponse.FromString
    assert observed["request"] == request
    assert observed["kwargs"] == {"timeout": 0.25}
    assert result.password == "secret-from-test"


def test_credential_messages_round_trip_and_default_fields():
    request = CredentialRequest(node_id=2**63 - 1)
    assert CredentialRequest.FromString(request.SerializeToString()) == request
    assert CredentialRequest().node_id == 0

    response = CredentialResponse(password="")
    assert CredentialResponse.FromString(response.SerializeToString()) == response
