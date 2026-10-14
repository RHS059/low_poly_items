# Item catalog and size-based geometry budgets

All **1,050 items** are listed below: 1,000 outdoor props and 50 modular building pieces. Counts and dimensions come from `manifest.json`. Each item links to its GLB.

## Budget rules

| Size class | Intended scale | Maximum vertices per item | Items |
| --- | --- | ---: | ---: |
| Large | Car-sized and larger objects, large assemblies and building modules | 10,000 | 413 |
| Medium (`person`) | Person-sized and smaller non-handheld props | 5,000 | 457 |
| Handheld | Small objects intended to fit in a hand | 999 (strictly below 1,000) | 180 |

These are size-based ceilings, not a universal 1,000-vertex target. Geometry should support recognizable silhouettes, construction details, and useful bevels; complex large and medium objects have room for more detail. Simple objects can remain below their ceiling without adding redundant geometry. Size classes below reflect the current manifest assignments, including complete assemblies rather than only their individual components.

The original numerical limits were specified in **vertices**. Triangles are reported separately: a triangle count is not interchangeable with a vertex count. **Source vertices** are the Blender mesh count after generation; **GLB vertices** include splits needed for flat normals and material boundaries. The budget applies to the exported vertex count as well as the source count. **Used** is GLB vertices divided by the vertex limit. Dimensions are Blender X × Y × Z in meters.

## Every item

### Accessible Paving (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_directional_ribbed_guidance_paving](exports/b13_directional_ribbed_guidance_paving.glb) | Medium | 0.72 × 1.6 × 0.089 | 5,000 | 288 | 1,152 | 528 | 23.0% |
| [b13_truncated_dome_warning_panel](exports/b13_truncated_dome_warning_panel.glb) | Medium | 1.22 × 0.65 × 0.094 | 5,000 | 856 | 2,568 | 1,424 | 51.4% |

### Accessible Ramp (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_switchback_accessibility_ramp](exports/b13_switchback_accessibility_ramp.glb) | Large | 2.78 × 5.005 × 1.804 | 10,000 | 1,616 | 6,064 | 3,016 | 60.6% |

### Area Lighting (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_stadium_floodlight_mast](exports/b18_stadium_floodlight_mast.glb) | Large | 2.3 × 0.836 × 8.557 | 10,000 | 964 | 2,892 | 1,548 | 28.9% |

### Awning Lighting (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_angled_awning_wash_light](exports/b18_angled_awning_wash_light.glb) | Medium | 1.14 × 0.516 × 0.35 | 5,000 | 352 | 1,376 | 656 | 27.5% |

### Bench (10)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b01_backless_boardwalk_bench](exports/b01_backless_boardwalk_bench.glb) | Medium | 2.15 × 0.54 × 0.535 | 5,000 | 264 | 992 | 484 | 19.8% |
| [b01_cantilever_concrete_bench](exports/b01_cantilever_concrete_bench.glb) | Medium | 2.1 × 0.689 × 1.06 | 5,000 | 188 | 742 | 344 | 14.8% |
| [b01_cast_iron_park_bench](exports/b01_cast_iron_park_bench.glb) | Medium | 1.8 × 0.497 × 1.004 | 5,000 | 720 | 2,208 | 1,264 | 44.2% |
| [b01_curve_segment_park_bench](exports/b01_curve_segment_park_bench.glb) | Medium | 2.83 × 1.023 × 1.021 | 5,000 | 1,648 | 4,944 | 2,784 | 98.9% |
| [b01_double_sided_station_bench](exports/b01_double_sided_station_bench.glb) | Medium | 2.15 × 0.96 × 1.115 | 5,000 | 480 | 1,872 | 884 | 37.4% |
| [b01_hexagonal_tree_bench](exports/b01_hexagonal_tree_bench.glb) | Large | 2.364 × 2.076 × 0.916 | 10,000 | 2,016 | 8,064 | 3,720 | 80.6% |
| [b01_memorial_wood_bench](exports/b01_memorial_wood_bench.glb) | Medium | 1.95 × 0.548 × 1.154 | 5,000 | 684 | 2,120 | 1,144 | 42.4% |
| [b01_perforated_steel_bench](exports/b01_perforated_steel_bench.glb) | Medium | 1.9 × 0.62 × 0.987 | 5,000 | 1,060 | 3,180 | 1,800 | 63.6% |
| [b01_rustic_split_log_bench](exports/b01_rustic_split_log_bench.glb) | Medium | 2.1 × 0.577 × 0.969 | 5,000 | 896 | 3,510 | 1,732 | 70.2% |
| [b01_wave_public_lounge_bench](exports/b01_wave_public_lounge_bench.glb) | Medium | 1.5 × 1.231 × 1.051 | 5,000 | 1,080 | 4,032 | 2,004 | 80.6% |

### Bike Rack (7)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b01_double_hoop_bike_rack](exports/b01_double_hoop_bike_rack.glb) | Medium | 1.705 × 0.18 × 1.027 | 5,000 | 832 | 3,120 | 1,612 | 62.4% |
| [b01_five_slot_wheel_bike_rack](exports/b01_five_slot_wheel_bike_rack.glb) | Medium | 2.34 × 0.98 × 0.621 | 5,000 | 800 | 2,400 | 1,384 | 48.0% |
| [b01_inverted_u_bike_rack](exports/b01_inverted_u_bike_rack.glb) | Medium | 1.08 × 0.18 × 0.921 | 5,000 | 576 | 2,160 | 1,084 | 43.2% |
| [b01_post_and_ring_bike_rack](exports/b01_post_and_ring_bike_rack.glb) | Medium | 0.762 × 0.26 × 1.046 | 5,000 | 496 | 1,864 | 956 | 37.3% |
| [b01_serpentine_wave_bike_rack](exports/b01_serpentine_wave_bike_rack.glb) | Medium | 2.38 × 0.18 × 0.986 | 5,000 | 1,184 | 4,288 | 2,224 | 85.8% |
| [b01_spiral_bicycle_corral](exports/b01_spiral_bicycle_corral.glb) | Large | 3.16 × 0.85 × 0.762 | 10,000 | 1,008 | 3,024 | 1,680 | 30.2% |
| [b01_vertical_bicycle_parking_stand](exports/b01_vertical_bicycle_parking_stand.glb) | Medium | 1.01 × 0.8 × 1.886 | 5,000 | 656 | 2,320 | 1,228 | 46.4% |

### Bollard (8)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b01_chain_linked_heritage_bollards](exports/b01_chain_linked_heritage_bollards.glb) | Large | 2.34 × 0.24 × 0.925 | 10,000 | 1,710 | 5,712 | 3,372 | 57.1% |
| [b01_decorative_cast_bollard](exports/b01_decorative_cast_bollard.glb) | Medium | 0.29 × 0.276 × 1.094 | 5,000 | 514 | 1,964 | 972 | 39.3% |
| [b01_flexible_lane_delineator](exports/b01_flexible_lane_delineator.glb) | Medium | 0.36 × 0.36 × 0.976 | 5,000 | 226 | 848 | 424 | 17.0% |
| [b01_fold_down_parking_bollard](exports/b01_fold_down_parking_bollard.glb) | Medium | 0.33 × 0.25 × 0.92 | 5,000 | 328 | 1,296 | 608 | 25.9% |
| [b01_retractable_security_bollard](exports/b01_retractable_security_bollard.glb) | Medium | 0.47 × 0.47 × 0.806 | 5,000 | 544 | 2,008 | 1,048 | 40.2% |
| [b01_spherical_concrete_bollard](exports/b01_spherical_concrete_bollard.glb) | Medium | 0.8 × 0.8 × 0.8 | 5,000 | 246 | 980 | 484 | 19.6% |
| [b01_stainless_dome_bollard](exports/b01_stainless_dome_bollard.glb) | Medium | 0.31 × 0.31 × 0.979 | 5,000 | 374 | 1,408 | 724 | 28.2% |
| [b01_timber_trail_bollard](exports/b01_timber_trail_bollard.glb) | Medium | 0.32 × 0.32 × 1.002 | 5,000 | 176 | 688 | 328 | 13.8% |

### Bollard Lighting (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_louvered_cylinder_light_bollard](exports/b18_louvered_cylinder_light_bollard.glb) | Medium | 0.36 × 0.36 × 1.04 | 5,000 | 577 | 2,100 | 1,098 | 42.0% |
| [b18_recessed_square_light_bollard](exports/b18_recessed_square_light_bollard.glb) | Medium | 0.28 × 0.335 × 1.018 | 5,000 | 288 | 1,152 | 532 | 23.0% |

### Building Ceilings (8)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b21_ceiling_exposed_beams_4x4m](exports/b21_ceiling_exposed_beams_4x4m.glb) | Large | 4 × 4 × 0.2 | 10,000 | 120 | 480 | 220 | 4.8% |
| [b21_ceiling_plain_1x1m](exports/b21_ceiling_plain_1x1m.glb) | Large | 1 × 1 × 0.1 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_ceiling_plain_2x2m](exports/b21_ceiling_plain_2x2m.glb) | Large | 2 × 2 × 0.1 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_ceiling_plain_2x4m](exports/b21_ceiling_plain_2x4m.glb) | Large | 2 × 4 × 0.1 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_ceiling_plain_4x4m](exports/b21_ceiling_plain_4x4m.glb) | Large | 4 × 4 × 0.1 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_ceiling_service_hatch_2x2m](exports/b21_ceiling_service_hatch_2x2m.glb) | Large | 2 × 2 × 0.1 | 10,000 | 144 | 576 | 264 | 5.8% |
| [b21_ceiling_suspended_grid_2m](exports/b21_ceiling_suspended_grid_2m.glb) | Large | 2 × 2 × 0.063 | 10,000 | 240 | 960 | 440 | 9.6% |
| [b21_ceiling_suspended_grid_4m](exports/b21_ceiling_suspended_grid_4m.glb) | Large | 4 × 4 × 0.063 | 10,000 | 624 | 2,496 | 1,144 | 25.0% |

### Building Doors (10)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b21_door_double_glazed_2m](exports/b21_door_double_glazed_2m.glb) | Medium | 2 × 0.176 × 2.2 | 5,000 | 888 | 3,456 | 1,636 | 69.1% |
| [b21_door_double_steel_2m](exports/b21_door_double_steel_2m.glb) | Medium | 2 × 0.176 × 2.2 | 5,000 | 1,080 | 4,224 | 1,988 | 84.5% |
| [b21_door_empty_frame_1m](exports/b21_door_empty_frame_1m.glb) | Medium | 1 × 0.176 × 2.2 | 5,000 | 168 | 672 | 308 | 13.4% |
| [b21_door_glazed_entry](exports/b21_door_glazed_entry.glb) | Medium | 1 × 0.176 × 2.2 | 5,000 | 528 | 2,064 | 972 | 41.3% |
| [b21_door_leaf_glass_900mm](exports/b21_door_leaf_glass_900mm.glb) | Medium | 0.916 × 0.128 × 2.13 | 5,000 | 360 | 1,392 | 664 | 27.8% |
| [b21_door_leaf_wood_900mm](exports/b21_door_leaf_wood_900mm.glb) | Medium | 0.916 × 0.128 × 2.13 | 5,000 | 312 | 1,200 | 576 | 24.0% |
| [b21_door_painted_panel](exports/b21_door_painted_panel.glb) | Medium | 1 × 0.176 × 2.2 | 5,000 | 576 | 2,256 | 1,060 | 45.1% |
| [b21_door_steel_service](exports/b21_door_steel_service.glb) | Medium | 1 × 0.176 × 2.2 | 5,000 | 624 | 2,448 | 1,148 | 49.0% |
| [b21_door_storefront_3_6m](exports/b21_door_storefront_3_6m.glb) | Large | 3.6 × 0.176 × 2.6 | 10,000 | 720 | 2,832 | 1,324 | 28.3% |
| [b21_door_wood_panel](exports/b21_door_wood_panel.glb) | Medium | 1 × 0.176 × 2.2 | 5,000 | 480 | 1,872 | 884 | 37.4% |

### Building Floors (10)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b21_floor_concrete_1x1m](exports/b21_floor_concrete_1x1m.glb) | Large | 1 × 1 × 0.2 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_floor_concrete_2x2m](exports/b21_floor_concrete_2x2m.glb) | Large | 2 × 2 × 0.2 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_floor_concrete_2x4m](exports/b21_floor_concrete_2x4m.glb) | Large | 2 × 4 × 0.2 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_floor_concrete_4x4m](exports/b21_floor_concrete_4x4m.glb) | Large | 4 × 4 × 0.2 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_floor_concrete_4x8m](exports/b21_floor_concrete_4x8m.glb) | Large | 4 × 8 × 0.2 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_floor_edge_fascia_4m](exports/b21_floor_edge_fascia_4m.glb) | Large | 4 × 0.204 × 0.2 | 10,000 | 40 | 160 | 72 | 1.6% |
| [b21_floor_stairwell_opening_4x4m](exports/b21_floor_stairwell_opening_4x4m.glb) | Large | 4 × 4 × 0.2 | 10,000 | 96 | 384 | 176 | 3.8% |
| [b21_floor_timber_2x2m](exports/b21_floor_timber_2x2m.glb) | Large | 2 × 2 × 0.2 | 10,000 | 264 | 1,056 | 484 | 10.6% |
| [b21_floor_timber_2x4m](exports/b21_floor_timber_2x4m.glb) | Large | 2 × 4 × 0.2 | 10,000 | 264 | 1,056 | 484 | 10.6% |
| [b21_floor_timber_4x4m](exports/b21_floor_timber_4x4m.glb) | Large | 4 × 4 × 0.2 | 10,000 | 504 | 2,016 | 924 | 20.2% |

### Building Walls (12)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b21_wall_corner_1m](exports/b21_wall_corner_1m.glb) | Large | 1 × 1 × 3 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_wall_door_opening_2m](exports/b21_wall_door_opening_2m.glb) | Large | 2 × 0.204 × 3 | 10,000 | 264 | 1,056 | 484 | 10.6% |
| [b21_wall_door_opening_4m](exports/b21_wall_door_opening_4m.glb) | Large | 4 × 0.204 × 3 | 10,000 | 264 | 1,056 | 484 | 10.6% |
| [b21_wall_double_door_opening_4m](exports/b21_wall_double_door_opening_4m.glb) | Large | 4 × 0.204 × 3 | 10,000 | 264 | 1,056 | 484 | 10.6% |
| [b21_wall_end_pier](exports/b21_wall_end_pier.glb) | Medium | 0.22 × 0.22 × 3 | 5,000 | 72 | 288 | 132 | 5.8% |
| [b21_wall_solid_1m](exports/b21_wall_solid_1m.glb) | Large | 1 × 0.2 × 3 | 10,000 | 72 | 288 | 132 | 2.9% |
| [b21_wall_solid_2m](exports/b21_wall_solid_2m.glb) | Large | 2 × 0.2 × 3 | 10,000 | 72 | 288 | 132 | 2.9% |
| [b21_wall_solid_4m](exports/b21_wall_solid_4m.glb) | Large | 4 × 0.2 × 3 | 10,000 | 72 | 288 | 132 | 2.9% |
| [b21_wall_storefront_opening_4m](exports/b21_wall_storefront_opening_4m.glb) | Large | 4 × 0.204 × 3 | 10,000 | 264 | 1,056 | 484 | 10.6% |
| [b21_wall_t_junction_1m](exports/b21_wall_t_junction_1m.glb) | Large | 1 × 1 × 3 | 10,000 | 48 | 192 | 88 | 1.9% |
| [b21_wall_window_opening_2m](exports/b21_wall_window_opening_2m.glb) | Large | 2 × 0.204 × 3 | 10,000 | 312 | 1,248 | 572 | 12.5% |
| [b21_wall_window_opening_4m](exports/b21_wall_window_opening_4m.glb) | Large | 4 × 0.204 × 3 | 10,000 | 312 | 1,248 | 572 | 12.5% |

### Building Windows (10)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b21_window_clerestory_2m](exports/b21_window_clerestory_2m.glb) | Medium | 2 × 0.14 × 0.6 | 5,000 | 120 | 480 | 220 | 9.6% |
| [b21_window_cross_mullion_1m](exports/b21_window_cross_mullion_1m.glb) | Medium | 1 × 0.14 × 1.4 | 5,000 | 240 | 960 | 440 | 19.2% |
| [b21_window_double_hung_1m](exports/b21_window_double_hung_1m.glb) | Medium | 1 × 0.14 × 1.4 | 5,000 | 192 | 768 | 352 | 15.4% |
| [b21_window_fixed_1m](exports/b21_window_fixed_1m.glb) | Medium | 1 × 0.14 × 1.4 | 5,000 | 120 | 480 | 220 | 9.6% |
| [b21_window_fixed_2m](exports/b21_window_fixed_2m.glb) | Medium | 2 × 0.14 × 1.4 | 5,000 | 120 | 480 | 220 | 9.6% |
| [b21_window_paired_2m](exports/b21_window_paired_2m.glb) | Medium | 2 × 0.14 × 1.4 | 5,000 | 168 | 672 | 308 | 13.4% |
| [b21_window_shopfront_3_6m](exports/b21_window_shopfront_3_6m.glb) | Large | 3.6 × 0.14 × 2.6 | 10,000 | 168 | 672 | 308 | 6.7% |
| [b21_window_sill_1m](exports/b21_window_sill_1m.glb) | Medium | 1 × 0.26 × 0.07 | 5,000 | 24 | 96 | 44 | 1.9% |
| [b21_window_sill_2m](exports/b21_window_sill_2m.glb) | Medium | 2 × 0.26 × 0.07 | 5,000 | 24 | 96 | 44 | 1.9% |
| [b21_window_sliding_2m](exports/b21_window_sliding_2m.glb) | Medium | 2 × 0.14 × 1.4 | 5,000 | 192 | 768 | 352 | 15.4% |

### Bus Shelter (5)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b01_barrel_vault_bus_shelter](exports/b01_barrel_vault_bus_shelter.glb) | Large | 3.54 × 1.91 × 2.67 | 10,000 | 1,680 | 5,040 | 2,820 | 50.4% |
| [b01_cantilever_transit_shelter](exports/b01_cantilever_transit_shelter.glb) | Large | 3.05 × 1.822 × 2.444 | 10,000 | 1,016 | 3,904 | 1,884 | 39.0% |
| [b01_gabled_neighborhood_bus_shelter](exports/b01_gabled_neighborhood_bus_shelter.glb) | Large | 3.42 × 1.777 × 2.782 | 10,000 | 2,336 | 9,040 | 4,332 | 90.4% |
| [b01_glass_flat_roof_bus_shelter](exports/b01_glass_flat_roof_bus_shelter.glb) | Large | 3.45 × 1.75 × 2.587 | 10,000 | 2,368 | 9,200 | 4,404 | 92.0% |
| [b01_louvered_shade_transit_shelter](exports/b01_louvered_shade_transit_shelter.glb) | Large | 3.135 × 1.94 × 2.435 | 10,000 | 1,088 | 3,264 | 1,756 | 32.6% |

### Canopy Lighting (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_linear_canopy_strip_light](exports/b18_linear_canopy_strip_light.glb) | Medium | 1.3 × 0.15 × 0.225 | 5,000 | 216 | 864 | 400 | 17.3% |

### Civic Banner (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_single_banner_street_standard](exports/b18_single_banner_street_standard.glb) | Large | 1.02 × 0.4 × 4.235 | 10,000 | 722 | 2,768 | 1,346 | 27.7% |
| [b18_twin_vertical_banner_gateway](exports/b18_twin_vertical_banner_gateway.glb) | Large | 2 × 0.52 × 4.5 | 10,000 | 548 | 2,120 | 1,008 | 21.2% |

### Civic Clock (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_double_face_sidewalk_clock](exports/b18_double_face_sidewalk_clock.glb) | Large | 1.08 × 0.408 × 3.915 | 10,000 | 1,874 | 7,184 | 3,528 | 71.8% |
| [b18_four_face_town_clock](exports/b18_four_face_town_clock.glb) | Large | 1.28 × 1.28 × 4.505 | 10,000 | 1,332 | 4,370 | 2,312 | 43.7% |

### Civic Flag Fixture (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_american_flag_civic_pole](exports/b18_american_flag_civic_pole.glb) | Large | 1.86 × 0.56 × 6.305 | 10,000 | 2,164 | 8,604 | 3,924 | 86.0% |
| [b18_angled_building_flagpole](exports/b18_angled_building_flagpole.glb) | Large | 0.21 × 1.892 × 2.339 | 10,000 | 264 | 1,014 | 496 | 10.1% |

### Civic Hanging Fixture (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_ornamental_hanging_basket_standard](exports/b18_ornamental_hanging_basket_standard.glb) | Large | 2.29 × 0.485 × 3.056 | 10,000 | 1,426 | 5,364 | 2,704 | 53.6% |

### Civic Marker (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_carved_boundary_milestone](exports/b18_carved_boundary_milestone.glb) | Medium | 0.56 × 0.45 × 0.989 | 5,000 | 158 | 632 | 288 | 12.6% |

### Civic Memorial (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_sloped_memorial_plaque_pedestal](exports/b18_sloped_memorial_plaque_pedestal.glb) | Medium | 0.87 × 0.57 × 1.032 | 5,000 | 302 | 1,254 | 560 | 25.1% |

### Civic Monument (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_civic_bell_memorial](exports/b18_civic_bell_memorial.glb) | Large | 1.55 × 0.921 × 2.375 | 10,000 | 1,006 | 3,788 | 1,864 | 37.9% |
| [b18_granite_civic_obelisk](exports/b18_granite_civic_obelisk.glb) | Large | 1.3 × 1.3 × 3.77 | 10,000 | 200 | 800 | 360 | 8.0% |

### Civic Sundial (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_stone_pedestal_sundial](exports/b18_stone_pedestal_sundial.glb) | Medium | 0.68 × 0.68 × 1.248 | 5,000 | 378 | 1,440 | 688 | 28.8% |

### Civic Weather Fixture (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_directional_weather_vane_column](exports/b18_directional_weather_vane_column.glb) | Large | 1.597 × 1.325 × 2.925 | 10,000 | 1,134 | 4,424 | 2,140 | 44.2% |

### Construction Machinery (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b07_adjustable_steel_shoring_tripod](exports/b07_adjustable_steel_shoring_tripod.glb) | Medium | 1.02 × 1.125 × 2.82 | 5,000 | 736 | 2,768 | 1,396 | 55.4% |
| [b07_aggregate_feed_hopper](exports/b07_aggregate_feed_hopper.glb) | Large | 2.97 × 2.15 × 2.745 | 10,000 | 552 | 2,180 | 1,008 | 21.8% |
| [b07_articulated_wheel_loader](exports/b07_articulated_wheel_loader.glb) | Large | 5.447 × 2.71 × 3.404 | 10,000 | 2,514 | 7,710 | 4,248 | 77.1% |
| [b07_articulating_boom_lift](exports/b07_articulating_boom_lift.glb) | Large | 5.698 × 2.335 × 4.468 | 10,000 | 1,960 | 6,088 | 3,324 | 60.9% |
| [b07_asphalt_patch_kettle_trailer](exports/b07_asphalt_patch_kettle_trailer.glb) | Large | 4.081 × 2.022 × 2.29 | 10,000 | 1,400 | 5,168 | 2,660 | 51.7% |
| [b07_backhoe_loader](exports/b07_backhoe_loader.glb) | Large | 5.878 × 3.34 × 2.933 | 10,000 | 2,296 | 7,056 | 3,832 | 70.6% |
| [b07_braced_wall_formwork_panels](exports/b07_braced_wall_formwork_panels.glb) | Large | 3.645 × 1.885 × 3.285 | 10,000 | 1,120 | 4,480 | 2,088 | 44.8% |
| [b07_bridge_style_wet_tile_saw](exports/b07_bridge_style_wet_tile_saw.glb) | Medium | 1.62 × 0.995 × 1.474 | 5,000 | 602 | 2,352 | 1,120 | 47.0% |
| [b07_circular_foundation_rebar_cage](exports/b07_circular_foundation_rebar_cage.glb) | Large | 1.338 × 1.64 × 3.523 | 10,000 | 1,968 | 7,872 | 3,832 | 78.7% |
| [b07_cold_planer_road_milling_machine](exports/b07_cold_planer_road_milling_machine.glb) | Large | 6.96 × 2.445 × 3.269 | 10,000 | 2,152 | 6,472 | 3,656 | 64.7% |
| [b07_compact_track_loader_grapple](exports/b07_compact_track_loader_grapple.glb) | Large | 3.015 × 1.905 × 2.169 | 10,000 | 1,824 | 5,448 | 3,004 | 54.5% |
| [b07_crane_concrete_pouring_bucket](exports/b07_crane_concrete_pouring_bucket.glb) | Large | 1.668 × 1.703 × 2.621 | 10,000 | 732 | 2,768 | 1,320 | 27.7% |
| [b07_crawler_bulldozer](exports/b07_crawler_bulldozer.glb) | Large | 4.832 × 3.16 × 2.896 | 10,000 | 1,504 | 4,488 | 2,492 | 44.9% |
| [b07_diesel_air_compressor_trailer](exports/b07_diesel_air_compressor_trailer.glb) | Large | 3.382 × 1.848 × 1.97 | 10,000 | 1,828 | 6,968 | 3,428 | 69.7% |
| [b07_diesel_dewatering_pump_skid](exports/b07_diesel_dewatering_pump_skid.glb) | Medium | 1.851 × 1.132 × 1.25 | 5,000 | 944 | 3,616 | 1,764 | 72.3% |
| [b07_electric_rebar_bending_table](exports/b07_electric_rebar_bending_table.glb) | Medium | 1.805 × 1.311 × 1.26 | 5,000 | 792 | 3,048 | 1,472 | 61.0% |
| [b07_electric_scissor_lift_extended](exports/b07_electric_scissor_lift_extended.glb) | Large | 2.718 × 1.274 × 3.884 | 10,000 | 2,508 | 9,312 | 4,760 | 93.1% |
| [b07_heavy_jobsite_gang_box](exports/b07_heavy_jobsite_gang_box.glb) | Medium | 1.688 × 0.872 × 1.177 | 5,000 | 528 | 2,064 | 984 | 41.3% |
| [b07_heavy_steel_shoring_trestle](exports/b07_heavy_steel_shoring_trestle.glb) | Large | 3.14 × 1.84 × 2.2 | 10,000 | 456 | 1,824 | 836 | 18.2% |
| [b07_hydraulic_trench_shore_assembly](exports/b07_hydraulic_trench_shore_assembly.glb) | Large | 0.68 × 2.1 × 2.59 | 10,000 | 792 | 3,056 | 1,504 | 30.6% |
| [b07_jobsite_office_trailer](exports/b07_jobsite_office_trailer.glb) | Large | 8.007 × 3.455 × 3.42 | 10,000 | 2,600 | 9,792 | 4,888 | 97.9% |
| [b07_lattice_boom_crawler_crane](exports/b07_lattice_boom_crawler_crane.glb) | Large | 7.761 × 3.095 × 7.444 | 10,000 | 1,718 | 5,170 | 2,812 | 51.7% |
| [b07_mason_frame_scaffold_bay](exports/b07_mason_frame_scaffold_bay.glb) | Large | 3.29 × 1.53 × 2.943 | 10,000 | 1,040 | 4,096 | 1,944 | 41.0% |
| [b07_masonry_cutoff_saw_bench](exports/b07_masonry_cutoff_saw_bench.glb) | Medium | 1.55 × 1.155 × 1.573 | 5,000 | 576 | 2,224 | 1,076 | 44.5% |
| [b07_mini_excavator_open_canopy](exports/b07_mini_excavator_open_canopy.glb) | Large | 3.494 × 1.665 × 2.221 | 10,000 | 1,460 | 4,396 | 2,448 | 44.0% |
| [b07_mobile_inclined_belt_conveyor](exports/b07_mobile_inclined_belt_conveyor.glb) | Large | 4.63 × 1.767 × 2.55 | 10,000 | 1,664 | 6,136 | 3,128 | 61.4% |
| [b07_motor_grader](exports/b07_motor_grader.glb) | Large | 5.796 × 2.936 × 2.967 | 10,000 | 2,832 | 8,760 | 4,776 | 87.6% |
| [b07_pipe_threading_machine_stand](exports/b07_pipe_threading_machine_stand.glb) | Medium | 1.399 × 0.962 × 1.78 | 5,000 | 726 | 2,808 | 1,364 | 56.2% |
| [b07_portable_cement_storage_silo](exports/b07_portable_cement_storage_silo.glb) | Large | 2.78 × 2.39 × 4.88 | 10,000 | 1,736 | 6,776 | 3,296 | 67.8% |
| [b07_portable_light_tower_trailer](exports/b07_portable_light_tower_trailer.glb) | Large | 3.211 × 2.38 × 5.406 | 10,000 | 1,920 | 7,296 | 3,592 | 73.0% |
| [b07_rack_and_pinion_material_hoist](exports/b07_rack_and_pinion_material_hoist.glb) | Large | 2.4 × 2.16 × 6.107 | 10,000 | 1,848 | 7,392 | 3,388 | 73.9% |
| [b07_remote_trench_padfoot_roller](exports/b07_remote_trench_padfoot_roller.glb) | Large | 1.99 × 1.14 × 1.412 | 10,000 | 1,536 | 6,024 | 2,844 | 60.2% |
| [b07_rolling_scaffold_tower](exports/b07_rolling_scaffold_tower.glb) | Large | 2.33 × 1.443 × 3.25 | 10,000 | 2,380 | 9,008 | 4,508 | 90.1% |
| [b07_rough_terrain_mobile_crane](exports/b07_rough_terrain_mobile_crane.glb) | Large | 6.001 × 4.4 × 5.655 | 10,000 | 2,157 | 6,674 | 3,646 | 66.7% |
| [b07_scaffold_access_stair_tower](exports/b07_scaffold_access_stair_tower.glb) | Large | 3.392 × 1.7 × 3.392 | 10,000 | 1,296 | 5,184 | 2,396 | 51.8% |
| [b07_self_erecting_tower_crane](exports/b07_self_erecting_tower_crane.glb) | Large | 11.391 × 3.4 × 10.04 | 10,000 | 1,217 | 3,654 | 1,898 | 36.5% |
| [b07_silenced_diesel_generator_trailer](exports/b07_silenced_diesel_generator_trailer.glb) | Large | 4.569 × 2.126 × 2.243 | 10,000 | 1,544 | 5,760 | 2,924 | 57.6% |
| [b07_single_drum_soil_compactor](exports/b07_single_drum_soil_compactor.glb) | Large | 4.096 × 2.61 × 3.253 | 10,000 | 1,176 | 3,600 | 1,960 | 36.0% |
| [b07_steel_trench_shoring_box](exports/b07_steel_trench_shoring_box.glb) | Large | 3.85 × 2.46 × 2.732 | 10,000 | 1,056 | 4,144 | 2,000 | 41.4% |
| [b07_tandem_vibratory_road_roller](exports/b07_tandem_vibratory_road_roller.glb) | Large | 3.34 × 1.97 × 2.91 | 10,000 | 1,076 | 4,044 | 2,036 | 40.4% |
| [b07_telescopic_construction_handler](exports/b07_telescopic_construction_handler.glb) | Large | 6.221 × 2.526 × 3.06 | 10,000 | 2,016 | 6,216 | 3,384 | 62.2% |
| [b07_tilting_drum_concrete_mixer](exports/b07_tilting_drum_concrete_mixer.glb) | Medium | 1.393 × 1.433 × 2.004 | 5,000 | 1,152 | 4,224 | 2,196 | 84.5% |
| [b07_towable_cherry_picker](exports/b07_towable_cherry_picker.glb) | Large | 4.151 × 3.16 × 3.642 | 10,000 | 2,076 | 7,856 | 3,908 | 78.6% |
| [b07_towable_paddle_mortar_mixer](exports/b07_towable_paddle_mortar_mixer.glb) | Large | 3.033 × 1.813 × 1.673 | 10,000 | 1,332 | 5,000 | 2,520 | 50.0% |
| [b07_tracked_asphalt_paver](exports/b07_tracked_asphalt_paver.glb) | Large | 4.79 × 3.35 × 2.924 | 10,000 | 1,492 | 4,492 | 2,468 | 44.9% |
| [b07_tracked_hydraulic_excavator](exports/b07_tracked_hydraulic_excavator.glb) | Large | 6.57 × 3.085 × 3.584 | 10,000 | 1,886 | 5,634 | 3,132 | 56.3% |
| [b07_trailer_concrete_line_pump](exports/b07_trailer_concrete_line_pump.glb) | Large | 5.418 × 2.08 × 1.548 | 10,000 | 1,692 | 6,288 | 3,184 | 62.9% |
| [b07_twin_tank_grout_injection_skid](exports/b07_twin_tank_grout_injection_skid.glb) | Large | 2.27 × 1.3 × 1.55 | 10,000 | 882 | 3,356 | 1,648 | 33.6% |
| [b07_water_storage_tank_skid](exports/b07_water_storage_tank_skid.glb) | Large | 3.364 × 1.619 × 2.09 | 10,000 | 968 | 3,704 | 1,864 | 37.0% |
| [b07_wheeled_skid_steer_loader](exports/b07_wheeled_skid_steer_loader.glb) | Large | 3.029 × 1.835 × 2.21 | 10,000 | 2,112 | 6,504 | 3,504 | 65.0% |

