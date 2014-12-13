from math import log, floor, sqrt

PRNG_A = 16807
PRNG_M = (1 << 31) - 1
PRNG_MAX_RAND = PRNG_M - 1

PRNG_DELTA = 0.5
PRNG_C     = 0.1

def gen_tau(S, K, delta):
    pivot = floor(K/S)
    return [S/K * 1/d for d in range(1, pivot)] \
            + [S/K * log(S/delta)] \
            + [0 for d in range(pivot, K)] 

def gen_rho(K):
    return [1/K] + [1/(d*(d-1)) for d in range(2, K+1)]

def gen_mu(K, delta, c):
    S = c * log(K/delta) * sqrt(K) 
    tau = gen_tau(S, K, delta)
    rho = gen_rho(K)
    normalizer = sum(rho) + sum(tau)
    return [(rho[d] + tau[d])/normalizer for d in range(K)]

def gen_rsd_cdf(K, delta, c):
    mu = gen_mu(K, delta, c)
    return [sum(mu[:d+1]) for d in range(K)]

# Tested
class PRNG(object):
    def __init__(self, params):
        K, delta, c = params
        self.K = K
        self.cdf = gen_rsd_cdf(K, delta, c)

    def set_seed(self, seed):
        self.seed = seed
        self.state = seed

    def get_next(self):
        self.state = PRNG_A * self.state % PRNG_M
        return self.state
    
    def get_state(self):
        return self.state

    def get_src_blocks(self, seed=None):
        if seed:
            self.state = seed

        blockseed = self.state
        d = self.sample_d()
        have = 0
        nums = set()
        while have < d:
            num = self.get_next() % self.K
            if num not in nums:
                nums.add(num)
                have += 1
        return blockseed, d, nums

    # Samples from the CDF of mu
    def sample_d(self):
        p = self.get_next() / PRNG_MAX_RAND
        for ix, v in enumerate(self.cdf):
            if v > p:
                return ix + 1
        return ix + 1
