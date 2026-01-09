"use client";

import { Canvas, useThree, useFrame } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";
import { useState, useRef, useEffect } from "react";
import { Search } from "@/components/search";
import { Splash } from "@/components/splash";
import { Welcome } from "@/components/welcome";
import { useNavigation } from "@/contexts/navigation-context";
import * as THREE from "three";
import Information from "@/components/information";
import Header from "@/components/header";

const INITIAL_CAMERA_POSITION: [number, number, number] = [-30, 4, 20];

function Model({ onLoad }: { onLoad?: () => void }) {
  const { scene } = useGLTF("/modal.glb");

  useEffect(() => {
    onLoad?.();
  }, [onLoad]);

  return <primitive object={scene} position={[0, 0, 10]} />;
}

function ModelLights() {
  return (
    <>
      <ambientLight intensity={1.2} />
      <hemisphereLight intensity={0.6} />

      <directionalLight position={[10, 10, 10]} intensity={1} />
      <directionalLight position={[-10, 10, 10]} intensity={0.8} />
      <directionalLight position={[10, -10, -10]} intensity={0.6} />
      <directionalLight position={[-10, -10, -10]} intensity={0.6} />
    </>
  );
}

function Camera({
  targetPosition,
  shouldAnimate,
  isResetting,
  onAnimationComplete,
}: {
  targetPosition: [number, number, number] | null;
  shouldAnimate: boolean;
  isResetting: boolean;
  onAnimationComplete: () => void;
}) {
  const { camera } = useThree();
  const {setIsNavigating} = useNavigation();

  const controlsRef = useRef<any>(null);

  const targetCameraPos = useRef<[number, number, number] | null>(null);
  const targetControlsPos = useRef<[number, number, number] | null>(null);
  const [isAnimating, setIsAnimating] = useState<boolean>(false);
  const initialCameraPos = useRef<[number, number, number] | null>(null);

  useEffect(() => {
    setIsNavigating(isAnimating);
  }, [isAnimating]);

  useEffect(() => {
    if (!initialCameraPos.current) {
      initialCameraPos.current = [
        camera.position.x,
        camera.position.y,
        camera.position.z,
      ];
    }
  }, []);

  useEffect(() => {
    if (isResetting) {
      if (initialCameraPos.current) {
        targetCameraPos.current = initialCameraPos.current;
      } else {
        targetCameraPos.current = INITIAL_CAMERA_POSITION;
      }
      targetControlsPos.current = [0, 0, 10];
      setIsAnimating(true);
    } else if (shouldAnimate && targetPosition) {
      const [x, y, z] = targetPosition;

      const distance = 14;
      const horizontalAngle = Math.PI / 4;
      const verticalAngle = Math.PI / 6;

      const camX =
        x + distance * Math.cos(verticalAngle) * Math.cos(horizontalAngle);
      const camY = y + distance * Math.sin(verticalAngle);
      const camZ =
        z + distance * Math.cos(verticalAngle) * Math.sin(horizontalAngle);

      targetCameraPos.current = [camX, camY, camZ];
      targetControlsPos.current = targetPosition;
      setIsAnimating(true);
    }
  }, [
    targetPosition,
    shouldAnimate,
    isResetting,
    INITIAL_CAMERA_POSITION,
    camera,
  ]);

  useFrame(() => {
    if (
      targetCameraPos.current &&
      targetControlsPos.current &&
      controlsRef.current
    ) {
      const [tx, ty, tz] = targetCameraPos.current;
      const [cx, cy, cz] = targetControlsPos.current;
      const lerpFactor = 0.05;

      camera.position.x += (tx - camera.position.x) * lerpFactor;
      camera.position.y += (ty - camera.position.y) * lerpFactor;
      camera.position.z += (tz - camera.position.z) * lerpFactor;

      controlsRef.current.target.x +=
        (cx - controlsRef.current.target.x) * lerpFactor;
      controlsRef.current.target.y +=
        (cy - controlsRef.current.target.y) * lerpFactor;
      controlsRef.current.target.z +=
        (cz - controlsRef.current.target.z) * lerpFactor;

      controlsRef.current.update();

      const distanceToCam = Math.sqrt(
        Math.pow(tx - camera.position.x, 2) +
          Math.pow(ty - camera.position.y, 2) +
          Math.pow(tz - camera.position.z, 2)
      );

      const distanceToTarget = Math.sqrt(
        Math.pow(cx - controlsRef.current.target.x, 2) +
          Math.pow(cy - controlsRef.current.target.y, 2) +
          Math.pow(cz - controlsRef.current.target.z, 2)
      );

      if (distanceToCam < 0.1 && distanceToTarget < 0.1) {
        targetCameraPos.current = null;
        targetControlsPos.current = null;
        setIsAnimating(false);
        onAnimationComplete();
      }
    }
  });

  return (
    <OrbitControls
      ref={controlsRef}
      enableZoom
      enablePan={false}
      enabled={!isAnimating}
      minDistance={8}
      maxDistance={50}
    />
  );
}

