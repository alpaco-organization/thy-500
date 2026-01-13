"use client";

import { useRef, useEffect } from "react";
import * as THREE from "three";
import { useThree } from "@react-three/fiber";

type Props = {
  targetMesh: THREE.Mesh;
  onSelect?: (data: {
    world: THREE.Vector3;
    local: THREE.Vector3;
    uv?: THREE.Vector2;
  }) => void;
};

export function SurfaceClickCoordinates({ targetMesh, onSelect }: Props) {
  const { camera, gl } = useThree();
  const raycaster = useRef(new THREE.Raycaster());
  const mouse = useRef(new THREE.Vector2());

  useEffect(() => {
    const dom = gl.domElement;

    function onPointerDown(e: PointerEvent) {
      const rect = dom.getBoundingClientRect();

      mouse.current.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.current.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.current.setFromCamera(mouse.current, camera);

      const hits = raycaster.current.intersectObject(targetMesh, true);
      if (!hits.length) return;

      const hit = hits[0];

      const world = hit.point.clone();
      const local = targetMesh.worldToLocal(hit.point.clone());
      const uv = hit.uv?.clone();

      console.log("WORLD:", world);
      console.log("LOCAL:", local);
      console.log("UV:", uv);

      onSelect?.({ world, local, uv });
    }

    dom.addEventListener("pointerdown", onPointerDown);
    return () => dom.removeEventListener("pointerdown", onPointerDown);
  }, [camera, gl, targetMesh, onSelect]);

  return null;
}
