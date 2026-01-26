# map_to_3d.py

import json
from pathlib import Path
from typing import Optional
import numpy as np

SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent


class TextureTo3DMapper:
    """Maps 2D texture coordinates to 3D positions using GLB mesh data."""
    
    def __init__(self, glb_path: str, texture_width: int, texture_height: int):
        self.texture_width = texture_width
        self.texture_height = texture_height
        self.triangles = []
        self._load_glb(glb_path)
        print(f"Loaded {len(self.triangles)} triangles from GLB")
    
    def _load_glb(self, glb_path: str):
        import pygltflib
        from pygltflib import BufferFormat
        
        gltf = pygltflib.GLTF2().load(glb_path)
        gltf.convert_buffers(BufferFormat.BINARYBLOB)
        binary_blob = gltf.binary_blob()
        node_matrices = self._compute_world_matrices(gltf)
        
        mesh_to_nodes = {}
        for node_idx, node in enumerate(gltf.nodes):
            if node.mesh is not None:
                mesh_to_nodes.setdefault(node.mesh, []).append(node_idx)
        
        for mesh_idx, mesh in enumerate(gltf.meshes):
            world_matrix = np.eye(4)
            if mesh_idx in mesh_to_nodes:
                world_matrix = node_matrices[mesh_to_nodes[mesh_idx][0]]
            
            for primitive in mesh.primitives:
                if primitive.attributes.POSITION is None or primitive.attributes.TEXCOORD_0 is None:
                    continue
                
                positions = self._get_accessor_data(gltf, binary_blob, primitive.attributes.POSITION, np.float32, 3)
                uvs = self._get_accessor_data(gltf, binary_blob, primitive.attributes.TEXCOORD_0, np.float32, 2)
                
                if primitive.indices is not None:
                    acc = gltf.accessors[primitive.indices]
                    dtype = {5123: np.uint16, 5125: np.uint32}.get(acc.componentType, np.uint8)
                    indices = self._get_accessor_data(gltf, binary_blob, primitive.indices, dtype, 1).flatten()
                else:
                    indices = np.arange(len(positions))
                
                positions = self._transform_positions(positions, world_matrix)
                
                for i in range(0, len(indices), 3):
                    i0, i1, i2 = indices[i:i+3]
                    uv0, uv1, uv2 = uvs[i0], uvs[i1], uvs[i2]
                    self.triangles.append({
                        'v0': positions[i0], 'v1': positions[i1], 'v2': positions[i2],
                        'uv0': uv0, 'uv1': uv1, 'uv2': uv2,
                        'minU': min(uv0[0], uv1[0], uv2[0]), 'maxU': max(uv0[0], uv1[0], uv2[0]),
                        'minV': min(uv0[1], uv1[1], uv2[1]), 'maxV': max(uv0[1], uv1[1], uv2[1])
                    })
    
    def _get_accessor_data(self, gltf, blob, idx, dtype, components):
        acc = gltf.accessors[idx]
        bv = gltf.bufferViews[acc.bufferView]
        offset = (bv.byteOffset or 0) + (acc.byteOffset or 0)
        item_size = np.dtype(dtype).itemsize * components
        stride = bv.byteStride
        
        if stride and stride != item_size:
            data = np.array([np.frombuffer(blob[offset + i*stride:offset + i*stride + item_size], dtype=dtype) for i in range(acc.count)])
        else:
            data = np.frombuffer(blob[offset:offset + acc.count * item_size], dtype=dtype)
            if components > 1:
                data = data.reshape(-1, components)
        return data
    
    def _compute_world_matrices(self, gltf):
        n = len(gltf.nodes) if gltf.nodes else 0
        local = [self._get_node_matrix(node) for node in (gltf.nodes or [])]
        world = [np.eye(4) for _ in range(n)]
        parents = [-1] * n
        
        def set_parents(idx, parent):
            parents[idx] = parent
            for child in (gltf.nodes[idx].children or []):
                set_parents(child, idx)
        
        def compute(idx):
            world[idx] = (world[parents[idx]] @ local[idx]) if parents[idx] >= 0 else local[idx].copy()
            for child in (gltf.nodes[idx].children or []):
                compute(child)
        
        for scene in (gltf.scenes or []):
            for root in (scene.nodes or []):
                set_parents(root, -1)
                compute(root)
        return world
    
    def _get_node_matrix(self, node):
        if node.matrix:
            return np.array(node.matrix).reshape(4, 4).T
        T, R, S = np.eye(4), np.eye(4), np.eye(4)
        if node.translation:
            T[:3, 3] = node.translation
        if node.rotation:
            x, y, z, w = node.rotation
            R[:3, :3] = [[1-2*y*y-2*z*z, 2*x*y-2*z*w, 2*x*z+2*y*w],
                         [2*x*y+2*z*w, 1-2*x*x-2*z*z, 2*y*z-2*x*w],
                         [2*x*z-2*y*w, 2*y*z+2*x*w, 1-2*x*x-2*y*y]]
        if node.scale:
            np.fill_diagonal(S[:3, :3], node.scale)
        return T @ R @ S
    
    def _transform_positions(self, positions, matrix):
        homo = np.hstack([positions, np.ones((len(positions), 1))])
        return (matrix @ homo.T).T[:, :3]
    
    def _barycentric(self, p, a, b, c):
        v0, v1, v2 = c - a, b - a, p - a
        d00, d01, d02 = np.dot(v0, v0), np.dot(v0, v1), np.dot(v0, v2)
        d11, d12 = np.dot(v1, v1), np.dot(v1, v2)
        denom = d00 * d11 - d01 * d01
        if abs(denom) < 1e-12:
            return None
        inv = 1.0 / denom
        u, v = (d11 * d02 - d01 * d12) * inv, (d00 * d12 - d01 * d02) * inv
        w = 1.0 - u - v
        if u >= -1e-6 and v >= -1e-6 and w >= -1e-6:
            return {'u': u, 'v': v, 'w': w}
        return None
    
    def _barycentric_clamped(self, p, a, b, c):
        """Calculate barycentric coords, clamped to triangle bounds."""
        v0, v1, v2 = c - a, b - a, p - a
        d00, d01, d02 = np.dot(v0, v0), np.dot(v0, v1), np.dot(v0, v2)
        d11, d12 = np.dot(v1, v1), np.dot(v1, v2)
        denom = d00 * d11 - d01 * d01
        
        if abs(denom) < 1e-12:
            return {'u': 1/3, 'v': 1/3, 'w': 1/3}
        
        inv = 1.0 / denom
        u = (d11 * d02 - d01 * d12) * inv
        v = (d00 * d12 - d01 * d02) * inv
        w = 1.0 - u - v
        
        u, v, w = max(0, u), max(0, v), max(0, w)
        total = u + v + w
        if total > 1e-10:
            u, v, w = u/total, v/total, w/total
        else:
            u, v, w = 1/3, 1/3, 1/3
        
        return {'u': u, 'v': v, 'w': w}
    
    def _find_nearest_position(self, u: float, v: float, max_distance: float) -> Optional[tuple[float, float, float]]:
        """Find nearest triangle and return interpolated 3D position."""
        best_result = None
        best_dist = float('inf')
        
        for flip in [False, True]:
            v_use = (1.0 - v) if flip else v
            uv = np.array([u, v_use], dtype=np.float64)
            
            for tri in self.triangles:
                tri_center = (tri['uv0'] + tri['uv1'] + tri['uv2']) / 3.0
                dist = np.linalg.norm(uv - tri_center)
                
                if dist > max_distance or dist >= best_dist:
                    continue
                
                bary = self._barycentric_clamped(
                    uv,
                    tri['uv0'].astype(np.float64),
                    tri['uv1'].astype(np.float64),
                    tri['uv2'].astype(np.float64)
                )
                
                pos = tri['v0'] * bary['w'] + tri['v1'] * bary['v'] + tri['v2'] * bary['u']
                best_dist = dist
                best_result = (float(pos[0]), float(pos[1]), float(pos[2]))
        
        return best_result
    
    def pixel_to_3d(self, px: float, py: float, max_search_distance: float = 0.1) -> Optional[tuple[float, float, float]]:
        """Convert pixel coordinates to 3D position with fallback."""
        u, v = px / self.texture_width, py / self.texture_height
        
        for flip in [False, True]:
            v_use = (1.0 - v) if flip else v
            uv = np.array([u, v_use], dtype=np.float64)
            
            for tri in self.triangles:
                if not (tri['minU'] <= u <= tri['maxU'] and tri['minV'] <= v_use <= tri['maxV']):
                    continue
                
                bary = self._barycentric(
                    uv,
                    tri['uv0'].astype(np.float64),
                    tri['uv1'].astype(np.float64),
                    tri['uv2'].astype(np.float64)
                )
                
                if bary:
                    pos = tri['v0'] * bary['w'] + tri['v1'] * bary['v'] + tri['v2'] * bary['u']
                    return (float(pos[0]), float(pos[1]), float(pos[2]))
        
        return self._find_nearest_position(u, v, max_search_distance)


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


