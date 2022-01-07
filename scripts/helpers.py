from brownie import accounts, network, config
import eth_utils

LOCAL_ENVIRONMENT = ["development", "ganache-local"]
FORK_ENVIRONMENT = ["mainnet-fork-dev", "mainnet-fork"]
GAS_LIMIT = 1000000


def should_publish_source(active_network):
    return config["networks"][active_network].get("verify", False)


def is_development(active_network):
    return active_network in LOCAL_ENVIRONMENT


def is_forked_local(active_network):
    return active_network in FORK_ENVIRONMENT


def get_account(index=0, id=None):
    if id:
        return accounts.load(id)
    if is_development(network.show_active()) or is_forked_local(network.show_active()):
        return accounts[index]
    return accounts.add(config["wallets"]["from_key"])


# initializer = contract.store, 1
def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


def upgrade_proxy(
    account, proxy, new_implementation_address, proxy_admin=None, initializer=None, *arg
):
    encode_function_call = (
        encode_function_data(initializer, *arg) if initializer else None
    )
    caller = proxy_admin if proxy_admin else proxy
    upgrade_method = "upgradeAndCall" if encode_function_call else "upgrade"

    param_1 = [proxy.address] if proxy_admin else []
    param_2 = [new_implementation_address]
    param_3 = [encode_function_call] if encode_function_call else []
    params = tuple(param_1 + param_2 + param_3 + [{"from": account}])

    print(params)
    return getattr(caller, upgrade_method)(*params)
