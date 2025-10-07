def get_reserves(pair_contract):
    r0, r1, _ = pair_contract.functions.getReserves().call()
    t0 = pair_contract.functions.token0().call()
    t1 = pair_contract.functions.token1().call()
    return int(r0), int(r1), t0, t1

def get_amount_out(amount_in, reserve_in, reserve_out, fee_rate):
    fee_multiplier = int((1 - fee_rate) * 1000)
    amount_in_with_fee = amount_in * fee_multiplier
    numerator = amount_in_with_fee * reserve_out
    denominator = (reserve_in * 1000) + amount_in_with_fee
    return numerator // denominator

def wei_to_eth(w3, wei_amount):
    return w3.fromWei(wei_amount, "ether")
