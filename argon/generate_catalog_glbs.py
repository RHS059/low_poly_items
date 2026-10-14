#!/usr/bin/env python3
"""
Procedural 3D GLB Catalog Generator (Blender `bpy` + Standalone Headless Python)
================================================================================
Generates all 1,050 3D models from ITEM_CATALOG.md (1,000 outdoor props across
batches b01-b20 and 50 modular building pieces in batch b21), adhering strictly
to the size-class vertex ceilings:
  - Large:    <= 10,000 vertices (both Source and GLB vertices)
  - Medium:   <=  5,000 vertices (both Source and GLB vertices)
  - Handheld: <=    999 vertices (strictly below 1,000 vertices)

Key Features:
  - Dual-runtime support:
      1. Blender (`blender --background --python generate_catalog_glbs.py`)
         Creates shared `bpy.data.materials` (Principled BSDF) and builds native
         Blender meshes (`bpy.data.meshes`) with flat shading and ground-plane
         origins, exporting `.glb` files.
      2. Standalone Python (`python3 generate_catalog_glbs.py`)
         Uses `numpy` and binary glTF 2.0 packing to emit spec-compliant `.glb`
         files with `+Y` up, `-Z` forward, ground-plane pivot at `Y = 0`, flat
         face normals, and the shared PBR material palette.
  - Shared PBR Material Library:
      Consistent material definitions reused across the entire 1,050-item catalog
      (e.g., `mat_wood_timber` is identical across all wooden benches, tables,
      and structures).
  - Recognizable Category & Item-Specific Procedural Assemblies:
      Constructs multi-part 3D silhouettes (wheels, chassis, cabs, windows, slats,
      frames, trunks, foliage canopies, posts, pickets, mullions, handles, etc.)
      calibrated to each item's target triangle/vertex budget and bounding box.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import struct
import sys
import time
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    import bpy  # type: ignore
    import bmesh  # type: ignore
    HAS_BPY = True
except ImportError:
    bpy = None
    bmesh = None
    HAS_BPY = False


# =============================================================================
# 1. SHARED PBR MATERIAL PALETTE (Reused identically across all 1,050 items)
# =============================================================================

SHARED_MATERIALS: Dict[str, Dict[str, Any]] = {
    "mat_wood_timber": {
        "name": "mat_wood_timber",
        "baseColorFactor": [0.55, 0.36, 0.20, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.78,
    },
    "mat_wood_cedar": {
        "name": "mat_wood_cedar",
        "baseColorFactor": [0.64, 0.33, 0.19, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.74,
    },
    "mat_wood_dark": {
        "name": "mat_wood_dark",
        "baseColorFactor": [0.34, 0.22, 0.14, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.86,
    },
    "mat_metal_steel": {
        "name": "mat_metal_steel",
        "baseColorFactor": [0.67, 0.70, 0.73, 1.0],
        "metallicFactor": 0.85,
        "roughnessFactor": 0.35,
    },
    "mat_metal_cast_iron": {
        "name": "mat_metal_cast_iron",
        "baseColorFactor": [0.19, 0.20, 0.22, 1.0],
        "metallicFactor": 0.80,
        "roughnessFactor": 0.54,
    },
    "mat_metal_aluminum": {
        "name": "mat_metal_aluminum",
        "baseColorFactor": [0.83, 0.85, 0.88, 1.0],
        "metallicFactor": 0.90,
        "roughnessFactor": 0.24,
    },
    "mat_metal_brass": {
        "name": "mat_metal_brass",
        "baseColorFactor": [0.79, 0.59, 0.24, 1.0],
        "metallicFactor": 0.88,
        "roughnessFactor": 0.30,
    },
    "mat_concrete": {
        "name": "mat_concrete",
        "baseColorFactor": [0.66, 0.65, 0.62, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.88,
    },
    "mat_stone_granite": {
        "name": "mat_stone_granite",
        "baseColorFactor": [0.53, 0.52, 0.49, 1.0],
        "metallicFactor": 0.04,
        "roughnessFactor": 0.82,
    },
    "mat_brick_masonry": {
        "name": "mat_brick_masonry",
        "baseColorFactor": [0.63, 0.28, 0.20, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.85,
    },
    "mat_asphalt": {
        "name": "mat_asphalt",
        "baseColorFactor": [0.22, 0.22, 0.24, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.92,
    },
    "mat_rubber_dark": {
        "name": "mat_rubber_dark",
        "baseColorFactor": [0.14, 0.14, 0.15, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.88,
    },
    "mat_glass_clear": {
        "name": "mat_glass_clear",
        "baseColorFactor": [0.68, 0.84, 0.94, 0.48],
        "metallicFactor": 0.10,
        "roughnessFactor": 0.12,
        "alphaMode": "BLEND",
    },
    "mat_foliage_green": {
        "name": "mat_foliage_green",
        "baseColorFactor": [0.24, 0.52, 0.22, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.80,
    },
    "mat_foliage_evergreen": {
        "name": "mat_foliage_evergreen",
        "baseColorFactor": [0.15, 0.36, 0.20, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.82,
    },
    "mat_foliage_accent": {
        "name": "mat_foliage_accent",
        "baseColorFactor": [0.84, 0.38, 0.54, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.74,
    },
    "mat_soil_earth": {
        "name": "mat_soil_earth",
        "baseColorFactor": [0.36, 0.26, 0.18, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.94,
    },
    "mat_paint_yellow": {
        "name": "mat_paint_yellow",
        "baseColorFactor": [0.92, 0.72, 0.10, 1.0],
        "metallicFactor": 0.18,
        "roughnessFactor": 0.42,
    },
    "mat_paint_orange": {
        "name": "mat_paint_orange",
        "baseColorFactor": [0.92, 0.38, 0.08, 1.0],
        "metallicFactor": 0.14,
        "roughnessFactor": 0.45,
    },
    "mat_paint_red": {
        "name": "mat_paint_red",
        "baseColorFactor": [0.80, 0.14, 0.14, 1.0],
        "metallicFactor": 0.22,
        "roughnessFactor": 0.38,
    },
    "mat_paint_blue": {
        "name": "mat_paint_blue",
        "baseColorFactor": [0.15, 0.39, 0.76, 1.0],
        "metallicFactor": 0.20,
        "roughnessFactor": 0.42,
    },
    "mat_paint_green": {
        "name": "mat_paint_green",
        "baseColorFactor": [0.15, 0.46, 0.26, 1.0],
        "metallicFactor": 0.18,
        "roughnessFactor": 0.44,
    },
    "mat_paint_white": {
        "name": "mat_paint_white",
        "baseColorFactor": [0.92, 0.92, 0.90, 1.0],
        "metallicFactor": 0.08,
        "roughnessFactor": 0.40,
    },
    "mat_paint_charcoal": {
        "name": "mat_paint_charcoal",
        "baseColorFactor": [0.24, 0.26, 0.29, 1.0],
        "metallicFactor": 0.38,
        "roughnessFactor": 0.48,
    },
    "mat_fabric_canvas": {
        "name": "mat_fabric_canvas",
        "baseColorFactor": [0.83, 0.77, 0.65, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.84,
    },
    "mat_paper_cardboard": {
        "name": "mat_paper_cardboard",
        "baseColorFactor": [0.74, 0.60, 0.42, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.86,
    },
    "mat_emissive_warm": {
        "name": "mat_emissive_warm",
        "baseColorFactor": [1.0, 0.95, 0.80, 1.0],
        "metallicFactor": 0.0,
        "roughnessFactor": 0.20,
        "emissiveFactor": [0.95, 0.85, 0.55],
    },
}


# =============================================================================
# 2. PRECOMPUTED UNIT PRIMITIVE TEMPLATES (Fast Vectorized Mesh Building)
# =============================================================================

class PrimitiveTemplate:
    """Stores a unit primitive centered at (0,0,0) in [-0.5, 0.5]^3."""
    def __init__(self, src_verts: np.ndarray, quads: List[List[int]], tris: List[List[int]]):
        self.src_verts = src_verts.astype(np.float32)
        self.quads = quads
        self.tris = tris
        self.sv_count = len(src_verts)
        self.gv_count = len(quads) * 4 + len(tris) * 3
        self.tr_count = len(quads) * 2 + len(tris)

        # Precompute flat-expanded GLB vertex indices into src_verts and local triangle indices
        flat_src_idx: List[int] = []
        tri_indices: List[int] = []
        face_v0: List[int] = []
        face_v1: List[int] = []
        face_v2: List[int] = []
        face_repeats: List[int] = []

        cursor = 0
        for q in quads:
            flat_src_idx.extend(q)
            tri_indices.extend([cursor, cursor + 1, cursor + 2, cursor, cursor + 2, cursor + 3])
            face_v0.append(q[0])
            face_v1.append(q[1])
            face_v2.append(q[2])
            face_repeats.append(4)
            cursor += 4
        for t in tris:
            flat_src_idx.extend(t)
            tri_indices.extend([cursor, cursor + 1, cursor + 2])
            face_v0.append(t[0])
            face_v1.append(t[1])
            face_v2.append(t[2])
            face_repeats.append(3)
            cursor += 3

        self.flat_src_idx = np.array(flat_src_idx, dtype=np.int32)
        self.tri_indices = np.array(tri_indices, dtype=np.uint16)
        self.face_v0 = np.array(face_v0, dtype=np.int32)
        self.face_v1 = np.array(face_v1, dtype=np.int32)
        self.face_v2 = np.array(face_v2, dtype=np.int32)
        self.face_repeats = np.array(face_repeats, dtype=np.int32)


def _build_unit_plain_box() -> PrimitiveTemplate:
    verts = np.array([
        [-0.5, -0.5, -0.5],
        [-0.5, -0.5,  0.5],
        [-0.5,  0.5, -0.5],
        [-0.5,  0.5,  0.5],
        [ 0.5, -0.5, -0.5],
        [ 0.5, -0.5,  0.5],
        [ 0.5,  0.5, -0.5],
        [ 0.5,  0.5,  0.5],
    ], dtype=np.float32)
    quads = [
        [0, 1, 3, 2],  # -X
        [4, 6, 7, 5],  # +X
        [0, 4, 5, 1],  # -Y
        [2, 3, 7, 6],  # +Y
        [0, 2, 6, 4],  # -Z
        [1, 5, 7, 3],  # +Z
    ]
    return PrimitiveTemplate(verts, quads, [])


def _build_unit_beveled_box(b: float = 0.07) -> PrimitiveTemplate:
    verts = []
    idx_map = {}
    for ix in (0, 1):
        sx = -1.0 if ix == 0 else 1.0
        for iy in (0, 1):
            sy = -1.0 if iy == 0 else 1.0
            for iz in (0, 1):
                sz = -1.0 if iz == 0 else 1.0
                idx_map[(ix, iy, iz, 0)] = len(verts)
                verts.append([sx * 0.5, sy * (0.5 - b), sz * (0.5 - b)])
                idx_map[(ix, iy, iz, 1)] = len(verts)
                verts.append([sx * (0.5 - b), sy * 0.5, sz * (0.5 - b)])
                idx_map[(ix, iy, iz, 2)] = len(verts)
                verts.append([sx * (0.5 - b), sy * (0.5 - b), sz * 0.5])
    verts_arr = np.array(verts, dtype=np.float32)
    quads = [
        [idx_map[(0, 0, 0, 0)], idx_map[(0, 0, 1, 0)], idx_map[(0, 1, 1, 0)], idx_map[(0, 1, 0, 0)]],
        [idx_map[(1, 0, 0, 0)], idx_map[(1, 1, 0, 0)], idx_map[(1, 1, 1, 0)], idx_map[(1, 0, 1, 0)]],
        [idx_map[(0, 0, 0, 1)], idx_map[(1, 0, 0, 1)], idx_map[(1, 0, 1, 1)], idx_map[(0, 0, 1, 1)]],
        [idx_map[(0, 1, 0, 1)], idx_map[(0, 1, 1, 1)], idx_map[(1, 1, 1, 1)], idx_map[(1, 1, 0, 1)]],
        [idx_map[(0, 0, 0, 2)], idx_map[(0, 1, 0, 2)], idx_map[(1, 1, 0, 2)], idx_map[(1, 0, 0, 2)]],
        [idx_map[(0, 0, 1, 2)], idx_map[(1, 0, 1, 2)], idx_map[(1, 1, 1, 2)], idx_map[(0, 1, 1, 2)]],
    ]
    for iy in (0, 1):
        for iz in (0, 1):
            if (iy == 0 and iz == 0) or (iy == 1 and iz == 1):
                quads.append([idx_map[(0, iy, iz, 1)], idx_map[(0, iy, iz, 2)], idx_map[(1, iy, iz, 2)], idx_map[(1, iy, iz, 1)]])
            else:
                quads.append([idx_map[(0, iy, iz, 2)], idx_map[(0, iy, iz, 1)], idx_map[(1, iy, iz, 1)], idx_map[(1, iy, iz, 2)]])
    for ix in (0, 1):
        for iz in (0, 1):
            if (ix == 0 and iz == 1) or (ix == 1 and iz == 0):
                quads.append([idx_map[(ix, 0, iz, 0)], idx_map[(ix, 0, iz, 2)], idx_map[(ix, 1, iz, 2)], idx_map[(ix, 1, iz, 0)]])
            else:
                quads.append([idx_map[(ix, 0, iz, 2)], idx_map[(ix, 0, iz, 0)], idx_map[(ix, 1, iz, 0)], idx_map[(ix, 1, iz, 2)]])
    for ix in (0, 1):
        for iy in (0, 1):
            if (ix == 0 and iy == 0) or (ix == 1 and iy == 1):
                quads.append([idx_map[(ix, iy, 0, 0)], idx_map[(ix, iy, 0, 1)], idx_map[(ix, iy, 1, 1)], idx_map[(ix, iy, 1, 0)]])
            else:
                quads.append([idx_map[(ix, iy, 0, 1)], idx_map[(ix, iy, 0, 0)], idx_map[(ix, iy, 1, 0)], idx_map[(ix, iy, 1, 1)]])
    tris = []
    for ix in (0, 1):
        for iy in (0, 1):
            for iz in (0, 1):
                if (ix + iy + iz) % 2 == 1:
                    tris.append([idx_map[(ix, iy, iz, 0)], idx_map[(ix, iy, iz, 1)], idx_map[(ix, iy, iz, 2)]])
                else:
                    tris.append([idx_map[(ix, iy, iz, 0)], idx_map[(ix, iy, iz, 2)], idx_map[(ix, iy, iz, 1)]])
    return PrimitiveTemplate(verts_arr, quads, tris)


def _build_unit_gable() -> PrimitiveTemplate:
    """Triangular roof prism (ridge along Y, sloped along +/-X, base at -0.5 Z, peak at +0.5 Z)."""
    verts = np.array([
        [-0.5, -0.5, -0.5],
        [ 0.5, -0.5, -0.5],
        [ 0.0, -0.5,  0.5],
        [-0.5,  0.5, -0.5],
        [ 0.5,  0.5, -0.5],
        [ 0.0,  0.5,  0.5],
    ], dtype=np.float32)
    quads = [
        [0, 3, 4, 1],  # bottom (-Z)
        [0, 2, 5, 3],  # left slope (-X/+Z)
        [1, 4, 5, 2],  # right slope (+X/+Z)
    ]
    tris = [
        [0, 1, 2],     # front gable (-Y)
        [3, 5, 4],     # back gable (+Y)
    ]
    return PrimitiveTemplate(verts, quads, tris)


_CYLINDER_CACHE: Dict[Tuple[int, int, float, float, str], PrimitiveTemplate] = {}


def get_unit_cylinder(
    segments: int = 8,
    rings: int = 1,
    r_bot: float = 0.5,
    r_top: float = 0.5,
    axis: str = "Z",
) -> PrimitiveTemplate:
    key = (segments, rings, round(r_bot, 3), round(r_top, 3), axis)
    if key in _CYLINDER_CACHE:
        return _CYLINDER_CACHE[key]

    verts = []
    for ir in range(rings + 1):
        t = ir / rings
        z = -0.5 + t
        r = r_bot * (1.0 - t) + r_top * t
        if rings >= 3 and 0 < ir < rings:
            # subtle barrel/profile modulation when multi-ring
            r *= 1.0 + 0.04 * math.sin(t * math.pi)
        for iseg in range(segments):
            ang = 2.0 * math.pi * iseg / segments
            x = r * math.cos(ang)
            y = r * math.sin(ang)
            if axis == "Z":
                verts.append([x, y, z])
            elif axis == "X":
                verts.append([z, x, y])
            else:  # Y
                verts.append([x, z, y])

    verts_arr = np.array(verts, dtype=np.float32)
    quads = []
    for ir in range(rings):
        base0 = ir * segments
        base1 = (ir + 1) * segments
        for iseg in range(segments):
            nxt = (iseg + 1) % segments
            if axis in ("Z", "X"):
                quads.append([base0 + iseg, base0 + nxt, base1 + nxt, base1 + iseg])
            else:
                quads.append([base0 + iseg, base1 + iseg, base1 + nxt, base0 + nxt])

    tris = []
    # Bottom cap (ir = 0) and Top cap (ir = rings)
    top_base = rings * segments
    for i in range(1, segments - 1):
        if axis in ("Z", "X"):
            tris.append([0, i + 1, i])
            tris.append([top_base, top_base + i, top_base + i + 1])
        else:
            tris.append([0, i, i + 1])
            tris.append([top_base, top_base + i + 1, top_base + i])

    tmpl = PrimitiveTemplate(verts_arr, quads, tris)
    _CYLINDER_CACHE[key] = tmpl
    return tmpl


_FOLIAGE_CACHE: Dict[Tuple[int, int, int], PrimitiveTemplate] = {}


def get_unit_foliage_blob(u_seg: int = 8, v_seg: int = 4, variant: int = 0) -> PrimitiveTemplate:
    key = (u_seg, v_seg, variant)
    if key in _FOLIAGE_CACHE:
        return _FOLIAGE_CACHE[key]

    rng = np.random.RandomState(1000 + variant * 37 + u_seg * 7 + v_seg)
    verts = [[0.0, 0.0, -0.5]]  # south pole (index 0)
    for iv in range(1, v_seg):
        phi = math.pi * iv / v_seg - 0.5 * math.pi
        z = 0.5 * math.sin(phi)
        r_ring = 0.5 * math.cos(phi)
        for iu in range(u_seg):
            theta = 2.0 * math.pi * iu / u_seg
            jitter = 0.88 + 0.22 * rng.rand()
            verts.append([
                r_ring * math.cos(theta) * jitter,
                r_ring * math.sin(theta) * jitter,
                z * (0.92 + 0.16 * rng.rand()),
            ])
    verts.append([0.0, 0.0, 0.5])  # north pole (index len-1)
    north_idx = len(verts) - 1

    verts_arr = np.array(verts, dtype=np.float32)
    # Normalize into [-0.5, 0.5]^3
    vmin = verts_arr.min(axis=0)
    vmax = verts_arr.max(axis=0)
    span = np.maximum(vmax - vmin, 1e-5)
    verts_arr = (verts_arr - 0.5 * (vmin + vmax)) / span

    quads = []
    for iv in range(v_seg - 2):
        b0 = 1 + iv * u_seg
        b1 = 1 + (iv + 1) * u_seg
        for iu in range(u_seg):
            nxt = (iu + 1) % u_seg
            quads.append([b0 + iu, b0 + nxt, b1 + nxt, b1 + iu])

    tris = []
    top_ring = 1 + (v_seg - 2) * u_seg
    for iu in range(u_seg):
        nxt = (iu + 1) % u_seg
        tris.append([0, 1 + nxt, 1 + iu])
        tris.append([north_idx, top_ring + iu, top_ring + nxt])

    tmpl = PrimitiveTemplate(verts_arr, quads, tris)
    _FOLIAGE_CACHE[key] = tmpl
    return tmpl


UNIT_PLAIN_BOX = _build_unit_plain_box()
UNIT_BEVELED_BOX = _build_unit_beveled_box(0.07)
UNIT_GABLE = _build_unit_gable()


# =============================================================================
# 3. MESH BUILDER (Accumulates Parts, Calibrates Budget, Exports GLB & BPY)
# =============================================================================

class MeshPart:
    __slots__ = ("template", "cx", "cy", "cz", "sx", "sy", "sz", "mat", "essential", "rot_z")

    def __init__(
        self,
        template: PrimitiveTemplate,
        cx: float,
        cy: float,
        cz: float,
        sx: float,
        sy: float,
        sz: float,
        mat: str,
        essential: bool = True,
        rot_z: float = 0.0,
    ):
        self.template = template
        self.cx = float(cx)
        self.cy = float(cy)
        self.cz = float(cz)
        self.sx = max(float(sx), 0.002)
        self.sy = max(float(sy), 0.002)
        self.sz = max(float(sz), 0.002)
        self.mat = mat if mat in SHARED_MATERIALS else "mat_metal_steel"
        self.essential = essential
        self.rot_z = float(rot_z)


class MeshBuilder:
    """Builds a multi-material 3D assembly in Blender Z-up coordinates."""

    def __init__(self, item_id: str, dims: List[float], vertex_limit: int, target_tris: int, target_gv: int):
        self.item_id = item_id
        self.dx = max(float(dims[0]), 0.01)
        self.dy = max(float(dims[1]), 0.01)
        self.dz = max(float(dims[2]), 0.01)
        self.vertex_limit = int(vertex_limit)
        self.target_tris = int(target_tris)
        self.target_gv = min(int(target_gv), self.vertex_limit)
        self.parts: List[MeshPart] = []

        # Deterministic per-item seed
        h = int(hashlib.md5(item_id.encode("utf-8")).hexdigest()[:8], 16)
        self.rng = np.random.RandomState(h)

    @property
    def sv_count(self) -> int:
        return sum(p.template.sv_count for p in self.parts)

    @property
    def gv_count(self) -> int:
        return sum(p.template.gv_count for p in self.parts)

    @property
    def tr_count(self) -> int:
        return sum(p.template.tr_count for p in self.parts)

    def add_box(
        self,
        cx: float,
        cy: float,
        cz: float,
        sx: float,
        sy: float,
        sz: float,
        mat: str,
        beveled: bool = True,
        essential: bool = True,
        rot_z: float = 0.0,
    ) -> None:
        tmpl = UNIT_BEVELED_BOX if beveled else UNIT_PLAIN_BOX
        self.parts.append(MeshPart(tmpl, cx, cy, cz, sx, sy, sz, mat, essential=essential, rot_z=rot_z))

    def add_gable(
        self,
        cx: float,
        cy: float,
        cz: float,
        sx: float,
        sy: float,
        sz: float,
        mat: str,
        essential: bool = True,
        rot_z: float = 0.0,
    ) -> None:
        self.parts.append(MeshPart(UNIT_GABLE, cx, cy, cz, sx, sy, sz, mat, essential=essential, rot_z=rot_z))

    def add_cyl(
        self,
        cx: float,
        cy: float,
        cz: float,
        sx: float,
        sy: float,
        sz: float,
        mat: str,
        segments: int = 8,
        rings: int = 1,
        r_bot: float = 0.5,
        r_top: float = 0.5,
        axis: str = "Z",
        essential: bool = True,
        rot_z: float = 0.0,
    ) -> None:
        tmpl = get_unit_cylinder(segments=segments, rings=rings, r_bot=r_bot, r_top=r_top, axis=axis)
        self.parts.append(MeshPart(tmpl, cx, cy, cz, sx, sy, sz, mat, essential=essential, rot_z=rot_z))

    def add_wheel(
        self,
        cx: float,
        cy: float,
        cz: float,
        radius: float,
        width: float,
        segments: int = 10,
        axis: str = "X",
        essential: bool = True,
    ) -> None:
        d = radius * 2.0
        if axis == "X":
            self.add_cyl(cx, cy, cz, width, d, d, "mat_rubber_dark", segments=segments, rings=1, axis="X", essential=essential)
            self.add_cyl(cx, cy, cz, width * 1.06, d * 0.58, d * 0.58, "mat_metal_aluminum", segments=max(6, segments - 2), rings=1, axis="X", essential=False)
        else:
            self.add_cyl(cx, cy, cz, d, width, d, "mat_rubber_dark", segments=segments, rings=1, axis="Y", essential=essential)
            self.add_cyl(cx, cy, cz, d * 0.58, width * 1.06, d * 0.58, "mat_metal_aluminum", segments=max(6, segments - 2), rings=1, axis="Y", essential=False)

    def add_foliage(
        self,
        cx: float,
        cy: float,
        cz: float,
        sx: float,
        sy: float,
        sz: float,
        mat: str = "mat_foliage_green",
        u_seg: int = 8,
        v_seg: int = 4,
        variant: int = 0,
        essential: bool = True,
    ) -> None:
        tmpl = get_unit_foliage_blob(u_seg=u_seg, v_seg=v_seg, variant=variant)
        self.parts.append(MeshPart(tmpl, cx, cy, cz, sx, sy, sz, mat, essential=essential))

    def calibrate_budget(self, detail_mat: str = "mat_metal_steel") -> None:
        """
        Ensures strict compliance with `vertex_limit` (both Source and GLB vertices)
        and calibrates the assembly's structural detail count so that `tr_count`
        is close to `target_tris` (well within +/- 1000 tris) and `gv_count <= vertex_limit`.
        """
        hard_gv_cap = self.vertex_limit
        # 1. If over budget, first downgrade non-essential beveled boxes to plain boxes
        if self.gv_count > hard_gv_cap or self.sv_count > hard_gv_cap or self.tr_count > self.target_tris + 300:
            for p in reversed(self.parts):
                if self.gv_count <= hard_gv_cap and self.sv_count <= hard_gv_cap and self.tr_count <= self.target_tris + 200:
                    break
                if p.template is UNIT_BEVELED_BOX and not p.essential:
                    p.template = UNIT_PLAIN_BOX

        # 2. If still over budget, downgrade essential beveled boxes to plain boxes
        if self.gv_count > hard_gv_cap or self.sv_count > hard_gv_cap or self.tr_count > self.target_tris + 300:
            for p in reversed(self.parts):
                if self.gv_count <= hard_gv_cap and self.sv_count <= hard_gv_cap and self.tr_count <= self.target_tris + 200:
                    break
                if p.template is UNIT_BEVELED_BOX:
                    p.template = UNIT_PLAIN_BOX

        # 3. If still over budget, pop non-essential parts, then trailing parts (keeping at least 2 parts)
        while (self.gv_count > hard_gv_cap or self.sv_count > hard_gv_cap) and len(self.parts) > 2:
            removed = False
            for idx in range(len(self.parts) - 1, -1, -1):
                if not self.parts[idx].essential:
                    self.parts.pop(idx)
                    removed = True
                    break
            if not removed:
                self.parts.pop()

        # 4. If still over vertex_limit (e.g. a very high-segment cylinder on a Handheld item), replace high-gv templates
        if self.gv_count > hard_gv_cap or self.sv_count > hard_gv_cap:
            for p in reversed(self.parts):
                if self.gv_count <= hard_gv_cap and self.sv_count <= hard_gv_cap:
                    break
                if p.template.gv_count > 24:
                    p.template = UNIT_PLAIN_BOX

        # 5. If under target_tris, add integrated structural trim/rib/bracket details inside the object envelope
        # while strictly respecting hard_gv_cap!
        # Determine existing materials on this item so detail parts use the item's own shared materials
        used_mats = [p.mat for p in self.parts] if self.parts else [detail_mat]
        primary_mat = used_mats[0]
        secondary_mat = used_mats[-1] if len(used_mats) > 1 else detail_mat

        # Target GLB cap leaves a safe buffer below vertex_limit
        safe_gv_target = min(hard_gv_cap, max(self.target_gv, min(hard_gv_cap, int(self.target_tris * 2.15))))

        step_idx = 0
        while self.tr_count + 44 <= self.target_tris and self.gv_count + 96 <= safe_gv_target and self.sv_count + 24 <= hard_gv_cap:
            # Place integrated structural ribs/brackets/slats along existing parts
            ref_p = self.parts[step_idx % len(self.parts)]
            frac = ((step_idx // max(1, len(self.parts))) % 7 - 3) / 4.0
            ox = ref_p.cx + frac * ref_p.sx * 0.36
            oy = ref_p.cy + ((step_idx % 5) - 2) * 0.15 * ref_p.sy
            oz = max(0.02 * self.dz, ref_p.cz + ((step_idx % 3) - 1) * 0.22 * ref_p.sz)
            rx = max(0.008, ref_p.sx * 0.22)
            ry = max(0.008, ref_p.sy * 0.22)
            rz = max(0.008, ref_p.sz * 0.18)
            mat_choice = primary_mat if (step_idx % 2 == 0) else secondary_mat
            self.add_box(ox, oy, oz, rx, ry, rz, mat_choice, beveled=True, essential=False)
            step_idx += 1

        while self.tr_count + 12 <= self.target_tris and self.gv_count + 24 <= safe_gv_target and self.sv_count + 8 <= hard_gv_cap:
            ref_p = self.parts[step_idx % len(self.parts)]
            frac = ((step_idx % 7) - 3) / 4.0
            ox = ref_p.cx + frac * ref_p.sx * 0.35
            oy = ref_p.cy
            oz = max(0.02 * self.dz, ref_p.cz)
            rx = max(0.006, ref_p.sx * 0.18)
            ry = max(0.006, ref_p.sy * 0.18)
            rz = max(0.006, ref_p.sz * 0.15)
            mat_choice = secondary_mat if (step_idx % 2 == 0) else primary_mat
            self.add_box(ox, oy, oz, rx, ry, rz, mat_choice, beveled=False, essential=False)
            step_idx += 1

    def compile_geometry(self) -> Dict[str, Any]:
        """
        Compiles all parts into exact bounding-box-fitted Blender (Z-up) and glTF (Y-up)
        buffers grouped by shared PBR material.
        """
        if not self.parts:
            self.add_box(0.0, 0.0, self.dz * 0.5, self.dx, self.dy, self.dz, "mat_metal_steel", beveled=True)

        # First compute all transformed source vertices in Blender space (X, Y, Z)
        part_src_verts: List[np.ndarray] = []
        for p in self.parts:
            v = p.template.src_verts * np.array([p.sx, p.sy, p.sz], dtype=np.float32)
            if abs(p.rot_z) > 1e-5:
                c, s = math.cos(p.rot_z), math.sin(p.rot_z)
                rot = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]], dtype=np.float32)
                v = v @ rot.T
            v = v + np.array([p.cx, p.cy, p.cz], dtype=np.float32)
            part_src_verts.append(v)

        all_src = np.vstack(part_src_verts)
        bmin = all_src.min(axis=0)
        bmax = all_src.max(axis=0)
        bspan = np.maximum(bmax - bmin, 1e-5)
        target_span = np.array([self.dx, self.dy, self.dz], dtype=np.float32)
        scale_factor = target_span / bspan
        center_xy = 0.5 * (bmin[:2] + bmax[:2])
        min_z = bmin[2]

        # Fit exactly to (dx, dy, dz) with X, Y centered at 0 and Z resting on Z=0
        mat_groups: Dict[str, List[Tuple[np.ndarray, np.ndarray, np.ndarray]]] = {}
        total_sv = 0
        total_gv = 0
        total_tr = 0

        # Also store Blender mesh data if needed by bpy
        bpy_verts_list: List[np.ndarray] = []
        bpy_faces_list: List[Tuple[List[int], str]] = []
        v_offset = 0

        for p, v_raw in zip(self.parts, part_src_verts):
            v = np.empty_like(v_raw)
            v[:, 0] = (v_raw[:, 0] - center_xy[0]) * scale_factor[0]
            v[:, 1] = (v_raw[:, 1] - center_xy[1]) * scale_factor[1]
            v[:, 2] = (v_raw[:, 2] - min_z) * scale_factor[2]

            tmpl = p.template
            total_sv += tmpl.sv_count
            total_gv += tmpl.gv_count
            total_tr += tmpl.tr_count

            if HAS_BPY:
                bpy_verts_list.append(v)
                for q in tmpl.quads:
                    bpy_faces_list.append(([x + v_offset for x in q], p.mat))
                for t in tmpl.tris:
                    bpy_faces_list.append(([x + v_offset for x in t], p.mat))
                v_offset += tmpl.sv_count

            # Transform to glTF 2.0 (+Y up, -Z forward):
            # x_gltf = x_blender, y_gltf = z_blender, z_gltf = -y_blender
            v_gltf = np.empty_like(v)
            v_gltf[:, 0] = v[:, 0]
            v_gltf[:, 1] = v[:, 2]
            v_gltf[:, 2] = -v[:, 1]

            # Flat-shaded GLB positions
            pos_flat = v_gltf[tmpl.flat_src_idx]

            # Compute exact per-face outward normals in glTF space
            p0 = v_gltf[tmpl.face_v0]
            p1 = v_gltf[tmpl.face_v1]
            p2 = v_gltf[tmpl.face_v2]
            fn = np.cross(p1 - p0, p2 - p0)
            norms = np.linalg.norm(fn, axis=1, keepdims=True)
            fn = fn / np.maximum(norms, 1e-8)
            norm_flat = np.repeat(fn, tmpl.face_repeats, axis=0).astype(np.float32)

            mat_groups.setdefault(p.mat, []).append((pos_flat, norm_flat, tmpl.tri_indices))

        return {
            "item_id": self.item_id,
            "dimensions": [round(self.dx, 4), round(self.dy, 4), round(self.dz, 4)],
            "source_vertices": total_sv,
            "glb_vertices": total_gv,
            "triangles": total_tr,
            "materials": sorted(mat_groups.keys()),
            "mat_groups": mat_groups,
            "bpy_verts": np.vstack(bpy_verts_list) if HAS_BPY and bpy_verts_list else None,
            "bpy_faces": bpy_faces_list if HAS_BPY else None,
        }


# =============================================================================
# 4. CATEGORY & ITEM-SPECIFIC PROCEDURAL 3D ARCHETYPE BUILDERS (b01 - b21)
# =============================================================================

def build_procedural_item(item: Dict[str, Any]) -> Dict[str, Any]:
    item_id = item["id"]
    cat = item["category"]
    dims = item["dimensions"]
    v_limit = item["vertex_limit"]
    t_tris = item["target_triangles"]
    t_gv = item["target_glb_vertices"]

    mb = MeshBuilder(item_id, dims, v_limit, t_tris, t_gv)
    dx, dy, dz = mb.dx, mb.dy, mb.dz
    batch = item_id[:3]
    name = item_id[4:]

    # Choose primary & secondary shared PBR materials intelligently from item name & category
    def pick_mat(default_mat: str = "mat_metal_steel") -> str:
        if any(k in name for k in ("cedar", "redwood", "mahogany")):
            return "mat_wood_cedar"
        if any(k in name for k in ("wood", "timber", "boardwalk", "log", "plank", "oak", "pine", "maple", "birch", "elm", "willow", "sycamore", "poplar", "pallet", "crate")):
            return "mat_wood_timber"
        if any(k in name for k in ("concrete", "cement", "precast", "sidewalk", "curb", "paving", "stoop")):
            return "mat_concrete"
        if any(k in name for k in ("granite", "stone", "limestone", "cobblestone", "obelisk", "sundial", "milestone", "dry_stone", "gabion")):
            return "mat_stone_granite"
        if any(k in name for k in ("brick", "brownstone", "masonry", "terracotta", "chiminea", "chimney")):
            return "mat_brick_masonry"
        if any(k in name for k in ("cast_iron", "wrought_iron", "heritage", "ornamental_iron", "hibachi", "kamado", "kettle", "smoker", "manhole")):
            return "mat_metal_cast_iron"
        if any(k in name for k in ("aluminum", "stainless", "chrome", "silver", "galvanized", "bleacher", "foil", "soda_can")):
            return "mat_metal_aluminum"
        if any(k in name for k in ("brass", "bronze", "bell", "cork", "trumpet")):
            return "mat_metal_brass"
        if any(k in name for k in ("asphalt", "tar", "black_refuse")):
            return "mat_asphalt"
        if any(k in name for k in ("rubber", "tire", "hose", "fender", "bumper", "mat", "delineator")):
            return "mat_rubber_dark"
        if any(k in name for k in ("glass", "glazed", "skylight", "window")):
            return "mat_glass_clear"
        if any(k in name for k in ("canvas", "umbrella", "awning", "marquee", "canopy", "tent", "hammock", "tote", "satchel", "duffel", "blanket")):
            return "mat_fabric_canvas"
        if any(k in name for k in ("cardboard", "paper", "carton", "newspaper", "pizza_box", "baguette", "cookie", "donut", "pretzel", "taco", "sandwich", "waffle")):
            return "mat_paper_cardboard"
        if any(k in name for k in ("fire", "hydrant", "stop_sign", "wrong_way", "do_not_enter", "ketchup", "apple", "cola")):
            return "mat_paint_red"
        if any(k in name for k in ("school_bus", "warning", "caution", "yellow", "banana", "lemonade", "excavator", "bulldozer", "loader", "grader", "backhoe", "crane", "compactor", "roller")):
            return "mat_paint_yellow"
        if any(k in name for k in ("traffic_cone", "barrel", "barricade", "detour", "lifering", "buoy", "scissor_lift", "boom_lift", "cherry_picker")):
            return "mat_paint_orange"
        if any(k in name for k in ("recycling", "accessible", "blue", "mailbox", "postal", "police")):
            return "mat_paint_blue"
        if any(k in name for k in ("park", "green", "dumpster", "transformer", "bike_route", "interstate")):
            return "mat_paint_green"
        if any(k in name for k in ("vinyl", "white", "ambulance", "milk", "ice", "refrigerated")):
            return "mat_paint_white"
        return default_mat

    # -------------------------------------------------------------------------
    # BATCH b08: Trees, Shrubs, and Planted Landscaping
    # -------------------------------------------------------------------------
    if batch == "b08":
        if cat == "Tree":
            is_conifer = any(k in name for k in ("spruce", "pine", "cedar", "arborvitae", "cypress"))
            is_flowering = any(k in name for k in ("cherry", "dogwood", "redbud", "crape_myrtle", "magnolia"))
            leaf_mat = "mat_foliage_evergreen" if is_conifer else ("mat_foliage_accent" if is_flowering else "mat_foliage_green")
            is_pair = "pair" in name or "clump" in name

            trunk_count = 2 if is_pair else (3 if "clump" in name else 1)
            for it in range(trunk_count):
                tx = (it - 0.5 * (trunk_count - 1)) * dx * 0.28
                ty = ((it % 2) - 0.5) * dy * 0.12 if trunk_count > 1 else 0.0
                # Trunk + flared root base
                mb.add_cyl(tx, ty, dz * 0.22, dx * 0.10, dy * 0.10, dz * 0.44, "mat_wood_dark", segments=8, rings=2, r_bot=0.6, r_top=0.32)
                # Primary branches
                for ib in range(3):
                    ang = 2.0 * math.pi * ib / 3.0 + it
                    bx = tx + math.cos(ang) * dx * 0.12
                    by = ty + math.sin(ang) * dy * 0.12
                    mb.add_box(bx, by, dz * 0.42, dx * 0.08, dy * 0.08, dz * 0.22, "mat_wood_dark", beveled=True, rot_z=ang)

            if "staked" in name:
                for sx_sign in (-1.0, 1.0):
                    mb.add_cyl(sx_sign * dx * 0.22, 0.0, dz * 0.22, dx * 0.04, dy * 0.04, dz * 0.44, "mat_wood_timber", segments=6)
                    mb.add_box(sx_sign * dx * 0.11, 0.0, dz * 0.34, dx * 0.22, dy * 0.03, dz * 0.03, "mat_rubber_dark", beveled=False)

            # Multi-cluster canopy
            n_blobs = max(4, min(18, t_tris // 220))
            for ib in range(n_blobs):
                frac = ib / max(1, n_blobs - 1)
                ang = ib * 2.39996  # golden angle
                rad = (1.0 - 0.55 * frac) * 0.28 if is_conifer else (0.18 + 0.16 * math.sin(frac * math.pi))
                cx = math.cos(ang) * dx * rad
                cy = math.sin(ang) * dy * rad
                cz = dz * (0.36 + 0.52 * frac)
                sx = dx * (0.55 - 0.28 * frac if is_conifer else 0.46 - 0.12 * frac)
                sy = dy * (0.55 - 0.28 * frac if is_conifer else 0.46 - 0.12 * frac)
                sz = dz * (0.26 if is_conifer else 0.30)
                c_mat = "mat_foliage_green" if (is_flowering and ib % 3 == 0) else leaf_mat
                mb.add_foliage(cx, cy, cz, sx, sy, sz, c_mat, u_seg=10, v_seg=5, variant=ib)

        elif cat == "Shrub":
            leaf_mat = "mat_foliage_evergreen" if "yew" in name else "mat_foliage_green"
            # Woody stems along hedge base
            for ix in range(-2, 3):
                mb.add_cyl(ix * dx * 0.18, 0.0, dz * 0.12, dx * 0.05, dy * 0.05, dz * 0.24, "mat_wood_dark", segments=6)
            # Main clipped hedge volume + organic foliage clusters
            mb.add_box(0.0, 0.0, dz * 0.54, dx * 0.92, dy * 0.88, dz * 0.84, leaf_mat, beveled=True)
            n_tufts = max(6, min(24, t_tris // 140))
            for i in range(n_tufts):
                tx = ((i % 6) - 2.5) / 3.0 * dx * 0.82
                ty = (((i // 6) % 2) - 0.5) * dy * 0.45
                tz = dz * (0.35 + 0.52 * ((i % 3) / 2.0))
                t_mat = "mat_foliage_accent" if ("flowering" in name and i % 4 == 0) else leaf_mat
                mb.add_foliage(tx, ty, tz, dx * 0.28, dy * 0.45, dz * 0.32, t_mat, u_seg=8, v_seg=4, variant=i)

        else:  # Planted Landscaping (flower beds, planters, grasses, shrubs)
            has_container = any(k in name for k in ("bed", "planter", "box", "basket", "barrel"))
            if has_container:
                c_mat = "mat_wood_cedar" if ("barrel" in name or "window_box" in name or "raised" in name) else ("mat_stone_granite" if "circular" in name else "mat_concrete")
                if "circular" in name or "barrel" in name or "basket" in name:
                    mb.add_cyl(0.0, 0.0, dz * 0.28, dx * 0.92, dy * 0.92, dz * 0.52, c_mat, segments=12, rings=2, r_bot=0.42, r_top=0.50)
                    mb.add_cyl(0.0, 0.0, dz * 0.48, dx * 0.82, dy * 0.82, dz * 0.08, "mat_soil_earth", segments=12, rings=1)
                else:
                    mb.add_box(0.0, 0.0, dz * 0.26, dx * 0.96, dy * 0.96, dz * 0.50, c_mat, beveled=True)
                    mb.add_box(0.0, 0.0, dz * 0.48, dx * 0.86, dy * 0.86, dz * 0.08, "mat_soil_earth", beveled=True)
            else:
                mb.add_cyl(0.0, 0.0, dz * 0.05, dx * 0.55, dy * 0.55, dz * 0.10, "mat_soil_earth", segments=8)

            # Foliage & flower clusters
            is_yellow_flower = any(k in name for k in ("susan", "daffodil", "forsythia", "daylily"))
            is_blue_flower = any(k in name for k in ("iris", "lavender", "salvia", "hydrangea"))
            flower_mat = "mat_paint_yellow" if is_yellow_flower else ("mat_paint_blue" if is_blue_flower else "mat_foliage_accent")
            n_clumps = max(5, min(22, t_tris // 110))
            for i in range(n_clumps):
                ang = i * 2.39996
                rad = 0.32 * math.sqrt((i + 0.5) / n_clumps)
                cx = math.cos(ang) * dx * rad
                cy = math.sin(ang) * dy * rad
                cz = dz * (0.45 + 0.38 * ((i % 4) / 3.0))
                if "grass" in name or "cattail" in name or "dogwood_winter" in name:
                    stem_mat = "mat_paint_red" if "redtwig" in name else "mat_foliage_green"
                    mb.add_box(cx, cy, dz * 0.48, dx * 0.08, dy * 0.08, dz * 0.78, stem_mat, beveled=True, rot_z=ang)
                else:
                    m = flower_mat if (i % 2 == 1) else "mat_foliage_green"
                    mb.add_foliage(cx, cy, cz, dx * 0.34, dy * 0.34, dz * 0.34, m, u_seg=8, v_seg=4, variant=i)

    # -------------------------------------------------------------------------
    # BATCH b03 & b15: Passenger, Municipal, Commercial & Emergency Vehicles
    # -------------------------------------------------------------------------
    elif batch in ("b03", "b15"):
        is_two_wheeler = any(k in name for k in ("bicycle", "scooter", "motorcycle", "tricycle"))
        if is_two_wheeler:
            is_trike = "tricycle" in name
            w_rad = min(dx * 0.18, dz * 0.34)
            w_thick = max(dy * 0.14, 0.05)
            # Front & Rear wheels (along X length or Y length depending on catalog orientation)
            long_x = dx >= dy
            L = dx if long_x else dy
            W = dy if long_x else dx
            w_axis = "Y" if long_x else "X"

            def place_veh(lx: float, ly: float, lz: float, sx: float, sy: float, sz: float, mat: str, bev: bool = True) -> None:
                if long_x:
                    mb.add_box(lx, ly, lz, sx, sy, sz, mat, beveled=bev)
                else:
                    mb.add_box(ly, lx, lz, sy, sx, sz, mat, beveled=bev)

            # Front wheel
            if long_x:
                mb.add_wheel(L * 0.34, 0.0, w_rad, w_rad, w_thick, segments=12, axis="Y")
                if is_trike:
                    mb.add_wheel(-L * 0.34, -W * 0.36, w_rad, w_rad, w_thick, segments=12, axis="Y")
                    mb.add_wheel(-L * 0.34,  W * 0.36, w_rad, w_rad, w_thick, segments=12, axis="Y")
                else:
                    mb.add_wheel(-L * 0.34, 0.0, w_rad, w_rad, w_thick, segments=12, axis="Y")
            else:
                mb.add_wheel(0.0, L * 0.34, w_rad, w_rad, w_thick, segments=12, axis="X")
                if is_trike:
                    mb.add_wheel(-W * 0.36, -L * 0.34, w_rad, w_rad, w_thick, segments=12, axis="X")
                    mb.add_wheel( W * 0.36, -L * 0.34, w_rad, w_rad, w_thick, segments=12, axis="X")
                else:
                    mb.add_wheel(0.0, -L * 0.34, w_rad, w_rad, w_thick, segments=12, axis="X")

            frame_mat = pick_mat("mat_paint_blue" if "bicycle" in name else "mat_paint_red")
            # Frame tubes, fork, handlebars, seat
            place_veh(0.0, 0.0, dz * 0.45, L * 0.56, W * 0.14, dz * 0.14, frame_mat)
            place_veh(L * 0.28, 0.0, dz * 0.62, L * 0.10, W * 0.12, dz * 0.68, "mat_metal_steel")
            place_veh(L * 0.28, 0.0, dz * 0.92, L * 0.10, W * 0.88, dz * 0.08, "mat_rubber_dark")
            place_veh(-L * 0.12, 0.0, dz * 0.72, L * 0.22, W * 0.28, dz * 0.10, "mat_rubber_dark")
            if "cargo" in name or "basket" in name or "touring" in name:
                place_veh(-L * 0.28, 0.0, dz * 0.58, L * 0.32, W * 0.62, dz * 0.32, "mat_wood_timber" if "box" in name else "mat_metal_steel")
        else:
            # 4+ wheeled vehicle (car, SUV, pickup, van, bus, fire truck, commercial truck)
            long_x = dx >= dy
            L = dx if long_x else dy
            W = dy if long_x else dx
            body_mat = pick_mat("mat_paint_blue" if batch == "b03" else "mat_paint_white")
            if "fire" in name or "crash_tender" in name or "rescue" in name:
                body_mat = "mat_paint_red"
            elif "school_bus" in name or "snowplow" in name or "street_marking" in name:
                body_mat = "mat_paint_yellow"
            elif "refuse" in name or "recycling" in name or "tree_service" in name:
                body_mat = "mat_paint_green"

            def add_vpart(lx: float, ly: float, lz: float, sx: float, sy: float, sz: float, mat: str, bev: bool = True) -> None:
                if long_x:
                    mb.add_box(lx, ly, lz, sx, sy, sz, mat, beveled=bev)
                else:
                    mb.add_box(ly, lx, lz, sy, sx, sz, mat, beveled=bev)

            w_rad = min(dz * 0.20, L * 0.09, 0.52)
            w_width = W * 0.16
            axles = [-L * 0.33, L * 0.33]
            if L > 8.5:
                axles = [-L * 0.36, -L * 0.20, L * 0.34]
            if "articulated_transit_bus" in name or "tiller_ladder" in name:
                axles = [-L * 0.38, -L * 0.04, L * 0.36]

            for ax in axles:
                for sy_sign in (-1.0, 1.0):
                    wy = sy_sign * (W * 0.42)
                    if long_x:
                        mb.add_wheel(ax, wy, w_rad, w_rad, w_width, segments=12, axis="Y")
                    else:
                        mb.add_wheel(wy, ax, w_rad, w_rad, w_width, segments=12, axis="X")

            # Chassis & bumpers
            add_vpart(0.0, 0.0, w_rad * 1.05, L * 0.94, W * 0.88, dz * 0.16, "mat_paint_charcoal")
            add_vpart( L * 0.47, 0.0, w_rad * 1.10, L * 0.06, W * 0.94, dz * 0.14, "mat_metal_steel")
            add_vpart(-L * 0.47, 0.0, w_rad * 1.10, L * 0.06, W * 0.94, dz * 0.14, "mat_metal_steel")

            if batch == "b03":
                # Lower body
                add_vpart(0.0, 0.0, dz * 0.40, L * 0.96, W * 0.94, dz * 0.34, body_mat)
                is_pickup = "pickup" in name
                is_van_suv = any(k in name for k in ("suv", "van", "wagon", "crossover", "hatchback"))
                is_open = any(k in name for k in ("convertible", "roadster"))
                if is_pickup:
                    # Front cab + rear open bed walls
                    add_vpart(L * 0.10, 0.0, dz * 0.74, L * 0.42, W * 0.86, dz * 0.38, body_mat)
                    add_vpart(L * 0.12, 0.0, dz * 0.75, L * 0.38, W * 0.88, dz * 0.28, "mat_glass_clear")
                    add_vpart(-L * 0.26, -W * 0.42, dz * 0.56, L * 0.40, W * 0.08, dz * 0.22, body_mat)
                    add_vpart(-L * 0.26,  W * 0.42, dz * 0.56, L * 0.40, W * 0.08, dz * 0.22, body_mat)
                elif is_open:
                    add_vpart(L * 0.14, 0.0, dz * 0.72, L * 0.08, W * 0.84, dz * 0.32, "mat_glass_clear")
                    add_vpart(-L * 0.05, -W * 0.22, dz * 0.58, L * 0.16, W * 0.28, dz * 0.24, "mat_rubber_dark")
                    add_vpart(-L * 0.05,  W * 0.22, dz * 0.58, L * 0.16, W * 0.28, dz * 0.24, "mat_rubber_dark")
                else:
                    cab_len = L * (0.74 if is_van_suv else 0.54)
                    cab_x = -L * 0.06 if is_van_suv else -L * 0.02
                    add_vpart(cab_x, 0.0, dz * 0.74, cab_len, W * 0.84, dz * 0.38, body_mat)
                    add_vpart(cab_x, 0.0, dz * 0.74, cab_len * 0.92, W * 0.87, dz * 0.26, "mat_glass_clear")
            else:
                # Heavy commercial/municipal/emergency vehicles (b15)
                is_bus = "bus" in name or "coach" in name
                if is_bus:
                    add_vpart(0.0, 0.0, dz * 0.56, L * 0.96, W * 0.94, dz * 0.68, body_mat)
                    add_vpart(0.0, 0.0, dz * 0.68, L * 0.90, W * 0.96, dz * 0.26, "mat_glass_clear")
                    add_vpart(0.0, 0.0, dz * 0.94, L * 0.45, W * 0.62, dz * 0.08, "mat_metal_steel")
                else:
                    # Front cab + rear specialized body
                    add_vpart(L * 0.32, 0.0, dz * 0.54, L * 0.28, W * 0.90, dz * 0.58, body_mat)
                    add_vpart(L * 0.36, 0.0, dz * 0.66, L * 0.20, W * 0.92, dz * 0.24, "mat_glass_clear")
                    if "tanker" in name or "tender" in name or "vacuum" in name or "spray" in name:
                        if long_x:
                            mb.add_cyl(-L * 0.12, 0.0, dz * 0.58, L * 0.62, W * 0.86, dz * 0.54, "mat_metal_steel", segments=12, axis="X")
                        else:
                            mb.add_cyl(0.0, -L * 0.12, dz * 0.58, W * 0.86, L * 0.62, dz * 0.54, "mat_metal_steel", segments=12, axis="Y")
                    elif "ladder" in name:
                        add_vpart(-L * 0.12, 0.0, dz * 0.48, L * 0.62, W * 0.92, dz * 0.42, body_mat)
                        add_vpart(-L * 0.05, 0.0, dz * 0.86, L * 0.78, W * 0.36, dz * 0.18, "mat_metal_aluminum")
                    else:
                        rear_mat = "mat_metal_steel" if ("dump" in name or "flatbed" in name) else body_mat
                        add_vpart(-L * 0.12, 0.0, dz * 0.58, L * 0.64, W * 0.94, dz * 0.64, rear_mat)

            # Headlights & Taillights
            for sy_sign in (-1.0, 1.0):
                add_vpart( L * 0.48, sy_sign * W * 0.32, dz * 0.36, L * 0.03, W * 0.14, dz * 0.08, "mat_emissive_warm")
                add_vpart(-L * 0.48, sy_sign * W * 0.32, dz * 0.36, L * 0.03, W * 0.14, dz * 0.08, "mat_paint_red")

    # -------------------------------------------------------------------------
    # BATCH b07: Construction Machinery
    # -------------------------------------------------------------------------
    elif batch == "b07":
        body_mat = pick_mat("mat_paint_yellow")
        has_tracks = any(k in name for k in ("tracked", "crawler", "excavator", "bulldozer", "planer", "paver"))
        has_wheels = any(k in name for k in ("wheel", "loader", "backhoe", "grader", "handler", "crane", "trailer", "lift", "picker", "mixer", "roller", "compactor", "conveyor"))
        if has_tracks:
            for sy_sign in (-1.0, 1.0):
                mb.add_box(0.0, sy_sign * dy * 0.38, dz * 0.14, dx * 0.72, dy * 0.18, dz * 0.26, "mat_rubber_dark")
            mb.add_box(-dx * 0.06, 0.0, dz * 0.46, dx * 0.52, dy * 0.76, dz * 0.34, body_mat)
            mb.add_box( dx * 0.04, -dy * 0.16, dz * 0.74, dx * 0.28, dy * 0.36, dz * 0.32, "mat_glass_clear")
            mb.add_box( dx * 0.32, 0.0, dz * 0.64, dx * 0.44, dy * 0.22, dz * 0.52, body_mat)
        elif has_wheels:
            w_rad = min(dz * 0.20, dx * 0.14, 0.55)
            for sx_sign in (-1.0, 1.0):
                for sy_sign in (-1.0, 1.0):
                    mb.add_wheel(sx_sign * dx * 0.30, sy_sign * dy * 0.40, w_rad, w_rad, dy * 0.14, segments=10, axis="Y")
            mb.add_box(0.0, 0.0, dz * 0.38, dx * 0.78, dy * 0.78, dz * 0.32, body_mat)
            mb.add_box(0.0, 0.0, dz * 0.72, dx * 0.44, dy * 0.66, dz * 0.42, "mat_glass_clear" if "trailer" not in name else body_mat)
        else:
            # Scaffolding, shoring, silos, hoppers, saws, gang boxes
            mb.add_box(0.0, 0.0, dz * 0.06, dx * 0.92, dy * 0.92, dz * 0.10, "mat_metal_steel")
            for sx_sign in (-1.0, 1.0):
                for sy_sign in (-1.0, 1.0):
                    mb.add_box(sx_sign * dx * 0.42, sy_sign * dy * 0.42, dz * 0.50, dx * 0.08, dy * 0.08, dz * 0.92, body_mat)
            mb.add_box(0.0, 0.0, dz * 0.62, dx * 0.88, dy * 0.84, dz * 0.48, body_mat)

    # -------------------------------------------------------------------------
    # BATCH b01: Benches, Bike Racks, Bollards, Bus Shelters, Fountains, Tables
    # -------------------------------------------------------------------------
    elif batch == "b01":
        if cat in ("Bench", "Public Seating"):
            seat_mat = pick_mat("mat_wood_timber")
            leg_mat = "mat_concrete" if "concrete" in name else "mat_metal_cast_iron"
            if "hexagonal" in name:
                for i in range(6):
                    ang = i * math.pi / 3.0
                    mb.add_box(math.cos(ang) * dx * 0.32, math.sin(ang) * dy * 0.32, dz * 0.48, dx * 0.42, dy * 0.18, dz * 0.12, seat_mat, rot_z=ang)
                    mb.add_box(math.cos(ang) * dx * 0.32, math.sin(ang) * dy * 0.32, dz * 0.24, dx * 0.12, dy * 0.18, dz * 0.46, leg_mat, rot_z=ang)
            else:
                for sx_sign in (-1.0, 0.0, 1.0):
                    mb.add_box(sx_sign * dx * 0.40, 0.0, dz * 0.24, dx * 0.06, dy * 0.82, dz * 0.48, leg_mat)
                for islat in range(5):
                    sy = -dy * 0.32 + islat * (dy * 0.16)
                    mb.add_box(0.0, sy, dz * 0.46, dx * 0.96, dy * 0.10, dz * 0.06, seat_mat)
                if "backless" not in name and "cube" not in name:
                    for islat in range(4):
                        sz = dz * 0.60 + islat * (dz * 0.10)
                        mb.add_box(0.0, dy * 0.36, sz, dx * 0.96, dy * 0.06, dz * 0.07, seat_mat)
        elif cat == "Bus Shelter":
            for sx_sign in (-1.0, 1.0):
                for sy_sign in (-1.0, 1.0):
                    mb.add_box(sx_sign * dx * 0.44, sy_sign * dy * 0.42, dz * 0.46, dx * 0.05, dy * 0.06, dz * 0.90, "mat_metal_steel")
            mb.add_box(0.0, dy * 0.42, dz * 0.48, dx * 0.88, dy * 0.03, dz * 0.76, "mat_glass_clear")
            mb.add_box(-dx * 0.44, 0.0, dz * 0.48, dx * 0.03, dy * 0.82, dz * 0.76, "mat_glass_clear")
            mb.add_box(0.0, dy * 0.22, dz * 0.20, dx * 0.56, dy * 0.24, dz * 0.08, "mat_wood_timber")
            if "gabled" in name:
                mb.add_gable(0.0, 0.0, dz * 0.90, dx * 0.98, dy * 0.98, dz * 0.20, "mat_metal_steel")
            else:
                mb.add_box(0.0, 0.0, dz * 0.92, dx * 0.98, dy * 0.98, dz * 0.12, "mat_metal_steel")
        elif cat in ("Bollard", "Drinking Fountain"):
            m = pick_mat("mat_metal_cast_iron" if cat == "Bollard" else "mat_metal_steel")
            mb.add_cyl(0.0, 0.0, dz * 0.06, dx * 0.88, dy * 0.88, dz * 0.12, m, segments=12)
            mb.add_cyl(0.0, 0.0, dz * 0.52, dx * 0.68, dy * 0.68, dz * 0.88, m, segments=12, rings=2)
            if cat == "Drinking Fountain":
                mb.add_cyl(0.0, -dy * 0.18, dz * 0.78, dx * 0.56, dy * 0.56, dz * 0.16, "mat_metal_aluminum", segments=12)
        else:
            # Bike racks & Picnic / Game tables
            m = pick_mat("mat_wood_timber" if "table" in name else "mat_metal_steel")
            mb.add_box(0.0, 0.0, dz * 0.05, dx * 0.92, dy * 0.88, dz * 0.08, "mat_metal_steel")
            for i in range(5):
                fx = (i - 2) * dx * 0.18
                mb.add_box(fx, 0.0, dz * 0.52, dx * 0.10, dy * 0.84, dz * 0.88, m)

    # -------------------------------------------------------------------------
    # BATCH b21: Modular Building Pieces (Ceilings, Doors, Floors, Walls, Windows)
    # -------------------------------------------------------------------------
    elif batch == "b21":
        if cat in ("Building Ceilings", "Building Floors"):
            base_mat = "mat_wood_timber" if ("timber" in name or "beams" in name) else "mat_concrete"
            if "stairwell_opening" in name:
                # U-shaped perimeter around stairwell opening
                mb.add_box(-dx * 0.35, 0.0, dz * 0.5, dx * 0.30, dy, dz, base_mat)
                mb.add_box( dx * 0.35, 0.0, dz * 0.5, dx * 0.30, dy, dz, base_mat)
                mb.add_box(0.0,  dy * 0.35, dz * 0.5, dx * 0.40, dy * 0.30, dz, base_mat)
                mb.add_box(0.0, -dy * 0.45, dz * 0.5, dx * 0.40, dy * 0.10, dz, "mat_metal_steel")
            else:
                mb.add_box(0.0, 0.0, dz * 0.45, dx, dy, dz * 0.85, base_mat)
                mb.add_box(0.0, 0.0, dz * 0.92, dx * 0.98, dy * 0.98, dz * 0.15, "mat_paint_white" if "ceiling" in name else base_mat)
        elif cat == "Building Walls":
            wall_mat = "mat_concrete"
            if "corner" in name or "t_junction" in name:
                mb.add_box(-dx * 0.38, 0.0, dz * 0.5, dx * 0.24, dy, dz, wall_mat)
                mb.add_box(0.0, -dy * 0.38, dz * 0.5, dx, dy * 0.24, dz, wall_mat)
            elif "opening" in name:
                # Left jamb pier, right jamb pier, top header lintel, optional window sill wall
                mb.add_box(-dx * 0.38, 0.0, dz * 0.5, dx * 0.24, dy * 0.94, dz, wall_mat)
                mb.add_box( dx * 0.38, 0.0, dz * 0.5, dx * 0.24, dy * 0.94, dz, wall_mat)
                mb.add_box(0.0, 0.0, dz * 0.86, dx * 0.52, dy * 0.94, dz * 0.28, wall_mat)
                if "window" in name:
                    mb.add_box(0.0, 0.0, dz * 0.16, dx * 0.52, dy * 0.94, dz * 0.32, wall_mat)
                mb.add_box(0.0, 0.0, dz * 0.50, dx * 0.54, dy, dz * 0.72, "mat_metal_steel")
            else:
                mb.add_box(0.0, 0.0, dz * 0.50, dx, dy * 0.90, dz * 0.94, wall_mat)
                mb.add_box(0.0, 0.0, dz * 0.04, dx, dy, dz * 0.08, "mat_stone_granite")
                mb.add_box(0.0, 0.0, dz * 0.96, dx, dy, dz * 0.08, "mat_stone_granite")
        elif cat in ("Building Doors", "Building Windows"):
            frame_mat = "mat_wood_timber" if "wood" in name else ("mat_paint_white" if "painted" in name else "mat_metal_steel")
            if "sill" in name:
                mb.add_box(0.0, 0.0, dz * 0.5, dx, dy, dz, "mat_stone_granite")
            else:
                # Outer frame jambs + head + sill
                mb.add_box(-dx * 0.45, 0.0, dz * 0.5, dx * 0.10, dy, dz, frame_mat)
                mb.add_box( dx * 0.45, 0.0, dz * 0.5, dx * 0.10, dy, dz, frame_mat)
                mb.add_box(0.0, 0.0, dz * 0.95, dx * 0.80, dy, dz * 0.10, frame_mat)
                mb.add_box(0.0, 0.0, dz * 0.05, dx * 0.80, dy, dz * 0.10, frame_mat)
                if "empty_frame" not in name:
                    infill_mat = "mat_glass_clear" if any(k in name for k in ("window", "glazed", "glass", "storefront", "shopfront", "clerestory", "mullion", "hung", "fixed", "paired", "sliding")) else frame_mat
                    mb.add_box(0.0, 0.0, dz * 0.50, dx * 0.82, dy * 0.42, dz * 0.82, infill_mat)
                    if "door" in name:
                        mb.add_box(dx * 0.32, -dy * 0.42, dz * 0.48, dx * 0.06, dy * 0.32, dz * 0.08, "mat_metal_brass")

    # -------------------------------------------------------------------------
    # BATCH b18 & b02: Lighting, Civic Fixtures, Signage, Traffic, Parking
    # -------------------------------------------------------------------------
    elif batch in ("b18", "b02"):
        main_mat = pick_mat("mat_metal_cast_iron" if batch == "b18" else "mat_metal_steel")
        if dz > max(dx, dy) * 1.4:
            # Pole / Pedestal / Post-mounted fixture or sign
            mb.add_cyl(0.0, 0.0, dz * 0.05, min(dx, dy) * 0.55, min(dx, dy) * 0.55, dz * 0.10, "mat_stone_granite" if "monument" in cat.lower() else main_mat, segments=10)
            mb.add_cyl(0.0, 0.0, dz * 0.48, min(dx, dy) * 0.22, min(dx, dy) * 0.22, dz * 0.88, main_mat, segments=10, rings=2, r_bot=0.5, r_top=0.36)
            if batch == "b18":
                # Top luminaire / clock / flag / banner
                top_mat = "mat_emissive_warm" if "light" in cat.lower() or "lamp" in name else ("mat_paint_red" if "flag" in name or "banner" in name else "mat_metal_brass")
                mb.add_box(0.0, 0.0, dz * 0.86, dx * 0.76, dy * 0.68, dz * 0.18, main_mat)
                mb.add_box(0.0, 0.0, dz * 0.82, dx * 0.62, dy * 0.56, dz * 0.14, top_mat)
            else:
                # Traffic sign plate or signal head
                sign_mat = pick_mat("mat_paint_red" if "stop" in name or "yield" in name else ("mat_paint_yellow" if "crossing" in name or "signal" in name else "mat_paint_white"))
                mb.add_box(0.0, 0.0, dz * 0.82, dx * 0.88, dy * 0.28, dz * 0.26, sign_mat)
                mb.add_box(0.0, -dy * 0.16, dz * 0.82, dx * 0.72, dy * 0.12, dz * 0.18, "mat_paint_white")
        else:
            # Compact wall light, step light, landscape light, barrier, curb stop, cone
            mb.add_box(0.0, 0.0, dz * 0.15, dx * 0.92, dy * 0.92, dz * 0.28, main_mat)
            mb.add_box(0.0, 0.0, dz * 0.62, dx * 0.78, dy * 0.78, dz * 0.68, "mat_emissive_warm" if batch == "b18" else main_mat)

    # -------------------------------------------------------------------------
    # BATCH b19: Fences, Gates, and Boundary Walls
    # -------------------------------------------------------------------------
    elif batch == "b19":
        f_mat = pick_mat("mat_wood_cedar")
        post_mat = "mat_brick_masonry" if "brick" in name else ("mat_stone_granite" if "stone" in name else f_mat)
        # Left & Right end posts/piers
        mb.add_box(-dx * 0.45, 0.0, dz * 0.50, dx * 0.10, dy * 0.92, dz, post_mat)
        mb.add_box( dx * 0.45, 0.0, dz * 0.50, dx * 0.10, dy * 0.92, dz, post_mat)
        if "wall" in name:
            mb.add_box(0.0, 0.0, dz * 0.46, dx * 0.84, dy * 0.82, dz * 0.88, f_mat)
            mb.add_box(0.0, 0.0, dz * 0.94, dx * 0.98, dy * 0.98, dz * 0.10, "mat_stone_granite")
        else:
            # Top & bottom horizontal rails + vertical pickets/slats
            mb.add_box(0.0, 0.0, dz * 0.22, dx * 0.86, dy * 0.36, dz * 0.08, f_mat)
            mb.add_box(0.0, 0.0, dz * 0.78, dx * 0.86, dy * 0.36, dz * 0.08, f_mat)
            n_pickets = max(4, min(18, t_tris // 95))
            for ip in range(n_pickets):
                px = -dx * 0.38 + ip * (dx * 0.76 / max(1, n_pickets - 1))
                mb.add_box(px, 0.0, dz * 0.50, dx * (0.55 / n_pickets), dy * 0.28, dz * 0.88, f_mat)

    # -------------------------------------------------------------------------
    # BATCH b06, b16, b17: Handheld Tools, Food/Packaging/Litter, Recreation Carry
    # -------------------------------------------------------------------------
    elif batch in ("b06", "b16", "b17"):
        m_main = pick_mat("mat_metal_steel" if batch == "b06" else ("mat_paper_cardboard" if batch == "b16" else "mat_fabric_canvas"))
        m_sec = "mat_rubber_dark" if batch == "b06" else ("mat_paint_red" if batch == "b16" else "mat_metal_aluminum")
        is_round = any(k in name for k in ("can", "bottle", "cup", "bowl", "plate", "cone", "cork", "cap", "roll", "ball", "disc", "hat", "helmet", "umbrella", "stool", "bucket"))
        if is_round:
            mb.add_cyl(0.0, 0.0, dz * 0.46, dx * 0.88, dy * 0.88, dz * 0.86, m_main, segments=10, rings=2, r_bot=0.42, r_top=0.48)
            mb.add_cyl(0.0, 0.0, dz * 0.91, dx * 0.74, dy * 0.74, dz * 0.14, m_sec, segments=10, rings=1)
        elif batch == "b06":
            # Tool handle + shaft + head/jaw
            mb.add_box(0.0, 0.0, dz * 0.28, dx * 0.45, dy * 0.55, dz * 0.52, m_sec)
            mb.add_box(0.0, 0.0, dz * 0.65, dx * 0.32, dy * 0.36, dz * 0.42, "mat_metal_steel")
            mb.add_box(0.0, 0.0, dz * 0.86, dx * 0.92, dy * 0.82, dz * 0.24, m_main)
        else:
            mb.add_box(0.0, 0.0, dz * 0.42, dx * 0.90, dy * 0.88, dz * 0.78, m_main)
            mb.add_box(0.0, 0.0, dz * 0.86, dx * 0.76, dy * 0.72, dz * 0.22, m_sec)

    # -------------------------------------------------------------------------
    # ALL REMAINING BATCHES (b04, b05, b09, b10, b11, b12, b13, b14, b20)
    # -------------------------------------------------------------------------
    else:
        m_main = pick_mat("mat_metal_steel")
        m_trim = "mat_metal_cast_iron" if m_main != "mat_metal_cast_iron" else "mat_metal_aluminum"
        if dz < 0.35 * max(dx, dy):
            # Flat infrastructure slab / paving / ramp / crossing / dock / track
            base_mat = "mat_asphalt" if "road" in cat.lower() or "crossing" in name else ("mat_concrete" if batch == "b13" else m_main)
            mb.add_box(0.0, 0.0, dz * 0.38, dx * 0.98, dy * 0.98, dz * 0.72, base_mat)
            for i in range(4):
                sx = (i - 1.5) * dx * 0.22
                mb.add_box(sx, 0.0, dz * 0.82, dx * 0.14, dy * 0.88, dz * 0.32, "mat_paint_yellow" if "warning" in name or "ramp" in name else m_trim)
        else:
            # Multi-part structural assembly (base plinth/wheels + main body + top hood/canopy/rails)
            mb.add_box(0.0, 0.0, dz * 0.10, dx * 0.94, dy * 0.94, dz * 0.18, m_trim)
            mb.add_box(0.0, 0.0, dz * 0.52, dx * 0.88, dy * 0.86, dz * 0.68, m_main)
            if any(k in name for k in ("glass", "vending", "display", "case", "kiosk", "booth", "window", "door", "cabinet")):
                mb.add_box(0.0, -dy * 0.42, dz * 0.58, dx * 0.76, dy * 0.08, dz * 0.48, "mat_glass_clear")
            if any(k in name for k in ("canopy", "umbrella", "awning", "roofed", "marquee", "stall", "stand", "house", "hutch")):
                mb.add_gable(0.0, 0.0, dz * 0.90, dx * 0.98, dy * 0.98, dz * 0.20, "mat_fabric_canvas" if batch in ("b10", "b20") else m_trim)
            else:
                mb.add_box(0.0, 0.0, dz * 0.91, dx * 0.92, dy * 0.90, dz * 0.16, m_trim)

    # Calibrate structural detail count to target triangle & vertex budgets
    mb.calibrate_budget()
    return mb.compile_geometry()


# =============================================================================
# 5. BINARY glTF 2.0 (.GLB) EXPORTER & BLENDER (`bpy`) SCENE EXPORTER
# =============================================================================

def write_glb_binary(filepath: Path, compiled: Dict[str, Any]) -> None:
    """Writes a standard Khronos glTF 2.0 binary (.glb) file with shared PBR materials."""
    item_id = compiled["item_id"]
    mat_names: List[str] = compiled["materials"]
    mat_groups = compiled["mat_groups"]

    gltf_materials = []
    for mname in mat_names:
        mdef = SHARED_MATERIALS[mname]
        mat_entry: Dict[str, Any] = {
            "name": mdef["name"],
            "pbrMetallicRoughness": {
                "baseColorFactor": mdef["baseColorFactor"],
                "metallicFactor": mdef["metallicFactor"],
                "roughnessFactor": mdef["roughnessFactor"],
            },
            "doubleSided": True,
        }
        if "emissiveFactor" in mdef:
            mat_entry["emissiveFactor"] = mdef["emissiveFactor"]
        if "alphaMode" in mdef:
            mat_entry["alphaMode"] = mdef["alphaMode"]
        gltf_materials.append(mat_entry)

    buffer_views: List[Dict[str, Any]] = []
    accessors: List[Dict[str, Any]] = []
    primitives: List[Dict[str, Any]] = []
    bin_chunks: List[bytes] = []
    byte_offset = 0

    def append_bin(raw: bytes, target: int) -> int:
        nonlocal byte_offset
        pad = (4 - (len(raw) % 4)) % 4
        padded = raw + (b"\x00" * pad)
        bv_idx = len(buffer_views)
        buffer_views.append({
            "buffer": 0,
            "byteOffset": byte_offset,
            "byteLength": len(raw),
            "target": target,
        })
        bin_chunks.append(padded)
        byte_offset += len(padded)
        return bv_idx

    for mat_idx, mname in enumerate(mat_names):
        chunks = mat_groups[mname]
        pos_list = []
        norm_list = []
        idx_list = []
        v_cursor = 0
        for pos_arr, norm_arr, tri_arr in chunks:
            pos_list.append(pos_arr)
            norm_list.append(norm_arr)
            idx_list.append((tri_arr.astype(np.uint32) + v_cursor).astype(np.uint16))
            v_cursor += len(pos_arr)

        pos_all = np.vstack(pos_list).astype(np.float32)
        norm_all = np.vstack(norm_list).astype(np.float32)
        idx_all = np.concatenate(idx_list).astype(np.uint16)

        pos_bv = append_bin(pos_all.tobytes(), 34962)
        pos_acc = len(accessors)
        accessors.append({
            "bufferView": pos_bv,
            "byteOffset": 0,
            "componentType": 5126,
            "count": int(len(pos_all)),
            "type": "VEC3",
            "min": [float(x) for x in pos_all.min(axis=0)],
            "max": [float(x) for x in pos_all.max(axis=0)],
        })

        norm_bv = append_bin(norm_all.tobytes(), 34962)
        norm_acc = len(accessors)
        accessors.append({
            "bufferView": norm_bv,
            "byteOffset": 0,
            "componentType": 5126,
            "count": int(len(norm_all)),
            "type": "VEC3",
        })

        idx_bv = append_bin(idx_all.tobytes(), 34963)
        idx_acc = len(accessors)
        accessors.append({
            "bufferView": idx_bv,
            "byteOffset": 0,
            "componentType": 5123,
            "count": int(len(idx_all)),
            "type": "SCALAR",
        })

        primitives.append({
            "attributes": {"POSITION": pos_acc, "NORMAL": norm_acc},
            "indices": idx_acc,
            "material": mat_idx,
            "mode": 4,
        })

    bin_blob = b"".join(bin_chunks)
    gltf_dict = {
        "asset": {
            "version": "2.0",
            "generator": "Blender 4.0 / Procedural Catalog GLB Generator",
        },
        "scene": 0,
        "scenes": [{"name": "Scene", "nodes": [0]}],
        "nodes": [{"name": item_id, "mesh": 0}],
        "meshes": [{"name": item_id, "primitives": primitives}],
        "materials": gltf_materials,
        "accessors": accessors,
        "bufferViews": buffer_views,
        "buffers": [{"byteLength": len(bin_blob)}],
    }

    json_bytes = json.dumps(gltf_dict, separators=(",", ":")).encode("utf-8")
    json_pad = (4 - (len(json_bytes) % 4)) % 4
    json_bytes += b" " * json_pad

    total_len = 12 + 8 + len(json_bytes) + 8 + len(bin_blob)
    header = struct.pack("<III", 0x46546C67, 2, total_len)
    json_header = struct.pack("<II", len(json_bytes), 0x4E4F534A)
    bin_header = struct.pack("<II", len(bin_blob), 0x004E4942)

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(header)
        f.write(json_header)
        f.write(json_bytes)
        f.write(bin_header)
        f.write(bin_blob)


def ensure_bpy_shared_materials() -> Dict[str, Any]:
    """Creates the shared Principled BSDF materials inside Blender (`bpy.data.materials`)."""
    if not HAS_BPY:
        return {}
    bpy_mats = {}
    for mname, mdef in SHARED_MATERIALS.items():
        mat = bpy.data.materials.get(mname)
        if mat is None:
            mat = bpy.data.materials.new(name=mname)
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes.get("Principled BSDF")
            if bsdf is not None:
                bsdf.inputs["Base Color"].default_value = mdef["baseColorFactor"]
                bsdf.inputs["Metallic"].default_value = mdef["metallicFactor"]
                bsdf.inputs["Roughness"].default_value = mdef["roughnessFactor"]
        bpy_mats[mname] = mat
    return bpy_mats


def export_via_bpy(filepath: Path, compiled: Dict[str, Any], bpy_mats: Dict[str, Any]) -> None:
    """Builds the object in Blender (`bpy`) and exports to GLB."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    item_id = compiled["item_id"]
    verts = compiled["bpy_verts"].tolist()
    faces_with_mat = compiled["bpy_faces"]
    faces = [f[0] for f in faces_with_mat]

    mesh = bpy.data.meshes.new(item_id)
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    used_mats = compiled["materials"]
    mat_to_slot = {}
    for idx, mname in enumerate(used_mats):
        mesh.materials.append(bpy_mats[mname])
        mat_to_slot[mname] = idx

    for poly, (_, mname) in zip(mesh.polygons, faces_with_mat):
        poly.use_smooth = False
        poly.material_index = mat_to_slot[mname]

    obj = bpy.data.objects.new(item_id, mesh)
    bpy.context.collection.objects.link(obj)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(filepath),
        export_format="GLB",
        use_selection=False,
        export_yup=True,
        export_apply=True,
    )
    bpy.data.objects.remove(obj, do_unlink=True)
    bpy.data.meshes.remove(mesh, do_unlink=True)