### Curb (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_granite_curb_sett_course](exports/b13_granite_curb_sett_course.glb) | Medium | 2.428 × 0.55 × 0.22 | 5,000 | 294 | 1,164 | 540 | 23.3% |
| [b13_rolled_concrete_gutter_curb](exports/b13_rolled_concrete_gutter_curb.glb) | Medium | 2.4 × 0.84 × 0.195 | 5,000 | 174 | 694 | 316 | 13.9% |

### Drinking Fountain (5)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b01_bottle_refill_station](exports/b01_bottle_refill_station.glb) | Medium | 0.774 × 0.39 × 1.625 | 5,000 | 1,024 | 3,920 | 1,920 | 78.4% |
| [b01_classic_pedestal_drinking_fountain](exports/b01_classic_pedestal_drinking_fountain.glb) | Medium | 0.498 × 0.498 × 1.057 | 5,000 | 896 | 3,328 | 1,704 | 66.6% |
| [b01_dual_height_drinking_fountain](exports/b01_dual_height_drinking_fountain.glb) | Medium | 1.028 × 0.46 × 1.127 | 5,000 | 1,040 | 3,784 | 1,980 | 75.7% |
| [b01_people_and_pet_drinking_fountain](exports/b01_people_and_pet_drinking_fountain.glb) | Medium | 0.849 × 0.46 × 1.187 | 5,000 | 1,088 | 3,940 | 2,076 | 78.8% |
| [b01_stone_spout_fountain](exports/b01_stone_spout_fountain.glb) | Medium | 0.508 × 0.704 × 1.135 | 5,000 | 744 | 2,752 | 1,416 | 55.0% |

### Exterior Building Components (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b12_arched_wood_entry](exports/b12_arched_wood_entry.glb) | Medium | 1.253 × 0.256 × 2.416 | 5,000 | 1,014 | 4,006 | 1,876 | 80.1% |
| [b12_barrel_entrance_awning](exports/b12_barrel_entrance_awning.glb) | Large | 1.99 × 1.003 × 1.14 | 10,000 | 600 | 2,400 | 1,100 | 24.0% |
| [b12_basement_hopper_window](exports/b12_basement_hopper_window.glb) | Medium | 1.43 × 0.538 × 0.718 | 5,000 | 500 | 2,000 | 916 | 40.0% |
| [b12_board_and_batten_shutters](exports/b12_board_and_batten_shutters.glb) | Medium | 1.33 × 0.124 × 1.4 | 5,000 | 672 | 2,688 | 1,248 | 53.8% |
| [b12_brick_arch_window_lintel](exports/b12_brick_arch_window_lintel.glb) | Medium | 1.87 × 0.34 × 1.09 | 5,000 | 432 | 1,728 | 792 | 34.6% |
| [b12_brownstone_entry_stair](exports/b12_brownstone_entry_stair.glb) | Large | 2.12 × 2.94 × 2.303 | 10,000 | 2,400 | 9,600 | 4,400 | 96.0% |
| [b12_cantilever_apartment_balcony](exports/b12_cantilever_apartment_balcony.glb) | Large | 2.79 × 1.34 × 1.497 | 10,000 | 1,416 | 5,664 | 2,596 | 56.6% |
| [b12_canvas_wedge_shop_awning](exports/b12_canvas_wedge_shop_awning.glb) | Large | 3.1 × 1.248 × 0.92 | 10,000 | 612 | 2,448 | 1,120 | 24.5% |
| [b12_carriage_house_garage_doors](exports/b12_carriage_house_garage_doors.glb) | Large | 2.74 × 0.24 × 2.56 | 10,000 | 1,416 | 5,664 | 2,624 | 56.6% |
| [b12_classical_entry_pediment](exports/b12_classical_entry_pediment.glb) | Large | 2.312 × 0.52 × 3.107 | 10,000 | 448 | 1,790 | 820 | 17.9% |
| [b12_commercial_glass_entry](exports/b12_commercial_glass_entry.glb) | Medium | 1.15 × 0.24 × 2.33 | 5,000 | 540 | 2,160 | 996 | 43.2% |
| [b12_curb_mounted_skylight](exports/b12_curb_mounted_skylight.glb) | Medium | 1.47 × 1.87 × 0.484 | 5,000 | 336 | 1,344 | 616 | 26.9% |
| [b12_dentil_cornice_section](exports/b12_dentil_cornice_section.glb) | Large | 2.93 × 0.57 × 0.717 | 10,000 | 696 | 2,784 | 1,276 | 27.8% |
| [b12_double_hung_sash_window](exports/b12_double_hung_sash_window.glb) | Medium | 1.09 × 0.27 × 1.8 | 5,000 | 648 | 2,592 | 1,188 | 51.8% |
| [b12_double_steel_service_door](exports/b12_double_steel_service_door.glb) | Large | 2.01 × 0.24 × 2.27 | 10,000 | 960 | 3,840 | 1,772 | 38.4% |
| [b12_entrance_threshold_ramp](exports/b12_entrance_threshold_ramp.glb) | Large | 1.385 × 2.508 × 0.31 | 10,000 | 604 | 2,414 | 1,108 | 24.1% |
| [b12_fire_escape_drop_ladder](exports/b12_fire_escape_drop_ladder.glb) | Large | 0.905 × 0.7 × 3.732 | 10,000 | 1,360 | 5,216 | 2,512 | 52.2% |
| [b12_fire_escape_landing](exports/b12_fire_escape_landing.glb) | Large | 2.2 × 1.255 × 1.344 | 10,000 | 1,992 | 7,968 | 3,652 | 79.7% |
| [b12_fire_escape_stair_flight](exports/b12_fire_escape_stair_flight.glb) | Large | 1.045 × 2.832 × 3.076 | 10,000 | 880 | 2,640 | 1,336 | 26.4% |
| [b12_foundation_crawlspace_hatch](exports/b12_foundation_crawlspace_hatch.glb) | Medium | 1.08 × 0.291 × 0.83 | 5,000 | 868 | 3,440 | 1,616 | 68.8% |
| [b12_gable_dormer_window](exports/b12_gable_dormer_window.glb) | Large | 1.545 × 1.115 × 1.927 | 10,000 | 906 | 3,624 | 1,660 | 36.2% |
| [b12_gabled_entry_portico](exports/b12_gabled_entry_portico.glb) | Large | 2.397 × 1.417 × 3.123 | 10,000 | 570 | 2,280 | 1,044 | 22.8% |
| [b12_glass_block_window_panel](exports/b12_glass_block_window_panel.glb) | Medium | 1.27 × 0.27 × 1.27 | 5,000 | 768 | 2,304 | 1,152 | 46.1% |
| [b12_industrial_steel_grid_window](exports/b12_industrial_steel_grid_window.glb) | Large | 2.66 × 0.36 × 2.06 | 10,000 | 624 | 2,496 | 1,144 | 25.0% |
| [b12_limestone_window_surround](exports/b12_limestone_window_surround.glb) | Medium | 1.65 × 0.49 × 2.212 | 5,000 | 384 | 1,536 | 704 | 30.7% |
| [b12_loading_dock_door_seal](exports/b12_loading_dock_door_seal.glb) | Large | 3.15 × 0.506 × 3.215 | 10,000 | 1,104 | 4,416 | 2,024 | 44.2% |
| [b12_louvered_window_shutters](exports/b12_louvered_window_shutters.glb) | Medium | 1.337 × 0.091 × 1.58 | 5,000 | 1,200 | 4,800 | 2,200 | 96.0% |
| [b12_masonry_chimney_stack](exports/b12_masonry_chimney_stack.glb) | Large | 0.99 × 0.81 × 1.815 | 10,000 | 1,704 | 6,816 | 3,004 | 68.2% |
| [b12_open_casement_window](exports/b12_open_casement_window.glb) | Medium | 1.36 × 0.508 × 1.56 | 5,000 | 660 | 2,664 | 1,212 | 53.3% |
| [b12_open_rooftop_access_hatch](exports/b12_open_rooftop_access_hatch.glb) | Medium | 0.99 × 1.514 × 1.505 | 5,000 | 480 | 1,884 | 884 | 37.7% |
| [b12_ornamental_juliet_balcony](exports/b12_ornamental_juliet_balcony.glb) | Medium | 1.55 × 0.278 × 1.08 | 5,000 | 780 | 3,120 | 1,480 | 62.4% |
| [b12_parapet_coping_corner](exports/b12_parapet_coping_corner.glb) | Large | 2.525 × 1.542 × 0.89 | 10,000 | 1,344 | 5,376 | 2,460 | 53.8% |
| [b12_projecting_bay_window](exports/b12_projecting_bay_window.glb) | Large | 2.643 × 0.792 × 2.022 | 10,000 | 638 | 2,548 | 1,168 | 25.5% |
| [b12_raised_loading_dock_platform](exports/b12_raised_loading_dock_platform.glb) | Large | 3.59 × 1.978 × 1.193 | 10,000 | 712 | 2,784 | 1,292 | 27.8% |
| [b12_retractable_shop_awning](exports/b12_retractable_shop_awning.glb) | Large | 3.48 × 1.89 × 0.556 | 10,000 | 848 | 3,340 | 1,560 | 33.4% |
| [b12_revolving_glass_entry](exports/b12_revolving_glass_entry.glb) | Large | 2.24 × 2.24 × 2.49 | 10,000 | 976 | 3,824 | 1,804 | 38.2% |
| [b12_roll_up_storefront_shutter](exports/b12_roll_up_storefront_shutter.glb) | Large | 3.6 × 0.442 × 3.02 | 10,000 | 1,744 | 6,944 | 3,200 | 69.4% |
| [b12_rooftop_stair_headhouse](exports/b12_rooftop_stair_headhouse.glb) | Large | 1.9 × 2.535 × 2.652 | 10,000 | 2,226 | 8,884 | 4,088 | 88.8% |
| [b12_round_attic_window](exports/b12_round_attic_window.glb) | Medium | 1.213 × 0.142 × 1.213 | 5,000 | 416 | 1,504 | 812 | 30.1% |
| [b12_sawtooth_roof_glazing_module](exports/b12_sawtooth_roof_glazing_module.glb) | Large | 3.24 × 1.47 × 1.12 | 10,000 | 516 | 2,064 | 944 | 20.6% |
| [b12_screen_storm_door](exports/b12_screen_storm_door.glb) | Medium | 0.99 × 0.155 × 2.13 | 5,000 | 1,164 | 4,656 | 2,140 | 93.1% |
| [b12_sectional_residential_garage](exports/b12_sectional_residential_garage.glb) | Large | 2.86 × 0.29 × 2.41 | 10,000 | 1,680 | 6,720 | 3,080 | 67.2% |
| [b12_side_entry_stair_landing](exports/b12_side_entry_stair_landing.glb) | Large | 2.31 × 2.578 × 1.843 | 10,000 | 1,872 | 7,488 | 3,432 | 74.9% |
| [b12_sidelight_transom_entry](exports/b12_sidelight_transom_entry.glb) | Large | 1.89 × 0.3 × 2.67 | 10,000 | 1,418 | 5,648 | 2,604 | 56.5% |
| [b12_six_panel_front_door](exports/b12_six_panel_front_door.glb) | Medium | 1.08 × 0.28 × 2.2 | 5,000 | 454 | 1,388 | 700 | 27.8% |
| [b12_sliding_patio_door](exports/b12_sliding_patio_door.glb) | Large | 2.15 × 0.271 × 2.28 | 10,000 | 660 | 2,640 | 1,216 | 26.4% |
| [b12_sloped_cellar_bulkhead](exports/b12_sloped_cellar_bulkhead.glb) | Large | 1.55 × 1.936 × 1.054 | 10,000 | 556 | 2,264 | 1,024 | 22.6% |
| [b12_standing_seam_metal_canopy](exports/b12_standing_seam_metal_canopy.glb) | Large | 3.33 × 1.462 × 0.839 | 10,000 | 504 | 2,016 | 924 | 20.2% |
| [b12_suspended_glass_entry_canopy](exports/b12_suspended_glass_entry_canopy.glb) | Large | 2.76 × 1.512 × 0.98 | 10,000 | 576 | 2,304 | 1,060 | 23.0% |
| [b12_three_step_front_stoop](exports/b12_three_step_front_stoop.glb) | Large | 1.66 × 1.627 × 1.393 | 10,000 | 1,344 | 5,376 | 2,464 | 53.8% |

### Fences Gates Boundaries (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b19_accordion_industrial_gate](exports/b19_accordion_industrial_gate.glb) | Large | 4.2 × 0.223 × 1.829 | 10,000 | 1,576 | 6,096 | 2,924 | 61.0% |
| [b19_aluminum_double_drive_gate](exports/b19_aluminum_double_drive_gate.glb) | Large | 4.63 × 0.23 × 1.833 | 10,000 | 1,866 | 7,456 | 3,420 | 74.6% |
| [b19_aluminum_spear_fence](exports/b19_aluminum_spear_fence.glb) | Medium | 2.575 × 0.175 × 1.639 | 5,000 | 1,208 | 4,832 | 2,228 | 96.6% |
| [b19_arched_wrought_iron_gate](exports/b19_arched_wrought_iron_gate.glb) | Medium | 1.73 × 0.3 × 1.933 | 5,000 | 654 | 2,060 | 1,100 | 41.2% |
| [b19_basketweave_timber_fence](exports/b19_basketweave_timber_fence.glb) | Medium | 2.6 × 0.2 × 1.69 | 5,000 | 744 | 2,976 | 1,364 | 59.5% |
| [b19_board_batten_fence](exports/b19_board_batten_fence.glb) | Medium | 2.62 × 0.225 × 1.973 | 5,000 | 810 | 3,232 | 1,488 | 64.6% |
| [b19_brick_pier_garden_gate](exports/b19_brick_pier_garden_gate.glb) | Medium | 2.4 × 0.53 × 1.573 | 5,000 | 680 | 2,160 | 1,108 | 43.2% |
| [b19_cantilever_security_slide_gate](exports/b19_cantilever_security_slide_gate.glb) | Large | 4.81 × 0.63 × 2.158 | 10,000 | 1,200 | 3,600 | 1,892 | 36.0% |
| [b19_capped_brick_boundary_wall](exports/b19_capped_brick_boundary_wall.glb) | Medium | 3.36 × 0.48 × 1.38 | 5,000 | 456 | 1,368 | 684 | 27.4% |
| [b19_cedar_fence_inside_corner](exports/b19_cedar_fence_inside_corner.glb) | Medium | 2.53 × 1.88 × 1.593 | 5,000 | 1,015 | 3,944 | 1,862 | 78.9% |
| [b19_cedar_lattice_top_fence](exports/b19_cedar_lattice_top_fence.glb) | Medium | 2.62 × 0.22 × 2.023 | 5,000 | 466 | 1,400 | 708 | 28.0% |
| [b19_chainlink_double_vehicle_gate](exports/b19_chainlink_double_vehicle_gate.glb) | Large | 4.501 × 0.2 × 1.928 | 10,000 | 2,524 | 9,968 | 4,672 | 99.7% |
| [b19_chainlink_walk_gate](exports/b19_chainlink_walk_gate.glb) | Medium | 1.64 × 0.295 × 1.598 | 5,000 | 632 | 1,896 | 1,016 | 37.9% |
| [b19_concrete_block_boundary_wall](exports/b19_concrete_block_boundary_wall.glb) | Medium | 3.4 × 0.48 × 1.47 | 5,000 | 984 | 3,936 | 1,804 | 78.7% |
| [b19_corrugated_metal_boundary](exports/b19_corrugated_metal_boundary.glb) | Medium | 2.575 × 0.205 × 1.993 | 5,000 | 606 | 1,820 | 1,040 | 36.4% |
| [b19_corrugated_utility_yard_gate](exports/b19_corrugated_utility_yard_gate.glb) | Medium | 1.985 × 0.402 × 2.023 | 5,000 | 686 | 2,060 | 1,140 | 41.2% |
| [b19_crossbuck_ranch_fence](exports/b19_crossbuck_ranch_fence.glb) | Medium | 3.05 × 0.25 × 1.373 | 5,000 | 258 | 1,024 | 468 | 20.5% |
| [b19_dogear_stockade_fence](exports/b19_dogear_stockade_fence.glb) | Medium | 2.62 × 0.22 × 1.873 | 5,000 | 898 | 3,456 | 1,664 | 69.1% |
| [b19_double_crossbuck_driveway_gate](exports/b19_double_crossbuck_driveway_gate.glb) | Large | 4.44 × 0.28 × 1.423 | 10,000 | 654 | 2,608 | 1,204 | 26.1% |
| [b19_dry_stone_boundary_wall](exports/b19_dry_stone_boundary_wall.glb) | Medium | 2.98 × 0.44 × 1 | 5,000 | 976 | 3,848 | 1,808 | 77.0% |
| [b19_flat_top_pool_fence](exports/b19_flat_top_pool_fence.glb) | Medium | 2.57 × 0.17 × 1.439 | 5,000 | 992 | 3,968 | 1,832 | 79.4% |
| [b19_gabion_boundary_wall](exports/b19_gabion_boundary_wall.glb) | Medium | 2.716 × 0.716 × 1.047 | 5,000 | 824 | 3,060 | 1,320 | 61.2% |
| [b19_garden_boundary_trellis](exports/b19_garden_boundary_trellis.glb) | Medium | 2.65 × 0.222 × 2.173 | 5,000 | 786 | 3,136 | 1,444 | 62.7% |
| [b19_geometric_metal_screen_gate](exports/b19_geometric_metal_screen_gate.glb) | Medium | 1.73 × 0.29 × 2.013 | 5,000 | 490 | 1,472 | 768 | 29.4% |
| [b19_gothic_picket_fence](exports/b19_gothic_picket_fence.glb) | Medium | 2.62 × 0.22 × 1.223 | 5,000 | 692 | 2,708 | 1,276 | 54.2% |
| [b19_horizontal_cedar_slat_fence](exports/b19_horizontal_cedar_slat_fence.glb) | Medium | 2.605 × 0.168 × 1.889 | 5,000 | 1,056 | 4,224 | 1,956 | 84.5% |
| [b19_lattice_trellis_gate](exports/b19_lattice_trellis_gate.glb) | Medium | 1.82 × 0.315 × 1.953 | 5,000 | 586 | 1,760 | 920 | 35.2% |
| [b19_ornamental_iron_fence](exports/b19_ornamental_iron_fence.glb) | Medium | 2.685 × 0.185 × 1.743 | 5,000 | 642 | 2,168 | 1,096 | 43.4% |
| [b19_picket_garden_gate](exports/b19_picket_garden_gate.glb) | Medium | 1.57 × 0.312 × 1.313 | 5,000 | 1,200 | 4,732 | 2,228 | 94.6% |
| [b19_precast_concrete_fence](exports/b19_precast_concrete_fence.glb) | Medium | 2.89 × 0.29 × 1.995 | 5,000 | 384 | 1,536 | 704 | 30.7% |
| [b19_ranch_wire_fence](exports/b19_ranch_wire_fence.glb) | Medium | 3.24 × 0.24 × 1.22 | 5,000 | 504 | 2,016 | 928 | 40.3% |
| [b19_residential_chainlink_fence](exports/b19_residential_chainlink_fence.glb) | Medium | 2.8 × 0.2 × 1.308 | 5,000 | 532 | 1,596 | 840 | 31.9% |
| [b19_retaining_wall_corner](exports/b19_retaining_wall_corner.glb) | Medium | 2.46 × 2.03 × 0.958 | 5,000 | 816 | 3,264 | 1,496 | 65.3% |
| [b19_scalloped_vinyl_fence](exports/b19_scalloped_vinyl_fence.glb) | Medium | 2.63 × 0.23 × 1.293 | 5,000 | 834 | 3,328 | 1,524 | 66.6% |
| [b19_security_chainlink_fence](exports/b19_security_chainlink_fence.glb) | Large | 3.2 × 0.412 × 2.4 | 10,000 | 1,124 | 4,368 | 1,992 | 43.7% |
| [b19_self_closing_pool_gate](exports/b19_self_closing_pool_gate.glb) | Medium | 1.495 × 0.282 × 1.61 | 5,000 | 470 | 1,412 | 748 | 28.2% |
| [b19_shadowbox_privacy_fence](exports/b19_shadowbox_privacy_fence.glb) | Medium | 2.62 × 0.245 × 1.913 | 5,000 | 858 | 3,424 | 1,580 | 68.5% |
| [b19_sliding_timber_driveway_gate](exports/b19_sliding_timber_driveway_gate.glb) | Large | 4.75 × 0.571 × 1.953 | 10,000 | 1,910 | 7,688 | 3,504 | 76.9% |
| [b19_split_rail_fence](exports/b19_split_rail_fence.glb) | Medium | 3.17 × 0.27 × 1.32 | 5,000 | 330 | 1,320 | 608 | 26.4% |
| [b19_split_rail_field_gate](exports/b19_split_rail_field_gate.glb) | Medium | 3.19 × 0.34 × 1.4 | 5,000 | 856 | 3,392 | 1,592 | 67.8% |
| [b19_stepped_block_retaining_wall](exports/b19_stepped_block_retaining_wall.glb) | Large | 3.62 × 0.52 × 0.963 | 10,000 | 720 | 2,880 | 1,320 | 28.8% |
| [b19_stockade_service_gate](exports/b19_stockade_service_gate.glb) | Medium | 1.68 × 0.367 × 1.993 | 5,000 | 1,218 | 4,768 | 2,256 | 95.4% |
| [b19_stone_pier_driveway_entry](exports/b19_stone_pier_driveway_entry.glb) | Large | 4.78 × 0.64 × 1.968 | 10,000 | 1,924 | 7,712 | 3,548 | 77.1% |
| [b19_timber_post_cable_boundary](exports/b19_timber_post_cable_boundary.glb) | Medium | 3.24 × 0.24 × 1.228 | 5,000 | 696 | 2,784 | 1,300 | 55.7% |
| [b19_timber_sleeper_retaining_wall](exports/b19_timber_sleeper_retaining_wall.glb) | Medium | 2.92 × 1.35 × 0.93 | 5,000 | 504 | 2,016 | 940 | 40.3% |
| [b19_tongue_groove_vinyl_fence](exports/b19_tongue_groove_vinyl_fence.glb) | Medium | 2.64 × 0.24 × 1.993 | 5,000 | 522 | 2,080 | 952 | 41.6% |
| [b19_tubular_field_gate](exports/b19_tubular_field_gate.glb) | Medium | 3.41 × 0.34 × 1.39 | 5,000 | 964 | 3,788 | 1,812 | 75.8% |
| [b19_vinyl_pedestrian_gate](exports/b19_vinyl_pedestrian_gate.glb) | Medium | 1.6 × 0.315 × 1.443 | 5,000 | 850 | 3,360 | 1,568 | 67.2% |
| [b19_welded_mesh_industrial_gate](exports/b19_welded_mesh_industrial_gate.glb) | Medium | 2.02 × 0.295 × 2.173 | 5,000 | 530 | 1,592 | 836 | 31.8% |
| [b19_welded_mesh_security_fence](exports/b19_welded_mesh_security_fence.glb) | Medium | 2.765 × 0.165 × 1.949 | 5,000 | 1,184 | 4,736 | 2,184 | 94.7% |

