# Asset production batches

Each batch contains 50 separately named, geometrically distinct assets. Color-only swaps do not count as new models. All dimensions are in meters. Shared material identifiers are defined in `tools/assetlib.py`.

| Batch | Scope |
|---|---|
| 01 | Street furniture, seating, bicycle racks, shelters |
| 02 | Traffic control, signs, parking equipment |
| 03 | Passenger vehicles, motorcycles, bicycles, scooters |
| 04 | Waste, recycling, street cleaning |
| 05 | Utility infrastructure, hydrants, HVAC, drains |
| 06 | Hand tools and portable construction tools |
| 07 | Construction machinery and worksite equipment |
| 08 | Trees, shrubs, flowers, planted landscaping |
| 09 | Playground, outdoor fitness and sports fixtures |
| 10 | Storefront displays, vending and food-service fixtures |
| 11 | Residential yard and garden furnishings |
| 12 | Exterior building components |
| 13 | Road, sidewalk and transit infrastructure |
| 14 | Mail, delivery, cargo and logistics |
| 15 | Municipal, commercial and emergency vehicles |
| 16 | Food, drinks, packaging and sidewalk litter |
| 17 | Personal outdoor recreation and everyday carry |
| 18 | Outdoor lighting and decorative civic fixtures |
| 19 | Fences, gates and property boundaries |
| 20 | Waterfront, winter and outdoor event equipment |

## Geometry limits

- Handheld: strictly fewer than 1,000 vertices.
- Person sized and smaller: at most 5,000 vertices.
- Car sized and larger: at most 10,000 vertices.

Both source mesh vertex counts and exported GLB vertex counts must pass. Hard normal and material boundaries may increase exported counts, so authors should retain headroom. Models must have a bottom-centered origin, identity transforms, finite geometry, outward face winding, and no zero-area faces.
