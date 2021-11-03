import json
import pytest

from web3 import (
    EthereumTesterProvider,
    Web3,
)

@pytest.fixture
def tester_provider():
    return EthereumTesterProvider()


@pytest.fixture
def eth_tester(tester_provider):
    return tester_provider.ethereum_tester


@pytest.fixture
def w3(tester_provider):
    return Web3(tester_provider)

@pytest.fixture
def deploy_address(eth_tester):
    return eth_tester.get_accounts()[0]

@pytest.fixture(params=[1, 1000])
def total_supply(request):
    return request.param

@pytest.fixture
def xyz_contract(eth_tester, deploy_address, w3, total_supply):
    with open("./build/contracts/XyzCoin.json", "r") as f:
        contract_json = json.load(f)

    abi = contract_json['abi']
    bytecode = contract_json['bytecode']

    XyzContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    # issue a transaction to deploy the contract.
    tx_hash = XyzContract.constructor(total_supply).transact({
        'from': deploy_address,
    })
    # wait for the transaction to be mined
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, 180)
    # instantiate and return an instance of our contract.
    return XyzContract(tx_receipt.contractAddress)

def test_total_supply(xyz_contract, total_supply):
    total_supply_under_test = xyz_contract.functions.totalSupply().call()
    assert total_supply_under_test == total_supply

def test_initial_balance(deploy_address, xyz_contract, total_supply):
    balance = xyz_contract.functions.balanceOf(deploy_address).call()
    assert balance == total_supply

def test_transfer_valid_amount(eth_tester, w3, deploy_address, xyz_contract):
    receiver_address = eth_tester.get_accounts()[1]
    initial_balance = xyz_contract.functions.balanceOf(receiver_address).call()
    assert initial_balance == 0
    amount = 1
    tx_hash = xyz_contract.functions.transfer(receiver_address, amount).transact({'from': deploy_address})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    balance = xyz_contract.functions.balanceOf(receiver_address).call()
    assert balance == amount

def test_transfer_invalid_amount(eth_tester, w3, deploy_address, xyz_contract, total_supply):
    receiver_address = eth_tester.get_accounts()[1]
    initial_balance = xyz_contract.functions.balanceOf(receiver_address).call()
    assert initial_balance == 0
    amount = total_supply + 1
    from eth_tester.exceptions import TransactionFailed
    with pytest.raises(TransactionFailed) as execinfo:
        tx_hash = xyz_contract.functions.transfer(receiver_address, amount).transact({'from': deploy_address})
    assert "transfer amount exceeds balance" in str(execinfo.value)
