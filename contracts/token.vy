# @version 0.3.7

totalSupply: public(uint256)
balances: public(HashMap[address, uint256])
dummy: String[8]

event Transfer:
    sender: address
    receiver: address
    value: uint256

@external
def __init__(total_supply: uint256):
    assert total_supply > 0

    self.totalSupply = total_supply
    self.balances[msg.sender] = total_supply
    self.dummy = "dummy"


@external
def transfer(receiver: address, val: uint256) -> bool:
    assert self.balances[msg.sender] >= val

    self.balances[msg.sender] -= val
    self.balances[receiver] += val

    log Transfer(msg.sender, receiver, val)

    return True

@pure
@external
def external_func(str: String[32]) -> String[32]:
    return str

@pure
@internal
def internal_func(int: uint256) -> uint256:
    return int