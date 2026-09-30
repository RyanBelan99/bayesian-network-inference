# Bayesian Network Inference

Exact and approximate inference on discrete Bayesian networks, implemented from
scratch in Python. Written for CSC 242 (Introduction to AI) at the University of
Rochester.

Given a network described in the [XMLBIF](https://www.cs.cmu.edu/afs/cs/user/fgcozman/www/Research/InterchangeFormat/)
format and some observed evidence, it answers queries of the form
*P(query variable | evidence)*.

## Verified result

Query: **P(Burglary | JohnCalls = true, MaryCalls = true)** on the classic
AIMA "alarm" network. The exact answer from Russell & Norvig is **0.284**.

| Method | P(Burglary = true) |
|---|---|
| Exact — enumeration | **0.2842** |
| Rejection sampling (10⁴ samples) | ~0.23 – 0.28 |
| Likelihood weighting (10⁴ samples) | ~0.28 – 0.33 |
| Gibbs sampling (10³ samples) | ~0.28 – 0.30 |

The approximate samplers are stochastic, so their output varies run to run and
carries visible sampling noise; they converge toward the exact value as the
sample count grows.

## Run it

```bash
cd src

# Demo: all four methods on the alarm network
python3 main.py

# Exact inference, general CLI:  Enumerate.py <network.xml> <query> [<evidence-var> <value> ...]
python3 Enumerate.py aima-alarm.xml B J true M true

# Approximate inference:  Sampling.py <n> <network.xml> <method> <query> [<evidence-var> <value> ...]
#   method ∈ {rejection, weighted, gibbs}
python3 Sampling.py 10000 aima-alarm.xml rejection B J true M true
```

Requires only the Python 3 standard library.

## How it works

| File | Responsibility |
|---|---|
| `BayGraph.py` | Network data structure: nodes, CPTs, topological sort, conditional-distribution lookup, normalization |
| `XMLBIFParser.py` | Parses an XMLBIF file into a `BayGraph` |
| `Enumerate.py` | **Exact** inference by enumeration (`enumeration-ask` from AIMA) |
| `Sampling.py` | **Approximate** inference: rejection sampling, likelihood weighting, and Gibbs sampling (with a Markov-blanket sampler) |

## Attribution

- The assignment is from CSC 242 (Prof. George Ferguson, University of Rochester).
- The network files (`aima-alarm.xml`, `aima-wet-grass.xml`) and the XMLBIF format
  come from the course / the AIMA textbook.
- **All inference code** — the graph structure, XMLBIF parser, enumeration, and
  the three samplers — was written from scratch by me. (The course also shipped a
  separate Java framework for this assignment; none of it is used here.)

## Known limitations

- Rejection sampling is inefficient when evidence is unlikely (most samples are
  discarded) — this is inherent to the algorithm, and the comparison against the
  other methods is part of the point.