def load_and_merge_raw_data(raw_data_dir: Path) -> list[dict]:
    """
    Load and merge all JSON files from raw_data directory.
    Returns combined list of all records.
    """
    all_records = []
    json_files = sorted(raw_data_dir.glob("*.json"))
    
    if not json_files:
        print(f"❌ No JSON files found in {raw_data_dir}")
        return []
    
    print(f"\n📁 Found {len(json_files)} JSON file(s) in {raw_data_dir}:")
    
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


def convert_raw_to_mapped(
    glb_filename: str = "model.glb",
    output_filename: str = "persons_mapped.json",
    input_image_size: int = 64000,
    texture_size: int = 8192,
    grid_filename: str = "grid_1.png",
    max_search_distance: float = 0.15
):
    """
    Merge all JSON files from raw_data and convert to 3D mapped data.
    """
    
    # Resolve paths
    raw_data_dir = get_data_path("datas/raw_data")
    output_path = get_data_path("datas/mapped_data") / output_filename
    glb_path = get_data_path(f"datas/models/{glb_filename}")
    
    print("=" * 60)
    print("3D MAPPING PIPELINE")
    print("=" * 60)
    print(f"Raw data dir:        {raw_data_dir}")
    print(f"Output path:         {output_path}")
    print(f"GLB path:            {glb_path}")
    print(f"Input image size:    {input_image_size}px")
    print(f"Texture size:        {texture_size}px")
    print(f"Max search distance: {max_search_distance}")
    
    # Verify directories/files exist
    if not raw_data_dir.exists():
        print(f"\n❌ ERROR: Raw data directory not found: {raw_data_dir}")
        return None
    
    if not glb_path.exists():
        print(f"\n❌ ERROR: GLB file not found: {glb_path}")
        return None
    
    # Step 1: Load and merge all JSON files
    print("\n" + "-" * 60)
    print("STEP 1: LOADING AND MERGING RAW DATA")
    print("-" * 60)
    
    raw_data = load_and_merge_raw_data(raw_data_dir)
    
    if not raw_data:
        print("❌ No data to process")
        return None
    
    # Step 2: Initialize 3D mapper
    print("\n" + "-" * 60)
    print("STEP 2: INITIALIZING 3D MAPPER")
    print("-" * 60)
    
    mapper = TextureTo3DMapper(str(glb_path), texture_size, texture_size)
    
    # Step 3: Map all records
    print("\n" + "-" * 60)
    print("STEP 3: MAPPING TO 3D COORDINATES")
    print("-" * 60)
    
    scale = texture_size / input_image_size
    
    mapped_data = []
    exact_count = 0
    fallback_count = 0
    fail_count = 0
    failed_records = []
    
    print(f"\nProcessing {len(raw_data)} records...")
    
    for i, record in enumerate(raw_data):
        pixel_x = record['center_global']['x']
        pixel_y = record['center_global']['y']
        
        scaled_x = pixel_x * scale
        scaled_y = pixel_y * scale
        
        # Check for exact match
        u, v = scaled_x / texture_size, scaled_y / texture_size
        exact_match = False
        
        for flip in [False, True]:
            if exact_match:
                break
            v_use = (1.0 - v) if flip else v
            uv = np.array([u, v_use], dtype=np.float64)
            
            for tri in mapper.triangles:
                if not (tri['minU'] <= u <= tri['maxU'] and tri['minV'] <= v_use <= tri['maxV']):
                    continue
                bary = mapper._barycentric(uv, tri['uv0'].astype(np.float64), tri['uv1'].astype(np.float64), tri['uv2'].astype(np.float64))
                if bary:
                    exact_match = True
                    break
        
        pos_3d = mapper.pixel_to_3d(scaled_x, scaled_y, max_search_distance)
        
        if pos_3d:
            matched = record.get('matched_person', {})
            person_id = matched.get('sicil', str(record.get('id', i)))
            name = matched.get('name_original', f"Unknown_{record.get('id', i)}")
            
            mapped_record = {
                "personId": person_id,
                "name": name,
                "grid_filename": grid_filename,
                "x": round(pos_3d[0], 3),
                "y": round(pos_3d[1], 3),
                "z": round(pos_3d[2], 3)
            }
            mapped_data.append(mapped_record)
            
            if exact_match:
                exact_count += 1
            else:
                fallback_count += 1
        else:
            fail_count += 1
            failed_records.append({
                "id": record.get('id', i),
                "pixel_x": pixel_x,
                "pixel_y": pixel_y,
                "name": record.get('matched_person', {}).get('name_original', 'Unknown')
            })
            if fail_count <= 10:
                print(f"  ⚠ Failed: id={record.get('id', i)}, pixel=({pixel_x}, {pixel_y})")
        
        if (i + 1) % 1000 == 0:
            print(f"  Processed {i + 1}/{len(raw_data)}...")
    
    # Step 4: Save results
    print("\n" + "-" * 60)
    print("STEP 4: SAVING RESULTS")
    print("-" * 60)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Saving mapped data to: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(mapped_data, f, indent=4, ensure_ascii=False)
    
    # Save failed records
    if failed_records:
        failed_path = output_path.parent / "failed_mappings.json"
        with open(failed_path, 'w', encoding='utf-8') as f:
            json.dump(failed_records, f, indent=2, ensure_ascii=False)
        print(f"Saved failed records to: {failed_path}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total input records:  {len(raw_data)}")
    print(f"Exact matches:        {exact_count}")
    print(f"Fallback matches:     {fallback_count}")
    print(f"Total mapped:         {exact_count + fallback_count}")
    print(f"Failed to map:        {fail_count}")
    print(f"Success rate:         {100 * (exact_count + fallback_count) / len(raw_data):.2f}%")
    print(f"Output saved to:      {output_path}")
    print("=" * 60)
    
    return mapped_data


if __name__ == "__main__":
    convert_raw_to_mapped(
        glb_filename="model.glb",
        output_filename="persons_mapped.json",
        input_image_size=64000,
        texture_size=8192,
        grid_filename="grid_1.png",
        max_search_distance=0.15
    )