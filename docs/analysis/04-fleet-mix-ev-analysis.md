# Critical Analysis: Fleet-mix EV Routing Problem vs. ShovelSense Automated Truck Diversion

**Paper:** Fleet-mix Electric Vehicle Routing Problem for the E-commerce Delivery with Limited Off-Hour Delivery Implementation
**Authors:** Hyun-Seop Uhm, Abdelrahman Ismael, Natalia Zuniga-Garcia, Olcay Sahin, James Cook, Joshua Auld, Monique Stinson (Argonne National Laboratory)
**Source:** Transportation Research (Argonne National Laboratory / DOE sponsored)
**Analysis Date:** April 2026

---

## 1. Paper Summary

### 1.1 Problem Definition

The paper addresses the **Fleet-mix Electric Vehicle Routing Problem with Off-Hour Delivery (EVRP-OHD)**, a novel variant combining:

1. **Fleet electrification decisions** - Optimal mix of electric vs conventional trucks
2. **Multi-shift operations** - Electric trucks can operate daytime AND nighttime (due to low noise)
3. **Vehicle routing** - Optimal routes for heterogeneous fleet
4. **Charging infrastructure** - Determining EVSE (charger) requirements at depots

The problem is formulated as a **Mixed-Integer Linear Programming (MILP)** model minimizing:
- Total Cost of Ownership (TCO) for trucks
- EVSE purchasing costs
- Daily transportation costs (travel time)

### 1.2 Key Contributions

1. **Joint Optimization Framework** - Simultaneously optimizes fleet composition, routing, and charging infrastructure

2. **Multi-Shift Electric Truck Operations** - Novel constraint structure allowing EVs to:
   - Operate daytime route
   - Return to depot for recharging
   - Operate nighttime route (OHD locations only)

3. **Bi-level VNS-TS Heuristic** - Efficient solution method:
   - **Upper level**: Variable Neighborhood Search for fleet assignment
   - **Lower level**: Tabu Search for route optimization

4. **POLARIS Simulation Integration** - Validated on Austin, TX metropolitan area with ~280,000 daily orders

### 1.3 Results

| Scenario | OHD Ratio | EV Ratio Required | Avg VMT Reduction | Avg VHT Reduction |
|----------|-----------|-------------------|-------------------|-------------------|
| 7hr EV range | 10% | 17.7% | 15.9% | 16.2% |
| 7hr EV range | 20% | 36.5% | 23.1% | 24.3% |
| 7hr EV range | 50% | 82.7% | 30.2% | 32.4% |
| 11hr EV range | 10% | 26.3% | 15.4% | 16.2% |
| 11hr EV range | 50% | 78.1% | 17.5% | 21.6% |

Key findings:
- Low OHD acceptance (10-20%) sufficient for significant benefits
- Longer EV range enables fleet size reduction (2,221 to 1,734 trucks)
- VNS-TS heuristic outperforms CPLEX solver in all scenarios

---

## 2. Relevance to ShovelSense Technology

### 2.1 Problem Domain Comparison

| Aspect | EVRP-OHD Paper | ShovelSense Application |
|--------|----------------|------------------------|
| **Domain** | Urban e-commerce delivery | Open-pit mining haulage |
| **Vehicles** | Heterogeneous (EV + conventional) | Typically homogeneous mining trucks |
| **Decision Type** | Route planning + fleet composition | Binary destination assignment |
| **Optimization Horizon** | Daily planning (batch) | Real-time, per-truck |
| **Primary Constraint** | Battery range, capacity, time windows | Grade cutoffs, processing capacity |
| **Objective** | Minimize cost (TCO + operations) | Maximize ore value recovery |
| **Network Type** | Urban road network (~15,800 links) | Mine haul road network (~10-50 routes) |
| **Scale** | ~280,000 orders/day, ~2,200 trucks | ~100-500 truck loads/day |

### 2.2 Conceptual Parallels

**The paper provides useful framework concepts despite domain differences:**

1. **Multi-Destination Routing** - Both problems involve routing vehicles to alternate destinations based on conditions (battery state vs ore grade)

2. **Heterogeneous Decision Variables** - EVRP-OHD handles truck type selection AND routing; ShovelSense handles grade classification AND destination selection

