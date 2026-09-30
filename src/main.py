"""
Demo: inference on the classic AIMA "Burglary" alarm network.

Computes P(Burglary | JohnCalls = true, MaryCalls = true) four ways:
one exact method (enumeration) and three approximate samplers. The exact
answer is 0.284 (Russell & Norvig, AIMA); the samplers converge toward it.
"""
from XMLBIFParser import XMLBIFParser
from Enumerate import Enumerate
from Sampling import Sampling


def fmt(dist):
    return {k: round(v, 4) for k, v in dist.items()}


def main():
    net = XMLBIFParser().xmlparse("aima-alarm.xml")
    query, evidence = "B", {"J": "true", "M": "true"}

    exact = Enumerate().enumeration_ask(query, evidence, net)
    print(f"Exact (enumeration):        {fmt(exact)}")

    sampler = Sampling()
    print(f"Rejection sampling (1e4):   {fmt(sampler.rejSample(query, evidence, net, 10000))}")
    print(f"Likelihood weighting (1e4): {fmt(sampler.LikelihoodWeight(query, evidence, net, 10000))}")
    print(f"Gibbs sampling (1e3):       {fmt(sampler.gibbsSample(query, evidence, net, 1000))}")


if __name__ == "__main__":
    main()
