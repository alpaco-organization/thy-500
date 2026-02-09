# map_to_3d.py

import json
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent


class UVFlipMode(Enum):
    """UV coordinate flip modes."""
    NONE = "none"           # No flip
    FLIP_V = "flip_v"       # Flip V coordinate (1 - v)
    FLIP_U = "flip_u"       # Flip U coordinate (1 - u)
    AUTO = "auto"           # Try both and pick best
    BOTH = "both"           # Collect from both (for diagnosis)


@dataclass
class Triangle:
    """Represents a mesh triangle with UV mapping."""
    index: int
    v0: np.ndarray
    v1: np.ndarray
    v2: np.ndarray
    uv0: np.ndarray
    uv1: np.ndarray
    uv2: np.ndarray
    
    # Precomputed bounds for fast rejection
    min_u: float = field(init=False)
    max_u: float = field(init=False)
    min_v: float = field(init=False)
    max_v: float = field(init=False)
    
    # Precomputed center
    uv_center: np.ndarray = field(init=False)
    pos_center: np.ndarray = field(init=False)
    
    # Precomputed normal for orientation checking
    normal: np.ndarray = field(init=False)
    
    def __post_init__(self):
        self.min_u = min(self.uv0[0], self.uv1[0], self.uv2[0])
        self.max_u = max(self.uv0[0], self.uv1[0], self.uv2[0])
        self.min_v = min(self.uv0[1], self.uv1[1], self.uv2[1])
        self.max_v = max(self.uv0[1], self.uv1[1], self.uv2[1])
        
        self.uv_center = (self.uv0 + self.uv1 + self.uv2) / 3.0
        self.pos_center = (self.v0 + self.v1 + self.v2) / 3.0
        
        # Calculate face normal
        edge1 = self.v1 - self.v0
        edge2 = self.v2 - self.v0
        self.normal = np.cross(edge1, edge2)
        norm = np.linalg.norm(self.normal)
        if norm > 1e-10:
            self.normal /= norm
    
    def contains_uv(self, u: float, v: float, margin: float = 0.001) -> bool:
        """Fast bounding box check."""
        return (self.min_u - margin <= u <= self.max_u + margin and
                self.min_v - margin <= v <= self.max_v + margin)


@dataclass
class MappingCandidate:
    """A candidate 3D position from UV mapping."""
    position: np.ndarray
    triangle_idx: int
    barycentric: Dict[str, float]
    uv_flipped: bool
    centrality: float  # How centered the point is in the triangle (0-1)
    uv_distance: float  # Distance from query UV to triangle center
    
    def in_region(self, region: Optional[Tuple[float, ...]] = None) -> bool:
        """Check if position is within expected region."""
        if region is None:
            return True
        min_x, max_x, min_y, max_y, min_z, max_z = region
        return (min_x <= self.position[0] <= max_x and
                min_y <= self.position[1] <= max_y and
                min_z <= self.position[2] <= max_z)


@dataclass 
class MappingResult:
    """Result of a mapping operation."""
    success: bool
    position: Optional[Tuple[float, float, float]] = None
    method: str = "none"  # "exact", "fallback", "failed"
    num_candidates: int = 0
    confidence: float = 0.0
    triangle_idx: Optional[int] = None
    warning: Optional[str] = None


