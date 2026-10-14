# Modular building kit

50 additional assets (`b21_`), preserving the original 1,000 props. All share the existing palette. Straight wall runs, floor/ceiling panels and door/window assemblies are modeled in metres. Parts have bottom-centred origins at world zero like every other source asset.

## Dimensions and placement

- Wall runs extend along Blender X, with thickness along Y, and height along Z. GLB converts Blender Z to +Y up.
- Wall height: **3 m**. Structural thickness: **0.2 m** (opening reveal trim reaches 0.204 m). Straight lengths: **1, 2 and 4 m**. Place adjacent run centres half the sum of their widths apart.
- Floor modules: **0.2 m** thick. Place walls **0.2 m above the floor module origin** to sit on the finished floor.
- Door openings: **1 m × 2.2 m** or **2 m × 2.2 m**. Door assemblies use the same outer dimensions and fit inside those openings. Place the door origin at the wall origin, aligned in X/Y.
- Window openings: **1 or 2 m wide × 1.4 m tall**, starting **0.9 m above the wall origin**. Put the matching window module at that height, at the wall centre in X/Y.
- Storefront opening: **3.6 m × 2.6 m**. Use the matching storefront door or shopfront window, at the wall origin.
- Ceiling panels: plain/grid panels have separate underside details and thicknesses. Put their bottom origins at the wall top (**wall origin +3 m**). Exposed beam ceiling is 0.2 m deep. Consult manifest dimensions for each ceiling.
- Corner/T wall modules occupy nominal **1 × 1 m** footprints. Their arms run along the sides of that footprint; rotate by 90-degree increments. The end pier is 0.2 m square with 0.22 m caps.
- The 2 × 0.6 m clerestory is a custom-opening insert; it does not fill the standard 1.4 m-tall window opening.
- Sills are separate optional parts, 0.07 m tall. Position them immediately below a window opening and offset toward the desired exterior side; they intentionally project beyond the wall.

## Assembly example

The master Blender file includes a **Building Kit Example** scene with collection instances: a 4 × 4 m floor, 3 m walls, matching window and door, corner piers, and a ceiling instance hidden by default for inspection. Original source meshes remain at world zero. To make an enclosed room, unhide the ceiling instance. The instance metadata records the source asset names.

For this example: floor origin `(0,0,0)`; wall centres `(0,±2.1,0.2)` and `(±2.1,0,0.2)` (side runs rotated 90°); corner piers `(±2.1,±2.1,0.2)` join the ends. Door sits at `(0,-2.1,0.2)`, window at `(0,2.1,1.1)`, ceiling at `(0,0,3.2)`.

Doors include fixed leaf and frame assemblies plus two separate leaf assets for engine-side hinge setup. They are static props, not pre-rigged interactive doors. Window glass follows the collection's opaque stylized material. Openings are actual geometric gaps, not painted rectangles.
