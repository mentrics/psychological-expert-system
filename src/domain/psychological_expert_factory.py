import json
from pathlib import Path
from typing import List, Optional

from .psychological_expert import (
    PsychologicalExpert,
    SpecializationArea,
    TherapeuticApproach,
    SessionType,
)


class PsychologicalExpertFactory:
    """Factory class for creating and managing psychological experts."""

    def __init__(self, experts_data_path: Path):
        """Initialize the factory with the path to experts data.

        Args:
            experts_data_path (Path): Path to the JSON file containing expert data
        """
        self.experts_data_path = experts_data_path
        self._experts: List[PsychologicalExpert] = []
        self._load_experts()

    def _load_experts(self) -> None:
        """Load experts from the data file."""
        if not self.experts_data_path.exists():
            raise FileNotFoundError(
                f"Experts data file not found at {self.experts_data_path}"
            )

        with open(self.experts_data_path, "r") as f:
            experts_data = json.load(f)

        for expert_data in experts_data:
            # Convert string values to enums
            expert_data["specializations"] = [
                SpecializationArea(s) for s in expert_data["specializations"]
            ]
            expert_data["therapeutic_approaches"] = [
                TherapeuticApproach(t) for t in expert_data["therapeutic_approaches"]
            ]
            
            # Create expert instance
            expert = PsychologicalExpert(**expert_data)
            self._experts.append(expert)

    def get_expert_by_id(self, expert_id: str) -> Optional[PsychologicalExpert]:
        """Get an expert by their ID.

        Args:
            expert_id (str): The ID of the expert to retrieve

        Returns:
            Optional[PsychologicalExpert]: The expert if found, None otherwise
        """
        for expert in self._experts:
            if expert.id == expert_id:
                return expert
        return None

    def get_experts_by_specialization(
        self, specialization: SpecializationArea
    ) -> List[PsychologicalExpert]:
        """Get all experts with a specific specialization.

        Args:
            specialization (SpecializationArea): The specialization to filter by

        Returns:
            List[PsychologicalExpert]: List of experts with the specified specialization
        """
        return [
            expert for expert in self._experts if expert.has_specialization(specialization)
        ]

    def get_experts_by_therapeutic_approach(
        self, approach: TherapeuticApproach
    ) -> List[PsychologicalExpert]:
        """Get all experts using a specific therapeutic approach.

        Args:
            approach (TherapeuticApproach): The therapeutic approach to filter by

        Returns:
            List[PsychologicalExpert]: List of experts using the specified approach
        """
        return [
            expert
            for expert in self._experts
            if expert.uses_therapeutic_approach(approach)
        ]

    def get_experts_for_session_type(
        self, session_type: SessionType
    ) -> List[PsychologicalExpert]:
        """Get all experts qualified to handle a specific session type.

        Args:
            session_type (SessionType): The session type to filter by

        Returns:
            List[PsychologicalExpert]: List of experts qualified for the session type
        """
        return [
            expert
            for expert in self._experts
            if expert.can_handle_session_type(session_type)
        ]

    def get_all_experts(self) -> List[PsychologicalExpert]:
        """Get all available experts.

        Returns:
            List[PsychologicalExpert]: List of all experts
        """
        return self._experts.copy() 