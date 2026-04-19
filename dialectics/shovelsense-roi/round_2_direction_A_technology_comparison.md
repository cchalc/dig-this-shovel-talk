# Direction A: Grade Control Technology Comparison for Copper Porphyry

**Question:** Which sensing technology offers the best ROI for this specific deposit type?

---

## Comparative Technology Analysis

### XRF (ShovelSense)

**Physics:** X-ray fluorescence excites surface atoms; emitted photons reveal elemental composition. Penetration depth is tens to hundreds of micrometers---essentially surface-only measurement.

**Sampling:** ShovelSense deploys 2-4 XRF sensors scanning bucket loads over 7 seconds, capturing multiple surface readings. This partially mitigates heterogeneity error but cannot overcome the fundamental surface limitation. Published research shows classification accuracy of 75-93% depending on cutoff grade, with machine learning enhancements pushing this to 86-92% ([Es-sahly et al., 2025](https://journals.sagepub.com/doi/10.1177/25726838251343415)).

**Vendor claims:** MineSense reports 4% recovery improvement and 8% higher concentrate grade at copper mines with high ShovelSense coverage ([CIM Magazine](http://magazine.cim.org/en/technology/no-time-for-waste/)). They claim 0.03% Cu head grade improvement and 10% higher delivered copper at a 65,000 tpd operation.

**Independent validation:** None exists. All published performance data originates from MineSense or their commercial partners. Academic XRF studies consistently identify "heterogeneity error"---the gap between surface measurement and volumetric grade---as the dominant error source.

**Deployment:** $200K/month lease, decision point at loading (earliest in material flow), operational at three Western Canadian copper mines including Highland Valley and Gibraltar.

**Copper porphyry applicability:** The 80% chalcopyrite composition creates significant iron absorption of copper X-rays (matrix effect). Surface-to-volume correlation in vein-hosted mineralization is the critical unknown.

### PGNAA/PFTNA (Thermo Fisher CB Omni)

**Physics:** Prompt gamma neutron activation bombards material with neutrons; gamma emissions from activated nuclei reveal elemental composition. Neutrons and gamma rays penetrate 0.5m---full cross-section of conveyor belt loads.

**Sampling:** Continuous measurement of the entire material stream. Not affected by particle size, layering, segregation, or dust. Correlations between analyzer and lab samples reach 0.8-0.999 for target elements ([Thermo Fisher](https://www.thermofisher.com/us/en/home/industrial/cement-coal-minerals/cement-coal-minerals-learning-center/cement-analysis-production-information/pgnaa-pftna-technology/technology.html)).

**Accuracy:** 2-sigma measurements achievable below typical copper cutoff grades in less than 30 seconds. Industry standard for bulk copper belt analysis specifically because it overcomes XRF's surface limitation.

**Independent validation:** Extensive. Thousands of installations across cement, coal, and mining industries. Thermo Fisher's technical literature is corroborated by independent mining consultant studies.

**Deployment:** Capital purchase (typically $500K-1.5M installed), decision point at conveyor (after loading). Major capital expenditure is in material handling infrastructure---diverters, routing, stockpiling---not the sensor itself.

**Copper porphyry applicability:** Excellent. Volumetric measurement eliminates surface-to-volume correlation problem. However, decision point is later in material flow than shovel-based systems.

### MRT (NextOre Magnetic Resonance)

**Physics:** Pulsed radiofrequency waves tuned to target mineral resonant frequencies. Response strength directly correlates to mineral content. Fully penetrative---measures the entire ore body, not just surfaces.

**Sampling:** Bulk grade measurements within 4 seconds for tonnages around 2.5t. 3-sigma detection limit of 0.045 wt% copper as chalcopyrite demonstrated at operational scale ([Kansanshi trial](https://im-mining.com/2022/05/24/nextore-first-quantum-fully-commission-worlds-largest-bulk-ore-sorting-system/)).

**Accuracy:** Precision of +/- 0.028% at Kansanshi. Sensing resolution below 0.05% copper achieved. Critically, MRT measures specific copper minerals (chalcopyrite, bornite) directly, not just elemental copper. This is directly relevant to this deposit's 80/20 chalcopyrite/bornite mineralogy.

**Independent validation:** Peer-reviewed publication ([Minerals Engineering, 2024](https://www.sciencedirect.com/science/article/pii/S0892687524000931)) documents the Kansanshi bulk sorting trial. Real-world installations at First Quantum's Kansanshi (2,800 t/h) and a 6,500 t/h operation in Chile provide operational validation.

**Deployment:** Capital model (pricing not publicly disclosed), decision point at conveyor. New underground truck-mounted system announced March 2025 for earlier decision points.

**Copper porphyry applicability:** Strong. Tuned specifically for copper sulfide minerals. The 80% chalcopyrite / 20% bornite mix is well within the technology's capability since both minerals are detectable. Volumetric measurement eliminates surface heterogeneity concerns.

### Improved Blast Hole Protocols

**Physics:** No new sensing technology. Better sampling practices, faster lab turnaround, tighter spacing, improved geostatistics.

**Sampling:** Research shows blast hole sampling error ranges from 10-70% of observed grade variability. Advanced RC drilling grids coupled with geostatistics significantly improve financial returns ([ResearchGate study](https://www.researchgate.net/publication/321780218_Optimal_grade_control_sampling_practice_in_open-pit_mining_-_a_full-scale_blast_hole_versus_reverse_circulation_variographic_experiment)).

**Accuracy:** Estimation methodology causes larger profit losses than sampling errors in porphyry copper---losses of 6-12% as sampling error increases ([Perez et al.](https://www.researchgate.net/publication/311706751_Estimation_of_economic_losses_due_to_poor_blast_hole_sampling_in_open_pits)).

**Independent validation:** Extensive academic literature on grade control optimization. Well-understood failure modes and improvement pathways.

**Deployment:** Incremental capital (additional drilling, lab equipment), no recurring technology lease. Benefits accrue through better block model accuracy, not real-time routing.

**Copper porphyry applicability:** High. The fundamental challenge---predicting grade before material moves---remains. Improvements are statistical rather than eliminative.

---

## Summary Comparison

| Factor | XRF (ShovelSense) | PGNAA | MRT (NextOre) | Blast Hole Optimization |
|--------|-------------------|-------|---------------|------------------------|
| **Penetration** | Surface only | Full bulk | Full bulk | N/A |
| **Decision Point** | At loading | At conveyor | At conveyor | Before mining |
| **Accuracy (published)** | 75-93% | R=0.8-0.999 | +/-0.028% Cu | 10-70% error reduction possible |
| **Independent Validation** | None | Extensive | Peer-reviewed + operational | Extensive |
| **Cost Model** | $200K/month lease | ~$500K-1.5M capital | Capital (undisclosed) | Incremental |
| **Copper Sulfide Suitability** | Matrix effects from Fe | Good | Excellent (mineral-specific) | Indirect |
| **Porphyry Heterogeneity** | Surface may not represent volume | Overcomes limitation | Overcomes limitation | Improves statistical model |

---

## Recommendation

**Evaluate MRT (NextOre) first, then PGNAA, then optimized blast holes. ShovelSense should be evaluated last, if at all.**

Here is my reasoning:

1. **MRT solves the right problem.** This deposit's value proposition is distinguishing 0.32% Cu cutoff in chalcopyrite-dominated ore. MRT measures chalcopyrite and bornite content directly, volumetrically, with sub-0.05% resolution. The Kansanshi peer-reviewed trial demonstrated exactly this capability at operational scale.

2. **XRF's surface limitation is not hypothetical.** The industry moved to neutron-based belt analyzers specifically because XRF cannot reliably predict bulk grade from surface measurements. ShovelSense attempts to overcome this through multiple readings and calibration, but no independent validation demonstrates success in heterogeneous porphyry ore. The academic literature consistently identifies surface-to-volume correlation as XRF's dominant error source.

3. **Decision point matters less than accuracy.** ShovelSense's advantage is making decisions at loading rather than conveyor. But this advantage is worthless if the decisions are wrong. A correct decision at the conveyor beats an incorrect decision at the shovel. Given the lack of independent XRF validation versus demonstrated MRT performance, decision timing is a secondary concern.

4. **The vendor-originated frame should be rejected.** The question "ShovelSense or not?" assumes ShovelSense is the reference technology. It is not. It is one option among several, with the weakest independent validation. The mine should evaluate technologies in order of evidence quality, not vendor marketing success.

**Specific next steps:**

- Contact NextOre for a Kansanshi-style trial feasibility assessment
- Request Thermo Fisher CB Omni technical specifications for copper porphyry applications
- Engage a geostatistics consultant to quantify blast hole optimization potential as a low-cost baseline improvement
- Request independent (non-MineSense-sourced) validation data from ShovelSense before any trial commitment

Do not commit $2.4M/year to a surface-only sensor when volumetric alternatives exist with superior validation evidence.

---

## Sources

- [CIM Magazine - No Time for Waste (ShovelSense)](http://magazine.cim.org/en/technology/no-time-for-waste/)
- [Es-sahly et al. 2025 - XRF Surface Analysis Classification](https://journals.sagepub.com/doi/10.1177/25726838251343415)
- [Thermo Fisher - PGNAA/PFTNA Technology](https://www.thermofisher.com/us/en/home/industrial/cement-coal-minerals/cement-coal-minerals-learning-center/cement-analysis-production-information/pgnaa-pftna-technology/technology.html)
- [Minerals Engineering 2024 - NextOre Bulk Sorting Trial](https://www.sciencedirect.com/science/article/pii/S0892687524000931)
- [International Mining - NextOre Kansanshi Commissioning](https://im-mining.com/2022/05/24/nextore-first-quantum-fully-commission-worlds-largest-bulk-ore-sorting-system/)
- [ResearchGate - Blast Hole vs RC Variographic Experiment](https://www.researchgate.net/publication/321780218_Optimal_grade_control_sampling_practice_in_open-pit_mining_-_a_full-scale_blast_hole_versus_reverse_circulation_variographic_experiment)
- [ResearchGate - Economic Losses from Poor Blast Hole Sampling](https://www.researchgate.net/publication/311706751_Estimation_of_economic_losses_due_to_poor_blast_hole_sampling_in_open_pits)
- [NextOre - Underground MR Analyser Announcement](https://www.nextore.com.au/nextore-unveils-world-first-mr-analyser-for-underground-copper-trucks/)
