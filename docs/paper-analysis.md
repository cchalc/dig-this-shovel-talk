# ShovelSense Automated Smart Truck Diversion - Paper Analysis

**Source:** Automated-Smart-Truck-Diversions_White-Paper-Aug-2022.pdf
**Author:** Anthony Ponce, MineSense Technologies Ltd.
**Date:** August 2022

---

## Paper Sections Breakdown

### 1. Abstract
- Mining industry faces increasing demand for metals amid declining ore grades
- Traditional methods inadequate for Industry 4.0 transformation
- ShovelSense provides real-time XRF-based grade measurement at point of extraction
- Enables automated truck diversions to proper destinations (crusher, stockpile, waste dump)
- Claims massive efficiency improvements in ore recovery and dilution reduction

### 2. Introduction
- MineSense commercial deployment since 2019
- Company focus: sensor-based ore sorting and data analytics
- Products use X-ray Fluorescence (XRF) technology
- **ShovelSense**: XRF sensors on mining shovel buckets
- **BeltSense**: XRF sensors on conveyor systems
- Compatible with electric rope shovels, hydraulic shovels, front-end loaders

### 3. The ShovelSense System

#### 3.1 Bucket Application Package
- Sensor heads with XRF emitter, detector, and laser
- Sensor Processing Unit (SPU) in protective steel housing
- Multiple sensor heads per bucket for reliability and coverage
- Data aggregated into single stream

#### 3.2 MineSense Edge Controller (MEC)
- Computer located in shovel housing
- Converts element peak intensities to truck grades
- Uses dynamic grade prediction algorithm
- Transmits to Fleet Management System (FMS)
- Human Machine Interface (HMI) for operators
- Cloud connectivity for data analytics

#### 3.3 Functionality Workflow
1. Laser takes continuous distance measurements in empty bucket
2. Material flow detected → XRF emitter/detector activated
3. Continuous element peak intensity data collection
4. Bucket fills → data pushed to SPU
5. SPU aggregates spectra from multiple heads
6. MEC performs grade/classification calculations
7. Results sent to HMI, FMS, and cloud

### 4. ShovelSense Truck Diversions

#### 4.1 Fleet Management Integration
- Bucket data aggregated to produce truck classification
- Configurable material designations:
  - Simple Ore/Waste cutoffs
  - Grade bins (High/Medium/Low)
  - Acid-generating vs non-acid-generating waste
  - Net Smelter Return (NSR) calculations
- API integration with major FMS vendors:
  - Caterpillar
  - Modular Mining
  - Wenco
  - Custom in-house systems

#### 4.2 Use Cases

**Ore Loss Reduction ("Ore from Waste")**
- Recovers economic material erroneously routed to waste
- Addresses: orebody complexity, blast movement, grade interpolation limits
- Provides greater resolution than traditional block modeling

**Dilution Control ("Waste from Ore")**
- Removes waste material from ore stream
- Addresses same challenges as ore loss
- Both use cases visualized through diversion tracking

### 5. Case Study: Copper-Porphyry Deposit (South America)

**Study Parameters:**
- 80 days of operation
- Single shovel, single bench
- 6,270 trucks evaluated

**Results:**
| Classification | Count | Percentage |
|----------------|-------|------------|
| Aligned Ore | 3,833 | 61.1% |
| Aligned Waste | 1,740 | 27.8% |
| Ore → Waste (Dilution) | 294 | 4.7% |
| Waste → Ore (Ore Loss) | 403 | 6.4% |
| **Total Diversions** | **697** | **~11%** |

**Key Findings:**
- Hidden barren dyke detected within mineralized zone (15 diversions)
- Blast movement effects successfully identified (~35 diversions)
- Additional revenue exceeding $2M USD claimed

### 6. Conclusion
- ShovelSense enables "digital smart mining" at extraction face
- Real-time bucket-level ore characterization
- Automated truck routing minimizes ore loss and dilution
- 11% truck diversion rate in case study

---

## Related Academic Research

### XRF and Ore Sorting Technology

