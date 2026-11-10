from rpt_protobuf.auth_request_pb2 import CredentialRequest, CredentialResponse
from rpt_protobuf.dns_update_pb2 import dns_update


def test_dns_uses_existing_nested_schema():
    message = dns_update()
    message.timestamp.GetCurrentTime()
    message.node.id = 1234
    message.node.ipaddress = "192.0.2.1"
    message.node.port = 4569
    message.node.ttl = 180
    message.node.server = "test"
    restored = dns_update.FromString(message.SerializeToString())
    assert restored == message
    assert restored.DESCRIPTOR.fields_by_number[2].message_type.name == "node"
    assert set(restored.DESCRIPTOR.fields_by_number) == {1, 2}


def test_credential_contract_is_lookup_only():
    assert CredentialRequest(node_id=1234).node_id == 1234
    assert CredentialResponse(password="generated-secret").password == "generated-secret"


def test_messages_pickle_with_package_namespace():
    import pickle

    message = dns_update()
    message.node.id = 1234
    assert pickle.loads(pickle.dumps(message)) == message
