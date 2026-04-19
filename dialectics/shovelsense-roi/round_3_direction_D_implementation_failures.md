# Direction D: Implementation Failure Modes in Grade Control Technology

**Question:** What goes wrong when mines deploy grade control technology, and how do you prevent it?

---

## The Failure Pattern Literature

Technology deployments in mining fail at rates that would be unacceptable in other industries. A [systematic review of automation in mining](https://journals.sagepub.com/doi/10.1177/25726668241270486) identifies interoperability and inadequate wireless networks as the most significant technical challenges, but the more insidious failures are organizational: lack of feedback to operators, insufficient training focused on technology rather than operations, and cognitive load that overwhelms human supervisors when systems disagree.

The [Global Mining Guidelines Group](https://gmggroup.org/guideline-for-the-implementation-of-autonomous-systems-in-mining-2/) documents cases where autonomous haulage systems failed catastrophically because remote operation centers could not update truck routes in real time. The pattern repeats: technology works in isolation but fails at integration boundaries.

---

## The Six Failure Modes

### 1. Operator Bypass

Experienced operators develop intuition over decades. When a sensor contradicts that intuition, operators override the system. Studies of [frontline technology adoption](https://www.mining-technology.com/contractors/data/sofvie/pressreleases/5-benefits-to-including-the-frontline-in-the-adoption-process/) show that resistance stems from lack of agency, not ignorance. When users are excluded from development, they find workarounds.

At one Canadian mine, operators routinely reclassified sensor-tagged loads because "the sensor doesn't understand this zone." They were sometimes right---the sensor calibration drifted---but the organization lost the ability to distinguish valid operator judgment from habit-driven override.

**Prevention:** Start in advisory mode. Display sensor recommendations without forcing compliance. Track agreement rates. When operators disagree, investigate why. Build trust before automation.

### 2. Integration Fragmentation

Grade control sensors produce data. Dispatch systems consume data. Block models provide reference data. The mill needs feed data. These systems rarely share a common data model.

[Research on mine reconciliation](https://www.sciencedirect.com/science/article/pii/S2095268617304895) finds that data integration problems arise because material may have been classified by holes/samples or by block models, with cutoff grades determined on different premises. When the sensor says 0.35% Cu and the block model says 0.28% Cu, which wins? Most mines never decide explicitly, leading to inconsistent routing.

**Prevention:** Define the data hierarchy before deployment. Specify which system is authoritative at each decision point. Build automated reconciliation that flags disagreements, not just logs them.

### 3. Calibration Decay

[PGNAA/PFTNA systems](https://www.thermofisher.com/blog/mining/which-pgnaa-pftna-online-analyzer-should-be-used-in-mining/) require ongoing calibration against laboratory assays. Factory calibration on static samples provides initial accuracy, but updating calibration should be based on samples from the same deposit as where the analyzer is used. Without continuous recalibration, measurement drift degrades accuracy over months.

XRF systems face additional challenges from matrix effects---the surrounding mineralogy affects X-ray absorption. As mining advances into different zones, the calibration built on one ore type fails on another.

**Prevention:** Budget for ongoing calibration. Assign responsibility to a specific role (not "the geology team"). Establish drift detection thresholds that trigger recalibration automatically.

### 4. The Set-and-Forget Trap

Mines declare success when the system goes live. Metrics are tracked for the first quarter, then attention shifts. By month 18, nobody can say whether the system is delivering claimed ROI because measurement stopped.

[Innovation in mining](https://www.qmarkets.net/resources/article/innovation-in-mining/) research notes that "promising ideas often lose momentum after pilot phases or become disconnected from business priorities." Without formal governance, the technology becomes infrastructure---assumed to work, never verified.

**Prevention:** Require quarterly performance reviews with comparison to pre-deployment baseline. Make continued operation contingent on demonstrated value, not sunk cost.

### 5. Training Failure

Training provided by sensor vendors focuses on the technology, not the workflow. Operators learn how to read the display but not how to integrate sensor data with their existing decision process. A [CDC study of mining automation](https://stacks.cdc.gov/view/cdc/148735/cdc_148735_DS1.pdf) found that some Australian mines' training was primarily delivered by the system's manufacturer, who focused mainly on technological aspects---which proved insufficient for operational success.

**Prevention:** Develop mine-specific training that addresses decision workflows, not just sensor operation. Include scenarios where sensors disagree with other data sources. Train on failure modes, not just normal operation.

### 6. Success Metric Mismatch

Vendors optimize for adoption metrics: tonnage scanned, sensors deployed, uptime percentage. Mines care about value metrics: misclassification rate, recovery improvement, cost per tonne. When these metrics diverge, the vendor claims success while the mine sees no ROI.

**Prevention:** Define success metrics before deployment. Include them in the contract. Require the vendor to provide measurement infrastructure for the metrics that matter, not just the metrics they can easily track.

---

## Contractual Protection

Contracts should include:

- **Performance guarantees with measurement protocols.** Not just "95% uptime" but "95% classification accuracy against independent validation." The measurement method must be specified.
- **Exit clauses tied to performance.** If accuracy drops below threshold for 90 days, the mine can terminate without penalty.
- **Calibration SLAs.** Vendor is responsible for maintaining accuracy, not just sensor availability.
- **Data ownership.** The mine owns all data generated. The vendor cannot use mine-specific data without permission.
- **Reconciliation requirements.** Vendor provides quarterly reconciliation against independent assay, not just internal consistency checks.

---

## Success Factor Patterns

[Research on scaling pilot projects](https://hbr.org/2021/01/how-to-scale-a-successful-pilot-project) finds that the leap from pilot to full implementation has more to do with people than technology. Mines that succeed:

- Include frontline workers in pilot design, not just rollout
- Run advisory mode before automated mode
- Designate a champion with authority to address problems
- Budget for continuous improvement, not just deployment
- Measure what matters, not what's easy

---

## Implementation Checklist

Regardless of which technology this mine selects, the following 10 actions maximize probability of successful deployment:

| # | Action | Why It Matters |
|---|--------|----------------|
| 1 | **Measure baseline misclassification rate before purchase** | You cannot prove improvement without a baseline. If current F1 > 0.92, no sensor delivers ROI. |
| 2 | **Define success metrics in the contract, with measurement protocols** | Prevents vendor from claiming success on metrics that don't matter to you. |
| 3 | **Include exit clauses tied to performance, not just uptime** | 95% uptime is worthless if accuracy degrades. Protect your ability to exit. |
| 4 | **Start in advisory mode for 6+ months** | Build operator trust. Identify disagreements. Refine calibration before automation. |
| 5 | **Assign a single owner for calibration and drift monitoring** | "The geology team" is nobody. Name a person with accountability. |
| 6 | **Define the data hierarchy before deployment** | When sensor and block model disagree, which wins? Decide now. |
| 7 | **Require vendor training on decision workflows, not just technology** | Operators need to know when to trust the sensor and when to override. |
| 8 | **Budget for ongoing calibration and maintenance** | Sensors decay. Budget 15-20% of annual cost for calibration labor and samples. |
| 9 | **Mandate quarterly performance reviews with go/no-go decisions** | Prevents the set-and-forget trap. Forces continuous measurement. |
| 10 | **Require independent validation before full commitment** | If the vendor cannot provide third-party evidence, run your own trial with belt analyzer ground truth. |

---

## Sources

- [Systematic Review of Automation Impacts in Mining](https://journals.sagepub.com/doi/10.1177/25726668241270486)
- [Global Mining Guidelines Group - Autonomous Systems Implementation](https://gmggroup.org/guideline-for-the-implementation-of-autonomous-systems-in-mining-2/)
- [Mining Technology - Frontline Adoption](https://www.mining-technology.com/contractors/data/sofvie/pressreleases/5-benefits-to-including-the-frontline-in-the-adoption-process/)
- [Canadian Mining Journal - Selling the Technology](https://www.canadianminingjournal.com/featured-article/selling-the-technology-bridging-the-gap-between-innovation-and-the-operational-realities-on-mine-sites/)
- [Proactive Reconciliation in Mining](https://www.sciencedirect.com/science/article/pii/S2095268617304895)
- [Thermo Fisher - PGNAA/PFTNA Selection](https://www.thermofisher.com/blog/mining/which-pgnaa-pftna-online-analyzer-should-be-used-in-mining/)
- [CDC Mining Automation Study](https://stacks.cdc.gov/view/cdc/148735/cdc_148735_DS1.pdf)
- [Innovation in Mining - Industry Trends](https://www.qmarkets.net/resources/article/innovation-in-mining/)
- [Harvard Business Review - Scaling Pilot Projects](https://hbr.org/2021/01/how-to-scale-a-successful-pilot-project)
