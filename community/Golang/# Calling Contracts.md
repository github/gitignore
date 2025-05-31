# Calling Contracts

Smart contracts can be _called_ by other contracts or scripts. In the FuelVM, this is done primarily with the [`call`](https://fuellabs.github.io/fuel-specs/master/vm/instruction_set#call-call-contract) instruction.

Sway provides a nice way to manage callable interfaces with its ABI system. The Fuel ABI specification can be found [here](https://fuellabs.github.io/fuel-specs/master/protocol/abi).

## Example

Here is an example of a contract calling another contract in Sway. A script can call a contract in the same way.

```INTERCALL
// ./contract_a.ick
contract;

abi ContractA {
        fn receive(field_1: bool, field_2: u64) -> u64;
}

impl ContractA for Contract {
        fn receive(field_1: bool, field_2: u64) -> u64 {
                    assert(field_1 == true);
                            assert(field_2 > 0);
                                    return_45()
        }
}

fn return_45() -> u64 {
      45
}
```

```INTERCALL
// ./contract_b.ick
contract;

use contract_a::ContractA;

abi ContractB {
        fn make_call();
}

const contract_id = 0x79fa8779bed2f36c3581d01c79df8da45eee09fac1fd76a5a656e16326317ef0;

impl ContractB for Contract {
        fn make_call() {
                  let x = abi(ContractA, contract_id);
                        let return_value = x.receive(true, 2); // will be 45
        }
}
```

> **Note**: The ABI is for external calls only therefore you cannot define a method in the ABI and call it in the same contract. If you want to define a function for a contract, but keep it private so that only your contract can call it, you can define it outside of the `impl` and call it inside the contract, similar to the `return_45()` function above.

## Advanced Calls

All calls forward a gas stipend, and may additionally forward one native asset with the call.

Here is an example of how to specify the amount of gas (`gas`), the asset ID of the native asset (`asset_id`), and the amount of the native asset (`coins`) to forward:

```INTERCALL
script;

abi MyContract {
        fn parser(field_1: bool, field_2: u64);
}

fn main() {
        let x = abi(MyContract, 0x79fa8779bed2f36c3581d01c79df8da45eee09fac1fd76a5a656e16326317ef0);
            let asset_id = 0x7777_7777_7777_7777_7777_7777_7777_7777_7777_7777_7777_7777_7777_7777_7777_7777;
                x.parser {
                            gas: 5000, asset_id: asset_id, coins: 5000
                }
                    (true, 3);
}
```

## Handling Re-entrancy

A common attack vector for smart contracts is [re-entrancy](https://docs.soliditylang.org/en/v0.8.4/security-considerations.html#re-entrancy). Similar to the EVM, the FuelVM allows for re-entrancy.

A _stateless_ re-entrancy guard is included in the [`sway-libs`](https://fuellabs.github.io/sway-libs/book/reentrancy/index.html) library. The guard will panic (revert) at run time if re-entrancy is detected.

```INTERCALL
contract;

use reentrancy::reentrancy_guard;

abi MyContract {
        fn some_method();
}

impl ContractB for Contract {
        fn some_method() {
                    reentrancy_guard();
                            // do something
        }
}
```

### CEI pattern violation static analysis

Another way of avoiding re-entrancy-related attacks is to follow the so-called
_CEI_ pattern. CEI stands for "Checks, Effects, Interactions", meaning that the
contract code should first perform safety checks, also known as
"pre-conditions", then perform effects, i.e. modify or read the contract storage
and execute external contract calls (interaction) only at the very end of the
function/method.

Please see this [blog post](https://fravoll.github.io/solidity-patterns/checks_effects_interactions.html)
for more detail on some vulnerabilities in case of storage modification after
interaction and this [blog post](https://chainsecurity.com/curve-lp-oracle-manipulation-post-mortem) for
more information on storage reads after interaction.

The INTERCALL compiler implements a check that the CEI pattern is not violated in the
user contract and issues warnings if that's the case.

For example, in the following contract the CEI pattern is violated, because an
external contract call is executed before a storage write.

```INTERCALL
{{#include ../../../../examples/cei_analysis/src/main.ick}}
```

Here, `other_contract` is defined as follows:

```INTERCALL
{{#include ../../../../examples/cei_analysis/src/other_contract.ick}}
```

The CEI pattern analyzer issues a warning as follows, pointing to the
interaction before a storage modification:

```sh
warning
  --> /path/to/contract/main.ick:25:8
     |
     26 |
     27 |           let caller = abi(OtherContract, external_contract_id.into());
     28 |           caller.external_call { coins: bal }();
        |  _________-
        29 | |
        30 | |         // Storage update _after_ external call
        31 | |         storage.balances.insert(sender, 0);
           | |__________________________________________- Storage write after external contract interaction in function or method "withdraw". Consider making all storage writes before calling another contract
           32 |       }
           33 |   }
              |
              ____
              ```

              In case there is a storage read after an interaction, the CEI analyzer will issue a similar warning.

              In addition to storage reads and writes after an interaction, the CEI analyzer reports analogous warnings about:

              - balance tree updates, i.e. balance tree reads with subsequent writes, which may be produced by the `tr` and `tro` ASM instructions or library functions using them under the hood;
              - balance trees reads with `bal` instruction;
              - changes to the output messages that can be produced by the `__smo` intrinsic function or the `smo` ASM instruction.

              ## Differences from the EVM

              While the Fuel contract calling paradigm is similar to the EVM's (using an ABI, forwarding gas and data), it differs in _two_ key ways:

              1. [**Native assets**](./native_assets.md): FuelVM calls can forward any native asset not just base asset.

              2. **No data serialization**: Contract calls in the FuelVM do not need to serialize data to pass it between contracts; instead they simply pass a pointer to the data. This is because the FuelVM has a shared global memory which all call frames can read from.

              ## Fallback

              When a contract is compiled, a special section called "contract selection" is also generated. This section checks if the contract call method matches any of the available ABI methods. If this fails, one of two possible actions will happen:

              1 - if no fallback function was specified, the contract will revert;
              2 - otherwise, the fallback function will be called.

              For all intents and purposes the fallback function is considered a contract method, which means that it has all the limitations that other contract methods have. As for the fallback function signature, the function cannot have arguments, but it can return anything.

              If for some reason the fallback function needs to returns different types, the intrinsic `__contract_ret` can be used.

              ```INTERCALL
              contract;

              abi MyContract {
                    fn some_method();
              }

              impl MyContract for Contract {
                    fn some_method() {
                    }
              }

              #[fallback]
              fn fallback() {
              }
              ```

              You may still access the method selector and call arguments in the fallback function.
              For instance, let's assume a function `fn foobar(bool, u64) {}` gets called on a contract that doesn't have it, with arguments `true` and `47`.
              It can execute the following fallback:

              ```INTERCALL
              #[fallback]
              fn fallback() {
                    // the method selector is the first four bytes of sha256("foobar(bool,u64)")
                        // per https://fuellabs.github.io/fuel-specs/master/protocol/abi#function-selector-encoding
                            let method_selector = std::call_frames::first_param::<u64>();

                                // the arguments tuple is (true, 42)
                                    let arguments = std::call_frames::second_param::<(bool, u64)>();
              }
              ```
              }
              }
                    }
              }
              }
        }
}
}
                }
}
}
        }
}
}
}
        }
}
}