function CircleMarker({ position }: { position: [number, number, number] }) {
  const meshRef = useRef<THREE.Mesh | null>(null);

  useFrame((state) => {
    if (!meshRef.current || !meshRef.current.material) return;
    const t = state.clock.getElapsedTime();
    const opacity = 0.3 + 0.6 * (0.5 + 0.5 * Math.sin(t * 2));
    (meshRef.current.material as THREE.MeshBasicMaterial).opacity = opacity;
  });

  return (
    <mesh ref={meshRef} position={position}>
      <sphereGeometry args={[2, 32, 32]} />
      <meshBasicMaterial color="#ffffff" transparent opacity={0.6} />
    </mesh>
  );
}

export default function Home() {
  const { setIsNavigating } = useNavigation();

  const [targetPosition, setTargetPosition] = useState<
    [number, number, number] | null
  >(null);
  const [shouldAnimate, setShouldAnimate] = useState<boolean>(false);
  const [isResetting, setIsResetting] = useState<boolean>(false);
  const [isModelLoaded, setIsModelLoaded] = useState<boolean>(false);
  const [isSearchComplete, setIsSearchComplete] = useState<boolean>(false);
  const [circleVisible, setCircleVisible] = useState<boolean>(false);

  const handleReset = () => {
    setTargetPosition(null);
    setShouldAnimate(false);
    setIsResetting(true);
    setIsSearchComplete(false);
    setCircleVisible(false);
  };

  const handleAnimationComplete = () => {
    setIsResetting(false);
    setShouldAnimate(false);
    if (targetPosition) {
      setCircleVisible(true);
      setIsSearchComplete(true);
    }
  };

  const handleSearch = async (
    searchType: "identity" | "fullName",
    query: string
  ) => {
    await new Promise((resolve) => setTimeout(resolve, 3000));

    const fixedCoords: [number, number, number] = [2, 3, 5];

    setTargetPosition(fixedCoords);
    setShouldAnimate(true);
    setIsResetting(false);
    setCircleVisible(false);
    setIsSearchComplete(false);
  };

  const handlePointerDown = () => {
    setIsNavigating(true);
  };

  const handlePointerUp = () => {
    setIsNavigating(false);
  };

  return (
    <div className="fixed w-screen h-full">
      <Header />
      {isModelLoaded ? (
        <Welcome onTimeout={handleReset}/>
      ) : (
        <Splash />
      )}

      <Information isSearchComplete={isSearchComplete} />

      <Search
        onSearch={handleSearch}
        onReset={handleReset}
        isSearchComplete={isSearchComplete}
      />

      <Canvas
        camera={{ position: INITIAL_CAMERA_POSITION, fov: 50 }}
        onPointerDown={handlePointerDown}
        onPointerUp={handlePointerUp}
      >
        <ModelLights />
        <Model onLoad={() => setIsModelLoaded(true)} />

        {circleVisible && targetPosition && (
          <CircleMarker position={targetPosition} />
        )}

        <Camera
          targetPosition={targetPosition}
          shouldAnimate={shouldAnimate}
          isResetting={isResetting}
          onAnimationComplete={handleAnimationComplete}
        />
      </Canvas>
    </div>
  );
}