### Food Drinks Packaging Litter (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b16_aluminum_soda_can](exports/b16_aluminum_soda_can.glb) | Handheld | 0.066 × 0.066 × 0.13 | 999 | 160 | 560 | 304 | 56.1% |
| [b16_baguette_in_paper_sleeve](exports/b16_baguette_in_paper_sleeve.glb) | Handheld | 0.07 × 0.356 × 0.052 | 999 | 166 | 620 | 286 | 62.1% |
| [b16_broken_chocolate_chip_cookie](exports/b16_broken_chocolate_chip_cookie.glb) | Handheld | 0.094 × 0.078 × 0.014 | 999 | 145 | 578 | 250 | 57.9% |
| [b16_burger_clamshell](exports/b16_burger_clamshell.glb) | Handheld | 0.126 × 0.135 × 0.09 | 999 | 136 | 512 | 252 | 51.3% |
| [b16_chopsticks_in_paper_sleeve](exports/b16_chopsticks_in_paper_sleeve.glb) | Handheld | 0.037 × 0.254 × 0.014 | 999 | 192 | 768 | 356 | 76.9% |
| [b16_closed_pizza_box](exports/b16_closed_pizza_box.glb) | Handheld | 0.354 × 0.358 × 0.053 | 999 | 120 | 480 | 216 | 48.0% |
| [b16_crumpled_food_wrapper](exports/b16_crumpled_food_wrapper.glb) | Handheld | 0.21 × 0.15 × 0.025 | 999 | 72 | 300 | 100 | 30.0% |
| [b16_crumpled_paper_napkin](exports/b16_crumpled_paper_napkin.glb) | Handheld | 0.126 × 0.104 × 0.034 | 999 | 182 | 656 | 296 | 65.7% |
| [b16_crushed_soda_can](exports/b16_crushed_soda_can.glb) | Handheld | 0.063 × 0.062 × 0.071 | 999 | 160 | 608 | 312 | 60.9% |
| [b16_curled_receipt_litter](exports/b16_curled_receipt_litter.glb) | Handheld | 0.171 × 0.058 × 0.055 | 999 | 158 | 610 | 296 | 61.1% |
| [b16_discarded_apple_core](exports/b16_discarded_apple_core.glb) | Handheld | 0.06 × 0.058 × 0.091 | 999 | 227 | 920 | 438 | 92.1% |
| [b16_discarded_banana_peel](exports/b16_discarded_banana_peel.glb) | Handheld | 0.171 × 0.194 × 0.054 | 999 | 214 | 704 | 360 | 70.5% |
| [b16_discarded_bottle_cork](exports/b16_discarded_bottle_cork.glb) | Handheld | 0.046 × 0.022 × 0.022 | 999 | 176 | 652 | 336 | 65.3% |
| [b16_discarded_crown_bottle_cap](exports/b16_discarded_crown_bottle_cap.glb) | Handheld | 0.032 × 0.032 × 0.011 | 999 | 120 | 428 | 232 | 42.8% |
| [b16_discarded_six_pack_rings](exports/b16_discarded_six_pack_rings.glb) | Handheld | 0.18 × 0.124 × 0.004 | 999 | 232 | 888 | 444 | 88.9% |
| [b16_disposable_plastic_fork](exports/b16_disposable_plastic_fork.glb) | Handheld | 0.034 × 0.174 × 0.003 | 999 | 136 | 536 | 252 | 53.7% |
| [b16_disposable_plastic_spoon](exports/b16_disposable_plastic_spoon.glb) | Handheld | 0.046 × 0.179 × 0.01 | 999 | 118 | 438 | 228 | 43.8% |
| [b16_donut_in_open_paper_bag](exports/b16_donut_in_open_paper_bag.glb) | Handheld | 0.13 × 0.135 × 0.086 | 999 | 152 | 528 | 288 | 52.9% |
| [b16_fluted_paper_plate](exports/b16_fluted_paper_plate.glb) | Handheld | 0.206 × 0.206 × 0.025 | 999 | 208 | 704 | 364 | 70.5% |
| [b16_foil_drink_pouch](exports/b16_foil_drink_pouch.glb) | Handheld | 0.094 × 0.036 × 0.191 | 999 | 220 | 848 | 396 | 84.9% |
| [b16_folded_newspaper](exports/b16_folded_newspaper.glb) | Handheld | 0.215 × 0.157 × 0.015 | 999 | 200 | 600 | 300 | 60.1% |
| [b16_folded_takeout_carton](exports/b16_folded_takeout_carton.glb) | Handheld | 0.101 × 0.081 × 0.145 | 999 | 176 | 724 | 324 | 72.5% |
| [b16_fountain_drink_with_straw](exports/b16_fountain_drink_with_straw.glb) | Handheld | 0.104 × 0.099 × 0.24 | 999 | 192 | 708 | 364 | 70.9% |
| [b16_french_fry_carton](exports/b16_french_fry_carton.glb) | Handheld | 0.075 × 0.047 × 0.154 | 999 | 248 | 976 | 456 | 97.7% |
| [b16_gable_top_milk_carton](exports/b16_gable_top_milk_carton.glb) | Handheld | 0.071 × 0.073 × 0.225 | 999 | 114 | 440 | 208 | 44.0% |
| [b16_hotdog_in_paper_boat](exports/b16_hotdog_in_paper_boat.glb) | Handheld | 0.195 × 0.082 × 0.076 | 999 | 196 | 756 | 372 | 75.7% |
| [b16_ice_cream_cup_with_spoon](exports/b16_ice_cream_cup_with_spoon.glb) | Handheld | 0.088 × 0.081 × 0.143 | 999 | 248 | 936 | 480 | 93.7% |
| [b16_juice_box_with_straw](exports/b16_juice_box_with_straw.glb) | Handheld | 0.061 × 0.043 × 0.166 | 999 | 160 | 640 | 296 | 64.1% |
| [b16_ketchup_sachet](exports/b16_ketchup_sachet.glb) | Handheld | 0.04 × 0.011 × 0.076 | 999 | 126 | 392 | 200 | 39.2% |
| [b16_lidded_salad_bowl](exports/b16_lidded_salad_bowl.glb) | Handheld | 0.16 × 0.16 × 0.076 | 999 | 152 | 480 | 280 | 48.0% |
| [b16_lidded_soup_cup](exports/b16_lidded_soup_cup.glb) | Handheld | 0.11 × 0.105 × 0.088 | 999 | 192 | 708 | 360 | 70.9% |
| [b16_longneck_glass_bottle](exports/b16_longneck_glass_bottle.glb) | Handheld | 0.064 × 0.063 × 0.227 | 999 | 226 | 844 | 436 | 84.5% |
| [b16_molded_four_cup_carrier](exports/b16_molded_four_cup_carrier.glb) | Handheld | 0.176 × 0.176 × 0.043 | 999 | 144 | 496 | 264 | 49.6% |
| [b16_paper_takeaway_bag](exports/b16_paper_takeaway_bag.glb) | Handheld | 0.14 × 0.082 × 0.274 | 999 | 176 | 520 | 276 | 52.1% |
| [b16_partly_eaten_ice_pop](exports/b16_partly_eaten_ice_pop.glb) | Handheld | 0.062 × 0.191 × 0.021 | 999 | 102 | 402 | 192 | 40.2% |
| [b16_pizza_slice_in_triangle_tray](exports/b16_pizza_slice_in_triangle_tray.glb) | Handheld | 0.17 × 0.255 × 0.029 | 999 | 214 | 776 | 396 | 77.7% |
| [b16_popcorn_carton](exports/b16_popcorn_carton.glb) | Handheld | 0.1 × 0.083 × 0.166 | 999 | 241 | 801 | 427 | 80.2% |
| [b16_rectangular_foil_takeaway_pan](exports/b16_rectangular_foil_takeaway_pan.glb) | Handheld | 0.197 × 0.14 × 0.05 | 999 | 256 | 832 | 428 | 83.3% |
| [b16_ribbed_water_bottle](exports/b16_ribbed_water_bottle.glb) | Handheld | 0.068 × 0.065 × 0.18 | 999 | 260 | 980 | 508 | 98.1% |
| [b16_rolled_newspaper](exports/b16_rolled_newspaper.glb) | Handheld | 0.27 × 0.064 × 0.062 | 999 | 152 | 536 | 280 | 53.7% |
| [b16_sealed_potato_chip_bag](exports/b16_sealed_potato_chip_bag.glb) | Handheld | 0.133 × 0.066 × 0.202 | 999 | 242 | 922 | 440 | 92.3% |
| [b16_serrated_takeout_knife](exports/b16_serrated_takeout_knife.glb) | Handheld | 0.026 × 0.181 × 0.005 | 999 | 174 | 690 | 316 | 69.1% |
| [b16_six_egg_carton](exports/b16_six_egg_carton.glb) | Handheld | 0.16 × 0.11 × 0.078 | 999 | 222 | 900 | 404 | 90.1% |
| [b16_soft_street_pretzel](exports/b16_soft_street_pretzel.glb) | Handheld | 0.184 × 0.166 × 0.034 | 999 | 198 | 688 | 368 | 68.9% |
| [b16_square_juice_bottle](exports/b16_square_juice_bottle.glb) | Handheld | 0.065 × 0.055 × 0.169 | 999 | 136 | 488 | 252 | 48.8% |
| [b16_street_taco_in_wrapper](exports/b16_street_taco_in_wrapper.glb) | Handheld | 0.184 × 0.138 × 0.08 | 999 | 210 | 782 | 356 | 78.3% |
| [b16_takeaway_coffee_cup](exports/b16_takeaway_coffee_cup.glb) | Handheld | 0.092 × 0.087 × 0.126 | 999 | 176 | 644 | 336 | 64.5% |
| [b16_torn_sugar_packet](exports/b16_torn_sugar_packet.glb) | Handheld | 0.122 × 0.053 × 0.01 | 999 | 206 | 834 | 384 | 83.5% |
| [b16_triangular_sandwich_half](exports/b16_triangular_sandwich_half.glb) | Handheld | 0.131 × 0.13 × 0.051 | 999 | 214 | 808 | 404 | 80.9% |
| [b16_waffle_ice_cream_cone](exports/b16_waffle_ice_cream_cone.glb) | Handheld | 0.084 × 0.084 × 0.16 | 999 | 221 | 896 | 434 | 89.7% |

### Game Table (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b01_concrete_checker_table](exports/b01_concrete_checker_table.glb) | Medium | 2 × 0.8 × 0.799 | 5,000 | 1,192 | 4,768 | 2,100 | 95.4% |
| [b01_outdoor_chess_pedestal_table](exports/b01_outdoor_chess_pedestal_table.glb) | Medium | 2.12 × 1.1 × 0.819 | 5,000 | 800 | 2,448 | 1,308 | 49.0% |

### Garden Lighting (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_shepherd_hook_lantern_light](exports/b18_shepherd_hook_lantern_light.glb) | Medium | 0.79 × 0.38 × 1.883 | 5,000 | 815 | 3,118 | 1,498 | 62.4% |

### Hand Tools And Portable Construction Tools (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b06_adjustable_wrench](exports/b06_adjustable_wrench.glb) | Handheld | 0.08 × 0.035 × 0.253 | 999 | 138 | 414 | 240 | 41.4% |
| [b06_angle_grinder](exports/b06_angle_grinder.glb) | Handheld | 0.338 × 0.229 × 0.113 | 999 | 280 | 864 | 472 | 86.5% |
| [b06_aviation_snips](exports/b06_aviation_snips.glb) | Handheld | 0.1 × 0.038 × 0.232 | 999 | 146 | 474 | 248 | 47.4% |
| [b06_ball_peen_hammer](exports/b06_ball_peen_hammer.glb) | Handheld | 0.127 × 0.04 × 0.299 | 999 | 234 | 880 | 440 | 88.1% |
| [b06_bolt_cutters](exports/b06_bolt_cutters.glb) | Handheld | 0.232 × 0.057 × 0.65 | 999 | 188 | 612 | 324 | 61.3% |
| [b06_carpenters_square](exports/b06_carpenters_square.glb) | Handheld | 0.24 × 0.004 × 0.4 | 999 | 164 | 492 | 248 | 49.2% |
| [b06_caulking_gun](exports/b06_caulking_gun.glb) | Handheld | 0.448 × 0.065 × 0.128 | 999 | 189 | 572 | 334 | 57.3% |
| [b06_chalk_line_reel](exports/b06_chalk_line_reel.glb) | Handheld | 0.084 × 0.056 × 0.252 | 999 | 234 | 876 | 436 | 87.7% |
| [b06_circular_saw](exports/b06_circular_saw.glb) | Handheld | 0.279 × 0.175 × 0.244 | 999 | 206 | 618 | 356 | 61.9% |
| [b06_claw_hammer](exports/b06_claw_hammer.glb) | Handheld | 0.185 × 0.044 × 0.334 | 999 | 132 | 420 | 228 | 42.0% |
| [b06_club_hammer](exports/b06_club_hammer.glb) | Handheld | 0.17 × 0.052 × 0.292 | 999 | 248 | 928 | 468 | 92.9% |
| [b06_cold_chisel](exports/b06_cold_chisel.glb) | Handheld | 0.038 × 0.03 × 0.213 | 999 | 128 | 496 | 240 | 49.6% |
| [b06_combination_pliers](exports/b06_combination_pliers.glb) | Handheld | 0.092 × 0.032 × 0.187 | 999 | 172 | 552 | 284 | 55.3% |
| [b06_combination_wrench](exports/b06_combination_wrench.glb) | Handheld | 0.068 × 0.012 × 0.235 | 999 | 160 | 602 | 308 | 60.3% |
| [b06_coping_saw](exports/b06_coping_saw.glb) | Handheld | 0.341 × 0.038 × 0.184 | 999 | 148 | 444 | 248 | 44.4% |
| [b06_cordless_drill](exports/b06_cordless_drill.glb) | Handheld | 0.33 × 0.088 × 0.279 | 999 | 246 | 738 | 404 | 73.9% |
| [b06_crowbar](exports/b06_crowbar.glb) | Handheld | 0.118 × 0.034 × 0.623 | 999 | 228 | 912 | 428 | 91.3% |
| [b06_flat_nail_pull_bar](exports/b06_flat_nail_pull_bar.glb) | Handheld | 0.092 × 0.03 × 0.305 | 999 | 120 | 468 | 224 | 46.8% |
| [b06_flat_screwdriver](exports/b06_flat_screwdriver.glb) | Handheld | 0.042 × 0.042 × 0.261 | 999 | 200 | 736 | 372 | 73.7% |
| [b06_folding_hex_key_set](exports/b06_folding_hex_key_set.glb) | Handheld | 0.127 × 0.049 × 0.117 | 999 | 176 | 528 | 296 | 52.9% |
| [b06_hacksaw](exports/b06_hacksaw.glb) | Handheld | 0.425 × 0.041 × 0.148 | 999 | 184 | 552 | 280 | 55.3% |
| [b06_hand_plane](exports/b06_hand_plane.glb) | Handheld | 0.25 × 0.063 × 0.121 | 999 | 132 | 422 | 216 | 42.2% |
| [b06_handsaw](exports/b06_handsaw.glb) | Handheld | 0.5 × 0.029 × 0.112 | 999 | 184 | 552 | 264 | 55.3% |
| [b06_hatchet](exports/b06_hatchet.glb) | Handheld | 0.159 × 0.041 × 0.354 | 999 | 176 | 676 | 328 | 67.7% |
| [b06_heat_gun](exports/b06_heat_gun.glb) | Handheld | 0.238 × 0.09 × 0.251 | 999 | 210 | 630 | 364 | 63.1% |
| [b06_hex_key](exports/b06_hex_key.glb) | Handheld | 0.061 × 0.011 × 0.175 | 999 | 144 | 576 | 272 | 57.7% |
| [b06_impact_driver](exports/b06_impact_driver.glb) | Handheld | 0.268 × 0.093 × 0.272 | 999 | 237 | 714 | 386 | 71.5% |
| [b06_jigsaw](exports/b06_jigsaw.glb) | Handheld | 0.19 × 0.074 × 0.283 | 999 | 190 | 570 | 304 | 57.1% |
| [b06_locking_pliers](exports/b06_locking_pliers.glb) | Handheld | 0.081 × 0.036 × 0.224 | 999 | 148 | 444 | 244 | 44.4% |
| [b06_masonry_bolster](exports/b06_masonry_bolster.glb) | Handheld | 0.112 × 0.084 × 0.23 | 999 | 188 | 700 | 352 | 70.1% |
| [b06_masonry_trowel](exports/b06_masonry_trowel.glb) | Handheld | 0.306 × 0.12 × 0.116 | 999 | 198 | 756 | 372 | 75.7% |
| [b06_needle_nose_pliers](exports/b06_needle_nose_pliers.glb) | Handheld | 0.087 × 0.03 × 0.198 | 999 | 168 | 540 | 276 | 54.1% |
| [b06_orbital_sander](exports/b06_orbital_sander.glb) | Handheld | 0.237 × 0.126 × 0.139 | 999 | 170 | 544 | 288 | 54.5% |
| [b06_pipe_wrench](exports/b06_pipe_wrench.glb) | Handheld | 0.081 × 0.048 × 0.307 | 999 | 142 | 426 | 220 | 42.6% |
| [b06_plastering_float](exports/b06_plastering_float.glb) | Handheld | 0.29 × 0.127 × 0.073 | 999 | 200 | 784 | 372 | 78.5% |
| [b06_plumb_bob](exports/b06_plumb_bob.glb) | Handheld | 0.064 × 0.048 × 0.285 | 999 | 219 | 776 | 406 | 77.7% |
| [b06_pointing_trowel](exports/b06_pointing_trowel.glb) | Handheld | 0.255 × 0.06 × 0.089 | 999 | 178 | 680 | 332 | 68.1% |
| [b06_pruning_secateurs](exports/b06_pruning_secateurs.glb) | Handheld | 0.09 × 0.03 × 0.189 | 999 | 100 | 300 | 164 | 30.0% |
| [b06_reciprocating_saw](exports/b06_reciprocating_saw.glb) | Handheld | 0.632 × 0.082 × 0.183 | 999 | 156 | 468 | 228 | 46.8% |
| [b06_retractable_tape_measure](exports/b06_retractable_tape_measure.glb) | Handheld | 0.252 × 0.056 × 0.079 | 999 | 172 | 516 | 272 | 51.7% |
| [b06_rivet_gun](exports/b06_rivet_gun.glb) | Handheld | 0.141 × 0.037 × 0.171 | 999 | 170 | 546 | 292 | 54.7% |
| [b06_rotary_hammer](exports/b06_rotary_hammer.glb) | Handheld | 0.499 × 0.205 × 0.185 | 999 | 224 | 696 | 380 | 69.7% |
| [b06_rubber_mallet](exports/b06_rubber_mallet.glb) | Handheld | 0.146 × 0.08 × 0.317 | 999 | 256 | 932 | 484 | 93.3% |
| [b06_socket_ratchet](exports/b06_socket_ratchet.glb) | Handheld | 0.05 × 0.077 × 0.223 | 999 | 132 | 420 | 240 | 42.0% |
| [b06_spirit_level](exports/b06_spirit_level.glb) | Handheld | 0.608 × 0.036 × 0.064 | 999 | 160 | 480 | 240 | 48.0% |
| [b06_stubby_phillips_screwdriver](exports/b06_stubby_phillips_screwdriver.glb) | Handheld | 0.052 × 0.049 × 0.1 | 999 | 227 | 840 | 422 | 84.1% |
| [b06_torque_wrench](exports/b06_torque_wrench.glb) | Handheld | 0.05 × 0.059 × 0.424 | 999 | 216 | 672 | 376 | 67.3% |
| [b06_utility_knife](exports/b06_utility_knife.glb) | Handheld | 0.054 × 0.04 × 0.206 | 999 | 190 | 752 | 352 | 75.3% |
| [b06_wire_stripper](exports/b06_wire_stripper.glb) | Handheld | 0.098 × 0.032 × 0.19 | 999 | 208 | 660 | 376 | 66.1% |
| [b06_wood_rasp](exports/b06_wood_rasp.glb) | Handheld | 0.038 × 0.038 × 0.325 | 999 | 162 | 486 | 232 | 48.6% |

### Hanging Lighting (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_festoon_bulb_cable](exports/b18_festoon_bulb_cable.glb) | Large | 5.08 × 0.104 × 0.783 | 10,000 | 1,306 | 5,152 | 2,464 | 51.5% |
| [b18_industrial_pendant_light](exports/b18_industrial_pendant_light.glb) | Medium | 0.61 × 0.61 × 1.116 | 5,000 | 476 | 1,804 | 896 | 36.1% |

### Illuminated Civic Fixture (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_backlit_address_pedestal](exports/b18_backlit_address_pedestal.glb) | Medium | 0.69 × 0.26 × 1.228 | 5,000 | 360 | 1,440 | 660 | 28.8% |

### Landscape Lighting (3)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_flush_inground_uplight](exports/b18_flush_inground_uplight.glb) | Handheld | 0.316 × 0.3 × 0.091 | 999 | 188 | 564 | 344 | 56.5% |
| [b18_ground_stake_spotlight](exports/b18_ground_stake_spotlight.glb) | Handheld | 0.15 × 0.271 × 0.409 | 999 | 155 | 468 | 274 | 46.8% |
| [b18_low_mushroom_landscape_light](exports/b18_low_mushroom_landscape_light.glb) | Handheld | 0.368 × 0.35 × 0.355 | 999 | 170 | 608 | 320 | 60.9% |

### Mail Delivery Cargo (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b14_braced_wood_shipping_crate](exports/b14_braced_wood_shipping_crate.glb) | Medium | 0.976 × 0.914 × 1.105 | 5,000 | 528 | 2,112 | 964 | 42.2% |
| [b14_building_mail_slot](exports/b14_building_mail_slot.glb) | Handheld | 0.38 × 0.103 × 0.26 | 999 | 168 | 672 | 312 | 67.3% |
| [b14_bulk_fertilizer_sack_on_pallet](exports/b14_bulk_fertilizer_sack_on_pallet.glb) | Medium | 1.1 × 1.1 × 1.329 | 5,000 | 508 | 1,536 | 808 | 30.7% |
| [b14_capped_triangular_shipping_tube](exports/b14_capped_triangular_shipping_tube.glb) | Handheld | 0.227 × 0.88 × 0.201 | 999 | 126 | 504 | 228 | 50.5% |
| [b14_cargo_net_secured_mixed_freight](exports/b14_cargo_net_secured_mixed_freight.glb) | Medium | 1.2 × 1.036 × 1.097 | 5,000 | 1,216 | 3,712 | 1,972 | 74.2% |
| [b14_countertop_parcel_postage_scale](exports/b14_countertop_parcel_postage_scale.glb) | Handheld | 0.41 × 0.375 × 0.185 | 999 | 136 | 424 | 216 | 42.4% |
| [b14_curbside_arched_mailbox](exports/b14_curbside_arched_mailbox.glb) | Medium | 0.48 × 0.613 × 1.548 | 5,000 | 304 | 1,172 | 560 | 23.4% |
| [b14_curbside_cluster_mail_station](exports/b14_curbside_cluster_mail_station.glb) | Medium | 1.16 × 0.527 × 1.686 | 5,000 | 824 | 2,488 | 1,248 | 49.8% |
| [b14_drive_through_mail_chute](exports/b14_drive_through_mail_chute.glb) | Medium | 0.68 × 0.993 × 1.61 | 5,000 | 288 | 1,120 | 528 | 22.4% |
| [b14_electronic_parcel_locker](exports/b14_electronic_parcel_locker.glb) | Medium | 2.16 × 0.854 × 2.132 | 5,000 | 780 | 2,356 | 1,236 | 47.1% |
| [b14_empty_wood_shipping_pallet](exports/b14_empty_wood_shipping_pallet.glb) | Medium | 1.2 × 1 × 0.202 | 5,000 | 696 | 2,784 | 1,260 | 55.7% |
| [b14_expandable_roller_conveyor](exports/b14_expandable_roller_conveyor.glb) | Large | 0.876 × 2.949 × 1.011 | 10,000 | 1,704 | 5,232 | 2,888 | 52.3% |
| [b14_floor_pallet_weighing_scale](exports/b14_floor_pallet_weighing_scale.glb) | Medium | 1.51 × 1.24 × 1.369 | 5,000 | 368 | 1,456 | 672 | 29.1% |
| [b14_folding_platform_delivery_cart](exports/b14_folding_platform_delivery_cart.glb) | Medium | 0.62 × 0.92 × 0.928 | 5,000 | 920 | 3,512 | 1,720 | 70.2% |
| [b14_handheld_stretch_wrap_dispenser](exports/b14_handheld_stretch_wrap_dispenser.glb) | Handheld | 0.228 × 0.217 × 0.7 | 999 | 248 | 880 | 468 | 88.1% |
| [b14_home_delivery_lock_chest](exports/b14_home_delivery_lock_chest.glb) | Medium | 0.82 × 0.7 × 0.875 | 5,000 | 492 | 1,936 | 908 | 38.7% |
| [b14_ibc_tote_with_valve](exports/b14_ibc_tote_with_valve.glb) | Medium | 1.2 × 1.084 × 1.27 | 5,000 | 708 | 2,140 | 1,156 | 42.8% |
| [b14_insulated_medical_shipping_chest](exports/b14_insulated_medical_shipping_chest.glb) | Medium | 0.71 × 0.476 × 0.535 | 5,000 | 512 | 1,984 | 956 | 39.7% |
| [b14_loading_dock_laminated_bumpers](exports/b14_loading_dock_laminated_bumpers.glb) | Medium | 1.85 × 0.301 × 0.76 | 5,000 | 792 | 3,168 | 1,468 | 63.4% |
| [b14_mail_sack_sorting_stand](exports/b14_mail_sack_sorting_stand.glb) | Medium | 0.55 × 0.45 × 1.022 | 5,000 | 632 | 2,344 | 1,188 | 46.9% |
| [b14_manual_pallet_jack](exports/b14_manual_pallet_jack.glb) | Medium | 0.61 × 1.539 × 1.28 | 5,000 | 800 | 3,012 | 1,512 | 60.2% |
| [b14_mobile_letter_sorting_cubbies](exports/b14_mobile_letter_sorting_cubbies.glb) | Medium | 1.238 × 0.585 × 1.769 | 5,000 | 1,164 | 4,528 | 2,160 | 90.6% |
| [b14_mobile_yard_loading_ramp](exports/b14_mobile_yard_loading_ramp.glb) | Large | 2.433 × 4.88 × 1.346 | 10,000 | 1,048 | 4,072 | 1,944 | 40.7% |
| [b14_open_slatted_parts_crate](exports/b14_open_slatted_parts_crate.glb) | Medium | 0.748 × 0.53 × 0.562 | 5,000 | 600 | 2,400 | 1,100 | 48.0% |
| [b14_pallet_bagged_mortar](exports/b14_pallet_bagged_mortar.glb) | Medium | 1.2 × 1 × 0.96 | 5,000 | 1,352 | 4,296 | 2,308 | 85.9% |
| [b14_pallet_carton_stack](exports/b14_pallet_carton_stack.glb) | Medium | 1.2 × 1 × 1.133 | 5,000 | 1,272 | 4,008 | 2,052 | 80.2% |
| [b14_pallet_four_chemical_drums](exports/b14_pallet_four_chemical_drums.glb) | Medium | 1.3 × 1.3 × 1.072 | 5,000 | 1,048 | 3,672 | 1,884 | 73.4% |
| [b14_pallet_lumber_bundle](exports/b14_pallet_lumber_bundle.glb) | Medium | 1.1 × 2.4 × 0.612 | 5,000 | 488 | 1,464 | 732 | 29.3% |
| [b14_pallet_strapped_masonry_bricks](exports/b14_pallet_strapped_masonry_bricks.glb) | Medium | 1.04 × 0.86 × 0.759 | 5,000 | 792 | 2,376 | 1,188 | 47.5% |
| [b14_parcel_hand_truck](exports/b14_parcel_hand_truck.glb) | Medium | 0.628 × 0.615 × 1.3 | 5,000 | 664 | 2,536 | 1,252 | 50.7% |
| [b14_postal_carrier_satchel](exports/b14_postal_carrier_satchel.glb) | Handheld | 0.4 × 0.192 × 0.586 | 999 | 176 | 540 | 288 | 54.1% |
| [b14_postal_collection_drop_box](exports/b14_postal_collection_drop_box.glb) | Medium | 0.64 × 0.658 × 1.4 | 5,000 | 388 | 1,538 | 712 | 30.8% |
| [b14_postal_relay_storage_box](exports/b14_postal_relay_storage_box.glb) | Medium | 0.75 × 0.691 × 1.34 | 5,000 | 460 | 1,826 | 852 | 36.5% |
| [b14_postal_rolling_canvas_hamper](exports/b14_postal_rolling_canvas_hamper.glb) | Medium | 0.83 × 0.8 × 1.111 | 5,000 | 688 | 2,196 | 1,196 | 43.9% |
| [b14_rackable_plastic_pallet](exports/b14_rackable_plastic_pallet.glb) | Medium | 1.2 × 1 × 0.193 | 5,000 | 504 | 2,016 | 924 | 40.3% |
| [b14_recessed_apartment_mail_wall](exports/b14_recessed_apartment_mail_wall.glb) | Medium | 1.26 × 0.218 × 1.36 | 5,000 | 608 | 1,824 | 952 | 36.5% |
| [b14_recessed_hydraulic_dock_leveler](exports/b14_recessed_hydraulic_dock_leveler.glb) | Large | 2.13 × 2.85 × 0.811 | 10,000 | 360 | 1,392 | 656 | 13.9% |
| [b14_reinforced_shipping_flight_case](exports/b14_reinforced_shipping_flight_case.glb) | Medium | 0.882 × 0.565 × 0.645 | 5,000 | 780 | 3,120 | 1,432 | 62.4% |
| [b14_skidded_steel_pipe_bundle](exports/b14_skidded_steel_pipe_bundle.glb) | Medium | 1.2 × 2.208 × 0.712 | 5,000 | 736 | 2,208 | 1,272 | 44.2% |
| [b14_skidded_wrapped_appliance](exports/b14_skidded_wrapped_appliance.glb) | Medium | 0.83 × 0.79 × 1.909 | 5,000 | 448 | 1,360 | 684 | 27.2% |
| [b14_stackable_attached_lid_delivery_tote](exports/b14_stackable_attached_lid_delivery_tote.glb) | Medium | 0.66 × 0.478 × 0.403 | 5,000 | 480 | 1,888 | 880 | 37.8% |
| [b14_stair_climbing_appliance_dolly](exports/b14_stair_climbing_appliance_dolly.glb) | Medium | 0.73 × 0.686 × 1.463 | 5,000 | 624 | 1,992 | 1,096 | 39.8% |
| [b14_steel_shipping_drum](exports/b14_steel_shipping_drum.glb) | Medium | 0.58 × 0.585 × 0.869 | 5,000 | 328 | 1,256 | 628 | 25.1% |
| [b14_strapping_reel_and_tensioner_cart](exports/b14_strapping_reel_and_tensioner_cart.glb) | Medium | 0.6 × 0.81 × 0.914 | 5,000 | 764 | 2,904 | 1,444 | 58.1% |
| [b14_truck_tail_liftgate_assembly](exports/b14_truck_tail_liftgate_assembly.glb) | Large | 1.96 × 2.02 × 1.48 | 10,000 | 696 | 2,656 | 1,284 | 26.6% |
| [b14_twenty_foot_freight_container](exports/b14_twenty_foot_freight_container.glb) | Large | 2.6 × 6.288 × 2.601 | 10,000 | 1,976 | 6,400 | 3,036 | 64.0% |
| [b14_wall_letterbox_with_flap](exports/b14_wall_letterbox_with_flap.glb) | Handheld | 0.375 × 0.214 × 0.472 | 999 | 240 | 928 | 448 | 92.9% |
| [b14_warehouse_counterbalance_forklift](exports/b14_warehouse_counterbalance_forklift.glb) | Large | 1.257 × 2.839 × 2.206 | 10,000 | 2,380 | 8,944 | 4,492 | 89.4% |
| [b14_wire_cage_roll_container](exports/b14_wire_cage_roll_container.glb) | Medium | 0.828 × 0.75 × 1.78 | 5,000 | 880 | 2,736 | 1,508 | 54.7% |
| [b14_wooden_cable_reel_on_skid](exports/b14_wooden_cable_reel_on_skid.glb) | Medium | 1.1 × 1 × 1.209 | 5,000 | 776 | 2,568 | 1,344 | 51.4% |

