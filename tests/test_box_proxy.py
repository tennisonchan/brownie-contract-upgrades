from scripts.helpers import encode_function_data, get_account, encode_function_data
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_can_proxy_delegate_calls():
    account = get_account()
    contract = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    contract_encode_function_call = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        contract.address,
        proxy_admin.address,
        contract_encode_function_call,
        {"from": account},
    )

    proxy_contract = Contract.from_abi(Box._name, proxy.address, Box.abi)

    assert proxy_contract.retrive() == 0
    proxy_contract.store(123, {"from": account})
    assert proxy_contract.retrive() == 123