# =============================================================================
# 6. CATALOG PARSER & MAIN ENTRYPOINT
# =============================================================================

def parse_catalog_md(md_path: Path) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    current_cat = "Uncategorized"
    with open(md_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if line.startswith("### "):
                current_cat = re.sub(r"\s*\(\d+\)\s*$", "", line[4:].strip())
            elif line.startswith("| [b"):
                parts = [p.strip() for p in line.strip("|").split("|")]
                m = re.match(r"\[([^\]]+)\]\(([^)]+)\)", parts[0])
                if not m:
                    continue
                item_id, rel_path = m.group(1), m.group(2)
                size_class = parts[1]
                dims = [float(x.strip()) for x in parts[2].split("×")]
                v_limit = int(parts[3].replace(",", ""))
                src_v = int(parts[4].replace(",", ""))
                glb_v = int(parts[5].replace(",", ""))
                tris = int(parts[6].replace(",", ""))
                items.append({
                    "id": item_id,
                    "path": rel_path,
                    "category": current_cat,
                    "size_class": size_class,
                    "dimensions": dims,
                    "vertex_limit": v_limit,
                    "target_source_vertices": src_v,
                    "target_glb_vertices": glb_v,
                    "target_triangles": tris,
                })
    return items


def main() -> None:
    argv = sys.argv[1:]
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]

    parser = argparse.ArgumentParser(description="Generate all 1,050 GLB models from ITEM_CATALOG.md")
    parser.add_argument("--catalog", type=str, default="ITEM_CATALOG.md", help="Path to ITEM_CATALOG.md")
    parser.add_argument("--out-dir", type=str, default=".", help="Output directory for exports/ and manifest.json")
    parser.add_argument("--use-bpy-exporter", action="store_true", help="Use bpy.ops.export_scene.gltf when running in Blender")
    args = parser.parse_args(argv)

    catalog_path = Path(args.catalog)
    if not catalog_path.exists():
        # Search common fallback locations
        candidates = [
            Path(__file__).resolve().parent / "ITEM_CATALOG.md",
            Path("/working_dir/c_aafbba589df4638a/user_uploaded_files/ttl=63d/user_uploaded/ITEM_CATALOG.md"),
        ]
        for c in candidates:
            if c.exists():
                catalog_path = c
                break

    if not catalog_path.exists():
        raise FileNotFoundError(f"Could not find ITEM_CATALOG.md at {args.catalog}")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    items = parse_catalog_md(catalog_path)
    print(f"Parsed {len(items)} items from {catalog_path}")

    bpy_mats = ensure_bpy_shared_materials() if (HAS_BPY and args.use_bpy_exporter) else {}
    manifest_items: List[Dict[str, Any]] = []

    for idx, item in enumerate(items, start=1):
        compiled = build_procedural_item(item)
        glb_path = out_dir / item["path"]
        if HAS_BPY and args.use_bpy_exporter:
            export_via_bpy(glb_path, compiled, bpy_mats)
        else:
            write_glb_binary(glb_path, compiled)

        used_pct = round(100.0 * compiled["glb_vertices"] / item["vertex_limit"], 1)
        manifest_items.append({
            "id": item["id"],
            "batch": item["id"][:3],
            "category": item["category"],
            "size_class": item["size_class"],
            "glb_path": item["path"],
            "dimensions_m": compiled["dimensions"],
            "vertex_limit": item["vertex_limit"],
            "source_vertices": compiled["source_vertices"],
            "glb_vertices": compiled["glb_vertices"],
            "triangles": compiled["triangles"],
            "catalog_target_triangles": item["target_triangles"],
            "triangle_delta": compiled["triangles"] - item["target_triangles"],
            "budget_used_percent": used_pct,
            "shared_materials": compiled["materials"],
        })

        if idx % 150 == 0 or idx == len(items):
            print(f"  [{idx:4d}/{len(items)}] Generated {item['id']} (gv={compiled['glb_vertices']}/{item['vertex_limit']}, tris={compiled['triangles']})")

    manifest_data = {
        "schema_version": "1.0.0",
        "generator": "generate_catalog_glbs.py (Blender bpy / glTF 2.0 Procedural Builder)",
        "coordinate_system": {
            "up_axis": "+Y",
            "forward_axis": "-Z",
            "origin": "bottom_center (Y=0 ground plane)",
            "units": "meters",
        },
        "budget_rules": {
            "Large": {"max_vertices": 10000, "count": sum(1 for x in manifest_items if x["size_class"] == "Large")},
            "Medium": {"max_vertices": 5000, "count": sum(1 for x in manifest_items if x["size_class"] == "Medium")},
            "Handheld": {"max_vertices": 999, "count": sum(1 for x in manifest_items if x["size_class"] == "Handheld")},
        },
        "shared_material_library": SHARED_MATERIALS,
        "total_items": len(manifest_items),
        "items": manifest_items,
    }

    manifest_path = out_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2)

    elapsed = time.time() - t0
    print(f"Completed {len(manifest_items)} GLB models and {manifest_path} in {elapsed:.2f}s.")


if __name__ == "__main__":
    main()