### Municipal Commercial Emergency Vehicles (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b15_aerial_ladder_fire_truck](exports/b15_aerial_ladder_fire_truck.glb) | Large | 11.579 × 3.08 × 3.692 | 10,000 | 3,306 | 8,836 | 4,700 | 88.4% |
| [b15_airport_crash_tender](exports/b15_airport_crash_tender.glb) | Large | 10.936 × 3.357 × 3.704 | 10,000 | 2,518 | 7,080 | 3,828 | 70.8% |
| [b15_airport_shuttle_bus](exports/b15_airport_shuttle_bus.glb) | Large | 9.26 × 3.075 × 3.4 | 10,000 | 1,874 | 5,154 | 2,764 | 51.5% |
| [b15_armored_security_truck](exports/b15_armored_security_truck.glb) | Large | 7.44 × 2.854 × 3.02 | 10,000 | 1,912 | 5,432 | 2,896 | 54.3% |
| [b15_articulated_transit_bus](exports/b15_articulated_transit_bus.glb) | Large | 18.085 × 3.125 × 3.45 | 10,000 | 3,200 | 8,794 | 4,696 | 87.9% |
| [b15_automated_side_loader_refuse_truck](exports/b15_automated_side_loader_refuse_truck.glb) | Large | 9.829 × 3.765 × 3.405 | 10,000 | 2,114 | 5,900 | 3,220 | 59.0% |
| [b15_beverage_delivery_truck](exports/b15_beverage_delivery_truck.glb) | Large | 9.829 × 3 × 3.235 | 10,000 | 2,790 | 7,930 | 4,224 | 79.3% |
| [b15_bucket_utility_truck](exports/b15_bucket_utility_truck.glb) | Large | 9.18 × 3.014 × 3.785 | 10,000 | 1,916 | 5,446 | 2,920 | 54.5% |
| [b15_cable_spool_utility_truck](exports/b15_cable_spool_utility_truck.glb) | Large | 8.68 × 2.882 × 2.93 | 10,000 | 1,912 | 5,434 | 2,928 | 54.3% |
| [b15_commercial_box_truck](exports/b15_commercial_box_truck.glb) | Large | 8.93 × 2.901 × 3.42 | 10,000 | 1,836 | 5,218 | 2,788 | 52.2% |
| [b15_conventional_school_bus](exports/b15_conventional_school_bus.glb) | Large | 11.095 × 3.005 × 3.18 | 10,000 | 1,968 | 5,402 | 2,920 | 54.0% |
| [b15_fire_pumper_engine](exports/b15_fire_pumper_engine.glb) | Large | 9.43 × 2.92 × 3.115 | 10,000 | 2,688 | 7,536 | 4,052 | 75.4% |
| [b15_fire_water_tender](exports/b15_fire_water_tender.glb) | Large | 9.85 × 2.911 × 3.16 | 10,000 | 2,594 | 7,450 | 4,076 | 74.5% |
| [b15_flatbed_stake_truck](exports/b15_flatbed_stake_truck.glb) | Large | 9.079 × 2.882 × 2.708 | 10,000 | 1,748 | 4,942 | 2,640 | 49.4% |
| [b15_food_service_truck](exports/b15_food_service_truck.glb) | Large | 7.76 × 3.451 × 3.76 | 10,000 | 1,535 | 4,310 | 2,342 | 43.1% |
| [b15_front_loader_refuse_truck](exports/b15_front_loader_refuse_truck.glb) | Large | 11.98 × 2.939 × 3.61 | 10,000 | 2,146 | 5,996 | 3,264 | 60.0% |
| [b15_fuel_delivery_tanker](exports/b15_fuel_delivery_tanker.glb) | Large | 9.88 × 2.921 × 3.683 | 10,000 | 2,586 | 7,510 | 4,100 | 75.1% |
| [b15_glass_transport_truck](exports/b15_glass_transport_truck.glb) | Large | 8.88 × 2.882 × 2.98 | 10,000 | 1,700 | 4,798 | 2,568 | 48.0% |
| [b15_heavy_recovery_wrecker](exports/b15_heavy_recovery_wrecker.glb) | Large | 11.909 × 3.08 × 3.03 | 10,000 | 2,518 | 7,170 | 3,888 | 71.7% |
| [b15_heavy_rescue_squad](exports/b15_heavy_rescue_squad.glb) | Large | 9.729 × 2.911 × 3.73 | 10,000 | 2,440 | 6,848 | 3,620 | 68.5% |
| [b15_hi_rail_utility_truck](exports/b15_hi_rail_utility_truck.glb) | Large | 8.35 × 2.825 × 2.933 | 10,000 | 2,060 | 5,878 | 3,192 | 58.8% |
| [b15_ice_cream_truck](exports/b15_ice_cream_truck.glb) | Large | 6.12 × 2.85 × 3.88 | 10,000 | 1,521 | 4,322 | 2,334 | 43.2% |
| [b15_intercity_motor_coach](exports/b15_intercity_motor_coach.glb) | Large | 12.785 × 3.125 × 3.89 | 10,000 | 2,622 | 7,156 | 3,856 | 71.6% |
| [b15_line_maintenance_service_truck](exports/b15_line_maintenance_service_truck.glb) | Large | 7.979 × 2.835 × 3.23 | 10,000 | 2,132 | 5,902 | 3,152 | 59.0% |
| [b15_low_floor_transit_bus](exports/b15_low_floor_transit_bus.glb) | Large | 12.531 × 3.125 × 3.625 | 10,000 | 1,986 | 5,362 | 2,868 | 53.6% |
| [b15_mobile_command_bus](exports/b15_mobile_command_bus.glb) | Large | 10.635 × 3.095 × 4.92 | 10,000 | 1,930 | 5,302 | 2,832 | 53.0% |
| [b15_mobile_library_bus](exports/b15_mobile_library_bus.glb) | Large | 9.635 × 3.851 × 3.61 | 10,000 | 1,858 | 5,074 | 2,724 | 50.7% |
| [b15_modular_ambulance](exports/b15_modular_ambulance.glb) | Large | 7.429 × 2.835 × 3.225 | 10,000 | 1,988 | 5,674 | 3,016 | 56.7% |
| [b15_municipal_dump_truck](exports/b15_municipal_dump_truck.glb) | Large | 9.43 × 2.921 × 3.04 | 10,000 | 2,230 | 6,250 | 3,388 | 62.5% |
| [b15_open_top_tour_bus](exports/b15_open_top_tour_bus.glb) | Large | 11.185 × 3.125 × 4.215 | 10,000 | 1,994 | 5,410 | 2,876 | 54.1% |
| [b15_paratransit_shuttle_bus](exports/b15_paratransit_shuttle_bus.glb) | Large | 7.235 × 2.905 × 3.24 | 10,000 | 1,770 | 4,938 | 2,656 | 49.4% |
| [b15_parcel_step_van](exports/b15_parcel_step_van.glb) | Large | 7.22 × 2.74 × 3.05 | 10,000 | 1,502 | 4,206 | 2,268 | 42.1% |
| [b15_postal_walkin_truck](exports/b15_postal_walkin_truck.glb) | Large | 5.48 × 2.52 × 3.1 | 10,000 | 2,738 | 9,718 | 4,788 | 97.2% |
| [b15_prisoner_transport_truck](exports/b15_prisoner_transport_truck.glb) | Large | 8.579 × 2.873 × 3.49 | 10,000 | 2,140 | 6,138 | 3,264 | 61.4% |
| [b15_rear_loader_refuse_truck](exports/b15_rear_loader_refuse_truck.glb) | Large | 10.019 × 2.939 × 3.35 | 10,000 | 2,134 | 5,960 | 3,248 | 59.6% |
| [b15_refrigerated_delivery_truck](exports/b15_refrigerated_delivery_truck.glb) | Large | 8.78 × 2.976 × 3.555 | 10,000 | 1,888 | 5,360 | 2,880 | 53.6% |
| [b15_rollback_tow_truck](exports/b15_rollback_tow_truck.glb) | Large | 9.27 × 2.873 × 2.708 | 10,000 | 1,720 | 4,858 | 2,636 | 48.6% |
| [b15_rolloff_container_truck](exports/b15_rolloff_container_truck.glb) | Large | 10.47 × 2.93 × 3.24 | 10,000 | 2,278 | 6,394 | 3,464 | 63.9% |
| [b15_sewer_vacuum_truck](exports/b15_sewer_vacuum_truck.glb) | Large | 10.18 × 2.921 × 3.69 | 10,000 | 2,414 | 6,884 | 3,788 | 68.8% |
| [b15_short_school_bus](exports/b15_short_school_bus.glb) | Large | 7.745 × 3.005 × 3.18 | 10,000 | 1,840 | 5,146 | 2,792 | 51.5% |
| [b15_snowplow_spreader_truck](exports/b15_snowplow_spreader_truck.glb) | Large | 11.341 × 3.189 × 2.985 | 10,000 | 2,286 | 6,402 | 3,472 | 64.0% |
| [b15_split_body_recycling_truck](exports/b15_split_body_recycling_truck.glb) | Large | 9.235 × 2.911 × 3.52 | 10,000 | 1,688 | 4,760 | 2,564 | 47.6% |
| [b15_street_marking_truck](exports/b15_street_marking_truck.glb) | Large | 8.68 × 3.292 × 2.928 | 10,000 | 1,988 | 5,648 | 3,096 | 56.5% |
| [b15_tactical_rescue_truck](exports/b15_tactical_rescue_truck.glb) | Large | 8.61 × 2.93 × 3.285 | 10,000 | 1,876 | 5,338 | 2,888 | 53.4% |
| [b15_tiller_ladder_fire_truck](exports/b15_tiller_ladder_fire_truck.glb) | Large | 15.93 × 3.08 × 3.692 | 10,000 | 3,538 | 9,372 | 4,976 | 93.7% |
| [b15_tree_service_chip_truck](exports/b15_tree_service_chip_truck.glb) | Large | 8.956 × 2.873 × 3.38 | 10,000 | 1,760 | 5,004 | 2,672 | 50.0% |
| [b15_van_ambulance](exports/b15_van_ambulance.glb) | Large | 6.42 × 2.56 × 2.925 | 10,000 | 1,486 | 4,158 | 2,244 | 41.6% |
| [b15_water_spray_truck](exports/b15_water_spray_truck.glb) | Large | 9.877 × 2.901 × 3.33 | 10,000 | 2,446 | 6,994 | 3,836 | 69.9% |
| [b15_wheel_lift_tow_truck](exports/b15_wheel_lift_tow_truck.glb) | Large | 8.309 × 2.797 × 2.77 | 10,000 | 1,932 | 5,550 | 2,984 | 55.5% |
| [b15_wildland_brush_fire_truck](exports/b15_wildland_brush_fire_truck.glb) | Large | 7.315 × 2.768 × 2.905 | 10,000 | 1,796 | 5,086 | 2,744 | 50.9% |

### Outdoor Event (20)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b20_dual_pump_handwash_station](exports/b20_dual_pump_handwash_station.glb) | Medium | 0.82 × 0.707 × 1.255 | 5,000 | 624 | 2,360 | 1,176 | 47.2% |
| [b20_event_lighting_truss_goalpost](exports/b20_event_lighting_truss_goalpost.glb) | Large | 4.14 × 0.72 × 3.025 | 10,000 | 2,376 | 9,912 | 4,392 | 99.1% |
| [b20_event_tent_ballast_water_tank](exports/b20_event_tent_ballast_water_tank.glb) | Medium | 0.72 × 0.725 × 1.059 | 5,000 | 576 | 2,236 | 1,088 | 44.7% |
| [b20_festival_ticket_inspection_podium](exports/b20_festival_ticket_inspection_podium.glb) | Medium | 0.76 × 0.58 × 1.166 | 5,000 | 232 | 928 | 424 | 18.6% |
| [b20_five_channel_event_cable_ramp](exports/b20_five_channel_event_cable_ramp.glb) | Medium | 1.075 × 0.597 × 0.105 | 5,000 | 476 | 1,900 | 872 | 38.0% |
| [b20_folding_banquet_service_table](exports/b20_folding_banquet_service_table.glb) | Large | 1.82 × 0.76 × 0.779 | 10,000 | 424 | 1,600 | 788 | 16.0% |
| [b20_interlocking_portable_dance_floor](exports/b20_interlocking_portable_dance_floor.glb) | Large | 2.6 × 2.63 × 0.087 | 10,000 | 1,728 | 6,912 | 3,168 | 69.1% |
| [b20_modular_stage_riser](exports/b20_modular_stage_riser.glb) | Large | 2.4 × 1.22 × 0.765 | 10,000 | 664 | 2,528 | 1,228 | 25.3% |
| [b20_outdoor_event_misting_fan](exports/b20_outdoor_event_misting_fan.glb) | Medium | 0.758 × 0.5 × 2.049 | 5,000 | 1,196 | 4,812 | 2,272 | 96.2% |
| [b20_outdoor_speaking_lectern](exports/b20_outdoor_speaking_lectern.glb) | Medium | 0.65 × 0.477 × 1.481 | 5,000 | 264 | 1,040 | 488 | 20.8% |
| [b20_pa_loudspeaker_on_tripod](exports/b20_pa_loudspeaker_on_tripod.glb) | Medium | 0.953 × 1.099 × 2.26 | 5,000 | 504 | 1,864 | 952 | 37.3% |
| [b20_pagoda_festival_marquee](exports/b20_pagoda_festival_marquee.glb) | Large | 4.1 × 4.1 × 4.145 | 10,000 | 637 | 2,410 | 1,122 | 24.1% |
| [b20_pop_up_event_canopy](exports/b20_pop_up_event_canopy.glb) | Large | 3.035 × 3.035 × 2.837 | 10,000 | 641 | 2,576 | 1,176 | 25.8% |
| [b20_portable_audio_mixing_console](exports/b20_portable_audio_mixing_console.glb) | Medium | 1.065 × 0.692 × 1.035 | 5,000 | 624 | 1,872 | 1,004 | 37.4% |
| [b20_portable_festival_restroom](exports/b20_portable_festival_restroom.glb) | Medium | 1.16 × 1.19 × 2.435 | 5,000 | 746 | 2,894 | 1,376 | 57.9% |
| [b20_portable_outdoor_shower_cubicle](exports/b20_portable_outdoor_shower_cubicle.glb) | Medium | 1.19 × 1.326 × 2.63 | 5,000 | 1,072 | 3,736 | 1,990 | 74.7% |
| [b20_portable_stage_stair_module](exports/b20_portable_stage_stair_module.glb) | Medium | 1.02 × 1.373 × 1.591 | 5,000 | 592 | 2,272 | 1,088 | 45.4% |
| [b20_retractable_belt_queue_stanchion](exports/b20_retractable_belt_queue_stanchion.glb) | Medium | 0.709 × 0.373 × 1.027 | 5,000 | 204 | 732 | 384 | 14.6% |
| [b20_stage_floor_monitor_wedge](exports/b20_stage_floor_monitor_wedge.glb) | Medium | 0.6 × 0.515 × 0.414 | 5,000 | 238 | 926 | 440 | 18.5% |
| [b20_wheeled_audio_flight_case](exports/b20_wheeled_audio_flight_case.glb) | Medium | 0.865 × 0.622 × 0.831 | 5,000 | 1,300 | 4,912 | 2,436 | 98.2% |

### Outdoor Table (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b01_standing_barrel_community_table](exports/b01_standing_barrel_community_table.glb) | Medium | 1.32 × 1.311 × 1.058 | 5,000 | 596 | 1,860 | 1,036 | 37.2% |

### Park Lighting (4)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_acorn_globe_park_lamp](exports/b18_acorn_globe_park_lamp.glb) | Large | 0.505 × 0.505 × 4.125 | 10,000 | 1,017 | 3,884 | 1,918 | 38.8% |
| [b18_schoolhouse_globe_lamp](exports/b18_schoolhouse_globe_lamp.glb) | Large | 0.615 × 0.615 × 3.78 | 10,000 | 785 | 2,888 | 1,486 | 28.9% |
| [b18_shielded_mushroom_posttop](exports/b18_shielded_mushroom_posttop.glb) | Large | 0.92 × 0.92 × 3.46 | 10,000 | 692 | 2,620 | 1,308 | 26.2% |
| [b18_tapered_lantern_avenue_lamp](exports/b18_tapered_lantern_avenue_lamp.glb) | Large | 0.722 × 0.722 × 4.155 | 10,000 | 1,198 | 4,584 | 2,220 | 45.8% |

### Parking (10)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b02_concrete_wheel_stop](exports/b02_concrete_wheel_stop.glb) | Medium | 1.68 × 0.28 × 0.186 | 5,000 | 216 | 828 | 404 | 16.6% |
| [b02_dual_parking_meter](exports/b02_dual_parking_meter.glb) | Medium | 0.69 × 0.3 × 1.695 | 5,000 | 848 | 3,312 | 1,568 | 66.2% |
| [b02_parking_gate_arm](exports/b02_parking_gate_arm.glb) | Large | 3.855 × 0.656 × 1.25 | 10,000 | 296 | 1,144 | 548 | 11.4% |
| [b02_parking_height_clearance_gantry](exports/b02_parking_height_clearance_gantry.glb) | Large | 4.42 × 0.205 × 3.13 | 10,000 | 1,392 | 5,376 | 2,592 | 53.8% |
| [b02_parking_pay_station](exports/b02_parking_pay_station.glb) | Medium | 0.62 × 0.53 × 1.749 | 5,000 | 616 | 2,464 | 1,128 | 49.3% |
| [b02_parking_ticket_dispenser](exports/b02_parking_ticket_dispenser.glb) | Medium | 0.65 × 0.66 × 1.585 | 5,000 | 224 | 876 | 412 | 17.5% |
| [b02_removable_locking_bollard](exports/b02_removable_locking_bollard.glb) | Medium | 0.22 × 0.22 × 1.05 | 5,000 | 252 | 1,008 | 468 | 20.2% |
| [b02_rubber_parking_curb](exports/b02_rubber_parking_curb.glb) | Medium | 1.4 × 0.273 × 0.132 | 5,000 | 360 | 1,332 | 672 | 26.6% |
| [b02_single_parking_meter](exports/b02_single_parking_meter.glb) | Medium | 0.23 × 0.301 × 1.685 | 5,000 | 536 | 2,080 | 1,000 | 41.6% |
| [b02_steel_safety_bollard](exports/b02_steel_safety_bollard.glb) | Medium | 0.3 × 0.3 × 1.126 | 5,000 | 290 | 1,132 | 548 | 22.6% |

### Parking Lighting (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_twin_shoebox_parking_lamp](exports/b18_twin_shoebox_parking_lamp.glb) | Large | 2 × 0.57 × 7.12 | 10,000 | 1,264 | 5,048 | 2,336 | 50.5% |

