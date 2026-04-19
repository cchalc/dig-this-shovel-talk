# Critical Analysis: Deep Reinforcement Learning for FSMVRP vs. ShovelSense Automated Truck Diversion

**Paper:** Deep Reinforcement Learning for Solving the Fleet Size and Mix Vehicle Routing Problem
**Authors:** Pengfu Wan, Jiawei Chen, Gangyan Xu (Hong Kong Polytechnic University)
**Source:** arXiv:2512.24251v1, December 2025
**Analysis Date:** April 2026

---

## 1. Paper Summary

### 1.1 Problem Definition

The paper addresses the **Fleet Size and Mix Vehicle Routing Problem (FSMVRP)**, a variant of the classical Vehicle Routing Problem (VRP) that requires simultaneous optimization of:

1. **Fleet composition** - selecting which vehicles from a heterogeneous pool to deploy
2. **Route planning** - determining optimal routes for selected vehicles

Each vehicle type is characterized by:
- Unique capacity (Q^k)
- Fixed cost per vehicle used (f^k)
- Variable cost per unit distance (c^k)

### 1.2 Key Contributions

1. **MDP Formulation** - Models FSMVRP as a Markov Decision Process capturing both fleet composition and routing decisions sequentially

2. **FRIPN Architecture** - Novel "Fleet-and-Route Integrated Policy Network" using:
   - Transformer-based encoder-decoder structure
   - Multi-head attention (MHA) mechanisms
   - Specialized input embeddings for heterogeneous decision variables

3. **Remaining Graph Embedding** - Novel embedding that captures unvisited customer demand to guide vehicle deployment decisions

4. **Policy Training** - REINFORCE-based algorithm with shared baseline for stable training

### 1.3 Results

| Problem Scale | DRL vs Best Heuristic | Runtime Advantage |
|---------------|----------------------|-------------------|
| 20 nodes | +1.74% cost | ~1800x faster |
| 50 nodes | -2.83% cost | ~1400x faster |
| 75 nodes | -7.45% cost | ~1200x faster |
| 100 nodes | -8.80% cost | ~700x faster |
| 200-1000 nodes | Superior | Consistent seconds |

- Benchmark dataset: 1.10% average gap from best-known algorithms
- All solutions generated within 1-3 seconds

---

## 2. Relevance to ShovelSense Technology

### 2.1 Problem Domain Alignment

| Aspect | FSMVRP Paper | ShovelSense Application |
|--------|-------------|------------------------|
| **Decision Type** | Route to which customer | Route truck to crusher/stockpile/waste |
| **Fleet** | Heterogeneous vehicles with varying capacities | Mining trucks (typically homogeneous within fleet) |
| **Optimization Goal** | Minimize total cost (fixed + variable) | Maximize ore recovery value, minimize dilution |
| **Decision Timing** | Offline/batch planning | Real-time, per-truck basis |
| **Cost Structure** | Distance-based variable costs | Value-based (ore grade differentials) |
| **Constraints** | Capacity, visit-once | Destination capacity, processing constraints |

### 2.2 Areas of Support

**The FSMVRP research supports ShovelSense in the following ways:**

1. **Computational Feasibility** - Demonstrates that DRL can solve routing decisions in seconds, validating real-time automated truck routing is computationally feasible

2. **Heterogeneous Decision Variables** - The paper's approach to handling mixed decision types (fleet selection + routing) is analogous to ShovelSense handling grade classification + destination assignment

3. **Scalability** - Shows DRL maintains performance advantages at larger scales (100+ nodes), relevant for large mining operations with many active trucks

4. **Generalization** - Pre-trained policies generalize to new instances without retraining, supporting ShovelSense's need to adapt to changing ore body conditions

### 2.3 Key Differences and Gaps

**The paper does NOT address several aspects critical to ShovelSense:**

1. **Real-Time Dynamic Decisions** - FSMVRP assumes static, known customer demands. ShovelSense operates with:
   - Uncertain grade measurements (XRF has measurement error)
   - Dynamic grade boundaries based on plant conditions
   - Continuously changing truck positions

2. **Single-Decision vs Multi-Step** - ShovelSense makes one binary/categorical decision per truck at loading. FSMVRP builds complete multi-stop routes.