3. **Real-Time Data Integration** - Paper uses POLARIS simulation for traffic conditions; ShovelSense uses XRF for grade conditions

4. **Constraint-Based Diversion** - EVs must divert to chargers; trucks must divert based on grade thresholds

### 2.3 Direct Applicability Assessment

**Limited Direct Applicability:**

| Factor | Applicability | Rationale |
|--------|---------------|-----------|
| Algorithm | Low | VRPs optimize multi-stop routes; mining is point-to-point |
| Mathematical Model | Low | MILP formulation assumes known demands; mining has grade uncertainty |
| Heuristics | Medium | VNS/TS meta-heuristics could inform shift/stockpile scheduling |
| Simulation Framework | Medium | POLARIS-style simulation could model mine traffic/queuing |
| Fleet Composition | Low | Mining trucks are typically homogeneous within operations |

---

## 3. Critical Analysis of ShovelSense Claims

### 3.1 The 11% Diversion Rate Claim

**ShovelSense Claims:** 11% of trucks (697/6,270) were diverted in 80-day case study

**Analysis Through VRP Lens:**

| Consideration | EVRP-OHD Context | ShovelSense Gap |
|---------------|------------------|-----------------|
| **Optimality** | Paper proves heuristic finds near-optimal solutions vs CPLEX | No baseline comparison for 11% rate |
| **Sensitivity Analysis** | Paper tests multiple scenarios (OHD ratios, EV ranges) | Single scenario reported |
| **Trade-off Analysis** | Explicit cost modeling (TCO, EVSE, operations) | No trade-off analysis |

**Key Concern:** The EVRP-OHD paper rigorously validates that 10-20% diversion rates for nighttime delivery yield significant benefits. ShovelSense's 11% diversion rate is plausible but **unvalidated**:
- Is 11% optimal or could it be 8% or 15%?
- What is the false positive rate (ore sent to waste)?
- What is the false negative rate (waste sent to crusher)?

### 3.2 The $2M+ Revenue Claim

**ShovelSense Claims:** Additional revenue exceeding $2M USD from ore recovery

**Critical Analysis Using EVRP-OHD Framework:**

The EVRP-OHD paper models **complete cost structures**:
- Fixed costs (truck purchase, EVSE)
- Variable costs (energy, time)
- Trade-offs explicitly quantified

**ShovelSense Revenue Claim Lacks:**

1. **Full Cost Accounting**
   - Capital cost of XRF/sensor systems
   - Integration/maintenance costs
   - Longer haul cycles for diverted trucks
   - Processing costs for additional ore

2. **Verification Methodology**
   - How were "diverted" loads verified post-processing?
   - What was actual recovery from diverted material?
   - What was dilution cost from false positives?

3. **Counterfactual Analysis**
   - What would baseline (no diversion) revenue have been?
   - Is comparison against actual production or theoretical?

### 3.3 FMS Integration Claims

**ShovelSense Claims:** API integration with Caterpillar, Modular Mining, Wenco

**EVRP-OHD Comparison:**

The paper demonstrates that **optimal fleet routing requires:**
- Global visibility of all vehicle states (positions, cargo, destinations)
- Queue state awareness (crusher capacity, stockpile levels)
- Dynamic re-optimization capability
- Multi-objective balancing

**ShovelSense Integration Appears Unidirectional:**
- Sends destination assignment to FMS
- No evidence of receiving fleet state information
- No evidence of queue-aware decision making
- No evidence of multi-truck coordination

---

## 4. Gaps and Concerns

### 4.1 Fundamental Methodological Differences

| EVRP-OHD Strength | ShovelSense Gap |
|-------------------|-----------------|
| Formal MILP optimization model | No optimization formulation disclosed |
| Multiple baselines (CPLEX, heuristics) | No baseline comparison |
| Sensitivity analysis across scenarios | Single case study |
| Explicit constraint modeling | Black-box decision system |
| Computational complexity analysis | No performance metrics |

### 4.2 What ShovelSense Could Learn from EVRP-OHD

**1. Multi-Objective Optimization**