1. **[Deployment of XRF Sensors Underground](https://www.mdpi.com/2075-163X/13/5/672)**
   - Grade monitoring and bulk ore sorting in cave mines
   - Addresses XRF sensor deployment challenges underground

2. **[Assessing XRF Surface Analysis for Copper Ore Classification](https://journals.sagepub.com/doi/10.1177/25726838251343415)** (Es-sahly et al., 2025)
   - High-grade vs low-grade classification using XRF
   - Surface analysis limitations in volumetric grade estimation

3. **[Ore Sorting Automation for Copper Mining with Advanced XRF Technology](https://www.researchgate.net/publication/350372489_Ore_Sorting_Automation_for_Copper_Mining_with_Advanced_XRF_Technology_From_Theory_to_Case_Study)**
   - Theory to case study approach
   - XRF automation implementation

4. **[Enhancing XRF Sensor-Based Sorting Using PSO-SVM](https://www.sciencedirect.com/science/article/pii/S2095268624000454)**
   - Particle Swarm Optimization + Support Vector Machine
   - Porphyritic copper ore sorting improvement

5. **[Sensor-Based Ore Sorting Technology: Past, Present and Future](https://www.mdpi.com/2075-163X/9/9/523)**
   - Comprehensive review of sensor-based sorting
   - Multiple sensor types and applications

6. **[A Review of Sensor-Based Sorting: Potential Benefits of Sensor Fusion](https://www.mdpi.com/2075-163X/12/11/1364)**
   - Multi-sensor integration approaches
   - Benefits of combining sensing modalities

### Mining Fleet Management and Truck Routing

7. **[OpenMines: Mining Simulation for Truck Dispatching](https://arxiv.org/abs/2404.00622)** (arXiv 2404.00622)
   - Open-source discrete event simulation
   - Algorithm comparison for mine fleet management
   - Shortest queue and nearest distance principles

8. **[Revolutionizing Open-Pit Mining Fleet Management](https://www.mdpi.com/2076-3417/15/9/4603)**
   - Computer vision + multi-objective optimization
   - Real-time truck dispatching

9. **[Heuristics for Vehicle Routing Problem: Survey](https://arxiv.org/pdf/2303.04147)** (arXiv)
   - Genetic algorithms, simulated annealing
   - Metaheuristic methods for VRP

10. **[Deep Reinforcement Learning for Fleet Size and Mix VRP](https://arxiv.org/abs/2512.24251)** (arXiv 2512.24251)
    - Heterogeneous vehicle fleet optimization
    - Capacity and cost considerations

### Ore Dilution and Machine Learning

11. **[Predicting Dilution with Stacking AI Models and Genetic Algorithms](https://www.mdpi.com/2076-3417/15/11/5996)**
    - Eight supervised ML algorithms evaluated
    - Genetic algorithm hyperparameter optimization

12. **[Dilution Prediction Using Gene Expression Programming and BPNN](https://journals.sagepub.com/doi/10.1177/25726668251348707)** (Chimunhu et al., 2025)
    - GEP model: R² = 0.740, RMSE = 0.361
    - BPNN model: R² = 0.681, RMSE = 0.409

13. **[Deep Learning for Ore Classification by XRF Data Fusion](https://www.sciencedirect.com/science/article/abs/pii/S0026265X25038561)**
    - Double-stream heterogeneous data fusion
    - Improved classification accuracy

14. **[Rock Classification through Knowledge-Enhanced Deep Learning](https://arxiv.org/html/2510.13937)** (arXiv)
    - Hybrid mineral-based approach
    - 1D-CNN for Raman spectroscopy analysis

15. **[Integrated Ore Classification Using ML Algorithms](https://www.nature.com/articles/s41598-026-42248-x)** (Scientific Reports)
    - Stand-alone and hybridized methods
    - Multi-parameter grade prediction

### Industry 4.0 and Digital Mining

16. **[Deep Learning in Industrial Internet of Things](https://arxiv.org/pdf/2008.06701)** (arXiv)
    - IIoT architecture and applications
    - Smart manufacturing integration

17. **[Industrial IoT Intelligence for Smart Manufacturing](https://arxiv.org/html/2312.16174v1)** (arXiv)
    - Literature review on IIoT
    - Equipment, network, software, model optimization layers

18. **[IoT-Enabled Smart Mining for Sustainable Mineral Processing](https://www.researchgate.net/publication/397319616_IOT-ENABLED_SMART_MINING_LEVERAGING_REAL-TIME_DATA_ANALYTICS_AND_INFORMATION_SYSTEMS_FOR_SUSTAINABLE_MINERAL_PROCESSING)**
    - Real-time data analytics
    - Information systems integration

19. **[Exploring Digital Twin Systems in Mining Operations](https://www.sciencedirect.com/science/article/pii/S2950555024000582)**
    - Digital twin technology review
    - Mining operations applications

20. **[Low-Cost Sensors for Mining Sustainability and Safety](https://pmc.ncbi.nlm.nih.gov/articles/PMC10422650/)**
    - Digitalization for smart mining
    - Sensor technology advances and gaps

---

## Key Research Themes

| Theme | White Paper Coverage | Related Research |
|-------|---------------------|------------------|
| XRF Technology | Core sensing method | Papers 1-6 |
| Fleet Management | FMS API integration | Papers 7-10 |
| Ore/Waste Classification | Grade bins, NSR | Papers 11-15 |
| Real-time Analytics | MEC, cloud platform | Papers 16-20 |
| Dilution/Ore Loss | Primary use cases | Papers 11-12 |

---

## References from Original Paper

1. Andrew Hall, MineSense Technologies, Ltd.
2. Marinin, M.; Marinina, O.; Wolniak, R. (2021). *Assessing of Losses and Dilution Impact on the Cost Chain: Case Study of Gold Ore Deposits.* Sustainability, 13, 3830. https://doi.org/10.3390/su13073830
3. Câmara, T. R., & Peroni, R. de. (2016). *Quantifying dilution caused by execution efficiency.* REM - International Engineering Journal, 69(4), 487–490. https://doi.org/10.1590/0370-44672014690006
