from web3 import Web3

def get_amount_out(amount_in, reserve_in, reserve_out, fee_rate=0.003):
    amount_in_with_fee = amount_in * int((1 - fee_rate) * 1000)
    numerator = amount_in_with_fee * reserve_out
    denominator = (reserve_in * 1000) + amount_in_with_fee
    return numerator // denominator

def get_reserves(pair):
    r0, r1, _ = pair.functions.getReserves().call()
    t0 = pair.functions.token0().call()
    t1 = pair.functions.token1().call()
    return int(r0), int(r1), t0, t1

def wei_to_eth(w3, amount):
    return w3.fromWei(amount, "ether")
