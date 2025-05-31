from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from .psychological_expert import PsychologicalExpert, SessionType


class SessionState(BaseModel):
    """Represents the current state of a therapy session."""
    session_id: str = Field(default_factory=lambda: str(uuid4()))
    expert_id: str
    client_id: str
    session_type: SessionType
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    current_focus: str
    progress_notes: List[str] = Field(default_factory=list)
    risk_level: int = Field(default=0, ge=0, le=10)  # 0-10 scale
    completed_steps: List[str] = Field(default_factory=list)
    next_steps: List[str] = Field(default_factory=list)
    homework_assigned: List[str] = Field(default_factory=list)
    session_summary: Optional[str] = None


class ClientHistory(BaseModel):
    """Represents a client's therapy history."""
    client_id: str
    sessions: List[SessionState] = Field(default_factory=list)
    treatment_goals: List[str] = Field(default_factory=list)
    risk_assessments: List[Dict] = Field(default_factory=list)
    progress_metrics: Dict[str, List[float]] = Field(default_factory=dict)
    emergency_contacts: List[Dict] = Field(default_factory=list)


class SessionManager:
    """Manages therapy sessions and client history."""

    def __init__(self):
        self._active_sessions: Dict[str, SessionState] = {}
        self._client_histories: Dict[str, ClientHistory] = {}

    def start_session(
        self,
        expert: PsychologicalExpert,
        client_id: str,
        session_type: SessionType,
        initial_focus: str,
    ) -> SessionState:
        """Start a new therapy session.

        Args:
            expert: The psychological expert conducting the session
            client_id: The client's unique identifier
            session_type: The type of session to conduct
            initial_focus: The initial focus area for the session

        Returns:
            SessionState: The created session state
        """
        session = SessionState(
            expert_id=expert.id,
            client_id=client_id,
            session_type=session_type,
            current_focus=initial_focus,
        )
        self._active_sessions[session.session_id] = session
        return session

    def end_session(self, session_id: str, summary: str) -> SessionState:
        """End an active therapy session.

        Args:
            session_id: The ID of the session to end
            summary: A summary of the session

        Returns:
            SessionState: The completed session state
        """
        if session_id not in self._active_sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self._active_sessions[session_id]
        session.end_time = datetime.now()
        session.session_summary = summary

        # Update client history
        if session.client_id not in self._client_histories:
            self._client_histories[session.client_id] = ClientHistory(
                client_id=session.client_id
            )
        self._client_histories[session.client_id].sessions.append(session)

        # Remove from active sessions
        del self._active_sessions[session_id]
        return session

    def update_session_progress(
        self,
        session_id: str,
        progress_note: str,
        risk_level: Optional[int] = None,
        completed_step: Optional[str] = None,
        next_step: Optional[str] = None,
        homework: Optional[str] = None,
    ) -> SessionState:
        """Update the progress of an active session.

        Args:
            session_id: The ID of the session to update
            progress_note: A note about the session progress
            risk_level: Updated risk level (0-10)
            completed_step: A step that was completed
            next_step: A step to be completed next
            homework: Homework assignment

        Returns:
            SessionState: The updated session state
        """
        if session_id not in self._active_sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self._active_sessions[session_id]
        session.progress_notes.append(progress_note)

        if risk_level is not None:
            session.risk_level = risk_level
        if completed_step:
            session.completed_steps.append(completed_step)
        if next_step:
            session.next_steps.append(next_step)
        if homework:
            session.homework_assigned.append(homework)

        return session

    def get_client_history(self, client_id: str) -> Optional[ClientHistory]:
        """Get a client's therapy history.

        Args:
            client_id: The client's unique identifier

        Returns:
            Optional[ClientHistory]: The client's history if found
        """
        return self._client_histories.get(client_id)

    def update_treatment_goals(
        self, client_id: str, goals: List[str]
    ) -> ClientHistory:
        """Update a client's treatment goals.

        Args:
            client_id: The client's unique identifier
            goals: List of treatment goals

        Returns:
            ClientHistory: The updated client history
        """
        if client_id not in self._client_histories:
            self._client_histories[client_id] = ClientHistory(client_id=client_id)
        self._client_histories[client_id].treatment_goals = goals
        return self._client_histories[client_id]

    def add_risk_assessment(
        self, client_id: str, assessment: Dict
    ) -> ClientHistory:
        """Add a risk assessment to a client's history.

        Args:
            client_id: The client's unique identifier
            assessment: The risk assessment data

        Returns:
            ClientHistory: The updated client history
        """
        if client_id not in self._client_histories:
            self._client_histories[client_id] = ClientHistory(client_id=client_id)
        self._client_histories[client_id].risk_assessments.append(assessment)
        return self._client_histories[client_id]

    def update_progress_metrics(
        self, client_id: str, metric_name: str, value: float
    ) -> ClientHistory:
        """Update a client's progress metrics.

        Args:
            client_id: The client's unique identifier
            metric_name: The name of the metric
            value: The metric value

        Returns:
            ClientHistory: The updated client history
        """
        if client_id not in self._client_histories:
            self._client_histories[client_id] = ClientHistory(client_id=client_id)
        if metric_name not in self._client_histories[client_id].progress_metrics:
            self._client_histories[client_id].progress_metrics[metric_name] = []
        self._client_histories[client_id].progress_metrics[metric_name].append(value)
        return self._client_histories[client_id]

    def get_active_sessions(self) -> List[SessionState]:
        """Get all active sessions.

        Returns:
            List[SessionState]: List of active sessions
        """
        return list(self._active_sessions.values())

    def get_session(self, session_id: str) -> Optional[SessionState]:
        """Get a specific session by ID.

        Args:
            session_id: The session ID to retrieve

        Returns:
            Optional[SessionState]: The session if found
        """
        return self._active_sessions.get(session_id) 