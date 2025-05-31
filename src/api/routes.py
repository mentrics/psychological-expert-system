from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..domain.psychological_expert import (
    PsychologicalExpert,
    SpecializationArea,
    TherapeuticApproach,
    SessionType,
)
from ..domain.psychological_expert_factory import PsychologicalExpertFactory
from ..domain.session_manager import SessionManager, SessionState, ClientHistory

router = APIRouter()
session_manager = SessionManager()
expert_factory = PsychologicalExpertFactory("data/psychological_experts.json")


# --- Expert Selection Endpoints ---

class ExpertResponse(BaseModel):
    id: str
    name: str
    specializations: List[str]
    therapeutic_approaches: List[str]
    communication_style: str


@router.get("/experts", response_model=List[ExpertResponse])
async def get_experts(
    specialization: Optional[SpecializationArea] = None,
    approach: Optional[TherapeuticApproach] = None,
    session_type: Optional[SessionType] = None,
):
    """Get available experts with optional filtering."""
    experts = expert_factory.get_all_experts()
    
    if specialization:
        experts = [e for e in experts if e.has_specialization(specialization)]
    if approach:
        experts = [e for e in experts if e.uses_therapeutic_approach(approach)]
    if session_type:
        experts = [e for e in experts if e.can_handle_session_type(session_type)]
    
    return [
        ExpertResponse(
            id=e.id,
            name=e.name,
            specializations=[s.value for s in e.specializations],
            therapeutic_approaches=[t.value for t in e.therapeutic_approaches],
            communication_style=e.communication_style,
        )
        for e in experts
    ]


@router.get("/experts/{expert_id}", response_model=ExpertResponse)
async def get_expert(expert_id: str):
    """Get a specific expert by ID."""
    expert = expert_factory.get_expert_by_id(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    
    return ExpertResponse(
        id=expert.id,
        name=expert.name,
        specializations=[s.value for s in expert.specializations],
        therapeutic_approaches=[t.value for t in expert.therapeutic_approaches],
        communication_style=expert.communication_style,
    )


# --- Session Management Endpoints ---

class SessionRequest(BaseModel):
    expert_id: str
    client_id: str
    session_type: SessionType
    initial_focus: str


class SessionResponse(BaseModel):
    session_id: str
    expert_id: str
    client_id: str
    session_type: SessionType
    current_focus: str
    progress_notes: List[str]
    risk_level: int
    completed_steps: List[str]
    next_steps: List[str]
    homework_assigned: List[str]


@router.post("/sessions", response_model=SessionResponse)
async def create_session(request: SessionRequest):
    """Start a new therapy session."""
    expert = expert_factory.get_expert_by_id(request.expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    
    if not expert.can_handle_session_type(request.session_type):
        raise HTTPException(
            status_code=400,
            detail=f"Expert {expert.name} cannot handle {request.session_type} sessions",
        )
    
    session = session_manager.start_session(
        expert=expert,
        client_id=request.client_id,
        session_type=request.session_type,
        initial_focus=request.initial_focus,
    )
    
    return SessionResponse(
        session_id=session.session_id,
        expert_id=session.expert_id,
        client_id=session.client_id,
        session_type=session.session_type,
        current_focus=session.current_focus,
        progress_notes=session.progress_notes,
        risk_level=session.risk_level,
        completed_steps=session.completed_steps,
        next_steps=session.next_steps,
        homework_assigned=session.homework_assigned,
    )


class SessionUpdateRequest(BaseModel):
    progress_note: str
    risk_level: Optional[int] = None
    completed_step: Optional[str] = None
    next_step: Optional[str] = None
    homework: Optional[str] = None


@router.put("/sessions/{session_id}", response_model=SessionResponse)
async def update_session(session_id: str, request: SessionUpdateRequest):
    """Update an active session's progress."""
    session = session_manager.update_session_progress(
        session_id=session_id,
        progress_note=request.progress_note,
        risk_level=request.risk_level,
        completed_step=request.completed_step,
        next_step=request.next_step,
        homework=request.homework,
    )
    
    return SessionResponse(
        session_id=session.session_id,
        expert_id=session.expert_id,
        client_id=session.client_id,
        session_type=session.session_type,
        current_focus=session.current_focus,
        progress_notes=session.progress_notes,
        risk_level=session.risk_level,
        completed_steps=session.completed_steps,
        next_steps=session.next_steps,
        homework_assigned=session.homework_assigned,
    )


@router.post("/sessions/{session_id}/end")
async def end_session(session_id: str, summary: str):
    """End an active session."""
    try:
        session = session_manager.end_session(session_id, summary)
        return {"message": "Session ended successfully", "session_id": session.session_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- Client Management Endpoints ---

class ClientHistoryResponse(BaseModel):
    client_id: str
    sessions: List[SessionResponse]
    treatment_goals: List[str]
    risk_assessments: List[dict]
    progress_metrics: dict


@router.get("/clients/{client_id}/history", response_model=ClientHistoryResponse)
async def get_client_history(client_id: str):
    """Get a client's therapy history."""
    history = session_manager.get_client_history(client_id)
    if not history:
        raise HTTPException(status_code=404, detail="Client history not found")
    
    return ClientHistoryResponse(
        client_id=history.client_id,
        sessions=[
            SessionResponse(
                session_id=s.session_id,
                expert_id=s.expert_id,
                client_id=s.client_id,
                session_type=s.session_type,
                current_focus=s.current_focus,
                progress_notes=s.progress_notes,
                risk_level=s.risk_level,
                completed_steps=s.completed_steps,
                next_steps=s.next_steps,
                homework_assigned=s.homework_assigned,
            )
            for s in history.sessions
        ],
        treatment_goals=history.treatment_goals,
        risk_assessments=history.risk_assessments,
        progress_metrics=history.progress_metrics,
    )


class TreatmentGoalsRequest(BaseModel):
    goals: List[str]


@router.put("/clients/{client_id}/goals")
async def update_treatment_goals(client_id: str, request: TreatmentGoalsRequest):
    """Update a client's treatment goals."""
    history = session_manager.update_treatment_goals(client_id, request.goals)
    return {"message": "Treatment goals updated successfully"}


class RiskAssessmentRequest(BaseModel):
    assessment: dict


@router.post("/clients/{client_id}/risk-assessment")
async def add_risk_assessment(client_id: str, request: RiskAssessmentRequest):
    """Add a risk assessment to a client's history."""
    history = session_manager.add_risk_assessment(client_id, request.assessment)
    return {"message": "Risk assessment added successfully"}


class ProgressMetricRequest(BaseModel):
    metric_name: str
    value: float


@router.post("/clients/{client_id}/progress")
async def update_progress_metric(client_id: str, request: ProgressMetricRequest):
    """Update a client's progress metrics."""
    history = session_manager.update_progress_metrics(
        client_id, request.metric_name, request.value
    )
    return {"message": "Progress metric updated successfully"} 