### Passenger Vehicles (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b03_angular_electric_pickup](exports/b03_angular_electric_pickup.glb) | Large | 5.89 × 2.522 × 1.982 | 10,000 | 3,299 | 8,966 | 4,910 | 89.7% |
| [b03_battery_kick_scooter](exports/b03_battery_kick_scooter.glb) | Medium | 1.134 × 0.47 × 1.199 | 5,000 | 1,004 | 3,824 | 1,908 | 76.5% |
| [b03_child_training_wheel_bicycle](exports/b03_child_training_wheel_bicycle.glb) | Medium | 1.35 × 0.61 × 0.78 | 5,000 | 976 | 3,312 | 1,712 | 66.2% |
| [b03_chrome_trim_classic_sedan](exports/b03_chrome_trim_classic_sedan.glb) | Large | 5.1 × 2.322 × 1.743 | 10,000 | 3,315 | 9,334 | 5,162 | 93.3% |
| [b03_classic_muscle_coupe](exports/b03_classic_muscle_coupe.glb) | Large | 5.09 × 2.344 × 1.363 | 10,000 | 3,295 | 9,620 | 5,158 | 96.2% |
| [b03_compact_notchback_sedan](exports/b03_compact_notchback_sedan.glb) | Large | 4.48 × 2.11 × 1.444 | 10,000 | 3,091 | 8,698 | 4,810 | 87.0% |
| [b03_compact_square_suv](exports/b03_compact_square_suv.glb) | Large | 4.74 × 2.277 × 1.945 | 10,000 | 3,211 | 9,014 | 4,958 | 90.1% |
| [b03_compact_station_wagon](exports/b03_compact_station_wagon.glb) | Large | 4.86 × 2.188 × 1.676 | 10,000 | 3,185 | 8,914 | 4,910 | 89.1% |
| [b03_compact_unibody_pickup](exports/b03_compact_unibody_pickup.glb) | Large | 5.19 × 2.288 × 1.773 | 10,000 | 3,275 | 8,926 | 4,898 | 89.3% |
| [b03_crew_cab_shortbed_pickup](exports/b03_crew_cab_shortbed_pickup.glb) | Large | 6.02 × 2.5 × 1.972 | 10,000 | 3,275 | 8,970 | 4,922 | 89.7% |
| [b03_drop_bar_road_bicycle](exports/b03_drop_bar_road_bicycle.glb) | Medium | 1.81 × 0.604 × 1.025 | 5,000 | 724 | 2,364 | 1,240 | 47.3% |
| [b03_extended_cab_pickup](exports/b03_extended_cab_pickup.glb) | Large | 6 × 2.422 × 1.902 | 10,000 | 3,275 | 8,914 | 4,874 | 89.1% |
| [b03_faired_sport_motorcycle](exports/b03_faired_sport_motorcycle.glb) | Medium | 2.15 × 0.91 × 1.36 | 5,000 | 1,086 | 3,556 | 1,892 | 71.1% |
| [b03_family_minivan](exports/b03_family_minivan.glb) | Large | 5.34 × 2.355 × 1.833 | 10,000 | 3,195 | 8,934 | 4,934 | 89.3% |
| [b03_five_door_fastback](exports/b03_five_door_fastback.glb) | Large | 5.11 × 2.299 × 1.483 | 10,000 | 3,099 | 9,114 | 4,822 | 91.1% |
| [b03_five_door_tall_hatchback](exports/b03_five_door_tall_hatchback.glb) | Large | 4.29 × 2.143 × 1.624 | 10,000 | 3,091 | 8,746 | 4,810 | 87.5% |
| [b03_folding_kick_scooter](exports/b03_folding_kick_scooter.glb) | Medium | 1.074 × 0.47 × 1.079 | 5,000 | 956 | 3,632 | 1,820 | 72.6% |
| [b03_four_seat_convertible](exports/b03_four_seat_convertible.glb) | Large | 5.06 × 2.299 × 1.484 | 10,000 | 3,023 | 8,522 | 4,564 | 85.2% |
| [b03_front_box_cargo_bicycle](exports/b03_front_box_cargo_bicycle.glb) | Medium | 2.85 × 0.695 × 1.088 | 5,000 | 752 | 2,448 | 1,280 | 49.0% |
| [b03_fullsize_luxury_sedan](exports/b03_fullsize_luxury_sedan.glb) | Large | 5.51 × 2.4 × 1.543 | 10,000 | 3,147 | 8,746 | 4,862 | 87.5% |
| [b03_fullsize_passenger_van](exports/b03_fullsize_passenger_van.glb) | Large | 5.76 × 2.467 × 2.295 | 10,000 | 3,315 | 9,242 | 5,082 | 92.4% |
| [b03_fullsize_towing_suv](exports/b03_fullsize_towing_suv.glb) | Large | 6.043 × 2.522 × 2.144 | 10,000 | 3,267 | 9,146 | 5,050 | 91.5% |
| [b03_highroof_passenger_van](exports/b03_highroof_passenger_van.glb) | Large | 6.15 × 2.534 × 2.865 | 10,000 | 3,347 | 9,306 | 5,130 | 93.1% |
| [b03_long_fork_dirt_motorcycle](exports/b03_long_fork_dirt_motorcycle.glb) | Medium | 2.23 × 0.91 × 1.36 | 5,000 | 1,120 | 3,674 | 1,956 | 73.5% |
| [b03_longroof_surf_wagon](exports/b03_longroof_surf_wagon.glb) | Large | 5.47 × 2.333 × 1.902 | 10,000 | 3,253 | 9,072 | 5,022 | 90.7% |
| [b03_longtail_family_cargo_bicycle](exports/b03_longtail_family_cargo_bicycle.glb) | Medium | 2.337 × 0.74 × 1.061 | 5,000 | 888 | 2,856 | 1,492 | 57.1% |
| [b03_luggage_touring_motorcycle](exports/b03_luggage_touring_motorcycle.glb) | Medium | 2.15 × 0.91 × 1.45 | 5,000 | 1,114 | 3,656 | 1,940 | 73.1% |
| [b03_midengine_sports_coupe](exports/b03_midengine_sports_coupe.glb) | Large | 4.61 × 2.4 × 1.184 | 10,000 | 3,038 | 8,938 | 4,718 | 89.4% |
| [b03_midsize_sedan](exports/b03_midsize_sedan.glb) | Large | 5.06 × 2.243 × 1.503 | 10,000 | 3,065 | 8,634 | 4,762 | 86.3% |
| [b03_rear_basket_adult_tricycle](exports/b03_rear_basket_adult_tricycle.glb) | Medium | 1.87 × 0.93 × 1.117 | 5,000 | 860 | 2,868 | 1,484 | 57.4% |
| [b03_recumbent_tadpole_tricycle](exports/b03_recumbent_tadpole_tricycle.glb) | Medium | 2.235 × 1.03 × 1.341 | 5,000 | 675 | 2,307 | 1,185 | 46.1% |
| [b03_regular_cab_work_pickup](exports/b03_regular_cab_work_pickup.glb) | Large | 5.49 × 2.411 × 1.882 | 10,000 | 3,155 | 8,634 | 4,706 | 86.3% |
| [b03_small_wheel_folding_bicycle](exports/b03_small_wheel_folding_bicycle.glb) | Medium | 1.587 × 0.57 × 1.063 | 5,000 | 776 | 2,520 | 1,308 | 50.4% |
| [b03_sport_coupe_crossover](exports/b03_sport_coupe_crossover.glb) | Large | 5.02 × 2.366 × 1.895 | 10,000 | 3,155 | 9,278 | 4,906 | 92.8% |
| [b03_stepside_sport_pickup](exports/b03_stepside_sport_pickup.glb) | Large | 5.08 × 2.221 × 1.733 | 10,000 | 3,363 | 9,246 | 5,050 | 92.5% |
| [b03_stepthrough_city_bicycle](exports/b03_stepthrough_city_bicycle.glb) | Medium | 1.937 × 0.74 × 1.042 | 5,000 | 844 | 2,724 | 1,420 | 54.5% |
| [b03_stepthrough_motor_scooter](exports/b03_stepthrough_motor_scooter.glb) | Medium | 1.752 × 0.91 × 1.27 | 5,000 | 870 | 2,890 | 1,544 | 57.8% |
| [b03_stretch_limousine](exports/b03_stretch_limousine.glb) | Large | 7.93 × 2.4 × 1.538 | 10,000 | 3,331 | 9,206 | 5,074 | 92.1% |
| [b03_stunt_bmx_bicycle](exports/b03_stunt_bmx_bicycle.glb) | Medium | 1.63 × 0.57 × 0.85 | 5,000 | 700 | 2,292 | 1,200 | 45.8% |
| [b03_subcompact_crossover](exports/b03_subcompact_crossover.glb) | Large | 4.45 × 2.199 × 1.856 | 10,000 | 3,155 | 8,938 | 4,906 | 89.4% |
| [b03_suspension_mountain_bicycle](exports/b03_suspension_mountain_bicycle.glb) | Medium | 1.81 × 0.57 × 1.025 | 5,000 | 740 | 2,452 | 1,280 | 49.0% |
| [b03_swept_bar_beach_cruiser](exports/b03_swept_bar_beach_cruiser.glb) | Medium | 1.937 × 0.62 × 1.042 | 5,000 | 836 | 2,700 | 1,412 | 54.0% |
| [b03_three_door_city_hatchback](exports/b03_three_door_city_hatchback.glb) | Large | 3.88 × 2.054 × 1.494 | 10,000 | 3,091 | 8,746 | 4,810 | 87.5% |
| [b03_three_row_family_suv](exports/b03_three_row_family_suv.glb) | Large | 5.21 × 2.389 × 1.975 | 10,000 | 3,211 | 9,036 | 4,958 | 90.4% |
| [b03_two_door_trail_suv](exports/b03_two_door_trail_suv.glb) | Large | 4.447 × 2.199 × 2.027 | 10,000 | 3,147 | 9,018 | 4,978 | 90.2% |
| [b03_two_rider_tandem_bicycle](exports/b03_two_rider_tandem_bicycle.glb) | Medium | 2.77 × 0.57 × 1.12 | 5,000 | 888 | 2,856 | 1,512 | 57.1% |
| [b03_two_seat_microcar](exports/b03_two_seat_microcar.glb) | Large | 2.87 × 1.842 × 1.545 | 10,000 | 3,083 | 8,754 | 4,822 | 87.5% |
| [b03_two_seat_open_roadster](exports/b03_two_seat_open_roadster.glb) | Large | 4.16 × 2.11 × 1.386 | 10,000 | 3,047 | 8,838 | 4,660 | 88.4% |
| [b03_vintage_farm_pickup](exports/b03_vintage_farm_pickup.glb) | Large | 5.1 × 2.266 × 1.883 | 10,000 | 3,323 | 8,970 | 4,974 | 89.7% |
| [b03_wheelchair_accessible_van](exports/b03_wheelchair_accessible_van.glb) | Large | 5.593 × 2.4 × 2.116 | 10,000 | 3,395 | 9,610 | 5,270 | 96.1% |

### Path Lighting (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_conical_path_lamp](exports/b18_conical_path_lamp.glb) | Medium | 0.56 × 0.533 × 1.02 | 5,000 | 155 | 544 | 290 | 10.9% |

### Pedestrian Bridge (3)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_concrete_arch_pedestrian_bridge](exports/b13_concrete_arch_pedestrian_bridge.glb) | Large | 1.95 × 5.05 × 1.787 | 10,000 | 1,152 | 3,456 | 1,896 | 34.6% |
| [b13_steel_through_truss_footbridge](exports/b13_steel_through_truss_footbridge.glb) | Large | 2.13 × 5.58 × 1.59 | 10,000 | 1,232 | 3,696 | 1,932 | 37.0% |
| [b13_timber_creek_pedestrian_bridge](exports/b13_timber_creek_pedestrian_bridge.glb) | Large | 1.8 × 4.13 × 1.525 | 10,000 | 2,400 | 9,600 | 4,448 | 96.0% |

### Pedestrian Infrastructure (9)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_basketweave_brick_sidewalk_panel](exports/b13_basketweave_brick_sidewalk_panel.glb) | Large | 2.25 × 2.25 × 0.15 | 10,000 | 1,320 | 5,280 | 2,420 | 52.8% |
| [b13_curb_extension_bulbout](exports/b13_curb_extension_bulbout.glb) | Large | 4.067 × 2.34 × 0.25 | 10,000 | 208 | 822 | 380 | 8.2% |
| [b13_dual_direction_corner_ramps](exports/b13_dual_direction_corner_ramps.glb) | Large | 2.975 × 3.01 × 0.24 | 10,000 | 1,930 | 6,708 | 3,536 | 67.1% |
| [b13_flared_accessible_curb_ramp](exports/b13_flared_accessible_curb_ramp.glb) | Large | 3.2 × 1.98 × 0.21 | 10,000 | 984 | 3,436 | 1,804 | 34.4% |
| [b13_parallel_depressed_curb_ramp](exports/b13_parallel_depressed_curb_ramp.glb) | Large | 4.65 × 1.535 × 0.32 | 10,000 | 984 | 3,504 | 1,804 | 35.0% |
| [b13_pedestrian_median_refuge_island](exports/b13_pedestrian_median_refuge_island.glb) | Large | 2 × 4.4 × 0.25 | 10,000 | 2,064 | 7,280 | 3,784 | 72.8% |
| [b13_radius_sidewalk_corner](exports/b13_radius_sidewalk_corner.glb) | Large | 2.32 × 2.32 × 0.24 | 10,000 | 398 | 1,526 | 736 | 15.3% |
| [b13_reentrant_sidewalk_corner](exports/b13_reentrant_sidewalk_corner.glb) | Large | 3 × 3 × 0.22 | 10,000 | 178 | 708 | 324 | 7.1% |
| [b13_scored_concrete_sidewalk_bay](exports/b13_scored_concrete_sidewalk_bay.glb) | Large | 2.5 × 3.4 × 0.22 | 10,000 | 122 | 484 | 220 | 4.8% |

### Pedestrian Stair (3)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_city_steps_with_bicycle_gutter](exports/b13_city_steps_with_bicycle_gutter.glb) | Large | 2.6 × 3.056 × 2.486 | 10,000 | 760 | 2,960 | 1,392 | 29.6% |
| [b13_open_steel_transit_access_stair](exports/b13_open_steel_transit_access_stair.glb) | Large | 1.77 × 4.241 × 3.135 | 10,000 | 1,424 | 4,272 | 2,252 | 42.7% |
| [b13_quarter_turn_pedestrian_stair](exports/b13_quarter_turn_pedestrian_stair.glb) | Large | 2.95 × 2.96 × 2.7 | 10,000 | 1,156 | 4,432 | 2,132 | 44.3% |

### Personal Recreation Carry (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b17_badminton_racket](exports/b17_badminton_racket.glb) | Handheld | 0.22 × 0.03 × 0.595 | 999 | 180 | 596 | 308 | 59.7% |
| [b17_baseball_cap](exports/b17_baseball_cap.glb) | Handheld | 0.183 × 0.272 × 0.117 | 999 | 165 | 652 | 310 | 65.3% |
| [b17_baseball_fielders_glove](exports/b17_baseball_fielders_glove.glb) | Handheld | 0.217 × 0.083 × 0.216 | 999 | 186 | 584 | 304 | 58.5% |
| [b17_canvas_shopping_tote](exports/b17_canvas_shopping_tote.glb) | Handheld | 0.34 × 0.126 × 0.554 | 999 | 112 | 360 | 184 | 36.0% |
| [b17_coiled_jump_rope](exports/b17_coiled_jump_rope.glb) | Handheld | 0.386 × 0.493 × 0.026 | 999 | 200 | 720 | 376 | 72.1% |
| [b17_compact_binoculars](exports/b17_compact_binoculars.glb) | Handheld | 0.138 × 0.146 × 0.059 | 999 | 176 | 528 | 312 | 52.9% |
| [b17_compact_digital_camera](exports/b17_compact_digital_camera.glb) | Handheld | 0.116 × 0.077 × 0.081 | 999 | 268 | 968 | 504 | 96.9% |
| [b17_diamond_flying_kite](exports/b17_diamond_flying_kite.glb) | Medium | 0.64 × 0.409 × 1.495 | 5,000 | 181 | 687 | 306 | 13.7% |
| [b17_external_frame_hiking_pack](exports/b17_external_frame_hiking_pack.glb) | Medium | 0.555 × 0.389 × 0.776 | 5,000 | 704 | 2,636 | 1,348 | 52.7% |
| [b17_feather_shuttlecock](exports/b17_feather_shuttlecock.glb) | Handheld | 0.065 × 0.065 × 0.073 | 999 | 202 | 672 | 332 | 67.3% |
| [b17_flying_disc](exports/b17_flying_disc.glb) | Handheld | 0.252 × 0.252 × 0.016 | 999 | 152 | 520 | 292 | 52.1% |
| [b17_folded_picnic_blanket](exports/b17_folded_picnic_blanket.glb) | Handheld | 0.43 × 0.355 × 0.106 | 999 | 152 | 456 | 228 | 45.6% |
| [b17_folded_sunglasses](exports/b17_folded_sunglasses.glb) | Handheld | 0.133 × 0.067 × 0.043 | 999 | 248 | 928 | 460 | 92.9% |
| [b17_folding_baby_stroller](exports/b17_folding_baby_stroller.glb) | Medium | 0.533 × 0.81 × 1.033 | 5,000 | 628 | 2,352 | 1,158 | 47.0% |
| [b17_folding_shopping_trolley](exports/b17_folding_shopping_trolley.glb) | Handheld | 0.344 × 0.322 × 0.938 | 999 | 200 | 648 | 356 | 64.9% |
| [b17_furled_walking_umbrella](exports/b17_furled_walking_umbrella.glb) | Handheld | 0.126 × 0.082 × 0.849 | 999 | 123 | 376 | 210 | 37.6% |
| [b17_handheld_torch_flashlight](exports/b17_handheld_torch_flashlight.glb) | Handheld | 0.07 × 0.067 × 0.21 | 999 | 208 | 624 | 372 | 62.5% |
| [b17_inline_skate](exports/b17_inline_skate.glb) | Handheld | 0.124 × 0.284 × 0.302 | 999 | 295 | 930 | 502 | 93.1% |
| [b17_lace_up_hiking_boot](exports/b17_lace_up_hiking_boot.glb) | Handheld | 0.13 × 0.284 × 0.202 | 999 | 247 | 786 | 414 | 78.7% |
| [b17_laced_american_football](exports/b17_laced_american_football.glb) | Handheld | 0.3 × 0.17 × 0.177 | 999 | 206 | 776 | 376 | 77.7% |
| [b17_messenger_satchel](exports/b17_messenger_satchel.glb) | Handheld | 0.41 × 0.175 × 0.533 | 999 | 136 | 456 | 236 | 45.6% |
| [b17_open_rain_umbrella](exports/b17_open_rain_umbrella.glb) | Medium | 1.06 × 1.008 × 1.043 | 5,000 | 428 | 1,708 | 752 | 34.2% |
| [b17_outdoor_two_way_radio](exports/b17_outdoor_two_way_radio.glb) | Handheld | 0.061 × 0.051 × 0.238 | 999 | 116 | 348 | 184 | 34.8% |
| [b17_padded_dog_walking_harness](exports/b17_padded_dog_walking_harness.glb) | Handheld | 0.178 × 0.166 × 0.191 | 999 | 152 | 568 | 284 | 56.9% |
| [b17_paneled_soccer_ball](exports/b17_paneled_soccer_ball.glb) | Handheld | 0.215 × 0.215 × 0.215 | 999 | 60 | 180 | 116 | 18.0% |
| [b17_portable_folding_camp_chair](exports/b17_portable_folding_camp_chair.glb) | Medium | 0.575 × 0.558 × 0.9 | 5,000 | 440 | 1,728 | 808 | 34.6% |
| [b17_quad_roller_skate](exports/b17_quad_roller_skate.glb) | Handheld | 0.208 × 0.297 × 0.198 | 999 | 275 | 870 | 474 | 87.1% |
| [b17_retractable_dog_leash](exports/b17_retractable_dog_leash.glb) | Handheld | 0.385 × 0.056 × 0.126 | 999 | 116 | 376 | 196 | 37.6% |
| [b17_ribbed_foam_sleeping_mat](exports/b17_ribbed_foam_sleeping_mat.glb) | Medium | 0.552 × 1.71 × 0.112 | 5,000 | 366 | 1,420 | 676 | 28.4% |
| [b17_ribbed_rolling_suitcase](exports/b17_ribbed_rolling_suitcase.glb) | Handheld | 0.383 × 0.249 × 0.995 | 999 | 232 | 696 | 396 | 69.7% |
| [b17_running_shoe](exports/b17_running_shoe.glb) | Handheld | 0.124 × 0.284 × 0.124 | 999 | 191 | 618 | 330 | 61.9% |
| [b17_seamed_basketball](exports/b17_seamed_basketball.glb) | Handheld | 0.243 × 0.243 × 0.243 | 999 | 206 | 696 | 408 | 69.7% |
| [b17_skate_elbow_guard](exports/b17_skate_elbow_guard.glb) | Handheld | 0.155 × 0.179 × 0.076 | 999 | 196 | 804 | 368 | 80.5% |
| [b17_soft_structured_baby_carrier](exports/b17_soft_structured_baby_carrier.glb) | Handheld | 0.47 × 0.305 × 0.498 | 999 | 152 | 504 | 260 | 50.5% |
| [b17_sports_duffel_bag](exports/b17_sports_duffel_bag.glb) | Handheld | 0.534 × 0.28 × 0.414 | 999 | 128 | 384 | 204 | 38.4% |
| [b17_stitched_baseball](exports/b17_stitched_baseball.glb) | Handheld | 0.07 × 0.067 × 0.074 | 999 | 282 | 900 | 440 | 90.1% |
| [b17_strapped_sleeping_bag_roll](exports/b17_strapped_sleeping_bag_roll.glb) | Handheld | 0.448 × 0.298 × 0.298 | 999 | 184 | 648 | 344 | 64.9% |
| [b17_street_skateboard](exports/b17_street_skateboard.glb) | Handheld | 0.252 × 0.8 × 0.091 | 999 | 248 | 744 | 424 | 74.5% |
| [b17_striped_volleyball](exports/b17_striped_volleyball.glb) | Handheld | 0.21 × 0.21 × 0.21 | 999 | 86 | 360 | 164 | 36.0% |
| [b17_table_tennis_paddle](exports/b17_table_tennis_paddle.glb) | Handheld | 0.166 × 0.025 × 0.266 | 999 | 200 | 712 | 380 | 71.3% |
| [b17_tennis_ball](exports/b17_tennis_ball.glb) | Handheld | 0.065 × 0.065 × 0.068 | 999 | 230 | 936 | 384 | 93.7% |
| [b17_tennis_racket](exports/b17_tennis_racket.glb) | Handheld | 0.302 × 0.036 × 0.551 | 999 | 208 | 688 | 348 | 68.9% |
| [b17_trail_sandal](exports/b17_trail_sandal.glb) | Handheld | 0.137 × 0.273 × 0.088 | 999 | 112 | 336 | 176 | 33.6% |
| [b17_tripod_folding_camp_stool](exports/b17_tripod_folding_camp_stool.glb) | Handheld | 0.394 × 0.401 × 0.448 | 999 | 242 | 856 | 452 | 85.7% |
| [b17_vented_bicycle_helmet](exports/b17_vented_bicycle_helmet.glb) | Handheld | 0.229 × 0.299 × 0.292 | 999 | 217 | 864 | 398 | 86.5% |
| [b17_ventilated_pet_carrier](exports/b17_ventilated_pet_carrier.glb) | Medium | 0.34 × 0.581 × 0.49 | 5,000 | 486 | 1,912 | 864 | 38.2% |
| [b17_wide_brim_sun_hat](exports/b17_wide_brim_sun_hat.glb) | Handheld | 0.398 × 0.398 × 0.306 | 999 | 224 | 832 | 420 | 83.3% |
| [b17_wooden_baseball_bat](exports/b17_wooden_baseball_bat.glb) | Handheld | 0.066 × 0.064 × 0.832 | 999 | 180 | 584 | 320 | 58.5% |
| [b17_wooden_boomerang](exports/b17_wooden_boomerang.glb) | Handheld | 0.385 × 0.172 × 0.01 | 999 | 102 | 402 | 188 | 40.2% |
| [b17_zippered_day_backpack](exports/b17_zippered_day_backpack.glb) | Handheld | 0.3 × 0.297 × 0.49 | 999 | 160 | 528 | 272 | 52.9% |

### Picnic Table (5)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b01_accessible_end_picnic_table](exports/b01_accessible_end_picnic_table.glb) | Large | 2.5 × 1.6 × 0.828 | 10,000 | 560 | 2,080 | 1,040 | 20.8% |
| [b01_classic_aframe_picnic_table](exports/b01_classic_aframe_picnic_table.glb) | Large | 1.85 × 1.565 × 0.804 | 10,000 | 432 | 1,728 | 792 | 17.3% |
| [b01_hexagonal_family_picnic_table](exports/b01_hexagonal_family_picnic_table.glb) | Large | 2.373 × 2.127 × 0.823 | 10,000 | 896 | 3,392 | 1,672 | 33.9% |
| [b01_round_pedestal_picnic_table](exports/b01_round_pedestal_picnic_table.glb) | Large | 2.022 × 2.013 × 0.8 | 10,000 | 2,000 | 7,792 | 3,720 | 77.9% |
| [b01_square_four_stool_table](exports/b01_square_four_stool_table.glb) | Large | 2.17 × 2.147 × 0.815 | 10,000 | 976 | 3,824 | 1,816 | 38.2% |

### Planted Landscaping (28)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b08_azalea_mound](exports/b08_azalea_mound.glb) | Medium | 1.541 × 1.314 × 0.76 | 5,000 | 1,200 | 4,978 | 2,004 | 99.6% |
| [b08_bearded_iris](exports/b08_bearded_iris.glb) | Medium | 0.455 × 0.358 × 1.098 | 5,000 | 562 | 2,252 | 980 | 45.0% |
| [b08_black_eyed_susans](exports/b08_black_eyed_susans.glb) | Medium | 0.531 × 0.675 × 0.65 | 5,000 | 930 | 3,680 | 1,380 | 73.6% |
| [b08_boxwood_globe](exports/b08_boxwood_globe.glb) | Medium | 1.162 × 1.17 × 1.064 | 5,000 | 1,203 | 4,770 | 2,310 | 95.4% |
| [b08_cattail_cluster](exports/b08_cattail_cluster.glb) | Medium | 0.583 × 0.814 × 2.06 | 5,000 | 674 | 2,672 | 1,220 | 53.4% |
| [b08_circular_civic_flower_bed](exports/b08_circular_civic_flower_bed.glb) | Large | 2.83 × 2.832 × 0.96 | 10,000 | 1,641 | 6,328 | 2,462 | 63.3% |
| [b08_common_lilac](exports/b08_common_lilac.glb) | Medium | 1.628 × 1.506 × 2.176 | 5,000 | 874 | 3,280 | 1,608 | 65.6% |
| [b08_concrete_mixed_planter](exports/b08_concrete_mixed_planter.glb) | Medium | 0.951 × 0.969 × 1.52 | 5,000 | 643 | 2,578 | 1,006 | 51.6% |
| [b08_creeping_juniper](exports/b08_creeping_juniper.glb) | Medium | 2.073 × 1.738 × 0.424 | 5,000 | 1,035 | 4,122 | 1,962 | 82.4% |
| [b08_daffodil_cluster](exports/b08_daffodil_cluster.glb) | Medium | 0.477 × 0.426 × 0.541 | 5,000 | 636 | 2,376 | 980 | 47.5% |
| [b08_daylily_clump](exports/b08_daylily_clump.glb) | Medium | 0.726 × 0.744 × 0.81 | 5,000 | 970 | 3,990 | 1,692 | 79.8% |
| [b08_flowering_hosta](exports/b08_flowering_hosta.glb) | Medium | 0.802 × 0.893 × 0.903 | 5,000 | 902 | 3,728 | 1,640 | 74.6% |
| [b08_forsythia](exports/b08_forsythia.glb) | Medium | 1.851 × 1.829 × 1.756 | 5,000 | 1,152 | 4,464 | 1,836 | 89.3% |
| [b08_fountain_grass](exports/b08_fountain_grass.glb) | Medium | 1.192 × 1.245 × 1.37 | 5,000 | 1,059 | 4,266 | 1,926 | 85.3% |
| [b08_geranium_window_box](exports/b08_geranium_window_box.glb) | Medium | 1.096 × 0.36 × 0.666 | 5,000 | 1,140 | 4,608 | 1,800 | 92.2% |
| [b08_hanging_petunia_basket](exports/b08_hanging_petunia_basket.glb) | Medium | 0.699 × 0.692 × 0.949 | 5,000 | 905 | 3,646 | 1,534 | 72.9% |
| [b08_hydrangea](exports/b08_hydrangea.glb) | Medium | 1.181 × 1.016 × 1.253 | 5,000 | 917 | 3,780 | 1,610 | 75.6% |
| [b08_lavender_patch](exports/b08_lavender_patch.glb) | Medium | 0.456 × 0.614 × 0.756 | 5,000 | 1,144 | 4,602 | 1,924 | 92.0% |
| [b08_maiden_grass](exports/b08_maiden_grass.glb) | Medium | 0.995 × 1.433 × 2.15 | 5,000 | 628 | 2,526 | 1,052 | 50.5% |
| [b08_pampas_grass](exports/b08_pampas_grass.glb) | Medium | 1.132 × 1.633 × 2.552 | 5,000 | 806 | 3,300 | 1,452 | 66.0% |
| [b08_purple_coneflowers](exports/b08_purple_coneflowers.glb) | Medium | 0.648 × 0.592 × 0.951 | 5,000 | 1,063 | 4,236 | 1,790 | 84.7% |
| [b08_raised_perennial_bed](exports/b08_raised_perennial_bed.glb) | Large | 2.69 × 1.09 × 1.27 | 10,000 | 1,725 | 6,880 | 2,862 | 68.8% |
| [b08_redtwig_dogwood_winter](exports/b08_redtwig_dogwood_winter.glb) | Medium | 0.881 × 1.183 × 1.617 | 5,000 | 946 | 4,004 | 1,760 | 80.1% |
| [b08_rhododendron](exports/b08_rhododendron.glb) | Medium | 1.349 × 1.361 × 1.159 | 5,000 | 1,045 | 4,200 | 1,590 | 84.0% |
| [b08_salvia_border](exports/b08_salvia_border.glb) | Medium | 0.74 × 0.481 × 0.745 | 5,000 | 1,098 | 4,482 | 1,908 | 89.6% |
| [b08_switchgrass](exports/b08_switchgrass.glb) | Medium | 0.724 × 0.72 × 1.776 | 5,000 | 1,046 | 3,848 | 1,736 | 77.0% |
| [b08_tulip_cluster](exports/b08_tulip_cluster.glb) | Medium | 0.551 × 0.43 × 0.617 | 5,000 | 1,150 | 4,568 | 2,020 | 91.4% |
| [b08_whiskey_barrel_flowers](exports/b08_whiskey_barrel_flowers.glb) | Medium | 0.808 × 0.788 × 1 | 5,000 | 1,026 | 3,908 | 1,600 | 78.2% |