EVRP-OHD optimizes multiple objectives simultaneously:
```
Minimize: TCO + EVSE_cost + travel_time
```

ShovelSense should similarly optimize:
```
Maximize: ore_recovery_value - processing_cost - cycle_time_cost - misclassification_cost
```

**2. Scenario Analysis**

EVRP-OHD tests 10 scenarios varying:
- EV driving range (7 vs 11 hours)
- OHD acceptance ratio (0%, 10%, 20%, 30%, 50%)

ShovelSense should test:
- Grade cutoff sensitivity
- XRF measurement accuracy ranges
- Plant feed requirements

**3. Computational Benchmarking**

EVRP-OHD compares against CPLEX optimal solver:
- Reports MIP gap percentages
- Quantifies heuristic performance

ShovelSense should benchmark against:
- Optimal classification (known grades)
- Rule-based alternatives
- Manual geologist decisions

### 4.3 What EVRP-OHD Does NOT Address Relevant to Mining

**1. Measurement Uncertainty**

EVRP-OHD assumes:
- Known demand volumes
- Deterministic travel times (from simulation)
- Binary constraints (location accepts OHD or not)

Mining reality:
- XRF grade estimates have measurement error
- Grades vary within bucket (surface vs volumetric)
- Cutoffs are continuous, not binary

**2. Sequential Decision Making Under Uncertainty**

EVRP-OHD is a **planning problem** - all decisions made before execution

Mining diversion is a **real-time control problem**:
- Decision made at loading
- Grade known imprecisely
- Cannot revise decision post-departure

**3. Value-Based vs Cost-Based Optimization**

EVRP-OHD minimizes costs

Mining should maximize expected value:
```
E[Value] = P(ore|measurement) * ore_value + P(waste|measurement) * (-processing_cost)
```

This requires probabilistic grade classification, not binary cutoffs.

---

## 5. Academic Rigor Assessment

### 5.1 EVRP-OHD Paper (Argonne National Laboratory)

| Criterion | Rating | Notes |
|-----------|--------|-------|
| **Problem Formulation** | Excellent | Complete MILP model with all constraints |
| **Methodology** | Strong | Bi-level heuristic with clear pseudocode |
| **Experimental Design** | Strong | Multiple scenarios, baseline comparisons |
| **Validation** | Strong | CPLEX comparison, POLARIS simulation |
| **Reproducibility** | Good | Parameters disclosed, POLARIS framework available |
| **Limitations Acknowledged** | Adequate | Notes need for micro-hub extensions |
| **Statistical Rigor** | Adequate | Multiple instances tested, consistent reporting |

**Overall: 8/10** - Well-executed operations research with government lab rigor

### 5.2 ShovelSense White Paper (August 2022) - Comparative Assessment

| Criterion | EVRP-OHD | ShovelSense | Gap |
|-----------|----------|-------------|-----|
| **Problem Formulation** | Complete MILP | Not disclosed | Critical |
| **Methodology** | Detailed algorithm | "Machine learning" | Critical |
| **Experimental Design** | 10 scenarios | 1 case study | Significant |
| **Validation** | Optimal solver comparison | None | Critical |
| **Reproducibility** | High | None (proprietary) | Critical |
| **Limitations** | Discussed | None mentioned | Significant |

**Comparative Rating: ShovelSense 3/10 vs EVRP-OHD 8/10**

---

## 6. Applicability to ShovelSense Development

### 6.1 Transferable Concepts

| Concept from EVRP-OHD | Mining Application |
|-----------------------|-------------------|
| Multi-shift operations | Multi-stockpile routing by time-of-day |
| Queue-aware constraints | Crusher queue management |
| Fleet heterogeneity handling | Multi-material type trucks |
| EVSE allocation | Stockpile capacity planning |
| Bi-level optimization | Grade classification + route assignment |

### 6.2 Research Gaps for Automated Truck Diversion

**Based on EVRP-OHD methodology, ShovelSense should address:**

1. **Formal Optimization Model**
   - Define decision variables (destination, timing)
   - Specify objective function (net value recovery)
   - Document constraints (capacity, grade requirements)

2. **Uncertainty Quantification**
   - XRF measurement accuracy
   - Grade distribution within buckets
   - Confidence intervals on decisions

