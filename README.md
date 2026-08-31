# URBION MASTER-61O

AI-Assisted Development Control and Spatial Decision Support System.

ARCHITECTURE
User / Web Interface
        ->
FastAPI Backend
        ->
GIS Spatial Engine
        ->
Planning Rule Retrieval
        ->
Applicability Engine
        ->
Compliance Engine
        ->
Explainable Planning Decision

API ENDPOINTS
GET /health
POST /assess

VERIFIED TEST
Site: 2.290, 102.138
TOD: 2.291, 102.138
Distance: 111.19 m
Classification: TOD 400m
Rule: RT-MBMB-2035-TOD-01
Decision: COMPLY

GIS: CONNECTED
Retrieval: CONNECTED
Applicability: CONNECTED
Compliance: CONNECTED

External authoritative GIS APIs are not directly connected.

Deployment target: Public FastAPI hosting.