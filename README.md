# Brownie Contract Upgrades

Showcasing how to use proxy, `TransparentUpgradeableProxy` to achieve upgrading the contracts

- Smart contracts are immutable but it can be "mutable" for upgrade or bug fixing
- 3 methods for upgrading:
  - Parameterize
  - Migration
  - Proxies

### Parameterization

- Cannot add new storage
- Cannot add new logic
- Simple but not flexible
- Who is the admin? than it'll be a centralized contract
- E.g. Contract registry
- Some argues we shouldn't do this https://blog.trailofbits.com/2018/09/05/contract-upgrade-anti-patterns/

## Migration

- Deploy a new contract and tell everyone "this is a new one now"
- Truly immutable
- Easy to audit
- lots of education
- Different address
- How contract migration works https://blog.trailofbits.com/2018/10/29/how-contract-migration-works/

### Proxies

- Use lots of low level functionality, like the `delegatecall`
- Delegatecall / Callcode and Libraries https://docs.soliditylang.org/en/v0.4.21/introduction-to-smart-contracts.html#delegatecall-callcode-and-libraries
- With the `fallback` function in Proxies contract, we can delegate our calls to a different contract

1. Implementation contract, has all the protocols. we launch a new implementation contract when we upgrade
2. Proxy contract, which points to the implementation contract
3. User, making calls to the proxy contract
4. Admin, who can upgrade the contract

## Potential Issues

- Storage clashes
  - Delegated function only storage value based on position, not by variable name
- Function selector clashes
  - The clashes of the functions with the same function selector in both implement contract and the proxy contract

### Transparent Proxy Pattern

- ProxyAdmin https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/transparent/ProxyAdmin.sol
- TransparentUpgradeableProxy https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/transparent/TransparentUpgradeableProxy.sol
- Admin cannot call implementation contract functions
- Admin can only call the functions that govern the upgrades in the proxy contract

### Universal Upgradable Proxies (UUPS)

- AdminOnly upgrade functions are in implementation contract
- Saving Gas
- Proxy contract is smaller

### Diamond Proxies, Multi-Facet Proxy

- https://eips.ethereum.org/EIPS/eip-2535
