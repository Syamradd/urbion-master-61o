"""Planning-guideline intelligence for Melaka-first screening.

This is a source-aware applicability catalogue, not a substitute for the
adopted local plan or agency approval. It deliberately distinguishes a
potentially relevant guideline from a verified applicable control.
"""
from __future__ import annotations
from typing import Any

GUIDELINES = [
    {"id":"GPP_PERDAGANGAN","title":"Garis Panduan Perancangan Kawasan Perdagangan","scope":["Commercial","Mixed Use","TOD Development / Mixed Use","Free Standing Building"],"topics":["site planning","commercial uses","access","parking"],"source":"MyTownNet / PLANMalaysia","url":"https://mytownnet.planmalaysia.gov.my/ver2/gp/GPP_PERDAGANGAN.pdf","status":"SOURCE_CONTEXT"},
    {"id":"GPP_TLK","title":"Garis Panduan Perancangan Tempat Letak Kenderaan","scope":["Commercial","Mixed Use","TOD Development / Mixed Use","Residential"],"topics":["parking","accessibility","safety"],"source":"MyTownNet / PLANMalaysia","url":"https://mytownnet.planmalaysia.gov.my/wp-content/uploads/2023/11/GARIS-PANDUAN-PERANCANGAN-TEMPAT-LETAK-KENDERAAN-PLANMalaysia-GP011-A.pdf","status":"SOURCE_CONTEXT"},
    {"id":"GPP_KEMUDAHAN_MASYARAKAT","title":"Garis Panduan Perancangan Kemudahan Masyarakat","scope":["Institutional","Recreation","Mixed Use","Commercial"],"topics":["community facilities","accessibility","emergency response","green technology"],"source":"MyTownNet / PLANMalaysia","url":"https://mytownnet.planmalaysia.gov.my/ver2/gp/GPP%20KEMUDAHAN%20MASYARAKAT%20%28GP004-A.2022%29.pdf","status":"SOURCE_CONTEXT"},
    {"id":"GPP_TAPAK_PERKHEMAHAN","title":"Garis Panduan Perancangan Tapak Perkhemahan","scope":["Recreation","Tourism"],"topics":["recreation","environment","site planning"],"source":"MyTownNet / PLANMalaysia","url":"https://mytownnet.planmalaysia.gov.my/wp-content/uploads/2023/12/GARIS-PANDUAN-PERANCANGAN-TAPAK-PERKHEMAHAN_03052024-1.pdf","status":"SOURCE_CONTEXT"},
]

def build_guideline_intelligence(development_type: str = "", development_class: str = "", topics: list[str] | None = None, pbt: str = "Majlis Bandaraya Melaka Bersejarah") -> dict[str, Any]:
    text = f"{development_type} {development_class}".lower()
    requested = {str(x).lower() for x in (topics or [])}
    matches=[]
    for g in GUIDELINES:
        scope_hit = not g["scope"] or any(s.lower() in text or s.lower() == development_class.lower() for s in g["scope"])
        topic_hit = not requested or bool(requested.intersection({x.lower() for x in g["topics"]}))
        if scope_hit or topic_hit:
            reason=[]
            if scope_hit: reason.append("development_scope")
            if topic_hit: reason.append("topic_match")
            matches.append({**g,"match_reason":reason,"applicability":"CANDIDATE_REVIEW"})
    return {"version":"MASTER-228","jurisdiction":pbt,"guidelines":matches,"candidate_count":len(matches),"decision_boundary":"GUIDELINE_APPLICABILITY_SUPPORT","statutory_verification":"NOT_CLAIMED","disclaimer":"Guideline catalogue identifies potentially relevant PLANMalaysia references. Confirm adopted status, local PBT/state applicability, current edition and project-specific conditions before treating any item as a control."}
