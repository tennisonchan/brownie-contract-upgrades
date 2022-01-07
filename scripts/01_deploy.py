from brownie import (
    Box,
    network,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)
from scripts.helpers import (
    should_publish_source,
    get_account,
    encode_function_data,
    GAS_LIMIT,
    upgrade_proxy,
)


def deploy_proxy_box():
    account = get_account()
    contract = Box.deploy(
        {"from": account}, publish_source=should_publish_source(network.show_active())
    )
    print(f"value: {contract.retrive()}")

    proxy_admin = ProxyAdmin.deploy(
        {"from": account}, publish_source=should_publish_source(network.show_active())
    )
    initializer = contract.store, 1
    contract_encoded_initializer_function = encode_function_data(initializer)

    proxy = TransparentUpgradeableProxy.deploy(
        contract.address,
        proxy_admin.address,
        contract_encoded_initializer_function,
        {"from": account, "gas_limit": GAS_LIMIT},
        publish_source=should_publish_source(network.show_active()),
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade to v2!")
    proxy_contract = Contract.from_abi(Box._name, proxy.address, Box.abi)
    tx_store = proxy_contract.store(2, {"from": account})
    tx_store.wait(1)
    print(proxy_contract.retrive())

    # AttributeError: Contract 'Box' object has no attribute 'increment'
    # print(f"increment: {contract.increment()}")

    ## Update to BoxV2
    box_v2 = BoxV2.deploy(
        {"from": account}, publish_source=should_publish_source(network.show_active())
    )
    upgrade_tx = upgrade_proxy(
        account,
        proxy,
        box_v2.address,
        proxy_admin,
    )
    upgrade_tx.wait(1)
    print(f"Proxy has been upgraded!")
    proxy_contract_v2 = Contract.from_abi(BoxV2._name, proxy.address, BoxV2.abi)
    tx_increment = proxy_contract_v2.increment({"from": account})
    tx_increment.wait(1)
    print(proxy_contract.retrive())

    return proxy_contract


def main():
    print(f"[network]: {network.show_active()}")
    deploy_proxy_box()
