import numpy as np

def tropical_plus(a, b):
    return np.maximum(a, b)

def tropical_sum(a):
    return np.max(a)

# Needs vectorized implementation
def tropical_multi(a, b):
    if type(a) == int or type(b) == int:
        return a + b
    c = np.zeros([a.shape[0], b.shape[1]])
    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            h = np.array([ a[i,k] + b[k,j] for k in range(a.shape[1]) ] )
            c[i,j] = tropical_sum(h)
    return c


def tropical_identity(n):
    identity = np.full((n,n), -np.inf)
    np.fill_diagonal(identity, 0)
    return identity

def tropical_exp(a, n):
    b = tropical_identity(a.shape[0])
    for i in range(n):
        b = tropical_multi(b, a)
    return b

def maximum_weighted_cycles(log_ccm, k):
    mwpaths = tropical_exp(log_ccm.values, k)
    mwcycles = np.diag(mwpaths)
    return mwcycles
    
def get_max_arbitrage2(ccm, exchange_fee=0.002, max_path_length=None):
    if not max_path_length:
        max_path_length = ccm.shape[0]
    ccm - (ccm * exchange_fee)
    log_ccm = np.log(ccm.values)
    max_arb = 0
    max_cycle = []
    e_k = log_ccm.copy()
    for k in range(2,max_path_length+1):
        e_k = tropical_multi(e_k, log_ccm)
        mwc = np.diag(e_k)
        arb = np.max(mwc)
        if arb > max_arb:
            max_arb = arb
            max_cycle = np.argwhere(np.isclose(mwc, np.max(mwc)))
        print("Max-arb with path of length{0}: {1}".format(k, max_arb))
    return max_arb, max_cycle


def get_max_arbitrage(ccm, exchange_fee=0.002):
    ccm - (ccm * exchange_fee)
    log_ccm = np.log(ccm)
    max_arb = 0
    max_cycle = []
    for k in range(ccm.shape[0]):
        print("Exponentiating e to the {}th power...".format(k))
        mwc = maximum_weighted_cycles(log_ccm, k+1)
        arb = np.max(mwc)
        if arb > max_arb:
            max_arb = arb
            max_cycle = np.argwhere(np.isclose(mwc, np.max(mwc)))
    return max_arb, max_cycle