class TextureTo3DMapper:
    """Maps 2D texture coordinates to 3D positions using GLB mesh data."""
    
    def __init__(
        self, 
        glb_path: str, 
        texture_width: int, 
        texture_height: int,
        uv_flip_mode: UVFlipMode = UVFlipMode.AUTO,
        verbose: bool = True
    ):
        self.texture_width = texture_width
        self.texture_height = texture_height
        self.uv_flip_mode = uv_flip_mode
        self.verbose = verbose
        self.triangles: List[Triangle] = []
        
        self._load_glb(glb_path)
        
        if self.verbose:
            print(f"✓ Loaded {len(self.triangles)} triangles from GLB")
            self._print_mesh_stats()
    
    def _print_mesh_stats(self):
        """Print statistics about loaded mesh."""
        if not self.triangles:
            return
            
        positions = np.array([t.pos_center for t in self.triangles])
        print(f"  3D bounds: X[{positions[:,0].min():.2f}, {positions[:,0].max():.2f}] "
              f"Y[{positions[:,1].min():.2f}, {positions[:,1].max():.2f}] "
              f"Z[{positions[:,2].min():.2f}, {positions[:,2].max():.2f}]")
        
        uv_centers = np.array([t.uv_center for t in self.triangles])
        print(f"  UV bounds: U[{uv_centers[:,0].min():.3f}, {uv_centers[:,0].max():.3f}] "
              f"V[{uv_centers[:,1].min():.3f}, {uv_centers[:,1].max():.3f}]")
    
    def _load_glb(self, glb_path: str):
        """Load mesh data from GLB file."""
        import pygltflib
        from pygltflib import BufferFormat
        
        gltf = pygltflib.GLTF2().load(glb_path)
        gltf.convert_buffers(BufferFormat.BINARYBLOB)
        binary_blob = gltf.binary_blob()
        node_matrices = self._compute_world_matrices(gltf)
        
        # Map mesh indices to node indices
        mesh_to_nodes = {}
        for node_idx, node in enumerate(gltf.nodes):
            if node.mesh is not None:
                mesh_to_nodes.setdefault(node.mesh, []).append(node_idx)
        
        triangle_idx = 0
        for mesh_idx, mesh in enumerate(gltf.meshes):
            world_matrix = np.eye(4)
            if mesh_idx in mesh_to_nodes:
                world_matrix = node_matrices[mesh_to_nodes[mesh_idx][0]]
            
            for primitive in mesh.primitives:
                if (primitive.attributes.POSITION is None or 
                    primitive.attributes.TEXCOORD_0 is None):
                    continue
                
                positions = self._get_accessor_data(
                    gltf, binary_blob, 
                    primitive.attributes.POSITION, np.float32, 3
                )
                uvs = self._get_accessor_data(
                    gltf, binary_blob,
                    primitive.attributes.TEXCOORD_0, np.float32, 2
                )
                
                if primitive.indices is not None:
                    acc = gltf.accessors[primitive.indices]
                    dtype = {5123: np.uint16, 5125: np.uint32}.get(
                        acc.componentType, np.uint8
                    )
                    indices = self._get_accessor_data(
                        gltf, binary_blob, primitive.indices, dtype, 1
                    ).flatten()
                else:
                    indices = np.arange(len(positions))
                
                positions = self._transform_positions(positions, world_matrix)
                
                for i in range(0, len(indices), 3):
                    if i + 2 >= len(indices):
                        break
                    i0, i1, i2 = indices[i], indices[i+1], indices[i+2]
                    
                    self.triangles.append(Triangle(
                        index=triangle_idx,
                        v0=positions[i0].astype(np.float64),
                        v1=positions[i1].astype(np.float64),
                        v2=positions[i2].astype(np.float64),
                        uv0=uvs[i0].astype(np.float64),
                        uv1=uvs[i1].astype(np.float64),
                        uv2=uvs[i2].astype(np.float64)
                    ))
                    triangle_idx += 1
    
    def _get_accessor_data(
        self, gltf, blob, idx: int, dtype, components: int
    ) -> np.ndarray:
        """Extract accessor data from binary blob."""
        acc = gltf.accessors[idx]
        bv = gltf.bufferViews[acc.bufferView]
        offset = (bv.byteOffset or 0) + (acc.byteOffset or 0)
        item_size = np.dtype(dtype).itemsize * components
        stride = bv.byteStride
        
        if stride and stride != item_size:
            data = np.array([
                np.frombuffer(
                    blob[offset + i*stride:offset + i*stride + item_size], 
                    dtype=dtype
                ) 
                for i in range(acc.count)
            ])
        else:
            data = np.frombuffer(
                blob[offset:offset + acc.count * item_size], 
                dtype=dtype
            )
            if components > 1:
                data = data.reshape(-1, components)
        return data.copy()
    
    def _compute_world_matrices(self, gltf) -> List[np.ndarray]:
        """Compute world transformation matrices for all nodes."""
        n = len(gltf.nodes) if gltf.nodes else 0
        local = [self._get_node_matrix(node) for node in (gltf.nodes or [])]
        world = [np.eye(4) for _ in range(n)]
        parents = [-1] * n
        
        def set_parents(idx: int, parent: int):
            parents[idx] = parent
            for child in (gltf.nodes[idx].children or []):
                set_parents(child, idx)
        
        def compute(idx: int):
            if parents[idx] >= 0:
                world[idx] = world[parents[idx]] @ local[idx]
            else:
                world[idx] = local[idx].copy()
            for child in (gltf.nodes[idx].children or []):
                compute(child)
        
        for scene in (gltf.scenes or []):
            for root in (scene.nodes or []):
                set_parents(root, -1)
                compute(root)
        
        return world
    
    def _get_node_matrix(self, node) -> np.ndarray:
        """Get local transformation matrix for a node."""
        if node.matrix:
            return np.array(node.matrix).reshape(4, 4).T
        
        T = np.eye(4)
        R = np.eye(4)
        S = np.eye(4)
        
        if node.translation:
            T[:3, 3] = node.translation
        
        if node.rotation:
            x, y, z, w = node.rotation
            R[:3, :3] = [
                [1-2*y*y-2*z*z, 2*x*y-2*z*w, 2*x*z+2*y*w],
                [2*x*y+2*z*w, 1-2*x*x-2*z*z, 2*y*z-2*x*w],
                [2*x*z-2*y*w, 2*y*z+2*x*w, 1-2*x*x-2*y*y]
            ]
        
        if node.scale:
            np.fill_diagonal(S[:3, :3], node.scale)
        
        return T @ R @ S
    
    def _transform_positions(
        self, positions: np.ndarray, matrix: np.ndarray
    ) -> np.ndarray:
        """Apply transformation matrix to positions."""
        homo = np.hstack([positions, np.ones((len(positions), 1))])
        return (matrix @ homo.T).T[:, :3]
    
    def _compute_barycentric(
        self, 
        p: np.ndarray, 
        a: np.ndarray, 
        b: np.ndarray, 
        c: np.ndarray,
        tolerance: float = 1e-6
    ) -> Optional[Dict[str, float]]:
        """
        Compute barycentric coordinates for point p in triangle abc.
        Returns None if point is outside triangle.
        """
        v0 = c - a
        v1 = b - a
        v2 = p - a
        
        d00 = np.dot(v0, v0)
        d01 = np.dot(v0, v1)
        d02 = np.dot(v0, v2)
        d11 = np.dot(v1, v1)
        d12 = np.dot(v1, v2)
        
        denom = d00 * d11 - d01 * d01
        
        if abs(denom) < 1e-12:
            return None
        
        inv_denom = 1.0 / denom
        u = (d11 * d02 - d01 * d12) * inv_denom
        v = (d00 * d12 - d01 * d02) * inv_denom
        w = 1.0 - u - v
        
        # Check if inside triangle with tolerance
        if u >= -tolerance and v >= -tolerance and w >= -tolerance:
            return {'u': u, 'v': v, 'w': w}
        
        return None
    
    def _compute_centrality(self, bary: Dict[str, float]) -> float:
        """
        Compute how centered a point is within a triangle.
        Returns 1.0 for center, 0.0 for vertices.
        """
        ideal = 1.0 / 3.0
        deviation = max(
            abs(bary['u'] - ideal),
            abs(bary['v'] - ideal),
            abs(bary['w'] - ideal)
        )
        return max(0.0, 1.0 - deviation * 1.5)
    
    def _interpolate_position(
        self, tri: Triangle, bary: Dict[str, float]
    ) -> np.ndarray:
        """Interpolate 3D position using barycentric coordinates."""
        return tri.v0 * bary['w'] + tri.v1 * bary['v'] + tri.v2 * bary['u']
    
    def _get_uv_variants(self, u: float, v: float) -> List[Tuple[float, float, bool]]:
        """Get UV variants to try based on flip mode."""
        if self.uv_flip_mode == UVFlipMode.NONE:
            return [(u, v, False)]
        elif self.uv_flip_mode == UVFlipMode.FLIP_V:
            return [(u, 1.0 - v, True)]
        elif self.uv_flip_mode == UVFlipMode.FLIP_U:
            return [(1.0 - u, v, True)]
        else:  # AUTO or BOTH
            return [(u, v, False), (u, 1.0 - v, True)]
    
    def _find_candidates(
        self,
        u: float,
        v: float,
        max_uv_distance: float = float('inf')
    ) -> List[MappingCandidate]:
        """Find all triangles that contain the UV coordinate."""
        candidates = []
        
        for u_test, v_test, flipped in self._get_uv_variants(u, v):
            uv = np.array([u_test, v_test], dtype=np.float64)
            
            for tri in self.triangles:
                # Fast bounding box rejection
                if not tri.contains_uv(u_test, v_test):
                    continue
                
                # Check UV distance for fallback searches
                uv_dist = np.linalg.norm(uv - tri.uv_center)
                if uv_dist > max_uv_distance:
                    continue
                
                # Compute barycentric coordinates
                bary = self._compute_barycentric(
                    uv, tri.uv0, tri.uv1, tri.uv2
                )
                
                if bary:
                    position = self._interpolate_position(tri, bary)
                    centrality = self._compute_centrality(bary)
                    
                    candidates.append(MappingCandidate(
                        position=position,
                        triangle_idx=tri.index,
                        barycentric=bary,
                        uv_flipped=flipped,
                        centrality=centrality,
                        uv_distance=uv_dist
                    ))
        
        return candidates
    
    def _find_nearest_triangle(
        self, 
        u: float, 
        v: float, 
        max_distance: float
    ) -> List[MappingCandidate]:
        """Find nearest triangles when exact match fails."""
        candidates = []
        
        for u_test, v_test, flipped in self._get_uv_variants(u, v):
            uv = np.array([u_test, v_test], dtype=np.float64)
            
            # Find triangles sorted by distance to UV center
            triangle_distances = []
            for tri in self.triangles:
                dist = np.linalg.norm(uv - tri.uv_center)
                if dist <= max_distance:
                    triangle_distances.append((dist, tri))
            
            triangle_distances.sort(key=lambda x: x[0])
            
            for dist, tri in triangle_distances[:10]:  # Check top 10 nearest
                # Project UV onto triangle and clamp to bounds
                bary = self._compute_barycentric_clamped(uv, tri.uv0, tri.uv1, tri.uv2)
                position = self._interpolate_position(tri, bary)
                centrality = self._compute_centrality(bary)
                
                candidates.append(MappingCandidate(
                    position=position,
                    triangle_idx=tri.index,
                    barycentric=bary,
                    uv_flipped=flipped,
                    centrality=centrality,
                    uv_distance=dist
                ))
        
        return candidates
    
    def _compute_barycentric_clamped(
        self,
        p: np.ndarray,
        a: np.ndarray,
        b: np.ndarray,
        c: np.ndarray
    ) -> Dict[str, float]:
        """Compute barycentric coords, clamped to valid range."""
        v0 = c - a
        v1 = b - a
        v2 = p - a
        
        d00 = np.dot(v0, v0)
        d01 = np.dot(v0, v1)
        d02 = np.dot(v0, v2)
        d11 = np.dot(v1, v1)
        d12 = np.dot(v1, v2)
        
        denom = d00 * d11 - d01 * d01
        
        if abs(denom) < 1e-12:
            return {'u': 1/3, 'v': 1/3, 'w': 1/3}
        
        inv_denom = 1.0 / denom
        u = (d11 * d02 - d01 * d12) * inv_denom
        v = (d00 * d12 - d01 * d02) * inv_denom
        w = 1.0 - u - v
        
        # Clamp to valid range
        u = max(0.0, u)
        v = max(0.0, v)
        w = max(0.0, w)
        
        # Renormalize
        total = u + v + w
        if total > 1e-10:
            u, v, w = u/total, v/total, w/total
        else:
            u, v, w = 1/3, 1/3, 1/3
        
        return {'u': u, 'v': v, 'w': w}
    
    def _select_best_candidate(
        self,
        candidates: List[MappingCandidate],
        expected_region: Optional[Tuple[float, ...]] = None
    ) -> Optional[MappingCandidate]:
        """Select the best candidate from multiple matches."""
        if not candidates:
            return None
        
        if len(candidates) == 1:
            return candidates[0]
        
        # Filter by region if specified
        if expected_region:
            in_region = [c for c in candidates if c.in_region(expected_region)]
            if in_region:
                candidates = in_region
        
        # Sort by: prefer non-flipped, then by centrality, then by UV distance
        candidates.sort(key=lambda c: (
            c.uv_flipped,           # Prefer non-flipped
            -c.centrality,          # Prefer more central
            c.uv_distance           # Prefer closer UV
        ))
        
        return candidates[0]
    
    def pixel_to_3d(
        self,
        px: float,
        py: float,
        max_search_distance: float = 0.15,
        expected_region: Optional[Tuple[float, ...]] = None
    ) -> MappingResult:
        """
        Convert pixel coordinates to 3D position.
        
        Args:
            px: Pixel X coordinate
            py: Pixel Y coordinate  
            max_search_distance: Maximum UV distance for fallback search
            expected_region: Optional (min_x, max_x, min_y, max_y, min_z, max_z)
                           to filter ambiguous matches
        
        Returns:
            MappingResult with position and metadata
        """
        u = px / self.texture_width
        v = py / self.texture_height
        
        # Step 1: Try exact match
        candidates = self._find_candidates(u, v)
        
        if candidates:
            best = self._select_best_candidate(candidates, expected_region)
            if best:
                warning = None
                if len(candidates) > 1:
                    # Check if candidates are far apart (ambiguous)
                    positions = [c.position for c in candidates]
                    max_dist = max(
                        np.linalg.norm(p1 - p2) 
                        for i, p1 in enumerate(positions) 
                        for p2 in positions[i+1:]
                    ) if len(positions) > 1 else 0
                    
                    if max_dist > 0.1:
                        warning = f"Ambiguous: {len(candidates)} matches, spread={max_dist:.3f}"
                
                return MappingResult(
                    success=True,
                    position=(
                        float(best.position[0]),
                        float(best.position[1]),
                        float(best.position[2])
                    ),
                    method="exact",
                    num_candidates=len(candidates),
                    confidence=best.centrality,
                    triangle_idx=best.triangle_idx,
                    warning=warning
                )
        
        # Step 2: Fallback to nearest triangle
        if max_search_distance > 0:
            fallback_candidates = self._find_nearest_triangle(u, v, max_search_distance)
            
            if fallback_candidates:
                best = self._select_best_candidate(fallback_candidates, expected_region)
                if best:
                    return MappingResult(
                        success=True,
                        position=(
                            float(best.position[0]),
                            float(best.position[1]),
                            float(best.position[2])
                        ),
                        method="fallback",
                        num_candidates=len(fallback_candidates),
                        confidence=best.centrality * 0.5,  # Lower confidence for fallback
                        triangle_idx=best.triangle_idx,
                        warning=f"Fallback match, UV distance={best.uv_distance:.4f}"
                    )
        
        # Step 3: Failed
        return MappingResult(
            success=False,
            method="failed",
            warning=f"No triangle found for UV ({u:.4f}, {v:.4f})"
        )
    
    def diagnose_pixel(self, px: float, py: float) -> Dict[str, Any]:
        """
        Diagnose mapping for a specific pixel.
        Useful for debugging problematic mappings.
        """
        u = px / self.texture_width
        v = py / self.texture_height
        
        # Find all candidates with extended search
        all_candidates = []
        
        for u_test, v_test, flipped in [(u, v, False), (u, 1-v, True)]:
            uv = np.array([u_test, v_test], dtype=np.float64)
            
            for tri in self.triangles:
                if not tri.contains_uv(u_test, v_test, margin=0.05):
                    continue
                
                bary = self._compute_barycentric(uv, tri.uv0, tri.uv1, tri.uv2)
                uv_dist = np.linalg.norm(uv - tri.uv_center)
                
                if bary:
                    position = self._interpolate_position(tri, bary)
                    all_candidates.append({
                        'triangle_idx': tri.index,
                        'flipped': flipped,
                        'position': position.tolist(),
                        'barycentric': bary,
                        'uv_distance': float(uv_dist),
                        'exact_match': True
                    })
        
        # Calculate spread if multiple matches
        spread = 0.0
        if len(all_candidates) > 1:
            positions = [np.array(c['position']) for c in all_candidates]
            spread = max(
                np.linalg.norm(p1 - p2)
                for i, p1 in enumerate(positions)
                for p2 in positions[i+1:]
            )
        
        return {
            'pixel': (px, py),
            'uv': (u, v),
            'num_exact_matches': len(all_candidates),
            'position_spread': float(spread),
            'candidates': all_candidates,
            'issue': self._diagnose_issue(all_candidates, spread)
        }
    
    def _diagnose_issue(
        self, 
        candidates: List[Dict], 
        spread: float
    ) -> str:
        """Diagnose the type of mapping issue."""
        if len(candidates) == 0:
            return "NO_MATCH"
        elif len(candidates) == 1:
            return "OK"
        elif spread < 0.05:
            return "OK_MULTIPLE_CLOSE"
        elif spread < 0.2:
            return "WARNING_MULTIPLE_MODERATE_SPREAD"
        else:
            return "ERROR_MULTIPLE_LARGE_SPREAD"


