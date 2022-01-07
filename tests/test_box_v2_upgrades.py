from brownie import (
    exceptions,
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
)
from scripts.helpers import get_account, encode_function_data, upgrade_proxy
import pytest


def test_can_proxy_upgrades():
    account = get_account()
    contract = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    contract_encode_data = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        contract.address, proxy_admin.address, contract_encode_data, {"from": account}
    )
    contract_v2 = BoxV2.deploy({"from": account})

    tx_upgrade = upgrade_proxy(
        account, proxy, contract_v2, proxy_admin, contract_encode_data
    )
    tx_upgrade.wait(1)

    proxy_contract = Contract.from_abi(
        contract_v2._name, proxy.address, contract_v2.abi
    )

    assert proxy_contract.retrive() == 0
    tx = proxy_contract.increment({"from": account})
    tx.wait(1)
    assert proxy_contract.retrive() == 1


def test_can_proxy_upgrade_revert():
    account = get_account()
    contract = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    contract_encode_data = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        contract.address, proxy_admin.address, contract_encode_data, {"from": account}
    )
    contract_v2 = BoxV2.deploy({"from": account})

    proxy_contract = Contract.from_abi(
        contract_v2._name, proxy.address, contract_v2.abi
    )

    with pytest.raises(exceptions.VirtualMachineError):
        proxy_contract.increment({"from": account})

    tx_upgrade = upgrade_proxy(
        account, proxy, contract_v2, proxy_admin, contract_encode_data
    )
    tx_upgrade.wait(1)

    assert proxy_contract.retrive() == 0
    proxy_contract.increment({"from": account})
    assert proxy_contract.retrive() == 1
