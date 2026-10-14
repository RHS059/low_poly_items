# Collection revision

All 1,000 original assets were reviewed across the 20 production categories by six Astra xhigh agents and the integrating author. 560 received geometry revisions; 440 were retained with review reasons where their existing shape and construction were appropriate. The original filenames are preserved. An additional 50 modular building parts brings the collection to 1,050 assets.

Per-model decisions are indexed in [revision_review/index.json](revision_review/index.json). Category ledgers record the shape changes and isolated validation evidence. Final authoritative geometry counts are in [manifest.json](manifest.json), with the complete integrated checks in [validation_report.json](validation_report.json). Exported-geometry contact sheets and individual images are regenerated in [previews/](previews/).

## Main changes

- Passenger vehicles: shaped longitudinal body sections, real wheel openings, recessed/framed glass, formed fascias, detailed dished wheels and fitted trim.
- Commercial vehicles and construction machines: tapered cab/hood sections, fenders, wheel/track mechanisms, shaped working attachments and functional openings.
- Furniture, waste, storefronts and logistics: formed housings, proper apertures, upholstery/fabric profiles, corrected support/hinge connections and more complete mechanisms.
- Utilities, tools and lighting: shaped grips, fan and vent openings, lamp optics/mounts, frame reveals and service hardware.
- Vegetation, playground and road fixtures: branched/asymmetric crowns, formed seats/chutes, operating joints, rail sections and ramp details.
- Handheld objects: shaped footwear, food, packaging and bags while preserving the strict under-1,000-vertex limit.
- Viewer: models cast floor shadows but do not receive artifact-prone self-shadow maps. A real Chromium check loads the exported GLBs and exercises search, rotate, pan, reset and navigation.
- Building kit: 50 interoperable walls, floors, ceilings, doors and windows, with a Blender assembly example and placement guide in [BUILDING_KIT.md](BUILDING_KIT.md).

Budgets remain ceilings, not subdivision targets: large ≤10,000 exported vertices; person-sized ≤5,000; handheld ≤999. Revisions use topology for visible form and construction, retaining economical geometry for simple slabs, rails and similar objects.
