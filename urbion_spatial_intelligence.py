"""Deterministic, evidence-aware spatial intelligence primitives for URBION."""
from __future__ import annotations
import math
EARTH_RADIUS_M = 6_371_000.0


def _coords(lat, lon):
    lat, lon = float(lat), float(lon)
    if not math.isfinite(lat) or not math.isfinite(lon): raise ValueError("coordinates must be finite")
    if not -90 <= lat <= 90 or not -180 <= lon <= 180: raise ValueError("latitude/longitude out of range")
    if (lat, lon) == (-90.0, -180.0): raise ValueError("placeholder coordinates are not allowed")
    return lat, lon


def haversine_m(lat1, lon1, lat2, lon2):
    lat1, lon1 = _coords(lat1, lon1); lat2, lon2 = _coords(lat2, lon2)
    p1, p2 = math.radians(lat1), math.radians(lat2); dp = math.radians(lat2-lat1); dl = math.radians(lon2-lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return EARTH_RADIUS_M * 2 * math.atan2(math.sqrt(a), math.sqrt(max(0.0, 1.0-a)))


def bearing_deg(lat1, lon1, lat2, lon2):
    lat1, lon1 = _coords(lat1, lon1); lat2, lon2 = _coords(lat2, lon2)
    p1, p2 = math.radians(lat1), math.radians(lat2); dl = math.radians(lon2-lon1)
    x = math.sin(dl)*math.cos(p2); y = math.cos(p1)*math.sin(p2)-math.sin(p1)*math.cos(p2)*math.cos(dl)
    return (math.degrees(math.atan2(x,y))+360.0)%360.0


def midpoint(lat1, lon1, lat2, lon2):
    lat1, lon1 = _coords(lat1, lon1); lat2, lon2 = _coords(lat2, lon2)
    p1, p2 = math.radians(lat1), math.radians(lat2); dl = math.radians(lon2-lon1)
    x = math.cos(p2)*math.cos(dl); y = math.cos(p2)*math.sin(dl)
    p3 = math.atan2(math.sin(p1)+math.sin(p2), math.sqrt((math.cos(p1)+x)**2+y**2)); l3 = math.radians(lon1)+math.atan2(y,math.cos(p1)+x)
    return {"latitude":math.degrees(p3),"longitude":((math.degrees(l3)+540)%360)-180}


def destination(lat, lon, distance_m, bearing):
    lat, lon = _coords(lat, lon); distance_m=float(distance_m)
    if not math.isfinite(distance_m) or distance_m<0: raise ValueError("distance_m must be a non-negative finite number")
    theta=math.radians(float(bearing)%360); delta=distance_m/EARTH_RADIUS_M; p1=math.radians(lat); l1=math.radians(lon)
    p2=math.asin(math.sin(p1)*math.cos(delta)+math.cos(p1)*math.sin(delta)*math.cos(theta)); l2=l1+math.atan2(math.sin(theta)*math.sin(delta)*math.cos(p1),math.cos(delta)-math.sin(p1)*math.sin(p2))
    return {"latitude":math.degrees(p2),"longitude":((math.degrees(l2)+540)%360)-180}


def circle_geojson(lat, lon, radius_m, segments=72):
    lat, lon = _coords(lat, lon); radius_m=float(radius_m)
    if not math.isfinite(radius_m) or radius_m<=0: raise ValueError("radius_m must be positive")
    segments=max(24,min(180,int(segments))); ring=[]
    for i in range(segments+1):
        p=destination(lat,lon,radius_m,i*360.0/segments); ring.append([p["longitude"],p["latitude"]])
    return {"type":"Feature","properties":{"radius_m":radius_m,"evidence":"CALCULATED"},"geometry":{"type":"Polygon","coordinates":[ring]}}


def catchment_features(lat, lon, radii=(400,800)):
    lat, lon = _coords(lat, lon); radii=tuple(sorted({int(r) for r in radii if int(r)>0})) or (400,800)
    return {"type":"FeatureCollection","features":[circle_geojson(lat,lon,r) for r in radii],"site":{"latitude":lat,"longitude":lon},"evidence":"CALCULATED","disclaimer":"Catchments are geometric decision-support buffers, not authoritative statutory boundaries."}


def nearest_feature(lat, lon, features):
    lat, lon = _coords(lat, lon); ranked=[]
    for index, feature in enumerate(features or []):
        if not isinstance(feature,dict): continue
        f_lat=feature.get("latitude",feature.get("lat")); f_lon=feature.get("longitude",feature.get("lon"))
        if f_lat is None or f_lon is None: continue
        try: d=haversine_m(lat,lon,f_lat,f_lon)
        except (TypeError,ValueError): continue
        ranked.append((d,index,feature))
    if not ranked: return None
    d,index,feature=min(ranked,key=lambda x:x[0]); return {"index":index,"distance_m":round(d,2),"feature":feature,"evidence":"CALCULATED"}


def proximity_matrix(origins, destinations):
    out=[]
    for oi,o in enumerate(origins or []):
        for di,t in enumerate(destinations or []):
            d=haversine_m(o["latitude"],o["longitude"],t["latitude"],t["longitude"])
            out.append({"origin_index":oi,"destination_index":di,"distance_m":round(d,2),"bearing_deg":round(bearing_deg(o["latitude"],o["longitude"],t["latitude"],t["longitude"]),2),"evidence":"CALCULATED"})
    return out


def constraint_summary(constraints=None):
    items=[]
    for key,raw in (constraints or {}).items():
        if isinstance(raw,bool): state="CONSTRAINT_PRESENT" if raw else "NOT_FLAGGED"
        elif raw in (None,"",[],{}): state="NOT_ASSESSED"
        else: state="CONTEXT_REPORTED"
        items.append({"id":str(key),"value":raw,"state":state,"evidence":"USER_PROVIDED"})
    return {"items":items,"flagged_count":sum(x["state"]=="CONSTRAINT_PRESENT" for x in items),"total":len(items),"evidence":"USER_PROVIDED","decision_boundary":"OBSERVATION_CONTEXT","statutory_verification":"NOT_CLAIMED"}


def _planning_signals(result):
    signals=[]
    tod=result.get("tod")
    if tod:
        signals.append({"id":"tod_access","value":tod["distance_m"],"unit":"m","classification":tod["classification"],"evidence":"CALCULATED","decision_use":"ACCESS_SCREENING"})
    catchments=result.get("catchments",{}).get("features",[])
    signals.append({"id":"catchment_coverage","value":len(catchments),"unit":"buffers","evidence":"CALCULATED","decision_use":"PROXIMITY_SCREENING"})
    constraints=result.get("constraints",{})
    flagged=constraints.get("flagged_count",0)
    signals.append({"id":"constraint_flags","value":flagged,"unit":"flags","evidence":"USER_PROVIDED","decision_use":"REVIEW_PRIORITY"})
    return signals


def build_spatial_intelligence(site_lat, site_lon, tod_lat=None, tod_lon=None, radii=(400,800), constraints=None):
    site_lat,site_lon=_coords(site_lat,site_lon)
    result={"site":{"latitude":site_lat,"longitude":site_lon},"catchments":catchment_features(site_lat,site_lon,radii),"constraints":constraint_summary(constraints),"evidence_model":{"geometry":"CALCULATED","constraints":"USER_PROVIDED","authoritative_overlay":"SOURCE_CONTEXT ONLY"}}
    if tod_lat is not None or tod_lon is not None:
        if tod_lat is None or tod_lon is None: raise ValueError("tod_lat and tod_lon must be provided together")
        tod_lat,tod_lon=_coords(tod_lat,tod_lon)
        d=haversine_m(site_lat,site_lon,tod_lat,tod_lon)
        result["tod"]={"latitude":tod_lat,"longitude":tod_lon,"distance_m":round(d,2),"bearing_deg":round(bearing_deg(site_lat,site_lon,tod_lat,tod_lon),2),"classification":"TOD 400m" if d<=400 else ("TOD 800m" if d<=800 else "OUTSIDE TOD 800m"),"midpoint":midpoint(site_lat,site_lon,tod_lat,tod_lon),"evidence":"CALCULATED"}
    result["planning_signals"]=_planning_signals(result)
    result["review_gaps"]=["Authoritative spatial overlays remain source context until verified."]
    if result["constraints"]["flagged_count"]:
        result["review_gaps"].append("User-provided constraint flags require planner/source verification.")
    return result
