from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class SourceType(str, Enum):
    RESEARCH_DATABASE = "research_database"
    PROFESSIONAL_GUIDELINE = "professional_guideline"
    TREATMENT_PROTOCOL = "treatment_protocol"
    CLINICAL_DOCUMENT = "clinical_document"
    CASE_STUDY = "case_study"
    ETHICAL_GUIDELINE = "ethical_guideline"
    LEGAL_FRAMEWORK = "legal_framework"


class SourceAccess(BaseModel):
    """Represents access configuration for a data source."""
    requires_auth: bool = False
    api_key: Optional[str] = None
    credentials: Optional[Dict[str, str]] = None
    rate_limit: Optional[int] = None
    cache_duration: Optional[int] = None  # in seconds


class DataSource(BaseModel):
    """Represents a data source for training and RAG."""
    id: str
    name: str
    type: SourceType
    description: str
    url: str
    access: SourceAccess
    specializations: List[str] = Field(default_factory=list)
    therapeutic_approaches: List[str] = Field(default_factory=list)
    last_updated: Optional[str] = None
    version: Optional[str] = None
    reliability_score: float = Field(default=1.0, ge=0.0, le=1.0)
    is_active: bool = True


# Research Databases
RESEARCH_DATABASES = [
    DataSource(
        id="pubmed",
        name="PubMed Central",
        type=SourceType.RESEARCH_DATABASE,
        description="Open access medical and psychological research database",
        url="https://www.ncbi.nlm.nih.gov/pmc/",
        access=SourceAccess(requires_auth=False),
        specializations=["all"],
        therapeutic_approaches=["all"],
        reliability_score=0.95,
    ),
    DataSource(
        id="psycinfo",
        name="PsycINFO",
        type=SourceType.RESEARCH_DATABASE,
        description="American Psychological Association's database",
        url="https://www.apa.org/pubs/databases/psycinfo",
        access=SourceAccess(requires_auth=True),
        specializations=["all"],
        therapeutic_approaches=["all"],
        reliability_score=0.98,
    ),
]

# Professional Guidelines
PROFESSIONAL_GUIDELINES = [
    DataSource(
        id="apa_guidelines",
        name="APA Guidelines",
        type=SourceType.PROFESSIONAL_GUIDELINE,
        description="American Psychological Association Clinical Practice Guidelines",
        url="https://www.apa.org/practice/guidelines",
        access=SourceAccess(requires_auth=True),
        specializations=["all"],
        therapeutic_approaches=["all"],
        reliability_score=0.99,
    ),
    DataSource(
        id="who_mental_health",
        name="WHO Mental Health Guidelines",
        type=SourceType.PROFESSIONAL_GUIDELINE,
        description="World Health Organization Mental Health Guidelines",
        url="https://www.who.int/mental_health/",
        access=SourceAccess(requires_auth=False),
        specializations=["all"],
        therapeutic_approaches=["all"],
        reliability_score=0.97,
    ),
]

# Treatment Protocols
TREATMENT_PROTOCOLS = [
    DataSource(
        id="cbt_manual",
        name="CBT Treatment Manual",
        type=SourceType.TREATMENT_PROTOCOL,
        description="Evidence-based CBT treatment protocols",
        url="https://www.apa.org/pubs/books/cbt-manual",
        access=SourceAccess(requires_auth=True),
        specializations=["anxiety", "depression", "trauma"],
        therapeutic_approaches=["cbt"],
        reliability_score=0.96,
    ),
    DataSource(
        id="dbt_skills",
        name="DBT Skills Manual",
        type=SourceType.TREATMENT_PROTOCOL,
        description="Dialectical Behavior Therapy skills training manual",
        url="https://www.apa.org/pubs/books/dbt-manual",
        access=SourceAccess(requires_auth=True),
        specializations=["personality_disorders", "trauma"],
        therapeutic_approaches=["dbt"],
        reliability_score=0.95,
    ),
]

# Clinical Documentation
CLINICAL_DOCUMENTS = [
    DataSource(
        id="assessment_templates",
        name="Clinical Assessment Templates",
        type=SourceType.CLINICAL_DOCUMENT,
        description="Standardized clinical assessment forms and templates",
        url="https://www.apa.org/practice/assessment",
        access=SourceAccess(requires_auth=True),
        specializations=["all"],
        therapeutic_approaches=["all"],
        reliability_score=0.94,
    ),
    DataSource(
        id="progress_notes",
        name="Progress Note Templates",
        type=SourceType.CLINICAL_DOCUMENT,
        description="Standardized progress note templates",
        url="https://www.apa.org/practice/notes",
        access=SourceAccess(requires_auth=True),
        specializations=["all"],
        therapeutic_approaches=["all"],
        reliability_score=0.93,
    ),
]

# Case Studies
CASE_STUDIES = [
    DataSource(
        id="clinical_cases",
        name="Clinical Case Database",
        type=SourceType.CASE_STUDY,
        description="Anonymized clinical cases and treatment outcomes",
        url="https://www.apa.org/practice/cases",
        access=SourceAccess(requires_auth=True),
        specializations=["all"],
        therapeutic_approaches=["all"],
        reliability_score=0.92,
    ),
]

# Ethical Guidelines
ETHICAL_GUIDELINES = [
    DataSource(
        id="apa_ethics",
        name="APA Ethical Guidelines",
        type=SourceType.ETHICAL_GUIDELINE,
        description="American Psychological Association Ethical Guidelines",
        url="https://www.apa.org/ethics",
        access=SourceAccess(requires_auth=False),
        specializations=["all"],
        therapeutic_approaches=["all"],
        reliability_score=1.0,
    ),
]

# Legal Framework
LEGAL_FRAMEWORK = [
    DataSource(
        id="hipaa",
        name="HIPAA Guidelines",
        type=SourceType.LEGAL_FRAMEWORK,
        description="Health Insurance Portability and Accountability Act",
        url="https://www.hhs.gov/hipaa",
        access=SourceAccess(requires_auth=False),
        specializations=["all"],
        therapeutic_approaches=["all"],
        reliability_score=1.0,
    ),
]

# Combine all sources
ALL_SOURCES = (
    RESEARCH_DATABASES
    + PROFESSIONAL_GUIDELINES
    + TREATMENT_PROTOCOLS
    + CLINICAL_DOCUMENTS
    + CASE_STUDIES
    + ETHICAL_GUIDELINES
    + LEGAL_FRAMEWORK
)

# Create lookup dictionaries
SOURCES_BY_ID = {source.id: source for source in ALL_SOURCES}
SOURCES_BY_TYPE = {
    source_type: [s for s in ALL_SOURCES if s.type == source_type]
    for source_type in SourceType
}
SOURCES_BY_SPECIALIZATION = {}
SOURCES_BY_APPROACH = {}

# Build specialization and approach indices
for source in ALL_SOURCES:
    for spec in source.specializations:
        if spec not in SOURCES_BY_SPECIALIZATION:
            SOURCES_BY_SPECIALIZATION[spec] = []
        SOURCES_BY_SPECIALIZATION[spec].append(source)
    
    for approach in source.therapeutic_approaches:
        if approach not in SOURCES_BY_APPROACH:
            SOURCES_BY_APPROACH[approach] = []
        SOURCES_BY_APPROACH[approach].append(source) 