# ============================================================================
# Data Processing Functions
# ============================================================================

def get_data_path(relative_path: str) -> Path:
    """Get absolute path for data files."""
    possible_roots = [
        Path("/app"),
        PROJECT_ROOT,
        Path.cwd(),
        Path(__file__).parent,
    ]
    
    for root in possible_roots:
        full_path = root / relative_path
        if full_path.exists():
            return full_path
    
    if Path("/app").exists():
        return Path("/app") / relative_path
    return PROJECT_ROOT / relative_path


def load_and_merge_raw_data(raw_data_dir: Path) -> List[Dict]:
    """Load and merge all JSON files from raw_data directory."""
    all_records = []
    json_files = sorted(raw_data_dir.glob("*.json"))
    
    if not json_files:
        print(f"❌ No JSON files found in {raw_data_dir}")
        return []
    
    print(f"\n📁 Found {len(json_files)} JSON file(s):")
    
    for json_file in json_files:
        print(f"   Loading: {json_file.name}...", end=" ")
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                all_records.extend(data)
                print(f"✓ {len(data)} records")
            else:
                print(f"⚠ Skipped (not a list)")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n📊 Total merged records: {len(all_records)}")
    return all_records


@dataclass
class ConversionStats:
    """Statistics for the conversion process."""
    total_input: int = 0
    exact_matches: int = 0
    fallback_matches: int = 0
    failed: int = 0
    ambiguous: int = 0
    
    @property
    def total_mapped(self) -> int:
        return self.exact_matches + self.fallback_matches
    
    @property
    def success_rate(self) -> float:
        if self.total_input == 0:
            return 0.0
        return 100.0 * self.total_mapped / self.total_input


