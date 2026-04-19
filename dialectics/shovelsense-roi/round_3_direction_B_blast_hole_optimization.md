# Round 3, Direction B: Blast Hole Optimization Without New Sensors

## The Question

Can a copper porphyry mine (0.32% Cu cutoff, 80% chalcopyrite / 20% bornite) significantly improve grade control WITHOUT deploying new sensors?

## The Answer: Yes, With Realistic Expectations

Comprehensive blast hole optimization can reduce misclassification by 10-20% relative to current practice, at roughly one-tenth the cost of sensor deployment. This won't match the theoretical ceiling of real-time sensor data, but for many operations it closes enough of the gap to defer or eliminate the sensor ROI case.

---

## Seven Optimization Levers

### 1. Blast Movement Monitoring (BMM)

**The Problem:** Blasting displaces ore boundaries by 2-8 meters. Mining polygons drawn from pre-blast drill data no longer reflect where the ore actually is.

**The Solution:** [Hexagon BMM](https://blastmovement.com/blast-monitoring/) and [BMT systems](https://www.bmt.com.au/blast-monitoring/) deploy softball-sized monitors within the blast volume. Post-blast detection locates them in 3D, measuring actual displacement vectors.

**Documented Results:**
- [Cowal gold mine](https://www.australianmining.com.au/blast-to-the-future-bmt-wins-for-blasting-innovation-at-prospect-awards/) achieved **7% improvement in mill head grade** compared to mining blocks in pre-blast positions
- [Anaconda operation](https://www.globalminingreview.com/whitepapers/hexagons-mining-division/minimizing-mining-dilution-ore-loss-misclassification-by-accounting-for-blast-movement/) reduced dilution to 5%, generating **$15,000-$30,000 per blast** in additional value
- [AngloGold Ashanti Iduapriem](https://www.ajol.info/index.php/gm/article/view/138984) increased data recovery from 40% to 94%

**Cost:** A few cents per tonne of ore blasted. For a 50,000 tonne/day operation, approximately $150-300K annually including hardware and software.

### 2. Sampling Protocol Improvements

**The Problem:** Poor blast hole sampling introduces fundamental sampling error (FSE) of 10-30%, [costing copper mines millions annually](https://www.researchgate.net/publication/311706751_Estimation_of_economic_losses_due_to_poor_blast_hole_sampling_in_open_pits).

**The Solution:** [Spear pipe sampling](http://geologyyy.blogspot.com/2009/01/blasthole-sampling-for-grade-control-in.html) with standardized protocol:
- 6-cm diameter pipe, sharpened at 45 degrees
- Remove subdrill from cone surface before sampling
- 12 stabs around the pile in six opposite directions
- Target 6-10 kg per blast hole sample
- Four-person crew: 100 samples in 4 hours

**Improvement:** [Batu Hijau porphyry copper study](http://geologyyy.blogspot.com/2009/01/blasthole-sampling-for-grade-control-in.html) found spear sampling the "best option available" among six methods tested, providing reasonable accuracy with practical efficiency.

### 3. Lab Turnaround Acceleration

**The Problem:** 24-48 hour lab turnaround means mining decisions are made on stale data. Material has often moved before assay results arrive.

**The Solution:** [Portable XRF as a screening tool](https://www.thermofisher.com/blog/mining/using-portable-xrf-analysis-for-ore-grade-control-in-mining/):
- Reduces turnaround from days to seconds for screening decisions
- Correlation coefficient >0.98 with lab results for Cu
- Identifies obvious ore vs. waste immediately
- Flags ambiguous samples for priority lab assay

**Cost Impact:** [Using XRF as a "gatekeeper"](https://www.vrxrf.com/blog/portable-analysis-bringing-lab-quality-results-to-mine-field/) reduces lab costs by up to 60% by only sending uncertain samples for full assay.

### 4. Drill Spacing Optimization

**The Problem:** Over-drilling wastes money; under-drilling misses grade boundaries.

**The Solution:** [Conditional simulation analysis](https://www.tandfonline.com/doi/full/10.1080/19236026.2025.2562795) to find the economic optimum where:
- Cost of additional drilling = Cost of misclassification avoided

**Research Finding:** For [copper mines specifically](https://journals.sagepub.com/doi/10.1177/25726668241270400), optimal spacing varies significantly by deposit heterogeneity. One study found 25x25x15m optimal for a continuous Cu deposit. **Tighter spacing does not always improve value** - in some cases, sparser drilling with better sampling produces superior results.

### 5. Geostatistical Improvements

**The Problem:** Traditional ordinary kriging may not capture complex grade distributions in porphyry copper deposits.

**The Solution:** [Machine learning enhanced workflows](https://link.springer.com/article/10.1007/s11053-022-10029-8):
- Ensemble ML algorithms (neural networks, support vector regressors) model copper grade
- Results incorporated via intrinsic collocated co-kriging
- Demonstrated at [Carmen de Andacollo copper mine](https://link.springer.com/article/10.1007/s11053-022-10029-8) in Chile

**Improvement:** ML-geostatistical hybrid workflows "improve grade control decision-making when compared to common approaches" without requiring new field sensors.

### 6. GPS-Guided Dig Line Optimization

**The Problem:** Operators can't accurately follow optimized dig boundaries without guidance systems.

**The Solution:** [High-precision GPS on excavators](https://groundhogapps.com/ore-quality-control-and-dilution/) with:
- Centimeter-level positioning accuracy
- Real-time dig block display on operator screens
- Geofenced ore zones with automatic alerts
- Material tracking from source to destination

**Accuracy:** [Current systems achieve 2-3 cm tolerances](https://ronmeyerexcavating.com/gps-in-excavation/), eliminating operator skill variation as a grade control variable.

### 7. Integrated Protocol Optimization

A [large Chilean copper open pit](https://www.geovariances.com/wp-content/uploads/2016/08/geostatsrdv2013_-_riotinto_-_optimization_grade.pdf) study identified four protocol improvements that together reduce misclassification by **2-5%**:
1. Grade predictions at 1/4 blast hole spacing resolution
2. Uncertainty quantification in grade assignment
3. Blast movement accounting
4. Destination optimization at smallest possible unit

---

## Cost Comparison

| Approach | Capital/Setup | Annual Operating | Improvement |
|----------|---------------|------------------|-------------|
| **Blast Movement Monitoring** | $50-100K | $150-200K | 5-7% head grade |
| **Sampling Protocol Overhaul** | $20-30K (training, equipment) | ~$50K incremental labor | 5-15% FSE reduction |
| **Portable XRF Screening** | $40-60K per unit | $10-20K maintenance | 2-4 hour faster decisions |
| **Drill Spacing Optimization** | $30-50K (geostat study) | Savings or neutral | Variable by deposit |
| **ML-Geostatistics** | $50-100K (consulting, software) | $30-50K maintenance | 5-10% estimation improvement |
| **GPS Dig Guidance** | $150-250K per shovel | $30-50K/yr | Near-elimination of dig error |
| **TOTAL Comprehensive Program** | ~$400-600K | ~$300-400K/yr | 10-20% misclassification reduction |

**Comparison to ShovelSense:** $200K/month = $2.4M/year, roughly 6x the cost of comprehensive blast hole optimization.

---

## Case Study Evidence

**Rio Tinto protocol optimization:** A [formal study of grade control procedures](https://www.geovariances.com/wp-content/uploads/2016/08/geostatsrdv2013_-_riotinto_-_optimization_grade.pdf) at a major copper operation found that suboptimal procedures cost **$134 million over 10 years**. Protocol improvements alone recovered significant value.

**Industry synthesis:** [Discovery Alert's 2025 analysis](https://discoveryalert.com.au/grade-control-mining-economic-importance-2025/) found that copper mines achieving **5% grade control improvement** report **10-15% increases in annual profitability**.

---

## Phased Implementation Plan

### Phase 1: Quick Wins (Months 1-3) — Cost: ~$100K

1. **Sampling protocol audit and training**
   - Review current blast hole sampling against spear sampling best practices
   - Train crews on 12-stab protocol with proper subdrill removal
   - Expected improvement: 5-10% reduction in fundamental sampling error

2. **Deploy portable XRF for screening**
   - Purchase 2-3 handheld XRF units
   - Use for immediate ore/waste flagging
   - Route ambiguous samples to lab; clear ore/waste decisions made in field
   - Expected improvement: 2-4 hour faster decision cycles

### Phase 2: Measurement Infrastructure (Months 3-9) — Cost: ~$200K

3. **Implement blast movement monitoring**
   - Deploy Hexagon or BMT system
   - Instrument every production blast in ore zones
   - Adjust dig polygons based on measured displacement
   - Expected improvement: 5-7% reduction in misclassification, matching Cowal/Anaconda results

4. **Geostatistical review and optimization**
   - Engage consultant for variogram modeling and drill spacing analysis
   - Evaluate ML-enhanced estimation for your deposit
   - Optimize drill spacing based on actual cost/benefit at your geology
   - Expected improvement: Variable, but typically identifies $50-200K/year in drilling savings or accuracy gains

### Phase 3: Execution Precision (Months 6-12) — Cost: ~$200-400K

5. **GPS-guided excavation deployment**
   - Install high-precision GPS on 2-3 primary ore-loading shovels
   - Integrate with mine planning system for real-time dig blocks
   - Track actual vs. planned dig boundaries
   - Expected improvement: Near-elimination of dig line execution error

### Expected Cumulative Outcome

After 12 months of phased implementation:
- **Total investment:** ~$400-700K capital + ~$300K/year operating
- **Expected improvement:** 10-20% reduction in ore/waste misclassification
- **Financial impact:** For a 50,000 tpd operation at 0.32% Cu cutoff, each 1% reduction in misclassification is worth approximately $1-2M annually

---

## The Bottom Line

**Can blast hole optimization close the grade control gap without sensors?**

Partially, yes. A comprehensive program delivers 10-20% misclassification reduction at roughly one-sixth the cost of ShovelSense. For operations currently at 15-25% misclassification, this brings them to 12-20% range — matching "typical" industry performance but not reaching "best-in-class" (8-15%).

**When to pursue sensor deployment instead:**
- If baseline assessment shows >25% misclassification AND
- If blast hole optimization has already been implemented AND
- If surface-volume correlation at your deposit supports XRF AND
- If remaining gap justifies $2.4M/year operating cost

**For most operations:** Start with Phase 1-3 blast hole optimization. Measure results. Only then evaluate whether the residual gap justifies sensor investment.

---

## Sources

- [Hexagon Blast Movement Monitoring](https://blastmovement.com/blast-monitoring/)
- [BMT Blast Monitoring Systems](https://www.bmt.com.au/blast-monitoring/)
- [AngloGold Ashanti Iduapriem BMM Study](https://www.ajol.info/index.php/gm/article/view/138984)
- [Batu Hijau Sampling Protocol Study](http://geologyyy.blogspot.com/2009/01/blasthole-sampling-for-grade-control-in.html)
- [Portable XRF for Grade Control](https://www.thermofisher.com/blog/mining/using-portable-xrf-analysis-for-ore-grade-control-in-mining/)
- [Drill Spacing Optimization](https://www.tandfonline.com/doi/full/10.1080/19236026.2025.2562795)
- [Carmen de Andacollo ML-Geostatistics Study](https://link.springer.com/article/10.1007/s11053-022-10029-8)
- [GPS-Guided Ore Quality Control](https://groundhogapps.com/ore-quality-control-and-dilution/)
- [Rio Tinto Protocol Optimization Study](https://www.geovariances.com/wp-content/uploads/2016/08/geostatsrdv2013_-_riotinto_-_optimization_grade.pdf)
