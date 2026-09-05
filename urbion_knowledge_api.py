"""Knowledge retrieval API: traceable context, never statutory verification."""
from fastapi import APIRouter
from pydantic import BaseModel, Field
from urbion_knowledge_orchestrator import build_knowledge_pack

router = APIRouter(tags=["knowledge"])

class KnowledgeRequest(BaseModel):
    development_type: str = Field(min_length=1, max_length=120)
    authority: str = Field(default="MBMB", min_length=1, max_length=80)
    spatial_context: dict = Field(default_factory=dict)

@router.post("/knowledge/retrieve")
def retrieve_knowledge(payload: KnowledgeRequest):
    return build_knowledge_pack(payload.development_type, payload.authority, payload.spatial_context)