3. **Value Maximization vs Cost Minimization** - Mining optimization is about maximizing recovered value (NSR), not minimizing distance costs

4. **No Grade Uncertainty Modeling** - The paper assumes deterministic customer demands. XRF grade estimates have:
   - Measurement noise
   - Sampling bias (surface vs volumetric grade)
   - Calibration drift

---

## 3. Critical Analysis of ShovelSense Claims

### 3.1 The 11% Diversion Rate Claim

**ShovelSense Claims:** 11% of trucks (697/6,270) were diverted in 80-day case study

**Analysis in Light of FSMVRP Research:**

| Consideration | Assessment |
|--------------|------------|
| **Statistical Significance** | 697 diversions is a meaningful sample size for demonstrating capability |
| **Optimization vs Detection** | ShovelSense performs grade-based classification, NOT route optimization as in FSMVRP |
| **Benchmark Comparison** | No comparison to optimal or near-optimal baseline provided |

**Concern:** The 11% figure represents detection of grade misclassification, not optimization improvement. The paper provides no evidence that:
- This is optimal (could it be 15%? 8%?)
- The classification cutoffs themselves are optimized
- There is no systematic bias in the XRF measurements

### 3.2 The $2M+ Revenue Claim

**ShovelSense Claims:** Additional revenue exceeding $2M USD from ore recovery

**Critical Questions Not Addressed:**

1. **Verification Method** - How was the diverted material's actual grade verified post-processing?

2. **False Positive Cost** - What is the cost of incorrectly diverting waste to crusher (dilution)?

3. **Opportunity Cost** - What is the cost of delayed truck cycles due to longer routes to alternate destinations?

4. **Net Value** - Is $2M gross or net of:
   - Additional processing costs for recovered ore
   - Capital/operating cost of ShovelSense system
   - Longer haul cycles

**Relevance of FSMVRP Research:** The FSMVRP paper explicitly models both fixed and variable costs. ShovelSense reporting lacks this rigor - only benefits are quantified, not costs.

### 3.3 Integration with Fleet Management

**ShovelSense Claims:** API integration with major FMS vendors (Caterpillar, Modular Mining, Wenco)

**Gap Identified:** The FSMVRP research demonstrates that optimal fleet routing requires:
- Global view of all vehicle states
- Capacity planning across the fleet
- Dynamic re-optimization

**ShovelSense appears to operate as a local decision system:**
- Each truck classified independently at point of loading
- No evidence of fleet-wide optimization
- No consideration of crusher/stockpile queue states
- No re-routing capability post-departure

This is a fundamentally simpler problem than FSMVRP, but also potentially suboptimal.

---

## 4. Gaps and Concerns

### 4.1 Methodological Gaps in ShovelSense

| Gap | Description | Impact |
|-----|-------------|--------|
| **No Baseline Comparison** | No comparison to rule-based or optimized alternatives | Cannot assess relative performance |
| **Single Site Study** | Only one copper-porphyry deposit in South America | Limited generalizability |
| **No Confidence Intervals** | Point estimates only for diversion rates and revenue | Cannot assess statistical reliability |
| **No A/B Testing** | No controlled comparison with/without system | Cannot isolate system effect from confounders |
| **No Long-term Performance** | 80 days is insufficient to assess calibration drift, seasonal effects | Unknown sustained performance |

### 4.2 Technical Concerns

**XRF Measurement Limitations:**
- Surface measurement vs volumetric grade (bucket interior not measured)
- Element-specific detection limits
- Matrix effects from varying mineralogy
- Sample representativeness of bucket contents

**Decision Boundary Sensitivity:**
- Binary ore/waste cutoffs are discontinuous
- Small measurement errors near cutoff cause large classification changes
- No evidence of probabilistic or fuzzy classification

### 4.3 Missing Optimization Layer

**Based on FSMVRP research, ShovelSense would benefit from:**

1. **Dynamic Cutoff Optimization** - Adjusting ore/waste thresholds based on:
   - Plant feed grade targets
   - Stockpile inventory levels
   - Processing capacity constraints

2. **Fleet-Level Coordination** - Considering:
   - Crusher queue lengths
   - Truck cycle time impacts
   - Blending requirements