### Playground Fitness Sports (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b09_accessible_sand_table](exports/b09_accessible_sand_table.glb) | Medium | 1.61 × 1.07 × 0.92 | 5,000 | 944 | 3,728 | 1,744 | 74.6% |
| [b09_air_walker](exports/b09_air_walker.glb) | Medium | 0.97 × 1.48 × 1.609 | 5,000 | 1,116 | 4,280 | 2,088 | 85.6% |
| [b09_baseball_backstop](exports/b09_baseball_backstop.glb) | Large | 8.62 × 1.72 × 4.013 | 10,000 | 1,972 | 7,848 | 3,452 | 78.5% |
| [b09_baseball_scoreboard](exports/b09_baseball_scoreboard.glb) | Large | 3.34 × 0.42 × 3.013 | 10,000 | 932 | 2,848 | 1,460 | 28.5% |
| [b09_basketball_gooseneck_pole](exports/b09_basketball_gooseneck_pole.glb) | Large | 1.834 × 2.03 × 3.887 | 10,000 | 868 | 3,424 | 1,608 | 34.2% |
| [b09_climbing_wall](exports/b09_climbing_wall.glb) | Large | 1.96 × 0.3 × 2.381 | 10,000 | 1,484 | 6,112 | 2,788 | 61.1% |
| [b09_crawl_tunnel](exports/b09_crawl_tunnel.glb) | Large | 2.113 × 1.2 × 1.24 | 10,000 | 960 | 3,888 | 1,816 | 38.9% |
| [b09_curved_slide](exports/b09_curved_slide.glb) | Large | 2.597 × 2.61 × 2.438 | 10,000 | 720 | 2,792 | 1,324 | 27.9% |
| [b09_disc_golf_basket](exports/b09_disc_golf_basket.glb) | Medium | 0.724 × 0.724 × 1.735 | 5,000 | 734 | 2,384 | 1,200 | 47.7% |
| [b09_dome_climber](exports/b09_dome_climber.glb) | Large | 3.22 × 3.22 × 1.742 | 10,000 | 1,360 | 4,512 | 2,272 | 45.1% |
| [b09_double_swing](exports/b09_double_swing.glb) | Large | 3.64 × 2.02 × 2.518 | 10,000 | 1,640 | 6,520 | 3,180 | 65.2% |
| [b09_dugout_equipment_bench](exports/b09_dugout_equipment_bench.glb) | Large | 3.9 × 1.01 × 1.43 | 10,000 | 1,560 | 6,192 | 2,896 | 61.9% |
| [b09_four_row_bleachers](exports/b09_four_row_bleachers.glb) | Large | 4.248 × 2.91 × 2.434 | 10,000 | 1,332 | 5,328 | 2,476 | 53.3% |
| [b09_four_seat_spring_rocker](exports/b09_four_seat_spring_rocker.glb) | Medium | 1.84 × 1.84 × 1.002 | 5,000 | 800 | 2,400 | 1,292 | 48.0% |
| [b09_horseshoe_pitching_pit](exports/b09_horseshoe_pitching_pit.glb) | Large | 2 × 2.4 × 0.675 | 10,000 | 552 | 2,136 | 1,040 | 21.4% |
| [b09_incline_situp_bench](exports/b09_incline_situp_bench.glb) | Medium | 1.972 × 0.88 × 1.145 | 5,000 | 772 | 3,024 | 1,432 | 60.5% |
| [b09_kinked_grind_rail](exports/b09_kinked_grind_rail.glb) | Large | 3.82 × 0.22 × 0.89 | 10,000 | 648 | 2,592 | 1,204 | 25.9% |
| [b09_lacrosse_goal](exports/b09_lacrosse_goal.glb) | Large | 1.92 × 1.89 × 1.872 | 10,000 | 702 | 2,728 | 1,188 | 27.3% |
| [b09_merry_go_round](exports/b09_merry_go_round.glb) | Large | 2.26 × 2.26 × 0.974 | 10,000 | 1,040 | 4,000 | 1,968 | 40.0% |
| [b09_monkey_bars](exports/b09_monkey_bars.glb) | Large | 3.52 × 1.22 × 2.144 | 10,000 | 1,308 | 5,200 | 2,452 | 52.0% |
| [b09_outdoor_elliptical](exports/b09_outdoor_elliptical.glb) | Medium | 1.505 × 0.96 × 1.703 | 5,000 | 600 | 1,816 | 1,020 | 36.3% |
| [b09_outdoor_rowing_station](exports/b09_outdoor_rowing_station.glb) | Medium | 1.65 × 0.83 × 0.953 | 5,000 | 1,084 | 4,108 | 2,028 | 82.2% |
| [b09_outdoor_table_tennis](exports/b09_outdoor_table_tennis.glb) | Large | 2.751 × 1.653 × 0.951 | 10,000 | 566 | 2,264 | 988 | 22.6% |
| [b09_overhead_ring_traverse](exports/b09_overhead_ring_traverse.glb) | Large | 3.62 × 1.22 × 2.417 | 10,000 | 1,840 | 7,412 | 3,536 | 74.1% |
| [b09_parallel_dip_station](exports/b09_parallel_dip_station.glb) | Medium | 1.78 × 0.84 × 1.245 | 5,000 | 768 | 3,040 | 1,432 | 60.8% |
| [b09_playground_abacus_panel](exports/b09_playground_abacus_panel.glb) | Medium | 1.74 × 0.22 × 1.696 | 5,000 | 1,152 | 4,256 | 2,160 | 85.1% |
| [b09_roofed_play_tower](exports/b09_roofed_play_tower.glb) | Large | 2.245 × 1.815 × 2.981 | 10,000 | 1,578 | 6,312 | 2,916 | 63.1% |
| [b09_rope_pyramid](exports/b09_rope_pyramid.glb) | Large | 2.86 × 2.86 × 2.89 | 10,000 | 1,427 | 5,696 | 2,654 | 57.0% |
| [b09_seated_chest_press](exports/b09_seated_chest_press.glb) | Medium | 1.371 × 1.106 × 1.615 | 5,000 | 1,122 | 4,220 | 2,108 | 84.4% |
| [b09_seated_leg_press](exports/b09_seated_leg_press.glb) | Medium | 1.607 × 0.92 × 1.337 | 5,000 | 896 | 3,360 | 1,676 | 67.2% |
| [b09_seesaw](exports/b09_seesaw.glb) | Large | 3.25 × 0.776 × 1.043 | 10,000 | 1,080 | 4,212 | 2,020 | 42.1% |
| [b09_shoulder_rotation_wheels](exports/b09_shoulder_rotation_wheels.glb) | Medium | 1.74 × 0.35 × 1.645 | 5,000 | 1,166 | 4,520 | 2,220 | 90.4% |
| [b09_skate_bowl_corner](exports/b09_skate_bowl_corner.glb) | Large | 2.071 × 2.071 × 1.526 | 10,000 | 396 | 1,562 | 756 | 15.6% |
| [b09_skate_funbox](exports/b09_skate_funbox.glb) | Large | 5.2 × 2.2 × 1.054 | 10,000 | 272 | 1,132 | 500 | 11.3% |
| [b09_skate_manual_pad](exports/b09_skate_manual_pad.glb) | Large | 2.98 × 1.36 × 0.425 | 10,000 | 288 | 1,152 | 528 | 11.5% |
| [b09_skate_quarter_pipe](exports/b09_skate_quarter_pipe.glb) | Large | 2.515 × 2.41 × 2.584 | 10,000 | 682 | 2,774 | 1,280 | 27.7% |
| [b09_soccer_goal](exports/b09_soccer_goal.glb) | Large | 7.44 × 1.965 × 2.5 | 10,000 | 1,050 | 4,040 | 1,768 | 40.4% |
| [b09_stepping_log_course](exports/b09_stepping_log_course.glb) | Large | 2.98 × 0.805 × 0.557 | 10,000 | 720 | 2,640 | 1,392 | 26.4% |
| [b09_straight_slide](exports/b09_straight_slide.glb) | Large | 4.106 × 1.02 × 2.274 | 10,000 | 1,704 | 6,704 | 3,200 | 67.0% |
| [b09_tennis_net](exports/b09_tennis_net.glb) | Large | 13.02 × 0.22 × 1.153 | 10,000 | 1,092 | 4,352 | 1,876 | 43.5% |
| [b09_tennis_umpire_chair](exports/b09_tennis_umpire_chair.glb) | Large | 1.459 × 0.985 × 2.156 | 10,000 | 1,020 | 4,080 | 1,916 | 40.8% |
| [b09_tetherball_pole](exports/b09_tetherball_pole.glb) | Large | 1.059 × 0.48 × 3.102 | 10,000 | 404 | 1,564 | 772 | 15.6% |
| [b09_three_height_pullup_station](exports/b09_three_height_pullup_station.glb) | Large | 3.82 × 0.22 × 2.494 | 10,000 | 996 | 3,952 | 1,872 | 39.5% |
| [b09_tire_swing](exports/b09_tire_swing.glb) | Large | 3.14 × 2.42 × 2.668 | 10,000 | 1,584 | 6,336 | 3,028 | 63.4% |
| [b09_toddler_bucket_swing](exports/b09_toddler_bucket_swing.glb) | Large | 2.44 × 1.82 × 2.268 | 10,000 | 1,096 | 4,400 | 2,084 | 44.0% |
| [b09_triple_twist_disc_station](exports/b09_triple_twist_disc_station.glb) | Medium | 1.705 × 1.879 × 1.289 | 5,000 | 858 | 3,280 | 1,624 | 65.6% |
| [b09_volleyball_net](exports/b09_volleyball_net.glb) | Large | 11.689 × 1.06 × 3.12 | 10,000 | 1,310 | 5,224 | 2,304 | 52.2% |
| [b09_wall_mount_basketball_goal](exports/b09_wall_mount_basketball_goal.glb) | Large | 1.834 × 1.75 × 1.26 | 10,000 | 1,000 | 4,000 | 1,860 | 40.0% |
| [b09_wave_slide](exports/b09_wave_slide.glb) | Large | 4.546 × 1.02 × 2.684 | 10,000 | 1,944 | 7,640 | 3,664 | 76.4% |
| [b09_zigzag_balance_beam](exports/b09_zigzag_balance_beam.glb) | Large | 3.62 × 0.9 × 0.51 | 10,000 | 456 | 1,824 | 836 | 18.2% |

### Plaza Lighting (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_four_lantern_plaza_standard](exports/b18_four_lantern_plaza_standard.glb) | Large | 1.7 × 1.7 × 4.165 | 10,000 | 1,338 | 4,160 | 2,160 | 41.6% |

### Promenade Lighting (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_rectangular_frame_promenade_light](exports/b18_rectangular_frame_promenade_light.glb) | Large | 1.17 × 0.5 × 4.26 | 10,000 | 336 | 1,304 | 628 | 13.0% |

### Public Art (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_interlocking_steel_ribbon_sculpture](exports/b18_interlocking_steel_ribbon_sculpture.glb) | Large | 1.877 × 1.38 × 2.852 | 10,000 | 336 | 1,344 | 616 | 13.4% |

### Public Seating (7)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b01_concrete_cube_seating_cluster](exports/b01_concrete_cube_seating_cluster.glb) | Medium | 1.6 × 0.795 × 0.57 | 5,000 | 432 | 1,728 | 792 | 34.6% |
| [b01_planter_integrated_sidewalk_seat](exports/b01_planter_integrated_sidewalk_seat.glb) | Large | 2.739 × 0.72 × 1.13 | 10,000 | 728 | 2,576 | 1,180 | 25.8% |
| [b01_sculpted_concrete_recliner](exports/b01_sculpted_concrete_recliner.glb) | Medium | 0.69 × 1.33 × 1 | 5,000 | 250 | 890 | 472 | 17.8% |
| [b01_stone_semicircular_seat](exports/b01_stone_semicircular_seat.glb) | Large | 3.5 × 1.84 × 1 | 10,000 | 1,134 | 4,320 | 2,100 | 43.2% |
| [b01_three_tier_bleachers](exports/b01_three_tier_bleachers.glb) | Large | 3.25 × 1.733 × 1.882 | 10,000 | 952 | 3,392 | 1,780 | 33.9% |
| [b01_timber_chaise_public_seat](exports/b01_timber_chaise_public_seat.glb) | Medium | 0.72 × 1.379 × 1.014 | 5,000 | 1,072 | 3,968 | 1,992 | 79.4% |
| [b01_transit_leaning_rail](exports/b01_transit_leaning_rail.glb) | Medium | 2 × 0.382 × 0.966 | 5,000 | 672 | 2,592 | 1,288 | 51.8% |

### Rail Track (6)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_ballasted_commuter_rail_track](exports/b13_ballasted_commuter_rail_track.glb) | Large | 3.3 × 4 × 0.464 | 10,000 | 940 | 3,072 | 1,452 | 30.7% |
| [b13_curved_streetcar_track_segment](exports/b13_curved_streetcar_track_segment.glb) | Large | 3.062 × 4.934 × 0.17 | 10,000 | 2,016 | 8,064 | 3,696 | 80.6% |
| [b13_embedded_grooved_streetcar_track](exports/b13_embedded_grooved_streetcar_track.glb) | Large | 2.7 × 3.6 × 0.167 | 10,000 | 216 | 864 | 392 | 8.6% |
| [b13_rubber_panel_rail_crossing](exports/b13_rubber_panel_rail_crossing.glb) | Large | 3.6 × 3.2 × 0.304 | 10,000 | 1,120 | 4,448 | 2,012 | 44.5% |
| [b13_timber_grade_rail_crossing](exports/b13_timber_grade_rail_crossing.glb) | Large | 2.497 × 3.4 × 0.334 | 10,000 | 1,984 | 7,904 | 3,656 | 79.0% |
| [b13_urban_rail_turnout_frog](exports/b13_urban_rail_turnout_frog.glb) | Large | 3.7 × 4.625 × 0.502 | 10,000 | 1,280 | 4,992 | 2,428 | 49.9% |

### Residential Yard Garden (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b11_a_frame_cucumber_trellis](exports/b11_a_frame_cucumber_trellis.glb) | Medium | 1.08 × 1.134 × 1.357 | 5,000 | 656 | 2,632 | 1,204 | 52.6% |
| [b11_adirondack_garden_chair](exports/b11_adirondack_garden_chair.glb) | Medium | 0.72 × 0.916 × 1.079 | 5,000 | 576 | 2,304 | 1,056 | 46.1% |
| [b11_adjustable_patio_chaise](exports/b11_adjustable_patio_chaise.glb) | Medium | 0.659 × 1.596 × 0.908 | 5,000 | 781 | 3,032 | 1,454 | 60.6% |
| [b11_backyard_pizza_oven_cart](exports/b11_backyard_pizza_oven_cart.glb) | Medium | 0.93 × 0.78 × 1.758 | 5,000 | 952 | 3,632 | 1,792 | 72.6% |
| [b11_backyard_porch_swing_frame](exports/b11_backyard_porch_swing_frame.glb) | Large | 2.42 × 1.58 × 2.115 | 10,000 | 744 | 3,024 | 1,364 | 30.2% |
| [b11_barrel_rainwater_collector](exports/b11_barrel_rainwater_collector.glb) | Medium | 0.701 × 0.734 × 1.046 | 5,000 | 608 | 2,216 | 1,164 | 44.3% |
| [b11_brick_backyard_barbecue](exports/b11_brick_backyard_barbecue.glb) | Large | 1.6 × 0.9 × 1.27 | 10,000 | 900 | 3,600 | 1,656 | 36.0% |
| [b11_cast_iron_hibachi](exports/b11_cast_iron_hibachi.glb) | Handheld | 0.846 × 0.458 × 0.301 | 999 | 252 | 756 | 408 | 75.7% |
| [b11_cedar_backyard_dog_house](exports/b11_cedar_backyard_dog_house.glb) | Medium | 1.159 × 1.28 × 1.274 | 5,000 | 490 | 1,960 | 860 | 39.2% |
| [b11_cedar_compost_bin](exports/b11_cedar_compost_bin.glb) | Medium | 1.13 × 0.985 × 1.215 | 5,000 | 944 | 3,760 | 1,732 | 75.2% |
| [b11_ceramic_kamado_grill](exports/b11_ceramic_kamado_grill.glb) | Medium | 1.21 × 0.748 × 1.317 | 5,000 | 1,272 | 4,752 | 2,420 | 95.0% |
| [b11_corrugated_steel_raised_bed](exports/b11_corrugated_steel_raised_bed.glb) | Medium | 1.523 × 0.923 × 0.495 | 5,000 | 1,216 | 4,544 | 2,368 | 90.9% |
| [b11_covered_firewood_rack](exports/b11_covered_firewood_rack.glb) | Medium | 1.47 × 0.69 × 1.456 | 5,000 | 820 | 3,104 | 1,520 | 62.1% |
| [b11_dual_chamber_compost_tumbler](exports/b11_dual_chamber_compost_tumbler.glb) | Medium | 1.37 × 0.788 × 1.261 | 5,000 | 864 | 3,336 | 1,596 | 66.7% |
| [b11_elevated_cedar_garden_planter](exports/b11_elevated_cedar_garden_planter.glb) | Medium | 1.285 × 0.705 × 1.065 | 5,000 | 792 | 3,216 | 1,452 | 64.3% |
| [b11_fan_climbing_trellis](exports/b11_fan_climbing_trellis.glb) | Medium | 1.258 × 0.082 × 1.75 | 5,000 | 372 | 1,488 | 688 | 29.8% |
| [b11_freestanding_hammock_and_stand](exports/b11_freestanding_hammock_and_stand.glb) | Large | 3.411 × 1.24 × 1.242 | 10,000 | 1,208 | 4,456 | 2,060 | 44.6% |
| [b11_garden_obelisk_support](exports/b11_garden_obelisk_support.glb) | Medium | 0.644 × 0.644 × 2.011 | 5,000 | 531 | 2,128 | 974 | 42.6% |
| [b11_garden_potting_bench_with_sink](exports/b11_garden_potting_bench_with_sink.glb) | Medium | 1.345 × 0.685 × 1.535 | 5,000 | 924 | 3,632 | 1,704 | 72.6% |
| [b11_glazed_garden_cold_frame](exports/b11_glazed_garden_cold_frame.glb) | Medium | 1.33 × 1.012 × 0.63 | 5,000 | 376 | 1,488 | 692 | 29.8% |
| [b11_half_whiskey_barrel_planter](exports/b11_half_whiskey_barrel_planter.glb) | Medium | 0.685 × 0.668 × 0.477 | 5,000 | 560 | 2,072 | 1,056 | 41.4% |
| [b11_hanging_tube_seed_feeder](exports/b11_hanging_tube_seed_feeder.glb) | Handheld | 0.32 × 0.3 × 0.801 | 999 | 284 | 908 | 508 | 90.9% |
| [b11_hanging_wire_basket_empty](exports/b11_hanging_wire_basket_empty.glb) | Handheld | 0.584 × 0.584 × 0.925 | 999 | 264 | 948 | 484 | 94.9% |
| [b11_hose_saddle_with_coiled_hose](exports/b11_hose_saddle_with_coiled_hose.glb) | Medium | 0.603 × 0.345 × 0.746 | 5,000 | 1,112 | 4,432 | 2,096 | 88.6% |
| [b11_kettle_charcoal_grill](exports/b11_kettle_charcoal_grill.glb) | Medium | 0.652 × 0.691 × 1.09 | 5,000 | 920 | 3,368 | 1,756 | 67.4% |
| [b11_offset_barrel_smoker](exports/b11_offset_barrel_smoker.glb) | Medium | 1.34 × 0.643 × 1.663 | 5,000 | 856 | 3,200 | 1,612 | 64.0% |
| [b11_outdoor_deck_storage_box](exports/b11_outdoor_deck_storage_box.glb) | Medium | 1.29 × 0.669 × 0.709 | 5,000 | 553 | 2,192 | 1,018 | 43.8% |
| [b11_patio_cushioned_ottoman](exports/b11_patio_cushioned_ottoman.glb) | Medium | 0.664 × 0.574 × 0.516 | 5,000 | 713 | 2,848 | 1,290 | 57.0% |
| [b11_pedestal_bird_bath](exports/b11_pedestal_bird_bath.glb) | Medium | 0.799 × 0.799 × 0.87 | 5,000 | 428 | 1,560 | 844 | 31.2% |
| [b11_pellet_grill_with_hopper](exports/b11_pellet_grill_with_hopper.glb) | Medium | 1.16 × 0.741 × 1.54 | 5,000 | 865 | 3,304 | 1,614 | 66.1% |
| [b11_pole_mounted_bat_house](exports/b11_pole_mounted_bat_house.glb) | Medium | 0.49 × 0.346 × 2.448 | 5,000 | 424 | 1,696 | 780 | 33.9% |
| [b11_post_mounted_songbird_house](exports/b11_post_mounted_songbird_house.glb) | Medium | 0.437 × 0.505 × 2.054 | 5,000 | 314 | 1,168 | 588 | 23.4% |
| [b11_raised_backyard_rabbit_hutch](exports/b11_raised_backyard_rabbit_hutch.glb) | Medium | 1.41 × 0.846 × 1.394 | 5,000 | 648 | 2,592 | 1,160 | 51.8% |
| [b11_rectangular_cedar_patio_table](exports/b11_rectangular_cedar_patio_table.glb) | Medium | 1.55 × 0.85 × 0.787 | 5,000 | 528 | 2,096 | 976 | 41.9% |
| [b11_roofed_platform_bird_feeder](exports/b11_roofed_platform_bird_feeder.glb) | Medium | 0.687 × 0.6 × 2.204 | 5,000 | 384 | 1,536 | 704 | 30.7% |
| [b11_rotary_backyard_clothesline](exports/b11_rotary_backyard_clothesline.glb) | Large | 1.93 × 1.93 × 2.15 | 10,000 | 856 | 3,544 | 1,580 | 35.4% |
| [b11_round_patio_dining_table](exports/b11_round_patio_dining_table.glb) | Medium | 1.16 × 1.16 × 0.795 | 5,000 | 552 | 1,972 | 1,076 | 39.4% |
| [b11_slim_wall_rainwater_tank](exports/b11_slim_wall_rainwater_tank.glb) | Medium | 0.8 × 0.572 × 1.677 | 5,000 | 449 | 1,724 | 834 | 34.5% |
| [b11_square_propane_fire_table](exports/b11_square_propane_fire_table.glb) | Medium | 1.15 × 1.15 × 0.61 | 5,000 | 840 | 3,476 | 1,580 | 69.5% |
| [b11_steel_fire_bowl](exports/b11_steel_fire_bowl.glb) | Medium | 1.016 × 1.016 × 0.481 | 5,000 | 464 | 1,760 | 896 | 35.2% |
| [b11_tapered_square_patio_planter](exports/b11_tapered_square_patio_planter.glb) | Medium | 0.632 × 0.632 × 0.759 | 5,000 | 240 | 960 | 444 | 19.2% |
| [b11_terracotta_chiminea](exports/b11_terracotta_chiminea.glb) | Medium | 0.72 × 0.748 × 1.192 | 5,000 | 384 | 1,440 | 736 | 28.8% |
| [b11_three_burner_gas_grill_cart](exports/b11_three_burner_gas_grill_cart.glb) | Medium | 1.51 × 0.645 × 1.135 | 5,000 | 1,176 | 4,394 | 2,220 | 87.9% |
| [b11_tiered_empty_planter_stand](exports/b11_tiered_empty_planter_stand.glb) | Medium | 0.83 × 0.821 × 1.099 | 5,000 | 480 | 1,920 | 880 | 38.4% |
| [b11_vertical_cabinet_smoker](exports/b11_vertical_cabinet_smoker.glb) | Medium | 0.537 × 0.561 × 1.255 | 5,000 | 768 | 2,984 | 1,424 | 59.7% |
| [b11_wall_mounted_hose_reel](exports/b11_wall_mounted_hose_reel.glb) | Medium | 0.568 × 0.588 × 0.55 | 5,000 | 896 | 3,232 | 1,740 | 64.6% |
| [b11_wheeled_garden_hose_reel](exports/b11_wheeled_garden_hose_reel.glb) | Medium | 0.72 × 0.781 × 1.034 | 5,000 | 748 | 2,676 | 1,416 | 53.5% |
| [b11_window_flower_box_empty](exports/b11_window_flower_box_empty.glb) | Medium | 1.23 × 0.393 × 0.432 | 5,000 | 432 | 1,728 | 796 | 34.6% |
| [b11_wire_tomato_cage](exports/b11_wire_tomato_cage.glb) | Medium | 0.614 × 0.614 × 1.281 | 5,000 | 384 | 1,440 | 752 | 28.8% |
| [b11_woven_patio_armchair](exports/b11_woven_patio_armchair.glb) | Medium | 0.618 × 0.617 × 0.971 | 5,000 | 882 | 3,512 | 1,616 | 70.2% |

