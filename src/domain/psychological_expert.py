from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class TherapeuticApproach(str, Enum):
    COGNITIVE_BEHAVIORAL = "cognitive_behavioral"
    PSYCHODYNAMIC = "psychodynamic"
    HUMANISTIC = "humanistic"
    GESTALT = "gestalt"
    DIALECTICAL_BEHAVIORAL = "dialectical_behavioral"
    MINDFULNESS = "mindfulness"
    INTEGRATIVE = "integrative"


class SpecializationArea(str, Enum):
    ANXIETY = "anxiety"
    DEPRESSION = "depression"
    TRAUMA = "trauma"
    RELATIONSHIPS = "relationships"
    ADDICTION = "addiction"
    PERSONALITY_DISORDERS = "personality_disorders"
    EATING_DISORDERS = "eating_disorders"
    CHILD_PSYCHOLOGY = "child_psychology"
    COUPLES_THERAPY = "couples_therapy"
    FAMILY_THERAPY = "family_therapy"


class SessionType(str, Enum):
    INITIAL_ASSESSMENT = "initial_assessment"
    REGULAR_SESSION = "regular_session"
    CRISIS_INTERVENTION = "crisis_intervention"
    PROGRESS_EVALUATION = "progress_evaluation"
    TERMINATION = "termination"


class PsychologicalExpert(BaseModel):
    """A class representing a psychological expert agent with therapeutic capabilities.

    Args:
        id (str): Unique identifier for the expert
        name (str): Name of the expert
        specializations (List[SpecializationArea]): List of psychological specializations
        therapeutic_approaches (List[TherapeuticApproach]): List of therapeutic approaches used
        communication_style (str): Description of the expert's communication style
        ethical_guidelines (str): Description of ethical guidelines and boundaries
        session_protocols (dict): Dictionary of session protocols for different session types
    """

    id: str = Field(description="Unique identifier for the expert")
    name: str = Field(description="Name of the expert")
    specializations: List[SpecializationArea] = Field(
        description="List of psychological specializations"
    )
    therapeutic_approaches: List[TherapeuticApproach] = Field(
        description="List of therapeutic approaches used"
    )
    communication_style: str = Field(
        description="Description of the expert's communication style"
    )
    ethical_guidelines: str = Field(
        description="Description of ethical guidelines and boundaries"
    )
    session_protocols: dict = Field(
        description="Dictionary of session protocols for different session types"
    )

    def __str__(self) -> str:
        return (
            f"PsychologicalExpert(id={self.id}, name={self.name}, "
            f"specializations={self.specializations}, "
            f"therapeutic_approaches={self.therapeutic_approaches})"
        )

    def can_handle_session_type(self, session_type: SessionType) -> bool:
        """Check if the expert is qualified to handle a specific session type."""
        return session_type in self.session_protocols

    def get_session_protocol(self, session_type: SessionType) -> Optional[dict]:
        """Get the protocol for a specific session type."""
        return self.session_protocols.get(session_type)

    def has_specialization(self, specialization: SpecializationArea) -> bool:
        """Check if the expert has a specific specialization."""
        return specialization in self.specializations

    def uses_therapeutic_approach(self, approach: TherapeuticApproach) -> bool:
        """Check if the expert uses a specific therapeutic approach."""
        return approach in self.therapeutic_approaches 