3. **Uncertainty-Aware Decisions** - Using probabilistic classification:
   - Expected value calculations
   - Risk-adjusted routing
   - Information value assessment

---

## 5. Academic Rigor Assessment

### 5.1 FSMVRP Paper (arXiv:2512.24251)

| Criterion | Rating | Notes |
|-----------|--------|-------|
| **Methodology** | Strong | Formal MDP formulation, clear architecture |
| **Experiments** | Strong | Multiple baselines, benchmark validation |
| **Reproducibility** | Excellent | Code available on GitHub |
| **Limitations Acknowledged** | Adequate | Notes differences from benchmark settings |
| **Statistical Rigor** | Good | Multiple instance testing, consistent metrics |

**Overall: 8/10** - Solid academic contribution with reproducible results

### 5.2 ShovelSense White Paper (August 2022)

| Criterion | Rating | Notes |
|-----------|--------|-------|
| **Methodology** | Weak | No experimental design described |
| **Experiments** | Weak | Single case study, no controls |
| **Reproducibility** | Poor | Proprietary system, no technical details |
| **Limitations Acknowledged** | None | No discussion of limitations |
| **Statistical Rigor** | Poor | Point estimates only, no uncertainty |

**Overall: 3/10** - Marketing document, not academic research

---

## 6. Applicability Assessment

### 6.1 Can FSMVRP Methods Improve ShovelSense?

**Potentially Yes, But Requires Reformulation:**

The core insight from FSMVRP - using DRL for sequential decision-making with heterogeneous objectives - could enhance ShovelSense by:

1. **Learning Optimal Cutoffs** - Train policy to learn grade thresholds that maximize net value across varying conditions

2. **Fleet-Aware Routing** - Expand decision space to include queue states and alternative destinations

3. **Multi-Objective Optimization** - Balance ore recovery, dilution reduction, and cycle time

**However, ShovelSense's Current Problem is Simpler:**
- Single-step classification (not multi-step routing)
- Independent truck decisions (not fleet-wide optimization)
- Pre-defined cutoffs (not learned policies)

### 6.2 Recommended Research Directions

1. **Benchmark ShovelSense Against Optimized Baselines** - Compare to rule-based systems, manual decisions, and theoretically optimal classification

2. **Quantify Uncertainty** - Publish XRF measurement accuracy, false positive/negative rates

3. **Economic Analysis** - Full cost-benefit including capital, operating, and opportunity costs

4. **Multi-Site Validation** - Demonstrate performance across diverse ore types and operations

5. **Fleet Optimization Integration** - Explore DRL-based fleet-wide routing as in FSMVRP

---

## 7. Conclusion

The FSMVRP paper represents rigorous academic research demonstrating DRL's potential for real-time fleet optimization. While computationally impressive, it addresses a different problem than ShovelSense's grade-based truck routing.

**Key Findings:**

1. **DRL is viable for real-time mining decisions** - The computational efficiency demonstrated (seconds for 100+ node problems) validates that AI-driven truck routing is feasible

2. **ShovelSense solves a simpler problem** - Single-step classification vs multi-step routing means FSMVRP methods are not directly applicable but offer architectural insights

3. **ShovelSense claims lack academic rigor** - The 11% diversion rate and $2M revenue claims are unverified, lack statistical analysis, and have no baseline comparison

4. **Integration opportunity exists** - Combining ShovelSense's real-time grade sensing with fleet-level optimization (inspired by FSMVRP) could yield superior results

**Bottom Line:** The FSMVRP research neither validates nor invalidates ShovelSense's claims. However, it does highlight the sophistication gap between academic optimization research and ShovelSense's reported methodology. ShovelSense would benefit from adopting the experimental rigor demonstrated in this paper.

---

## References

1. Wan, P., Chen, J., & Xu, G. (2025). Deep Reinforcement Learning for Solving the Fleet Size and Mix Vehicle Routing Problem. arXiv:2512.24251v1.

2. Ponce, A. (2022). Automated Smart Truck Diversions White Paper. MineSense Technologies Ltd.

3. Golden, B., Assad, A., Levy, L., & Gheysens, F. (1984). The fleet size and mix vehicle routing problem. Computers & Operations Research, 11(1), 49-66.