### Retail Food Service (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b10_automated_ice_bag_vending_kiosk](exports/b10_automated_ice_bag_vending_kiosk.glb) | Large | 2.31 × 1.42 × 2.27 | 10,000 | 712 | 2,768 | 1,308 | 27.7% |
| [b10_bakery_sidewalk_glass_case](exports/b10_bakery_sidewalk_glass_case.glb) | Medium | 1.24 × 0.707 × 1.573 | 5,000 | 1,078 | 4,272 | 2,020 | 85.4% |
| [b10_bottled_drink_vending_machine](exports/b10_bottled_drink_vending_machine.glb) | Medium | 1.1 × 0.977 × 1.796 | 5,000 | 1,000 | 3,760 | 1,856 | 75.2% |
| [b10_bulk_nut_dispenser_stand](exports/b10_bulk_nut_dispenser_stand.glb) | Medium | 1.1 × 0.57 × 1.665 | 5,000 | 835 | 3,200 | 1,534 | 64.0% |
| [b10_cafe_bar_stool_with_back](exports/b10_cafe_bar_stool_with_back.glb) | Medium | 0.51 × 0.51 × 1.186 | 5,000 | 384 | 1,416 | 736 | 28.3% |
| [b10_chalkboard_sandwich_a_frame](exports/b10_chalkboard_sandwich_a_frame.glb) | Medium | 0.62 × 0.67 × 1.072 | 5,000 | 376 | 1,488 | 688 | 29.8% |
| [b10_commercial_barbecue_smoker_trailer_cart](exports/b10_commercial_barbecue_smoker_trailer_cart.glb) | Large | 1.865 × 1.195 × 1.935 | 10,000 | 1,328 | 4,892 | 2,520 | 48.9% |
| [b10_commercial_flat_top_griddle_cart](exports/b10_commercial_flat_top_griddle_cart.glb) | Medium | 1.53 × 0.69 × 1.355 | 5,000 | 1,072 | 3,856 | 2,012 | 77.1% |
| [b10_commercial_rotisserie_display_cabinet](exports/b10_commercial_rotisserie_display_cabinet.glb) | Medium | 1.39 × 1.509 × 1.772 | 5,000 | 694 | 2,428 | 1,212 | 48.6% |
| [b10_digital_restaurant_menu_totem](exports/b10_digital_restaurant_menu_totem.glb) | Medium | 0.66 × 0.47 × 2.03 | 5,000 | 456 | 1,808 | 824 | 36.2% |
| [b10_donut_shop_display_counter](exports/b10_donut_shop_display_counter.glb) | Medium | 1.25 × 0.67 × 1.525 | 5,000 | 632 | 2,296 | 1,188 | 45.9% |
| [b10_farmers_market_canvas_stall](exports/b10_farmers_market_canvas_stall.glb) | Large | 2.35 × 1.493 × 2.42 | 10,000 | 2,344 | 8,880 | 4,236 | 88.8% |
| [b10_farmers_market_scale_table](exports/b10_farmers_market_scale_table.glb) | Medium | 1.065 × 0.649 × 1.337 | 5,000 | 1,208 | 4,616 | 2,236 | 92.3% |
| [b10_filtered_water_refill_station](exports/b10_filtered_water_refill_station.glb) | Medium | 0.93 × 0.985 × 1.816 | 5,000 | 616 | 2,368 | 1,140 | 47.4% |
| [b10_florist_bucket_sidewalk_display](exports/b10_florist_bucket_sidewalk_display.glb) | Medium | 1.03 × 0.77 × 1.29 | 5,000 | 992 | 3,420 | 1,696 | 68.4% |
| [b10_free_weekly_news_dispenser](exports/b10_free_weekly_news_dispenser.glb) | Medium | 0.58 × 0.503 × 1.158 | 5,000 | 264 | 1,008 | 484 | 20.2% |
| [b10_freestanding_barber_pole_sign](exports/b10_freestanding_barber_pole_sign.glb) | Medium | 0.5 × 0.5 × 1.84 | 5,000 | 480 | 1,148 | 600 | 23.0% |
| [b10_giant_ice_cream_cone_shop_sign](exports/b10_giant_ice_cream_cone_shop_sign.glb) | Medium | 0.723 × 0.723 × 1.8 | 5,000 | 391 | 1,644 | 722 | 32.9% |
| [b10_greeting_card_spinner_rack](exports/b10_greeting_card_spinner_rack.glb) | Medium | 0.56 × 0.56 × 1.755 | 5,000 | 880 | 3,464 | 1,620 | 69.3% |
| [b10_hot_dog_pushcart](exports/b10_hot_dog_pushcart.glb) | Large | 2.31 × 1.752 × 2.267 | 10,000 | 993 | 3,696 | 1,866 | 37.0% |
| [b10_insulated_ice_cream_pushcart](exports/b10_insulated_ice_cream_pushcart.glb) | Medium | 1.604 × 0.91 × 1.079 | 5,000 | 848 | 3,184 | 1,592 | 63.7% |
| [b10_lemonade_stand_with_canopy](exports/b10_lemonade_stand_with_canopy.glb) | Medium | 1.43 × 0.884 × 2.023 | 5,000 | 928 | 3,344 | 1,628 | 66.9% |
| [b10_outdoor_bagged_ice_chest](exports/b10_outdoor_bagged_ice_chest.glb) | Medium | 1.75 × 0.917 × 1.312 | 5,000 | 784 | 3,088 | 1,456 | 61.8% |
| [b10_outdoor_bookshop_cart](exports/b10_outdoor_bookshop_cart.glb) | Medium | 0.94 × 0.55 × 1.607 | 5,000 | 1,232 | 4,784 | 2,272 | 95.7% |
| [b10_outdoor_cafeteria_tray_return_station](exports/b10_outdoor_cafeteria_tray_return_station.glb) | Medium | 1.13 × 0.846 × 1.52 | 5,000 | 688 | 2,704 | 1,284 | 54.1% |
| [b10_paid_newspaper_honor_box](exports/b10_paid_newspaper_honor_box.glb) | Medium | 0.61 × 0.548 × 1.249 | 5,000 | 420 | 1,632 | 780 | 32.6% |
| [b10_popcorn_concession_pushcart](exports/b10_popcorn_concession_pushcart.glb) | Medium | 1.1 × 0.87 × 1.575 | 5,000 | 1,096 | 4,024 | 2,064 | 80.5% |
| [b10_portable_commercial_handwash_sink](exports/b10_portable_commercial_handwash_sink.glb) | Medium | 0.79 × 0.805 × 1.405 | 5,000 | 1,036 | 3,888 | 1,936 | 77.8% |
| [b10_pretzel_warmer_cart](exports/b10_pretzel_warmer_cart.glb) | Medium | 0.91 × 0.665 × 1.489 | 5,000 | 1,244 | 4,784 | 2,376 | 95.7% |
| [b10_restaurant_busser_service_cart](exports/b10_restaurant_busser_service_cart.glb) | Medium | 0.897 × 0.54 × 1.084 | 5,000 | 1,224 | 4,512 | 2,292 | 90.2% |
| [b10_restaurant_hostess_station](exports/b10_restaurant_hostess_station.glb) | Medium | 0.88 × 0.67 × 1.191 | 5,000 | 354 | 1,356 | 656 | 27.1% |
| [b10_restaurant_menu_display_podium](exports/b10_restaurant_menu_display_podium.glb) | Medium | 0.58 × 0.47 × 1.314 | 5,000 | 192 | 752 | 356 | 15.0% |
| [b10_rolling_sidewalk_garment_rack](exports/b10_rolling_sidewalk_garment_rack.glb) | Medium | 1.164 × 0.64 × 1.668 | 5,000 | 682 | 2,146 | 1,152 | 42.9% |
| [b10_rotating_sunglasses_display](exports/b10_rotating_sunglasses_display.glb) | Medium | 0.52 × 0.52 × 1.75 | 5,000 | 1,152 | 4,568 | 2,072 | 91.4% |
| [b10_round_bistro_pedestal_table](exports/b10_round_bistro_pedestal_table.glb) | Medium | 0.8 × 0.8 × 0.76 | 5,000 | 288 | 1,104 | 536 | 22.1% |
| [b10_seafood_crushed_ice_display_table](exports/b10_seafood_crushed_ice_display_table.glb) | Medium | 1.5 × 0.82 × 1.225 | 5,000 | 866 | 3,308 | 1,620 | 66.2% |
| [b10_shaved_ice_vendor_cart](exports/b10_shaved_ice_vendor_cart.glb) | Medium | 1.317 × 0.724 × 1.385 | 5,000 | 1,136 | 4,184 | 2,148 | 83.7% |
| [b10_sidewalk_clearance_wire_bin](exports/b10_sidewalk_clearance_wire_bin.glb) | Medium | 0.872 × 0.722 × 0.972 | 5,000 | 638 | 1,994 | 1,084 | 39.9% |
| [b10_sidewalk_coffee_kiosk](exports/b10_sidewalk_coffee_kiosk.glb) | Large | 2.18 × 1.805 × 2.355 | 10,000 | 1,008 | 3,880 | 1,856 | 38.8% |
| [b10_sidewalk_condiment_service_station](exports/b10_sidewalk_condiment_service_station.glb) | Medium | 1.06 × 0.714 × 1.23 | 5,000 | 804 | 3,040 | 1,520 | 60.8% |
| [b10_sidewalk_magazine_ladder](exports/b10_sidewalk_magazine_ladder.glb) | Medium | 0.555 × 0.667 × 1.597 | 5,000 | 704 | 2,864 | 1,280 | 57.3% |
| [b10_sidewalk_photo_booth](exports/b10_sidewalk_photo_booth.glb) | Large | 1.31 × 1.38 × 2.215 | 10,000 | 352 | 1,236 | 586 | 12.4% |
| [b10_spiral_snack_vending_machine](exports/b10_spiral_snack_vending_machine.glb) | Medium | 1.03 × 0.95 × 1.816 | 5,000 | 728 | 2,600 | 1,308 | 52.0% |
| [b10_square_cafe_umbrella_table](exports/b10_square_cafe_umbrella_table.glb) | Large | 2.049 × 2.049 × 2.365 | 10,000 | 689 | 2,648 | 1,274 | 26.5% |
| [b10_street_vendor_skewer_grill_cart](exports/b10_street_vendor_skewer_grill_cart.glb) | Medium | 1.435 × 0.835 × 1.045 | 5,000 | 1,192 | 4,612 | 2,236 | 92.2% |
| [b10_taco_preparation_service_station](exports/b10_taco_preparation_service_station.glb) | Medium | 1.5 × 0.87 × 1.621 | 5,000 | 1,160 | 4,320 | 2,184 | 86.4% |
| [b10_tiered_sidewalk_produce_stand](exports/b10_tiered_sidewalk_produce_stand.glb) | Medium | 1.3 × 0.88 × 1.627 | 5,000 | 1,434 | 4,788 | 2,240 | 95.8% |
| [b10_twin_globe_candy_dispenser](exports/b10_twin_globe_candy_dispenser.glb) | Medium | 0.62 × 0.56 × 1.305 | 5,000 | 852 | 3,472 | 1,604 | 69.4% |
| [b10_wood_fired_pizza_oven_cart](exports/b10_wood_fired_pizza_oven_cart.glb) | Large | 1.36 × 1.25 × 2.034 | 10,000 | 1,159 | 4,249 | 2,155 | 42.5% |
| [b10_woven_metal_cafe_chair](exports/b10_woven_metal_cafe_chair.glb) | Medium | 0.46 × 0.488 × 0.916 | 5,000 | 424 | 1,568 | 788 | 31.4% |

### Road Joint (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_road_bridge_finger_expansion_joint](exports/b13_road_bridge_finger_expansion_joint.glb) | Large | 3.6 × 1.44 × 0.187 | 10,000 | 1,320 | 5,280 | 2,456 | 52.8% |
| [b13_sidewalk_sliding_expansion_cover](exports/b13_sidewalk_sliding_expansion_cover.glb) | Medium | 1.8 × 0.81 × 0.148 | 5,000 | 648 | 2,592 | 1,200 | 51.8% |

### Road Surface (10)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_bridge_approach_settlement_slab](exports/b13_bridge_approach_settlement_slab.glb) | Large | 5 × 3.207 × 0.49 | 10,000 | 176 | 704 | 320 | 7.0% |
| [b13_crowned_cobblestone_alley](exports/b13_crowned_cobblestone_alley.glb) | Large | 2.96 × 3.3 × 0.27 | 10,000 | 2,184 | 8,736 | 4,004 | 87.4% |
| [b13_cycletrack_driveway_crossing](exports/b13_cycletrack_driveway_crossing.glb) | Large | 3.8 × 3.6 × 0.202 | 10,000 | 336 | 1,344 | 616 | 13.4% |
| [b13_ladder_crossing_road_section](exports/b13_ladder_crossing_road_section.glb) | Large | 4.5 × 2.8 × 0.13 | 10,000 | 208 | 832 | 380 | 8.3% |
| [b13_permeable_concrete_grid_paving](exports/b13_permeable_concrete_grid_paving.glb) | Large | 2.474 × 2.474 × 0.18 | 10,000 | 1,224 | 4,896 | 2,244 | 49.0% |
| [b13_raised_neighborhood_intersection](exports/b13_raised_neighborhood_intersection.glb) | Large | 6 × 6 × 0.25 | 10,000 | 440 | 1,760 | 788 | 17.6% |
| [b13_raised_pedestrian_crossing_table](exports/b13_raised_pedestrian_crossing_table.glb) | Large | 4.8 × 4.1 × 0.268 | 10,000 | 184 | 736 | 328 | 7.4% |
| [b13_reinforced_alley_sidewalk_crossover](exports/b13_reinforced_alley_sidewalk_crossover.glb) | Large | 4.2 × 2.5 × 0.28 | 10,000 | 336 | 1,344 | 612 | 13.4% |
| [b13_residential_driveway_apron](exports/b13_residential_driveway_apron.glb) | Large | 4.53 × 2.56 × 0.223 | 10,000 | 180 | 716 | 328 | 7.2% |
| [b13_zebra_crossing_road_section](exports/b13_zebra_crossing_road_section.glb) | Large | 4.6 × 3.2 × 0.18 | 10,000 | 216 | 864 | 396 | 8.6% |

### Security Lighting (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_twin_motion_sensor_security_light](exports/b18_twin_motion_sensor_security_light.glb) | Medium | 0.794 × 0.336 × 0.418 | 5,000 | 450 | 1,724 | 848 | 34.5% |
| [b18_yoke_mounted_rectangular_floodlight](exports/b18_yoke_mounted_rectangular_floodlight.glb) | Medium | 0.55 × 0.314 × 0.553 | 5,000 | 424 | 1,664 | 784 | 33.3% |

### Shrub (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b08_clipped_yew_hedge](exports/b08_clipped_yew_hedge.glb) | Large | 2.867 × 1.109 × 1.393 | 10,000 | 1,765 | 7,196 | 3,406 | 72.0% |
| [b08_privet_flowering_hedge](exports/b08_privet_flowering_hedge.glb) | Large | 3.015 × 1.05 × 1.572 | 10,000 | 1,214 | 4,690 | 2,328 | 46.9% |

### Signage (19)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b02_accessible_parking_sign](exports/b02_accessible_parking_sign.glb) | Medium | 0.62 × 0.203 × 2.49 | 5,000 | 1,016 | 4,000 | 1,880 | 80.0% |
| [b02_bike_route](exports/b02_bike_route.glb) | Medium | 0.69 × 0.198 × 2.45 | 5,000 | 648 | 1,944 | 996 | 38.9% |
| [b02_bus_stop_sign](exports/b02_bus_stop_sign.glb) | Medium | 0.49 × 0.219 × 2.55 | 5,000 | 1,024 | 4,016 | 1,896 | 80.3% |
| [b02_construction_detour_sign](exports/b02_construction_detour_sign.glb) | Medium | 1.034 × 0.5 × 2.177 | 5,000 | 1,208 | 4,816 | 2,224 | 96.3% |
| [b02_do_not_enter](exports/b02_do_not_enter.glb) | Medium | 0.74 × 0.196 × 2.47 | 5,000 | 544 | 1,632 | 848 | 32.6% |
| [b02_interstate_80_direction](exports/b02_interstate_80_direction.glb) | Medium | 0.68 × 0.214 × 2.62 | 5,000 | 1,132 | 4,442 | 2,100 | 88.8% |
| [b02_no_left_turn](exports/b02_no_left_turn.glb) | Medium | 0.7 × 0.226 × 2.455 | 5,000 | 984 | 3,888 | 1,820 | 77.8% |
| [b02_no_parking_sign](exports/b02_no_parking_sign.glb) | Medium | 0.62 × 0.226 × 2.5 | 5,000 | 1,104 | 4,368 | 2,040 | 87.4% |
| [b02_no_u_turn](exports/b02_no_u_turn.glb) | Medium | 0.7 × 0.226 × 2.455 | 5,000 | 1,056 | 4,176 | 1,952 | 83.5% |
| [b02_one_way_arrow](exports/b02_one_way_arrow.glb) | Medium | 1.04 × 0.214 × 2.51 | 5,000 | 456 | 1,776 | 852 | 35.5% |
| [b02_pedestrian_crossing](exports/b02_pedestrian_crossing.glb) | Medium | 0.998 × 0.22 × 2.599 | 5,000 | 584 | 2,304 | 1,084 | 46.1% |
| [b02_public_parking_sign](exports/b02_public_parking_sign.glb) | Medium | 0.62 × 0.214 × 2.485 | 5,000 | 600 | 2,352 | 1,116 | 47.0% |
| [b02_railroad_crossbuck](exports/b02_railroad_crossbuck.glb) | Medium | 1.484 × 0.202 × 2.882 | 5,000 | 744 | 2,232 | 1,128 | 44.6% |
| [b02_school_crossing](exports/b02_school_crossing.glb) | Medium | 0.8 × 0.214 × 2.534 | 5,000 | 756 | 2,968 | 1,400 | 59.4% |
| [b02_speed_limit_25](exports/b02_speed_limit_25.glb) | Medium | 0.66 × 0.205 × 2.49 | 5,000 | 544 | 1,632 | 840 | 32.6% |
| [b02_stop_sign](exports/b02_stop_sign.glb) | Medium | 0.721 × 0.201 × 2.44 | 5,000 | 936 | 3,696 | 1,732 | 73.9% |
| [b02_street_name_pair](exports/b02_street_name_pair.glb) | Medium | 1.2 × 1.12 × 2.95 | 5,000 | 912 | 3,600 | 1,684 | 72.0% |
| [b02_wrong_way](exports/b02_wrong_way.glb) | Medium | 0.8 × 0.2 × 2.41 | 5,000 | 456 | 1,368 | 708 | 27.4% |
| [b02_yield_sign](exports/b02_yield_sign.glb) | Medium | 0.817 × 0.195 × 2.44 | 5,000 | 620 | 2,464 | 1,144 | 49.3% |

### Step Lighting (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_recessed_brick_step_light](exports/b18_recessed_brick_step_light.glb) | Handheld | 0.26 × 0.091 × 0.11 | 999 | 216 | 864 | 400 | 86.5% |

### Street Lighting (6)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_cobrahead_roadway_lamp](exports/b18_cobrahead_roadway_lamp.glb) | Large | 2.644 × 0.528 × 7.447 | 10,000 | 726 | 2,772 | 1,368 | 27.7% |
| [b18_double_arm_boulevard_light](exports/b18_double_arm_boulevard_light.glb) | Large | 4.26 × 0.528 × 7.492 | 10,000 | 1,536 | 5,976 | 2,856 | 59.8% |
| [b18_flat_led_roadway_lamp](exports/b18_flat_led_roadway_lamp.glb) | Large | 2.24 × 0.44 × 6.794 | 10,000 | 896 | 3,520 | 1,668 | 35.2% |
| [b18_gooseneck_industrial_post_light](exports/b18_gooseneck_industrial_post_light.glb) | Large | 1.418 × 0.857 × 5.102 | 10,000 | 846 | 3,108 | 1,588 | 31.1% |
| [b18_historic_teardrop_streetlight](exports/b18_historic_teardrop_streetlight.glb) | Large | 1.737 × 0.571 × 6.078 | 10,000 | 1,087 | 3,956 | 2,042 | 39.6% |
| [b18_solar_panel_street_lamp](exports/b18_solar_panel_street_lamp.glb) | Large | 2.24 × 0.818 × 6.132 | 10,000 | 1,088 | 4,288 | 2,020 | 42.9% |

### Suspended Street Lighting (1)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_catenary_lighting_span](exports/b18_catenary_lighting_span.glb) | Large | 8.04 × 0.44 × 5.018 | 10,000 | 1,780 | 7,088 | 3,292 | 70.9% |

### Traffic (21)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b02_cable_protector_ramp](exports/b02_cable_protector_ramp.glb) | Handheld | 1.002 × 0.5 × 0.122 | 999 | 120 | 360 | 192 | 36.0% |
| [b02_concrete_jersey_barrier](exports/b02_concrete_jersey_barrier.glb) | Large | 2.35 × 0.66 × 0.9 | 10,000 | 120 | 472 | 220 | 4.7% |
| [b02_construction_traffic_barrel](exports/b02_construction_traffic_barrel.glb) | Medium | 0.74 × 0.704 × 1.3 | 5,000 | 474 | 1,708 | 896 | 34.2% |
| [b02_convex_traffic_mirror](exports/b02_convex_traffic_mirror.glb) | Medium | 0.77 × 0.25 × 2.61 | 5,000 | 472 | 1,844 | 900 | 36.9% |
| [b02_flashing_school_beacon](exports/b02_flashing_school_beacon.glb) | Medium | 0.64 × 0.435 × 2.74 | 5,000 | 1,218 | 4,776 | 2,180 | 95.5% |
| [b02_flexible_lane_delineator](exports/b02_flexible_lane_delineator.glb) | Medium | 0.28 × 0.28 × 0.905 | 5,000 | 200 | 736 | 376 | 14.7% |
| [b02_folding_warning_triangle](exports/b02_folding_warning_triangle.glb) | Handheld | 0.695 × 0.315 × 0.64 | 999 | 192 | 768 | 352 | 76.9% |
| [b02_horizontal_traffic_signal](exports/b02_horizontal_traffic_signal.glb) | Medium | 1.145 × 0.63 × 2.721 | 5,000 | 1,070 | 3,898 | 1,964 | 78.0% |
| [b02_mast_arm_traffic_signal](exports/b02_mast_arm_traffic_signal.glb) | Large | 5.38 × 0.704 × 6.115 | 10,000 | 2,028 | 7,332 | 3,716 | 73.3% |
| [b02_modular_speed_hump](exports/b02_modular_speed_hump.glb) | Large | 1.742 × 0.84 × 0.1 | 10,000 | 900 | 3,390 | 1,700 | 33.9% |
| [b02_pedestrian_walk_signal](exports/b02_pedestrian_walk_signal.glb) | Medium | 0.815 × 0.57 × 2.55 | 5,000 | 544 | 2,104 | 1,012 | 42.1% |
| [b02_plastic_water_barrier](exports/b02_plastic_water_barrier.glb) | Large | 2.05 × 0.6 × 0.975 | 10,000 | 632 | 2,352 | 1,172 | 23.5% |
| [b02_portable_arrow_message_board](exports/b02_portable_arrow_message_board.glb) | Large | 2.62 × 2.478 × 2.665 | 10,000 | 2,488 | 9,296 | 4,664 | 93.0% |
| [b02_railroad_crossing_gate](exports/b02_railroad_crossing_gate.glb) | Large | 4.375 × 0.714 × 2.7 | 10,000 | 560 | 2,068 | 1,052 | 20.7% |
| [b02_road_closed_barricade](exports/b02_road_closed_barricade.glb) | Large | 2.48 × 0.85 × 1.725 | 10,000 | 2,344 | 9,344 | 4,308 | 93.4% |
| [b02_sidewalk_closed_a_frame](exports/b02_sidewalk_closed_a_frame.glb) | Medium | 0.85 × 0.642 × 1.143 | 5,000 | 640 | 1,920 | 972 | 38.4% |
| [b02_striped_sawhorse_barricade](exports/b02_striped_sawhorse_barricade.glb) | Medium | 1.4 × 0.651 × 1.273 | 5,000 | 498 | 1,984 | 916 | 39.7% |
| [b02_traffic_camera_pole](exports/b02_traffic_camera_pole.glb) | Medium | 0.861 × 0.745 × 3.28 | 5,000 | 600 | 2,304 | 1,124 | 46.1% |
| [b02_traffic_cone](exports/b02_traffic_cone.glb) | Handheld | 0.39 × 0.39 × 0.708 | 999 | 208 | 736 | 388 | 73.7% |
| [b02_traffic_control_cabinet](exports/b02_traffic_control_cabinet.glb) | Medium | 0.81 × 0.605 × 1.545 | 5,000 | 360 | 1,424 | 660 | 28.5% |
| [b02_vertical_traffic_signal](exports/b02_vertical_traffic_signal.glb) | Medium | 0.715 × 0.63 × 3.211 | 5,000 | 1,070 | 3,898 | 1,964 | 78.0% |

### Transit Access (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_hinged_platform_gap_bridge](exports/b13_hinged_platform_gap_bridge.glb) | Medium | 1.3 × 1.325 × 0.66 | 5,000 | 568 | 2,172 | 1,048 | 43.4% |
| [b13_portable_rail_boarding_ramp](exports/b13_portable_rail_boarding_ramp.glb) | Medium | 1.161 × 2.18 × 0.334 | 5,000 | 824 | 3,256 | 1,528 | 65.1% |

### Transit Entrance (4)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_subway_entry_escalator](exports/b13_subway_entry_escalator.glb) | Large | 1.52 × 3.35 × 2.759 | 10,000 | 1,312 | 3,936 | 2,024 | 39.4% |
| [b13_subway_sidewalk_stair_entrance](exports/b13_subway_sidewalk_stair_entrance.glb) | Large | 2.33 × 3.23 × 2.945 | 10,000 | 2,136 | 7,944 | 3,936 | 79.4% |
| [b13_sunken_transit_ramp_entrance](exports/b13_sunken_transit_ramp_entrance.glb) | Large | 2.81 × 5.6 × 1.955 | 10,000 | 2,006 | 7,150 | 3,692 | 71.5% |
| [b13_transit_elevator_headhouse](exports/b13_transit_elevator_headhouse.glb) | Large | 2.34 × 2.15 × 3.145 | 10,000 | 816 | 3,248 | 1,496 | 32.5% |

### Transit Platform (4)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_bus_bulb_boarding_pad](exports/b13_bus_bulb_boarding_pad.glb) | Large | 5.2 × 1.97 × 0.274 | 10,000 | 1,462 | 5,196 | 2,680 | 52.0% |
| [b13_center_island_light_rail_platform](exports/b13_center_island_light_rail_platform.glb) | Large | 2.85 × 5.4 × 0.454 | 10,000 | 2,276 | 6,828 | 3,776 | 68.3% |
| [b13_elevated_commuter_platform_end](exports/b13_elevated_commuter_platform_end.glb) | Large | 2.7 × 4.7 × 2.435 | 10,000 | 2,360 | 7,080 | 3,908 | 70.8% |
| [b13_low_station_platform_with_access_ramp](exports/b13_low_station_platform_with_access_ramp.glb) | Large | 2.5 × 5.02 × 1.385 | 10,000 | 1,548 | 4,644 | 2,572 | 46.4% |

### Transit Structure (2)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b13_pedestrian_underpass_box_section](exports/b13_pedestrian_underpass_box_section.glb) | Large | 4.09 × 2.7 × 3.155 | 10,000 | 1,008 | 3,936 | 1,852 | 39.4% |
| [b13_streetcar_cut_stone_tunnel_portal](exports/b13_streetcar_cut_stone_tunnel_portal.glb) | Large | 5.25 × 1.6 × 4.59 | 10,000 | 712 | 2,816 | 1,316 | 28.2% |

### Tree (20)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b08_american_elm](exports/b08_american_elm.glb) | Large | 6.626 × 6.149 × 6.23 | 10,000 | 1,890 | 7,776 | 3,552 | 77.8% |
| [b08_arborvitae_screen_pair](exports/b08_arborvitae_screen_pair.glb) | Large | 2.658 × 1.218 × 3.52 | 10,000 | 927 | 3,714 | 1,790 | 37.1% |
| [b08_bald_cypress](exports/b08_bald_cypress.glb) | Large | 4.703 × 4.032 × 6.041 | 10,000 | 2,032 | 7,902 | 3,880 | 79.0% |
| [b08_blue_spruce](exports/b08_blue_spruce.glb) | Large | 3.388 × 2.732 × 5.551 | 10,000 | 2,240 | 9,042 | 4,136 | 90.4% |
| [b08_crape_myrtle](exports/b08_crape_myrtle.glb) | Large | 2.58 × 2.617 × 3.945 | 10,000 | 1,004 | 3,994 | 1,888 | 39.9% |
| [b08_eastern_red_cedar](exports/b08_eastern_red_cedar.glb) | Large | 2.076 × 2.001 × 4.731 | 10,000 | 1,383 | 5,556 | 2,682 | 55.6% |
| [b08_eastern_redbud](exports/b08_eastern_redbud.glb) | Large | 3.908 × 3.926 × 3.4 | 10,000 | 1,718 | 6,804 | 3,232 | 68.0% |
| [b08_eastern_white_pine](exports/b08_eastern_white_pine.glb) | Large | 5.131 × 4.666 × 6.9 | 10,000 | 1,892 | 7,382 | 3,616 | 73.8% |
| [b08_flowering_cherry](exports/b08_flowering_cherry.glb) | Large | 4.755 × 4.729 × 4.051 | 10,000 | 1,540 | 6,402 | 2,904 | 64.0% |
| [b08_flowering_dogwood](exports/b08_flowering_dogwood.glb) | Large | 3.474 × 3.09 × 2.767 | 10,000 | 2,355 | 9,686 | 4,230 | 96.9% |
| [b08_ginkgo](exports/b08_ginkgo.glb) | Large | 3.846 × 3.442 × 5.622 | 10,000 | 1,029 | 4,066 | 1,910 | 40.7% |
| [b08_honeylocust](exports/b08_honeylocust.glb) | Large | 5.614 × 4.949 × 4.549 | 10,000 | 2,023 | 7,922 | 3,850 | 79.2% |
| [b08_mature_white_oak](exports/b08_mature_white_oak.glb) | Large | 7.168 × 4.936 × 6.34 | 10,000 | 1,820 | 6,992 | 3,476 | 69.9% |
| [b08_river_birch_clump](exports/b08_river_birch_clump.glb) | Large | 3.96 × 3.747 × 6.235 | 10,000 | 1,960 | 7,284 | 3,740 | 72.8% |
| [b08_southern_magnolia](exports/b08_southern_magnolia.glb) | Large | 3.707 × 3.147 × 4.867 | 10,000 | 1,728 | 6,824 | 3,160 | 68.2% |
| [b08_staked_young_street_tree](exports/b08_staked_young_street_tree.glb) | Large | 1.877 × 1.714 × 2.971 | 10,000 | 658 | 2,502 | 1,248 | 25.0% |
| [b08_sugar_maple](exports/b08_sugar_maple.glb) | Large | 4.54 × 4.311 × 5.924 | 10,000 | 1,434 | 5,112 | 2,544 | 51.1% |
| [b08_sycamore](exports/b08_sycamore.glb) | Large | 6.34 × 4.82 × 6.924 | 10,000 | 1,562 | 6,192 | 3,000 | 61.9% |
| [b08_tulip_poplar](exports/b08_tulip_poplar.glb) | Large | 3.712 × 3.596 × 7.448 | 10,000 | 1,406 | 5,082 | 2,504 | 50.8% |
| [b08_weeping_willow](exports/b08_weeping_willow.glb) | Large | 5.829 × 5.516 × 5.126 | 10,000 | 1,752 | 7,038 | 3,240 | 70.4% |

### Utilities Covers Drains (8)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b05_curb_inlet_storm_drain](exports/b05_curb_inlet_storm_drain.glb) | Medium | 1.25 × 0.635 × 0.47 | 5,000 | 360 | 1,440 | 660 | 28.8% |
| [b05_double_panel_sump_grate](exports/b05_double_panel_sump_grate.glb) | Medium | 1.22 × 0.78 × 0.223 | 5,000 | 912 | 3,648 | 1,672 | 73.0% |
| [b05_linear_trench_drain](exports/b05_linear_trench_drain.glb) | Medium | 1.56 × 0.33 × 0.189 | 5,000 | 768 | 3,072 | 1,408 | 61.4% |
| [b05_round_landscape_area_drain](exports/b05_round_landscape_area_drain.glb) | Handheld | 0.44 × 0.44 × 0.131 | 999 | 160 | 480 | 292 | 48.0% |
| [b05_sanitary_manhole_cover](exports/b05_sanitary_manhole_cover.glb) | Medium | 0.86 × 0.86 × 0.145 | 5,000 | 704 | 2,656 | 1,332 | 53.1% |
| [b05_square_catch_basin_grate](exports/b05_square_catch_basin_grate.glb) | Medium | 0.84 × 0.84 × 0.229 | 5,000 | 624 | 2,496 | 1,152 | 49.9% |
| [b05_storm_sewer_radial_cover](exports/b05_storm_sewer_radial_cover.glb) | Medium | 0.98 × 0.98 × 0.16 | 5,000 | 1,152 | 4,236 | 2,228 | 84.7% |
| [b05_telecom_vault_access_cover](exports/b05_telecom_vault_access_cover.glb) | Medium | 1.12 × 0.72 × 0.167 | 5,000 | 456 | 1,824 | 836 | 36.5% |