3. **Baseline Comparisons**
   - Manual geologist classification
   - Simple rule-based systems
   - Theoretically optimal (known grades)

4. **Economic Analysis**
   - Full lifecycle costs
   - Sensitivity to commodity prices
   - Break-even analysis

5. **Multi-Site Validation**
   - Different ore types
   - Different fleet configurations
   - Different plant constraints

### 6.3 Recommended Methodological Improvements

**From EVRP-OHD Best Practices:**

1. **Publish Complete Problem Formulation**
   - Mathematical model of diversion decision
   - Constraint structure
   - Objective function components

2. **Implement Scenario Analysis**
   - Vary grade cutoffs
   - Test measurement accuracy ranges
   - Model different production targets

3. **Establish Computational Benchmarks**
   - Decision latency requirements
   - Accuracy vs speed trade-offs
   - Scalability to larger operations

4. **Integrate Fleet-Level Optimization**
   - Consider crusher queue states
   - Coordinate multiple active trucks
   - Balance blending requirements

---

## 7. Conclusion

The EVRP-OHD paper represents rigorous operations research addressing fleet optimization with heterogeneous vehicles and multi-destination routing. While the domain (urban e-commerce) differs significantly from mining, the methodological approach offers valuable lessons.

### Key Findings

1. **Problem Complexity Comparison**
   - EVRP-OHD is computationally harder (NP-hard VRP)
   - ShovelSense solves a simpler classification problem
   - But mining adds uncertainty that EVRP-OHD does not address

2. **Methodological Gap**
   - EVRP-OHD: Complete formal model, multiple baselines, sensitivity analysis
   - ShovelSense: Single case study, no baselines, no formal model

3. **Claims Validation**
   - EVRP-OHD validates 10-20% diversion yields benefits (for OHD)
   - ShovelSense 11% diversion rate is plausible but unvalidated
   - Revenue claims lack the cost accounting rigor shown in EVRP-OHD

4. **Integration Opportunity**
   - EVRP-OHD demonstrates fleet-wide optimization value
   - ShovelSense operates at individual truck level
   - Combining real-time sensing with fleet optimization could yield superior results

### Concerns About ShovelSense Approach

| Concern | Severity | Evidence |
|---------|----------|----------|
| No optimization formulation | High | Only detection, not optimization |
| No baseline comparison | High | Cannot assess relative value |
| Ignores measurement uncertainty | High | Binary cutoffs vs probabilistic |
| No fleet-level coordination | Medium | Individual truck decisions |
| Single case study | Medium | Limited generalizability |
| No economic rigor | High | Benefits claimed without full costs |

### Bottom Line

**The EVRP-OHD paper does not validate ShovelSense claims** but highlights the sophistication gap between academic operations research and ShovelSense's reported methodology. The 11% diversion rate and $2M revenue claims remain unverified from an academic perspective. ShovelSense would benefit from adopting the experimental rigor, formal modeling, and comprehensive economic analysis demonstrated in this paper.

The paper does demonstrate that real-time routing optimization is computationally feasible, which indirectly supports the viability of automated truck diversion systems. However, ShovelSense appears to implement detection/classification rather than optimization, which is a fundamentally simpler - and potentially suboptimal - approach.

---

## References

1. Uhm, H.S., Ismael, A., Zuniga-Garcia, N., Sahin, O., Cook, J., Auld, J., & Stinson, M. (2023). Fleet-mix Electric Vehicle Routing Problem for the E-commerce Delivery with Limited Off-Hour Delivery Implementation. Argonne National Laboratory / U.S. Department of Energy.

2. Ponce, A. (2022). Automated Smart Truck Diversions White Paper. MineSense Technologies Ltd.

3. Auld, J., Hope, M., Ley, H., Sokolov, V., Xu, B., & Zhang, K. (2016). POLARIS: Agent-based modeling framework development and implementation. Transportation Research Part C, 64, 101-116.

4. Kucukoglu, I., Dewil, R., & Cattrysse, D. (2021). The electric vehicle routing problem and its variations: A literature review. Computers and Industrial Engineering, 161, 107650.
