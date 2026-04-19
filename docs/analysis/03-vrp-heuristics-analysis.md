# Critical Analysis: VRP Heuristics Survey vs. ShovelSense Truck Diversion

**Paper:** "Heuristics for Vehicle Routing Problem: A Survey and Recent Advances"
**Authors:** Liu et al. (City University of Hong Kong, Huawei Noah's Ark Lab)
**Source:** arXiv:2303.04147v1, March 2023
**Analysis Date:** 2026-04-18

---

## 1. Paper Summary

### 1.1 Core Contributions

This comprehensive 67-page survey systematically reviews vehicle routing heuristics developed over six decades of research. The key contributions include:

1. **Taxonomy of VRP Heuristics**: Three-tier classification:
   - Constructive heuristics (Nearest Neighbor, Insert, Saving, Sweep methods)
   - Improvement heuristics (Intra-route: Relocate, Exchange, lambda-opt; Inter-route: Insert, Swap, CROSS)
   - Metaheuristics (Simulated Annealing, Tabu Search, Iterated Local Search, Large Neighborhood Search, Genetic Algorithm, Ant Colony Optimization, Memetic Algorithm)

2. **State-of-the-Art Framework**: General algorithm framework for SOTA methods comprising:
   - Solution Initialization
   - Solution Perturbation
   - Solution Improvement
   - Solution Selection

3. **Emerging Research Topics**:
   - Unified heuristics for rich VRPs
   - Automatic heuristic design
   - Machine learning-assisted heuristics

### 1.2 Key Technical Findings

- **Heuristics dominate VRP literature**: Over 80% of VRP publications (2009-2013) used heuristic methods
- **Metaheuristics are state-of-the-art**: Genetic Algorithm most studied, followed by Tabu Search, Large Neighborhood Search
- **Hybrid approaches excel**: SOTA methods combine multiple heuristic concepts (collaboration principle)
- **Diversity control critical**: Population-based methods require explicit diversity management for competitive performance
- **Scalability remains challenging**: ML-assisted methods struggle with generalization to larger instances

---

## 2. Relevance to ShovelSense Technology

### 2.1 Problem Mapping

The ShovelSense system performs a **simplified variant** of vehicle routing:

| VRP Characteristic | ShovelSense Implementation |
|-------------------|---------------------------|
| Multiple destinations | 2-4 destinations (crusher, stockpile, waste dump, grade bins) |
| Cost minimization | Value maximization (ore recovery vs. dilution) |
| Dynamic routing | Real-time per-truck decisions |
| Capacity constraints | Fixed truck capacity, single-delivery |
| Time windows | Implicit (production rate constraints) |

**Critical observation**: ShovelSense's routing problem is a **degenerate case** of the classical VRP. Each truck makes a single delivery to one of N fixed destinations. This is closer to a **classification problem with routing constraints** than a full VRP.

### 2.2 What the Paper Supports

1. **Real-time heuristics are feasible**: Constructive heuristics (O(n) to O(n^3) complexity) can execute in milliseconds, supporting ShovelSense's real-time decision requirements.

2. **Simple heuristics can be effective**: The survey notes that even basic nearest neighbor or sweep methods, when combined with improvement procedures, can be competitive for practical applications.

3. **FMS integration is established**: The survey references numerous real-world VRP applications in logistics, transportation, and fleet management, validating that heuristic-based routing integrates well with fleet management systems.

4. **Dynamic VRP variants exist**: The paper discusses dynamic VRP with stochastic elements, though ShovelSense's problem (uncertainty in ore grade, not demand) differs from typical stochastic VRP formulations.

### 2.3 What the Paper Contradicts or Challenges

1. **Lack of optimization sophistication**: ShovelSense appears to use a **threshold-based classification** (cutoff grades) rather than any heuristic optimization. The paper demonstrates that even simple problems benefit from:
   - Multi-objective consideration
   - Look-ahead planning
   - Global optimization across truck fleet

2. **Single-truck decisions are suboptimal**: The VRP literature emphasizes **inter-route optimization** (moving loads between vehicles). ShovelSense makes isolated per-truck decisions without considering:
   - Crusher capacity constraints over time
   - Stockpile management optimization
   - Queue balancing at destinations

3. **No consideration of dynamic re-routing**: The survey discusses **dynamic VRP** where routes are adjusted based on new information. ShovelSense's one-shot decision model lacks:
   - Re-routing capability if conditions change
   - Coordination between multiple shovels
   - Production schedule optimization

---

## 3. Gaps and Concerns About ShovelSense

### 3.1 Algorithmic Simplicity

The ShovelSense white paper describes a **rule-based classification** system:
- Material exceeds cutoff grade --> Route to ore destination
- Material below cutoff grade --> Route to waste

This approach ignores decades of VRP research showing that **greedy local decisions are suboptimal**. Specific concerns:

| Ignored Factor | Potential Impact |
|---------------|-----------------|
| Crusher queue length | Truck idle time, production delays |
| Stockpile inventory levels | Blending constraints not met |
| Multiple-shovel coordination | Conflicting routing decisions |
| Haul distance optimization | Fuel/time costs not minimized |
| Grade variability within truck | Misclassification risk |

### 3.2 Missing Multi-Objective Optimization

The VRP survey extensively covers **multi-objective VRP** variants that balance:
- Cost minimization
- Service quality
- Time constraints
- Environmental factors

ShovelSense optimizes a single implicit objective (grade recovery) without formulating or solving an optimization problem. The claimed "$2M additional revenue" has no:
- Comparison to optimized baseline
- Accounting for operational costs of diversions
- Analysis of downstream processing impacts

### 3.3 Scalability Questions

The survey highlights that **unified heuristics** can handle 10+ VRP attributes simultaneously. ShovelSense's approach does not scale well to:
- Multi-element optimization (Cu + Mo + Au)
- Net Smelter Return calculations
- Dynamic market price integration
- Multiple processing pathways

### 3.4 Machine Learning Integration Disconnect

The survey's Section 6.3 reviews ML-assisted heuristics showing:
- Algorithm selection via meta-learning
- Parameter tuning with reinforcement learning
- Neural network-guided local search

ShovelSense uses ML only for **grade prediction**, not for **routing optimization**. This is a missed opportunity given that:
- Real-time sensor data is ideal for online learning
- Historical diversion outcomes could train routing policies
- Fleet-wide optimization could use RL approaches

---

## 4. Specific Technical Criticisms

### 4.1 The 11% Diversion Rate Claim

The case study claims 11% of trucks (697 of 6,270) were diverted. Analysis:

**Positive interpretation**:
- 6.4% ore recovery (403 trucks) suggests meaningful value capture
- 4.7% dilution prevention (294 trucks) improves mill feed quality

**Critical questions**:
1. What is the **false positive/negative rate** of the XRF classification?
2. How were diversions **validated** post-hoc?
3. What was the **cost** of each diversion (additional haul distance)?
4. Were any diversions **incorrect** (misclassification)?

The paper provides no confusion matrix or validation methodology.

### 4.2 Missing Baseline Comparison

The VRP survey emphasizes **benchmark comparison** as essential for algorithm evaluation. ShovelSense provides no comparison to:
- Optimized geological block model (no XRF)
- Alternative sensor technologies
- Alternative routing algorithms
- Human expert decisions

The "$2M revenue" claim has no counterfactual analysis.

### 4.3 Single-Shovel Limitation

The case study uses **one shovel on one bench** for 80 days. This ignores:
- Multi-shovel coordination problems
- Spatial variability across benches
- Fleet-wide optimization opportunities

The VRP literature shows that **multi-depot** and **heterogeneous fleet** problems require significantly different algorithms.

---

## 5. Recommendations for ShovelSense Evaluation

### 5.1 Required Algorithmic Enhancements

Based on VRP research, ShovelSense should consider:

1. **Look-ahead optimization**: Use demand forecasting (crusher capacity, stockpile levels) to optimize routing beyond single-truck decisions

2. **Multi-objective formulation**: Explicitly trade off:
   - Grade recovery
   - Haul distance
   - Queue times
   - Blending targets

3. **Dynamic re-optimization**: Implement rolling horizon optimization as new sensor data arrives

4. **Fleet-wide coordination**: Use inter-route heuristics to balance loads across the truck fleet

### 5.2 Required Validation

1. **Confusion matrix**: Validate XRF classifications against assay data
2. **A/B testing**: Compare sensor-routed vs. block-model-routed trucks
3. **Cost-benefit analysis**: Account for diversion costs (fuel, time, wear)
4. **Sensitivity analysis**: Test robustness to sensor calibration drift

---

## 6. Academic Rigor Assessment

### 6.1 VRP Survey Paper

| Criterion | Score | Notes |
|-----------|-------|-------|
| Literature coverage | 5/5 | 328 references, comprehensive taxonomy |
| Methodology | 4/5 | Clear classification, some overlap in categories |
| Reproducibility | 4/5 | Algorithms described; implementation details vary |
| Recency | 5/5 | Covers work through 2022, ML integration current |
| Practical applicability | 4/5 | Strong industrial relevance, some theory gaps |
| **Overall** | **4.4/5** | Excellent survey, authoritative reference |

### 6.2 ShovelSense White Paper (for comparison)

| Criterion | Score | Notes |
|-----------|-------|-------|
| Literature coverage | 1/5 | Only 3 references, no algorithm citations |
| Methodology | 2/5 | System described, no optimization formulation |
| Reproducibility | 1/5 | Proprietary, no algorithmic details |
| Validation | 2/5 | Single case study, no statistical analysis |
| Practical applicability | 3/5 | Deployed system, limited scope |
| **Overall** | **1.8/5** | Marketing document, not academic work |

---

## 7. Conclusions

### 7.1 Key Findings

1. **The VRP survey demonstrates that ShovelSense uses no VRP optimization**: The system performs threshold-based classification, not route optimization. This is a fundamental limitation compared to SOTA approaches.

2. **Significant optimization potential exists**: Applying even basic improvement heuristics or metaheuristics could enhance ShovelSense's routing decisions beyond greedy classification.

3. **The 11% diversion claim lacks context**: Without comparison to optimized baselines or validation of diversion accuracy, the claimed benefits cannot be critically assessed.

4. **ML-assisted routing is a missed opportunity**: The survey shows ML integration improves VRP heuristics; ShovelSense uses ML only for sensing, not optimization.

### 7.2 Bottom Line

The VRP heuristics survey is a rigorous academic work that exposes the **algorithmic immaturity** of ShovelSense's routing approach. While the XRF sensing technology may be innovative, the decision-making layer appears to be a simple rule-based system that ignores decades of optimization research.

ShovelSense's claims of value ($2M revenue, 11% diversions) are **not supported by the type of validation** that the VRP community would require for a new algorithm. The white paper reads as marketing material rather than a technical contribution.

**Recommendation**: Any evaluation of ShovelSense should require:
- Explicit algorithmic description of the routing logic
- Benchmark comparison against optimal or near-optimal solutions
- Statistical validation of classification accuracy
- Cost-benefit analysis including operational impacts

---

## 8. References

1. Liu, F., Lu, C., Gui, L., Zhang, Q., Tong, X., & Yuan, M. (2023). Heuristics for Vehicle Routing Problem: A Survey and Recent Advances. arXiv:2303.04147v1.

2. Ponce, A. (2022). Automated Smart Truck Diversions. MineSense Technologies Ltd. White Paper.

3. Vidal, T., Crainic, T.G., Gendreau, M., & Prins, C. (2014). A unified solution framework for multi-attribute vehicle routing problems. European Journal of Operational Research, 234, 658-673.

4. Pisinger, D., & Ropke, S. (2007). A general heuristic for vehicle routing problems. Computers & Operations Research, 34, 2403-2435.