### Utilities Electrical (12)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b05_coax_cable_junction_pedestal](exports/b05_coax_cable_junction_pedestal.glb) | Medium | 0.4 × 0.4 × 0.975 | 5,000 | 206 | 784 | 384 | 15.7% |
| [b05_fiber_distribution_cabinet](exports/b05_fiber_distribution_cabinet.glb) | Medium | 0.85 × 0.649 × 1.445 | 5,000 | 544 | 2,176 | 1,008 | 43.5% |
| [b05_four_meter_service_bank](exports/b05_four_meter_service_bank.glb) | Large | 1.37 × 0.374 × 1.4 | 10,000 | 944 | 3,520 | 1,768 | 35.2% |
| [b05_generator_transfer_switch](exports/b05_generator_transfer_switch.glb) | Medium | 0.72 × 0.561 × 1.185 | 5,000 | 800 | 3,148 | 1,480 | 63.0% |
| [b05_outdoor_fused_disconnect](exports/b05_outdoor_fused_disconnect.glb) | Medium | 0.489 × 0.45 × 1.26 | 5,000 | 580 | 2,288 | 1,076 | 45.8% |
| [b05_padmount_transformer](exports/b05_padmount_transformer.glb) | Large | 1.7 × 1.38 × 1.345 | 10,000 | 912 | 3,648 | 1,692 | 36.5% |
| [b05_polemount_transformer_can](exports/b05_polemount_transformer_can.glb) | Medium | 0.75 × 0.8 × 1.06 | 5,000 | 784 | 2,816 | 1,472 | 56.3% |
| [b05_streetlight_control_cabinet](exports/b05_streetlight_control_cabinet.glb) | Medium | 0.66 × 0.516 × 1.36 | 5,000 | 706 | 2,784 | 1,308 | 55.7% |
| [b05_telephone_distribution_pedestal](exports/b05_telephone_distribution_pedestal.glb) | Medium | 0.36 × 0.3 × 1.04 | 5,000 | 204 | 816 | 376 | 16.3% |
| [b05_three_phase_transformer_rack](exports/b05_three_phase_transformer_rack.glb) | Large | 2.25 × 0.74 × 1.647 | 10,000 | 1,848 | 6,792 | 3,476 | 67.9% |
| [b05_traffic_signal_controller_cabinet](exports/b05_traffic_signal_controller_cabinet.glb) | Large | 1 × 0.826 × 1.76 | 10,000 | 708 | 2,832 | 1,308 | 28.3% |
| [b05_utility_meter_pedestal](exports/b05_utility_meter_pedestal.glb) | Medium | 0.44 × 0.439 × 1.445 | 5,000 | 256 | 976 | 476 | 19.5% |

### Utilities Fire Water (6)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b05_backflow_preventer_assembly](exports/b05_backflow_preventer_assembly.glb) | Large | 1.52 × 0.395 × 1.172 | 10,000 | 924 | 3,448 | 1,764 | 34.5% |
| [b05_breakaway_barrel_hydrant](exports/b05_breakaway_barrel_hydrant.glb) | Medium | 0.58 × 0.48 × 1.665 | 5,000 | 900 | 3,386 | 1,700 | 67.7% |
| [b05_classic_fire_hydrant](exports/b05_classic_fire_hydrant.glb) | Medium | 0.68 × 0.54 × 1 | 5,000 | 860 | 3,266 | 1,620 | 65.3% |
| [b05_post_indicator_valve](exports/b05_post_indicator_valve.glb) | Medium | 0.42 × 0.32 × 1.18 | 5,000 | 312 | 1,184 | 584 | 23.7% |
| [b05_siamese_fire_department_connection](exports/b05_siamese_fire_department_connection.glb) | Medium | 0.624 × 0.38 × 0.854 | 5,000 | 448 | 1,724 | 832 | 34.5% |
| [b05_wall_fire_hose_connection](exports/b05_wall_fire_hose_connection.glb) | Medium | 0.64 × 0.314 × 0.6 | 5,000 | 396 | 1,476 | 744 | 29.5% |

### Utilities Hvac (10)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b05_evaporative_cooler](exports/b05_evaporative_cooler.glb) | Medium | 1.054 × 1.317 × 1.11 | 5,000 | 696 | 2,808 | 1,276 | 56.2% |
| [b05_gooseneck_roof_vent](exports/b05_gooseneck_roof_vent.glb) | Medium | 0.62 × 1.06 × 1.193 | 5,000 | 468 | 1,680 | 888 | 33.6% |
| [b05_industrial_axial_exhaust_fan](exports/b05_industrial_axial_exhaust_fan.glb) | Large | 1.332 × 0.69 × 1.506 | 10,000 | 1,168 | 4,160 | 2,224 | 41.6% |
| [b05_long_rooftop_air_handler](exports/b05_long_rooftop_air_handler.glb) | Large | 3.41 × 1.313 × 1.585 | 10,000 | 1,024 | 3,232 | 1,768 | 32.3% |
| [b05_louvered_air_intake_tower](exports/b05_louvered_air_intake_tower.glb) | Large | 1.1 × 1 × 2.09 | 10,000 | 720 | 2,880 | 1,320 | 28.8% |
| [b05_mini_split_outdoor_unit](exports/b05_mini_split_outdoor_unit.glb) | Medium | 0.988 × 0.403 × 0.753 | 5,000 | 1,186 | 4,470 | 2,216 | 89.4% |
| [b05_mushroom_roof_exhaust](exports/b05_mushroom_roof_exhaust.glb) | Medium | 0.871 × 0.871 × 0.767 | 5,000 | 696 | 2,544 | 1,312 | 50.9% |
| [b05_residential_ac_condenser](exports/b05_residential_ac_condenser.glb) | Medium | 0.94 × 1.11 × 0.965 | 5,000 | 1,008 | 3,216 | 1,696 | 64.3% |
| [b05_rooftop_packaged_hvac](exports/b05_rooftop_packaged_hvac.glb) | Large | 2.385 × 1.46 × 1.285 | 10,000 | 1,392 | 4,496 | 2,492 | 45.0% |
| [b05_wind_turbine_roof_vent](exports/b05_wind_turbine_roof_vent.glb) | Medium | 0.65 × 0.65 × 0.74 | 5,000 | 648 | 2,102 | 1,112 | 42.0% |

### Utilities Meters Valves (8)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b05_curb_stop_valve_cover](exports/b05_curb_stop_valve_cover.glb) | Handheld | 0.26 × 0.26 × 0.184 | 999 | 232 | 860 | 440 | 86.1% |
| [b05_gas_pressure_regulator_station](exports/b05_gas_pressure_regulator_station.glb) | Large | 1.45 × 0.64 × 1.195 | 10,000 | 586 | 2,144 | 1,104 | 21.4% |
| [b05_gas_vent_riser](exports/b05_gas_vent_riser.glb) | Medium | 0.32 × 0.502 × 2.048 | 5,000 | 360 | 1,284 | 676 | 25.7% |
| [b05_irrigation_valve_access_box](exports/b05_irrigation_valve_access_box.glb) | Handheld | 0.54 × 0.38 × 0.256 | 999 | 88 | 264 | 132 | 26.4% |
| [b05_residential_gas_meter](exports/b05_residential_gas_meter.glb) | Medium | 0.626 × 0.414 × 0.816 | 5,000 | 820 | 3,088 | 1,532 | 61.8% |
| [b05_sewer_cleanout_access_cap](exports/b05_sewer_cleanout_access_cap.glb) | Handheld | 0.32 × 0.304 × 0.305 | 999 | 148 | 524 | 280 | 52.5% |
| [b05_water_meter_lid_box](exports/b05_water_meter_lid_box.glb) | Handheld | 0.45 × 0.3 × 0.21 | 999 | 112 | 336 | 172 | 33.6% |
| [b05_water_sampling_station](exports/b05_water_sampling_station.glb) | Medium | 0.498 × 0.45 × 1.21 | 5,000 | 552 | 2,160 | 1,028 | 43.2% |

### Utilities Poles (6)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b05_concrete_utility_pole](exports/b05_concrete_utility_pole.glb) | Large | 1.7 × 0.54 × 7.4 | 10,000 | 888 | 3,208 | 1,660 | 32.1% |
| [b05_guyed_corner_power_pole](exports/b05_guyed_corner_power_pole.glb) | Large | 3.265 × 0.569 × 7.5 | 10,000 | 964 | 3,512 | 1,820 | 35.1% |
| [b05_overhead_service_mast](exports/b05_overhead_service_mast.glb) | Large | 0.4 × 0.706 × 3.444 | 10,000 | 488 | 1,984 | 904 | 19.8% |
| [b05_small_cell_network_pole](exports/b05_small_cell_network_pole.glb) | Large | 0.61 × 0.6 × 7.255 | 10,000 | 668 | 2,560 | 1,260 | 25.6% |
| [b05_telecom_splice_pole](exports/b05_telecom_splice_pole.glb) | Large | 1.1 × 0.33 × 6.35 | 10,000 | 544 | 1,984 | 1,044 | 19.8% |
| [b05_wood_distribution_power_pole](exports/b05_wood_distribution_power_pole.glb) | Large | 2.45 × 0.307 × 7.8 | 10,000 | 832 | 3,080 | 1,572 | 30.8% |

### Wall Lighting (6)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b18_barn_gooseneck_wall_light](exports/b18_barn_gooseneck_wall_light.glb) | Medium | 0.694 × 1.044 × 0.581 | 5,000 | 498 | 1,812 | 928 | 36.2% |
| [b18_coach_house_wall_lantern](exports/b18_coach_house_wall_lantern.glb) | Medium | 0.445 × 0.67 × 0.667 | 5,000 | 795 | 3,096 | 1,466 | 61.9% |
| [b18_cylindrical_up_down_sconce](exports/b18_cylindrical_up_down_sconce.glb) | Handheld | 0.152 × 0.203 × 0.332 | 999 | 264 | 792 | 500 | 79.3% |
| [b18_modern_cube_downlight](exports/b18_modern_cube_downlight.glb) | Handheld | 0.22 × 0.237 × 0.236 | 999 | 112 | 336 | 176 | 33.6% |
| [b18_rectangular_caged_wall_light](exports/b18_rectangular_caged_wall_light.glb) | Handheld | 0.187 × 0.125 × 0.36 | 999 | 240 | 960 | 440 | 96.1% |
| [b18_round_bulkhead_wall_light](exports/b18_round_bulkhead_wall_light.glb) | Handheld | 0.29 × 0.123 × 0.29 | 999 | 144 | 492 | 268 | 49.2% |

### Waste Recycling Street Cleaning (50)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b04_baled_plastic_bottles](exports/b04_baled_plastic_bottles.glb) | Medium | 0.748 × 0.66 × 0.597 | 5,000 | 1,211 | 4,688 | 2,050 | 93.8% |
| [b04_bear_resistant_trail_refuse_bin](exports/b04_bear_resistant_trail_refuse_bin.glb) | Medium | 0.95 × 1 × 1.273 | 5,000 | 216 | 864 | 396 | 17.3% |
| [b04_broken_pallet_scrap_stack](exports/b04_broken_pallet_scrap_stack.glb) | Large | 1.23 × 0.96 × 0.422 | 10,000 | 576 | 2,304 | 1,052 | 23.0% |
| [b04_bulky_pickup_worn_armchair](exports/b04_bulky_pickup_worn_armchair.glb) | Medium | 0.94 × 0.859 × 1.084 | 5,000 | 671 | 2,649 | 1,257 | 53.0% |
| [b04_cardboard_dumpster_with_slot](exports/b04_cardboard_dumpster_with_slot.glb) | Large | 2.38 × 1.573 × 1.827 | 10,000 | 1,440 | 5,408 | 2,680 | 54.1% |
| [b04_cigarette_butt_disposal_tower](exports/b04_cigarette_butt_disposal_tower.glb) | Medium | 0.41 × 0.39 × 1.135 | 5,000 | 192 | 720 | 360 | 14.4% |
| [b04_clear_sack_of_recyclables](exports/b04_clear_sack_of_recyclables.glb) | Handheld | 0.562 × 0.453 × 0.589 | 999 | 134 | 444 | 236 | 44.4% |
| [b04_clothing_donation_dropbox](exports/b04_clothing_donation_dropbox.glb) | Large | 1.35 × 1.358 × 2.013 | 10,000 | 248 | 976 | 456 | 9.8% |
| [b04_compact_municipal_street_sweeper](exports/b04_compact_municipal_street_sweeper.glb) | Large | 2.985 × 2.144 × 2.162 | 10,000 | 2,466 | 7,486 | 4,130 | 74.9% |
| [b04_compact_open_debris_skip](exports/b04_compact_open_debris_skip.glb) | Large | 3.265 × 1.97 × 1.135 | 10,000 | 632 | 2,464 | 1,168 | 24.6% |
| [b04_compressed_aluminum_can_bale](exports/b04_compressed_aluminum_can_bale.glb) | Medium | 0.7 × 0.648 × 0.615 | 5,000 | 1,171 | 4,748 | 1,990 | 95.0% |
| [b04_construction_rolloff_container](exports/b04_construction_rolloff_container.glb) | Large | 5.79 × 2.457 × 2.095 | 10,000 | 1,712 | 6,672 | 3,196 | 66.7% |
| [b04_curbside_discarded_mattress](exports/b04_curbside_discarded_mattress.glb) | Large | 1.065 × 1.96 × 0.31 | 10,000 | 1,137 | 4,344 | 2,134 | 43.4% |
| [b04_curbside_tied_brush_bundle](exports/b04_curbside_tied_brush_bundle.glb) | Medium | 1.302 × 0.676 × 0.462 | 5,000 | 704 | 2,752 | 1,336 | 55.0% |
| [b04_discarded_tire_stack](exports/b04_discarded_tire_stack.glb) | Medium | 0.755 × 0.722 × 0.557 | 5,000 | 624 | 2,352 | 1,200 | 47.0% |
| [b04_dog_waste_bag_and_bin_station](exports/b04_dog_waste_bag_and_bin_station.glb) | Medium | 0.497 × 0.636 × 1.765 | 5,000 | 254 | 956 | 472 | 19.1% |
| [b04_dual_stream_transit_bin_station](exports/b04_dual_stream_transit_bin_station.glb) | Large | 1.43 × 0.665 × 1.76 | 10,000 | 880 | 3,344 | 1,592 | 33.4% |
| [b04_flattened_cardboard_tied_stack](exports/b04_flattened_cardboard_tied_stack.glb) | Handheld | 0.646 × 0.486 × 0.146 | 999 | 220 | 644 | 336 | 64.5% |
| [b04_folded_top_paper_leaf_sack](exports/b04_folded_top_paper_leaf_sack.glb) | Handheld | 0.44 × 0.314 × 0.762 | 999 | 122 | 488 | 220 | 48.8% |
| [b04_front_load_commercial_dumpster](exports/b04_front_load_commercial_dumpster.glb) | Large | 2.68 × 1.84 × 1.945 | 10,000 | 800 | 3,184 | 1,468 | 31.8% |
| [b04_galvanized_ash_can](exports/b04_galvanized_ash_can.glb) | Medium | 0.489 × 0.487 × 0.573 | 5,000 | 628 | 2,216 | 1,228 | 44.3% |
| [b04_handheld_litter_collection_hoop_bag](exports/b04_handheld_litter_collection_hoop_bag.glb) | Handheld | 0.501 × 0.576 × 0.608 | 999 | 270 | 892 | 480 | 89.3% |
| [b04_hooded_side_entry_street_bin](exports/b04_hooded_side_entry_street_bin.glb) | Medium | 0.669 × 0.669 × 1.17 | 5,000 | 386 | 1,440 | 748 | 28.8% |
| [b04_household_lidded_refuse_cart](exports/b04_household_lidded_refuse_cart.glb) | Medium | 0.675 × 0.819 × 1.098 | 5,000 | 728 | 2,672 | 1,360 | 53.4% |
| [b04_igloo_glass_bottle_recycling_bank](exports/b04_igloo_glass_bottle_recycling_bank.glb) | Large | 1.76 × 1.764 × 1.753 | 10,000 | 316 | 1,160 | 608 | 11.6% |
| [b04_open_yard_waste_cart](exports/b04_open_yard_waste_cart.glb) | Medium | 0.65 × 0.786 × 1.655 | 5,000 | 860 | 3,236 | 1,612 | 64.7% |
| [b04_outdoor_janitor_pushcart](exports/b04_outdoor_janitor_pushcart.glb) | Medium | 1.294 × 0.59 × 1.195 | 5,000 | 1,083 | 3,874 | 2,042 | 77.5% |
| [b04_oversize_blue_recycling_cart](exports/b04_oversize_blue_recycling_cart.glb) | Medium | 0.765 × 0.931 × 1.198 | 5,000 | 944 | 3,536 | 1,756 | 70.7% |
| [b04_perforated_steel_drum_bin](exports/b04_perforated_steel_drum_bin.glb) | Medium | 0.615 × 0.604 × 0.851 | 5,000 | 912 | 2,736 | 1,408 | 54.7% |
| [b04_rear_load_rolling_dumpster](exports/b04_rear_load_rolling_dumpster.glb) | Large | 2.21 × 1.24 × 1.578 | 10,000 | 1,584 | 5,936 | 2,948 | 59.4% |
| [b04_restaurant_used_grease_container](exports/b04_restaurant_used_grease_container.glb) | Medium | 0.87 × 0.9 × 1.14 | 5,000 | 616 | 2,256 | 1,152 | 45.1% |
| [b04_round_household_trash_can](exports/b04_round_household_trash_can.glb) | Medium | 0.635 × 0.579 × 0.726 | 5,000 | 428 | 1,716 | 788 | 34.3% |
| [b04_slatted_park_litter_bin](exports/b04_slatted_park_litter_bin.glb) | Medium | 0.66 × 0.66 × 0.941 | 5,000 | 672 | 2,424 | 1,244 | 48.5% |
| [b04_small_food_scrap_curb_cart](exports/b04_small_food_scrap_curb_cart.glb) | Medium | 0.475 × 0.649 × 0.978 | 5,000 | 848 | 3,104 | 1,584 | 62.1% |
| [b04_solar_compacting_public_bin](exports/b04_solar_compacting_public_bin.glb) | Medium | 0.69 × 0.758 × 1.46 | 5,000 | 296 | 1,168 | 536 | 23.4% |
| [b04_square_concrete_park_receptacle](exports/b04_square_concrete_park_receptacle.glb) | Medium | 0.73 × 0.73 × 0.89 | 5,000 | 312 | 1,248 | 568 | 25.0% |
| [b04_street_cleaning_water_hose_cart](exports/b04_street_cleaning_water_hose_cart.glb) | Medium | 1.044 × 0.974 × 1.092 | 5,000 | 774 | 2,632 | 1,436 | 52.6% |
| [b04_three_bag_yard_clippings_pile](exports/b04_three_bag_yard_clippings_pile.glb) | Medium | 0.948 × 0.849 × 0.625 | 5,000 | 417 | 1,608 | 794 | 32.2% |
| [b04_three_hole_public_recycling_sorter](exports/b04_three_hole_public_recycling_sorter.glb) | Large | 1.77 × 0.723 × 1.145 | 10,000 | 870 | 3,252 | 1,564 | 32.5% |
| [b04_tied_black_refuse_sack](exports/b04_tied_black_refuse_sack.glb) | Handheld | 0.58 × 0.468 × 0.628 | 999 | 127 | 484 | 242 | 48.4% |
| [b04_towable_leaf_vacuum](exports/b04_towable_leaf_vacuum.glb) | Large | 2.945 × 1.689 × 1.754 | 10,000 | 1,380 | 4,702 | 2,488 | 47.0% |
| [b04_trigger_litter_picker_tongs](exports/b04_trigger_litter_picker_tongs.glb) | Handheld | 0.188 × 0.06 × 1.071 | 999 | 204 | 816 | 380 | 81.7% |
| [b04_twine_bound_newspaper_bundle](exports/b04_twine_bound_newspaper_bundle.glb) | Handheld | 0.416 × 0.32 × 0.213 | 999 | 196 | 588 | 308 | 58.9% |
| [b04_two_wheel_refuse_bin_dolly](exports/b04_two_wheel_refuse_bin_dolly.glb) | Medium | 0.659 × 0.58 × 1.22 | 5,000 | 568 | 2,016 | 1,068 | 40.3% |
| [b04_upright_lobby_dustpan](exports/b04_upright_lobby_dustpan.glb) | Handheld | 0.33 × 0.315 × 1.06 | 999 | 180 | 720 | 332 | 72.1% |
| [b04_used_motor_oil_collection_tank](exports/b04_used_motor_oil_collection_tank.glb) | Large | 1.556 × 1.016 × 1.503 | 10,000 | 492 | 1,760 | 944 | 17.6% |
| [b04_walk_behind_parking_lot_sweeper](exports/b04_walk_behind_parking_lot_sweeper.glb) | Medium | 1.305 × 1.112 × 1.039 | 5,000 | 1,184 | 3,600 | 2,012 | 72.0% |
| [b04_wide_street_push_broom](exports/b04_wide_street_push_broom.glb) | Handheld | 0.57 × 0.385 × 1.444 | 999 | 120 | 360 | 192 | 36.0% |
| [b04_wire_leaf_collection_cage](exports/b04_wire_leaf_collection_cage.glb) | Medium | 0.869 × 0.869 × 0.914 | 5,000 | 672 | 2,424 | 1,284 | 48.5% |
| [b04_wire_mesh_street_basket](exports/b04_wire_mesh_street_basket.glb) | Medium | 0.733 × 0.733 × 0.817 | 5,000 | 832 | 3,204 | 1,600 | 64.1% |

### Waterfront (15)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b20_boat_launch_hand_winch_pedestal](exports/b20_boat_launch_hand_winch_pedestal.glb) | Medium | 0.63 × 1.003 × 1.315 | 5,000 | 564 | 2,156 | 1,064 | 43.1% |
| [b20_cast_dock_mooring_cleat](exports/b20_cast_dock_mooring_cleat.glb) | Medium | 0.838 × 0.19 × 0.31 | 5,000 | 264 | 1,056 | 492 | 21.1% |
| [b20_channel_marker_buoy](exports/b20_channel_marker_buoy.glb) | Medium | 0.899 × 0.899 × 1.79 | 5,000 | 424 | 1,560 | 812 | 31.2% |
| [b20_dock_corner_rubber_fender](exports/b20_dock_corner_rubber_fender.glb) | Medium | 0.67 × 0.65 × 0.62 | 5,000 | 336 | 1,344 | 624 | 26.9% |
| [b20_dock_piling_protective_sleeve](exports/b20_dock_piling_protective_sleeve.glb) | Medium | 0.519 × 0.526 × 1.72 | 5,000 | 473 | 1,848 | 926 | 37.0% |
| [b20_dock_swim_ladder](exports/b20_dock_swim_ladder.glb) | Medium | 0.71 × 0.855 × 2.102 | 5,000 | 800 | 3,040 | 1,464 | 60.8% |
| [b20_fishing_line_recycling_tube](exports/b20_fishing_line_recycling_tube.glb) | Medium | 0.34 × 0.417 × 1.41 | 5,000 | 400 | 1,440 | 768 | 28.8% |
| [b20_hinged_marina_gangway](exports/b20_hinged_marina_gangway.glb) | Large | 1.32 × 3.955 × 1.65 | 10,000 | 1,288 | 4,832 | 2,400 | 48.3% |
| [b20_lifering_emergency_stand](exports/b20_lifering_emergency_stand.glb) | Medium | 0.803 × 0.4 × 1.98 | 5,000 | 812 | 3,184 | 1,560 | 63.7% |
| [b20_marina_gear_handcart](exports/b20_marina_gear_handcart.glb) | Medium | 0.889 × 1.349 × 1.1 | 5,000 | 912 | 3,280 | 1,724 | 65.6% |
| [b20_marina_sewage_pumpout_station](exports/b20_marina_sewage_pumpout_station.glb) | Medium | 1.105 × 0.705 × 1.24 | 5,000 | 840 | 3,152 | 1,616 | 63.0% |
| [b20_marina_shore_power_pedestal](exports/b20_marina_shore_power_pedestal.glb) | Medium | 0.43 × 0.36 × 1.353 | 5,000 | 520 | 2,048 | 960 | 41.0% |
| [b20_modular_floating_dock_section](exports/b20_modular_floating_dock_section.glb) | Large | 2.118 × 3.125 × 0.601 | 10,000 | 1,272 | 5,424 | 2,336 | 54.2% |
| [b20_roller_boat_launch_cradle](exports/b20_roller_boat_launch_cradle.glb) | Large | 1.5 × 2.8 × 0.59 | 10,000 | 688 | 2,624 | 1,272 | 26.2% |
| [b20_three_level_kayak_storage_rack](exports/b20_three_level_kayak_storage_rack.glb) | Large | 2.25 × 1.65 × 2.23 | 10,000 | 1,096 | 4,192 | 2,024 | 41.9% |

### Winter Equipment (15)

| Item / GLB | Size | Dimensions (m) | Vertex limit | Source vertices | GLB vertices | Triangles | Used |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [b20_bagged_road_salt_pallet](exports/b20_bagged_road_salt_pallet.glb) | Medium | 1.05 × 0.89 × 0.804 | 5,000 | 1,104 | 4,224 | 2,024 | 84.5% |
| [b20_brine_mixing_service_cart](exports/b20_brine_mixing_service_cart.glb) | Medium | 0.857 × 0.94 × 1.14 | 5,000 | 1,148 | 4,152 | 2,200 | 83.0% |
| [b20_heated_walkway_mat_controller](exports/b20_heated_walkway_mat_controller.glb) | Large | 1.355 × 2.12 × 1.115 | 10,000 | 588 | 2,336 | 1,084 | 23.4% |
| [b20_municipal_salt_grit_bunker](exports/b20_municipal_salt_grit_bunker.glb) | Medium | 1.11 × 0.853 × 0.86 | 5,000 | 340 | 1,328 | 632 | 26.6% |
| [b20_reflective_driveway_snow_marker](exports/b20_reflective_driveway_snow_marker.glb) | Medium | 0.094 × 0.053 × 1.599 | 5,000 | 154 | 604 | 288 | 12.1% |
| [b20_sidewalk_broadcast_salt_spreader](exports/b20_sidewalk_broadcast_salt_spreader.glb) | Medium | 0.8 × 0.767 × 1.047 | 5,000 | 636 | 2,342 | 1,196 | 46.8% |
| [b20_sidewalk_ice_chopper](exports/b20_sidewalk_ice_chopper.glb) | Handheld | 0.2 × 0.067 × 1.427 | 999 | 208 | 752 | 396 | 75.3% |
| [b20_snow_boot_brush_station](exports/b20_snow_boot_brush_station.glb) | Medium | 0.7 × 0.46 × 1.028 | 5,000 | 672 | 2,640 | 1,236 | 52.8% |
| [b20_snowplow_blade_storage_dolly](exports/b20_snowplow_blade_storage_dolly.glb) | Large | 2.16 × 1.095 × 0.965 | 10,000 | 868 | 3,200 | 1,640 | 32.0% |
| [b20_telescopic_roof_snow_rake](exports/b20_telescopic_roof_snow_rake.glb) | Handheld | 0.69 × 0.917 × 3.003 | 999 | 256 | 968 | 476 | 96.9% |
| [b20_towable_ice_grit_sledge](exports/b20_towable_ice_grit_sledge.glb) | Medium | 0.758 × 1.522 × 0.586 | 5,000 | 312 | 1,248 | 572 | 25.0% |
| [b20_two_stage_walkbehind_snowblower](exports/b20_two_stage_walkbehind_snowblower.glb) | Medium | 0.912 × 1.735 × 1.266 | 5,000 | 794 | 2,592 | 1,376 | 51.8% |
| [b20_wheeled_snow_scoop](exports/b20_wheeled_snow_scoop.glb) | Medium | 0.856 × 1.253 × 1.083 | 5,000 | 500 | 1,816 | 948 | 36.3% |
| [b20_wide_push_snow_shovel](exports/b20_wide_push_snow_shovel.glb) | Handheld | 0.69 × 0.619 × 1.466 | 999 | 128 | 384 | 208 | 38.4% |
| [b20_winter_maintenance_storage_locker](exports/b20_winter_maintenance_storage_locker.glb) | Medium | 0.9 × 0.651 × 1.925 | 5,000 | 508 | 2,032 | 936 | 40.6% |
