from solcx import compile_standard, install_solc

import json

install_solc("0.6.0")

with open("./web3_py_simple_storage/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    print(simple_storage_file)


# Compiled our solidity

complied_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(complied_sol, file)


# Gets bytecode - (object code that an interpreter converts into binary machine code)
bytecode = complied_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# Get the Abi - ()
abi = complied_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
