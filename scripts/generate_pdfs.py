"""
Generate synthetic PDF documents for RAG testing related to mining operations.

This creates technical documentation, geological reports, and validation studies
that would be relevant for a ShovelSense deployment.
"""
import os
import subprocess
import json

# Configuration
CATALOG = os.environ.get("CATALOG", "ai_dev_kit")
SCHEMA = os.environ.get("SCHEMA", "shovelsense")

# Document categories to generate
DOCUMENT_SPECS = [
    {
        "description": """
Technical documentation for XRF-based ore grade measurement systems in open-pit copper mining operations, including:
- XRF sensor calibration procedures and maintenance schedules
- Measurement accuracy specifications and confidence interval calculations
- Sensor head configuration for different bucket types (electric rope shovels, hydraulic excavators)
- Data processing algorithms for real-time grade estimation
- Integration protocols with Fleet Management Systems (FMS)
- Troubleshooting guides for common sensor failures
- Environmental factors affecting XRF accuracy (moisture, dust, temperature)
""",
        "count": 8,
        "folder": "technical_docs",
        "doc_size": "MEDIUM"
    },
    {
        "description": """
Geological survey reports and block model documentation for a copper-porphyry deposit, including:
- Orebody characterization with copper, iron, zinc, and arsenic grade distributions
- Geological domain definitions (porphyry core, supergene enrichment, leached cap)
- Blast movement analysis and material displacement patterns
- Grade control sampling protocols and blasthole assay procedures
- Block model reconciliation reports comparing planned vs actual grades
- Dyke and fault identification affecting ore continuity
- Cutoff grade optimization studies
""",
        "count": 6,
        "folder": "geological_reports",
        "doc_size": "LARGE"
    },
    {
        "description": """
Validation and verification studies for automated truck diversion systems in mining, including:
- Statistical analysis of diversion accuracy (confusion matrices, precision/recall)
- Baseline comparison methodologies (manual vs automated classification)
- Mill head grade reconciliation procedures
- Economic impact assessment frameworks
- False positive/negative rate analysis
- Downstream grade verification protocols
- Independent third-party audit procedures
""",
        "count": 5,
        "folder": "validation_studies",
        "doc_size": "MEDIUM"
    },
    {
        "description": """
Mining operations procedures and safety documentation, including:
- Truck dispatching and routing optimization protocols
- Shift handover procedures for grade control personnel
- Emergency response for sensor system failures
- Cybersecurity guidelines for industrial control systems
- Data governance and audit trail requirements
- Operator training materials for HMI interfaces
- Change management procedures for technology adoption
""",
        "count": 5,
        "folder": "operations_procedures",
        "doc_size": "MEDIUM"
    },
    {
        "description": """
Academic research papers and literature reviews on ore sorting and mining technology, including:
- Sensor-based ore sorting technology review (XRF, NIR, electromagnetic)
- Machine learning applications in mineral classification
- Vehicle routing optimization in open-pit mining
- Industry 4.0 and digital transformation in mining
- Dilution control and ore loss mitigation strategies
- Real-time decision systems in mineral processing
""",
        "count": 6,
        "folder": "research_papers",
        "doc_size": "LARGE"
    }
]


def main():
    """Generate all PDF document sets."""
    print("=" * 60)
    print("ShovelSense PDF Document Generation")
    print("=" * 60)
    print(f"Catalog: {CATALOG}")
    print(f"Schema: {SCHEMA}")
    print()

    # Note: This script prepares the configuration for PDF generation
    # The actual generation uses the Databricks MCP tool which should be
    # invoked from Claude Code

    config_output = []

    for spec in DOCUMENT_SPECS:
        config_output.append({
            "catalog": CATALOG,
            "schema": SCHEMA,
            "volume": "pdf_documents",
            "folder": spec["folder"],
            "description": spec["description"].strip(),
            "count": spec["count"],
            "doc_size": spec["doc_size"],
            "overwrite_folder": True
        })

        print(f"\nDocument Set: {spec['folder']}")
        print(f"  Count: {spec['count']}")
        print(f"  Size: {spec['doc_size']}")

    # Save configuration for reference
    os.makedirs("data", exist_ok=True)
    with open("data/pdf_generation_config.json", "w") as f:
        json.dump(config_output, f, indent=2)

    print("\n" + "=" * 60)
    print("CONFIGURATION SAVED")
    print("=" * 60)
    print("PDF generation config saved to: data/pdf_generation_config.json")
    print()
    print("To generate PDFs, use the generate_pdf_documents MCP tool with")
    print("the configurations above. Total documents to generate:")
    print(f"  {sum(s['count'] for s in DOCUMENT_SPECS)} PDFs across {len(DOCUMENT_SPECS)} categories")
    print()
    print("Categories:")
    for spec in DOCUMENT_SPECS:
        print(f"  - {spec['folder']}: {spec['count']} documents")


if __name__ == "__main__":
    main()