def convert_raw_to_mapped(
    glb_filename: str = "model.glb",
    output_filename: str = "persons_mapped.json",
    input_image_size: int = 64000,
    texture_size: int = 8192,
    grid_filename: str = "grid_1.png",
    max_search_distance: float = 0.15,
    uv_flip_mode: UVFlipMode = UVFlipMode.AUTO,
    expected_region: Optional[Tuple[float, ...]] = None,
    diagnose_failures: bool = True
) -> Optional[List[Dict]]:
    """
    Merge all JSON files from raw_data and convert to 3D mapped data.
    
    Args:
        glb_filename: Name of GLB file in models directory
        output_filename: Name of output JSON file
        input_image_size: Size of input image in pixels
        texture_size: Size of UV texture in pixels
        grid_filename: Grid filename to include in output
        max_search_distance: Maximum UV distance for fallback matching
        uv_flip_mode: How to handle UV coordinate flipping
        expected_region: Optional 3D region bounds for disambiguation
        diagnose_failures: Whether to diagnose and save failed mappings
    
    Returns:
        List of mapped records or None if failed
    """
    
    # Resolve paths
    raw_data_dir = get_data_path("datas/raw_data")
    
    if Path("/app/app/scripts").exists():
        output_path = Path("/app/app/scripts/datas/mapped_data") / output_filename
    else:
        output_path = SCRIPT_DIR / "datas" / "mapped_data" / output_filename
    
    glb_path = get_data_path(f"datas/models/{glb_filename}")
    
    # Print configuration
    print("=" * 70)
    print("3D MAPPING PIPELINE - IMPROVED VERSION")
    print("=" * 70)
    print(f"Raw data dir:        {raw_data_dir}")
    print(f"Output path:         {output_path}")
    print(f"GLB path:            {glb_path}")
    print(f"Input image size:    {input_image_size}px")
    print(f"Texture size:        {texture_size}px")
    print(f"UV flip mode:        {uv_flip_mode.value}")
    print(f"Max search distance: {max_search_distance}")
    if expected_region:
        print(f"Expected region:     {expected_region}")
    
    # Verify paths
    if not raw_data_dir.exists():
        print(f"\n❌ ERROR: Raw data directory not found: {raw_data_dir}")
        return None
    
    if not glb_path.exists():
        print(f"\n❌ ERROR: GLB file not found: {glb_path}")
        return None
    
    # Step 1: Load raw data
    print("\n" + "-" * 70)
    print("STEP 1: LOADING RAW DATA")
    print("-" * 70)
    
    raw_data = load_and_merge_raw_data(raw_data_dir)
    if not raw_data:
        print("❌ No data to process")
        return None
    
    # Step 2: Initialize mapper
    print("\n" + "-" * 70)
    print("STEP 2: INITIALIZING 3D MAPPER")
    print("-" * 70)
    
    mapper = TextureTo3DMapper(
        str(glb_path), 
        texture_size, 
        texture_size,
        uv_flip_mode=uv_flip_mode,
        verbose=True
    )
    
    # Step 3: Map records
    print("\n" + "-" * 70)
    print("STEP 3: MAPPING TO 3D COORDINATES")
    print("-" * 70)
    
    scale = texture_size / input_image_size
    stats = ConversionStats(total_input=len(raw_data))
    
    mapped_data = []
    failed_records = []
    ambiguous_records = []
    
    print(f"\nProcessing {len(raw_data)} records...")
    
    for i, record in enumerate(raw_data):
        pixel_x = record['center_global']['x']
        pixel_y = record['center_global']['y']
        
        scaled_x = pixel_x * scale
        scaled_y = pixel_y * scale
        
        result = mapper.pixel_to_3d(
            scaled_x, 
            scaled_y,
            max_search_distance=max_search_distance,
            expected_region=expected_region
        )
        
        if result.success:
            matched = record.get('matched_person', {})
            sicil = matched.get('sicil', '')
            person_id = sicil if sicil else str(record.get('id', i))
            name = matched.get('name_original', f"Unknown_{record.get('id', i)}")
            
            mapped_record = {
                "personId": person_id,
                "name": name,
                "grid_filename": grid_filename,
                "x": result.position[0],
                "y": result.position[1],
                "z": result.position[2],
                "_meta": {
                    "method": result.method,
                    "confidence": round(result.confidence, 3),
                    "triangle_idx": result.triangle_idx
                }
            }
            
            if result.warning:
                mapped_record["_meta"]["warning"] = result.warning
                if "Ambiguous" in result.warning:
                    stats.ambiguous += 1
                    ambiguous_records.append({
                        "id": record.get('id', i),
                        "name": name,
                        "warning": result.warning,
                        "position": result.position
                    })
            
            mapped_data.append(mapped_record)
            
            if result.method == "exact":
                stats.exact_matches += 1
            else:
                stats.fallback_matches += 1
        else:
            stats.failed += 1
            
            failed_info = {
                "id": record.get('id', i),
                "pixel_x": pixel_x,
                "pixel_y": pixel_y,
                "scaled_x": scaled_x,
                "scaled_y": scaled_y,
                "name": record.get('matched_person', {}).get('name_original', 'Unknown'),
                "warning": result.warning
            }
            
            if diagnose_failures:
                diagnosis = mapper.diagnose_pixel(scaled_x, scaled_y)
                failed_info["diagnosis"] = diagnosis
            
            failed_records.append(failed_info)
            
            if stats.failed <= 10:
                print(f"  ⚠ Failed: id={record.get('id', i)}, "
                      f"pixel=({pixel_x}, {pixel_y})")
        
        if (i + 1) % 1000 == 0:
            print(f"  Processed {i + 1}/{len(raw_data)}... "
                  f"(exact: {stats.exact_matches}, fallback: {stats.fallback_matches}, "
                  f"failed: {stats.failed})")
    
    # Step 4: Save results
    print("\n" + "-" * 70)
    print("STEP 4: SAVING RESULTS")
    print("-" * 70)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save mapped data (without _meta for production)
    production_data = []
    for record in mapped_data:
        prod_record = {k: v for k, v in record.items() if not k.startswith('_')}
        production_data.append(prod_record)
    
    print(f"Saving mapped data to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(production_data, f, indent=4, ensure_ascii=False)
    
    # Save detailed data with metadata
    detailed_path = output_path.parent / output_path.name.replace('.json', '_detailed.json')
    print(f"Saving detailed data to: {detailed_path}")
    with open(detailed_path, 'w', encoding='utf-8') as f:
        json.dump(mapped_data, f, indent=4, ensure_ascii=False)
    
    # Save failed records
    if failed_records:
        failed_path = output_path.parent / "failed_mappings.json"
        print(f"Saving {len(failed_records)} failed records to: {failed_path}")
        with open(failed_path, 'w', encoding='utf-8') as f:
            json.dump(failed_records, f, indent=2, ensure_ascii=False)
    
    # Save ambiguous records
    if ambiguous_records:
        ambiguous_path = output_path.parent / "ambiguous_mappings.json"
        print(f"Saving {len(ambiguous_records)} ambiguous records to: {ambiguous_path}")
        with open(ambiguous_path, 'w', encoding='utf-8') as f:
            json.dump(ambiguous_records, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total input records:     {stats.total_input}")
    print(f"Exact matches:           {stats.exact_matches}")
    print(f"Fallback matches:        {stats.fallback_matches}")
    print(f"Ambiguous (resolved):    {stats.ambiguous}")
    print(f"Total mapped:            {stats.total_mapped}")
    print(f"Failed to map:           {stats.failed}")
    print(f"Success rate:            {stats.success_rate:.2f}%")
    print(f"Output saved to:         {output_path}")
    print("=" * 70)
    
    return production_data


def diagnose_specific_records(
    mapper: TextureTo3DMapper,
    records: List[Dict],
    scale: float,
    texture_size: int
) -> List[Dict]:
    """
    Diagnose specific problematic records.
    
    Usage:
        mapper = TextureTo3DMapper(...)
        problems = diagnose_specific_records(mapper, raw_data[:10], scale, texture_size)
    """
    results = []
    
    for record in records:
        px = record['center_global']['x'] * scale
        py = record['center_global']['y'] * scale
        
        diagnosis = mapper.diagnose_pixel(px, py)
        diagnosis['record_id'] = record.get('id')
        diagnosis['name'] = record.get('matched_person', {}).get('name_original', 'Unknown')
        
        results.append(diagnosis)
    
    return results


def find_all_ambiguous_mappings(
    mapper: TextureTo3DMapper,
    raw_data: List[Dict],
    scale: float,
    min_spread: float = 0.1
) -> List[Dict]:
    """
    Find all records that have ambiguous mappings (multiple distant matches).
    """
    ambiguous = []
    
    for i, record in enumerate(raw_data):
        px = record['center_global']['x'] * scale
        py = record['center_global']['y'] * scale
        
        diagnosis = mapper.diagnose_pixel(px, py)
        
        if diagnosis['position_spread'] >= min_spread:
            ambiguous.append({
                'record_id': record.get('id', i),
                'name': record.get('matched_person', {}).get('name_original', 'Unknown'),
                'num_matches': diagnosis['num_exact_matches'],
                'spread': diagnosis['position_spread'],
                'positions': [c['position'] for c in diagnosis['candidates']],
                'issue': diagnosis['issue']
            })
    
    return sorted(ambiguous, key=lambda x: -x['spread'])


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Cabin region bounds - positions outside this are from wrong UV flip
    # Based on analysis: cabin X is -3 to 3, Y is 1.5 to 4.5, Z is -26 to 6
    CABIN_REGION = (-4.0, 4.0, 1.0, 5.0, -27.0, 10.0)  # (min_x, max_x, min_y, max_y, min_z, max_z)

    # Configuration
    config = {
        "glb_filename": "map_model.glb",
        "output_filename": "persons_mapped.json",
        "input_image_size": 64000,
        "texture_size": 9000,
        "grid_filename": "grid_1.png",
        "max_search_distance": 0.15,
        "uv_flip_mode": UVFlipMode.AUTO,
        "expected_region": CABIN_REGION,
        "diagnose_failures": True
    }

    # Run conversion
    result = convert_raw_to_mapped(**config)

    if result:
        print(f"\n Successfully mapped {len(result)} records")
    else:
        print("\n Conversion failed")