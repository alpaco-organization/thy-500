"use client";

import { Canvas, useThree, useFrame, type RootState } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";
import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import { Search } from "@/components/search";
import { Splash } from "@/components/splash";
import { Welcome } from "@/components/welcome";
import { useNavigation } from "@/contexts/navigation-context";
import { useLanguage } from "@/contexts/language-context";
import * as THREE from "three";
import Information from "@/components/information";
import {
  searchPerson,
  type PersonSearchOut,
  type SearchType,
} from "@/lib/services/search";
import Header from "@/components/header";
import { Button } from "@/components/ui/button";
import { clsx } from "clsx";

const INITIAL_CAMERA_POSITION: [number, number, number] = [60, 3.5, 22.7];
const CENTER_POSITION: [number, number, number] = [0, 0, 0];
const MARKER_RADIUS = 0.1;

function preloadImage(url: string, timeoutMs = 15000): Promise<void> {
  return new Promise((resolve) => {
    if (!url) return resolve();
    const img = new window.Image();
    let settled = false;

    const finish = () => {
      if (settled) return;
      settled = true;
      resolve();
    };

    const timeout = window.setTimeout(finish, timeoutMs);

    img.onload = () => {
      window.clearTimeout(timeout);
      finish();
    };
    img.onerror = () => {
      window.clearTimeout(timeout);
      finish();
    };

    img.src = url;
  });
}

function Model({
  onLoad,
  modelRef,
}: {
  onLoad?: () => void;
  modelRef?: React.MutableRefObject<THREE.Object3D | null>;
}) {
  const { scene } = useGLTF("/model.glb");

  useEffect(() => {
    const box = new THREE.Box3().setFromObject(scene);
    const center = new THREE.Vector3();
    box.getCenter(center);
    scene.position.sub(center);

    if (modelRef) {
      modelRef.current = scene;
    }

    onLoad?.();
  }, [onLoad, modelRef, scene]);

  return <primitive object={scene} />;
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
  const { setIsNavigating } = useNavigation();
  const controlsRef = useRef<any>(null);

  const targetCameraPos = useRef<[number, number, number] | null>(null);
  const targetControlsPos = useRef<[number, number, number] | null>(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const initialCameraPos = useRef<[number, number, number] | null>(null);

  useEffect(() => {
    setIsNavigating(isAnimating);
  }, [isAnimating, setIsNavigating]);

  useEffect(() => {
    if (!initialCameraPos.current) {
      initialCameraPos.current = [
        camera.position.x,
        camera.position.y,
        camera.position.z,
      ];
    }
  }, [camera]);

  useEffect(() => {
    if (isResetting) {
      targetCameraPos.current =
        initialCameraPos.current ?? INITIAL_CAMERA_POSITION;
      targetControlsPos.current = CENTER_POSITION;
      setIsAnimating(true);
    } else if (shouldAnimate && targetPosition) {
      const [x, y, z] = targetPosition;

      const distance = 14;
      const verticalAngle = Math.PI / 6;
      const horizontalAngle = x < 0 ? Math.PI / 4 + Math.PI : -Math.PI / 4;

      targetCameraPos.current = [
        x + distance * Math.cos(verticalAngle) * Math.cos(horizontalAngle),
        y + distance * Math.sin(verticalAngle),
        z + distance * Math.cos(verticalAngle) * Math.sin(horizontalAngle),
      ];

      targetControlsPos.current = targetPosition;
      setIsAnimating(true);
    }
  }, [targetPosition, shouldAnimate, isResetting]);

  useFrame(() => {
    if (
      targetCameraPos.current &&
      targetControlsPos.current &&
      controlsRef.current
    ) {
      const [tx, ty, tz] = targetCameraPos.current;
      const [cx, cy, cz] = targetControlsPos.current;
      const lerp = 0.05;

      camera.position.lerp(new THREE.Vector3(tx, ty, tz), lerp);
      controlsRef.current.target.lerp(new THREE.Vector3(cx, cy, cz), lerp);
      controlsRef.current.update();

      if (
        camera.position.distanceTo(new THREE.Vector3(tx, ty, tz)) < 0.1 &&
        controlsRef.current.target.distanceTo(new THREE.Vector3(cx, cy, cz)) <
          0.1
      ) {
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
      minDistance={0}
      maxDistance={80}
    />
  );
}

function Marker({ position }: { position: [number, number, number] }) {
  const coreRef = useRef<THREE.Mesh | null>(null);
  const rippleRef = useRef<THREE.Mesh | null>(null);

  useFrame((state: RootState) => {
    const elapsed = state.clock.getElapsedTime();
    const cycleDuration = 1.5;
    const t = (elapsed % cycleDuration) / cycleDuration;

    if (rippleRef.current) {
      const scale = 1 + 2 * t;
      rippleRef.current.scale.set(scale, scale, scale);

      const material = rippleRef.current.material as THREE.MeshBasicMaterial;
      material.opacity = 1 - t;
    }
  });

  return (
    <group position={position}>
      <mesh ref={coreRef}>
        <sphereGeometry args={[MARKER_RADIUS * 0.6, 32, 32]} />
        <meshBasicMaterial color="#ffffff" />
      </mesh>

      <mesh ref={rippleRef}>
        <sphereGeometry args={[MARKER_RADIUS, 32, 32]} />
        <meshBasicMaterial
          color="#ffffff"
          transparent
          opacity={1}
          side={THREE.DoubleSide}
        />
      </mesh>
    </group>
  );
}

function ViewModeSelector({
  viewMode,
  onViewModeChange,
}: {
  viewMode: "2D" | "3D";
  onViewModeChange: (mode: "2D" | "3D") => void;
}) {
  const { isNavigating } = useNavigation();

  return (
    <div
      className={clsx(
        "fixed left-1/2 -translate-x-1/2 z-40 flex gap-1.5 top-1/6",
        { hidden: isNavigating }
      )}
    >
      {(["2D", "3D"] as const).map((mode) => (
        <Button
          key={mode}
          size="sm"
          variant={viewMode === mode ? "default" : "secondary"}
          onClick={() => onViewModeChange(mode)}
          className="rounded-full text-xs"
        >
          {mode} Görünüm
        </Button>
      ))}
    </div>
  );
}

export default function Home() {
  const { setIsNavigating, isNavigating } = useNavigation();
  const { t } = useLanguage();

  const modelRef = useRef<THREE.Object3D | null>(null);
  const searchCompleteResolverRef = useRef<null | (() => void)>(null);

  const [targetPosition, setTargetPosition] = useState<
    [number, number, number] | null
  >(null);
  const [shouldAnimate, setShouldAnimate] = useState(false);
  const [isResetting, setIsResetting] = useState(false);
  const [isModelLoaded, setIsModelLoaded] = useState(false);
  const [isSearchComplete, setIsSearchComplete] = useState(false);
  const [circleVisible, setCircleVisible] = useState(false);
  const [searchResult, setSearchResult] = useState<PersonSearchOut | null>(
    null
  );
  const [isAnimationDone, setIsAnimationDone] = useState(false);
  const [isPhotoLoaded, setIsPhotoLoaded] = useState(false);
  const [query, setQuery] = useState("");
  const [isSplashReady, setIsSplashReady] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [viewMode, setViewMode] = useState<"2D" | "3D">("3D");

  useEffect(() => {
    const t = setTimeout(() => setIsSplashReady(true), 5000);
    return () => clearTimeout(t);
  }, []);

  const handleReset = () => {
    searchCompleteResolverRef.current?.();
    searchCompleteResolverRef.current = null;

    setTargetPosition(null);
    setShouldAnimate(false);
    setIsResetting(true);
    setIsSearchComplete(false);
    setCircleVisible(false);
    setSearchResult(null);
    setIsAnimationDone(false);
    setIsPhotoLoaded(false);
    setQuery("");
    setViewMode("3D");
  };

  const handleAnimationComplete = () => {
    setIsResetting(false);
    setShouldAnimate(false);
    setIsAnimationDone(true);
  };

  const handlePointerDown = () => {
    setIsNavigating(true);
  };

  const handlePointerUp = () => {
    setIsNavigating(false);
  };

  useEffect(() => {
    const ready = Boolean(targetPosition) && isAnimationDone && isPhotoLoaded;
    setCircleVisible(ready);
    setIsSearchComplete(ready);
    if (ready) searchCompleteResolverRef.current?.();
  }, [targetPosition, isAnimationDone, isPhotoLoaded]);

  const handleSearch = async (searchType: SearchType, query: string) => {
    const donePromise = new Promise<void>((resolve) => {
      searchCompleteResolverRef.current = resolve;
    });

    try {
      const result = await searchPerson({ searchType, query });
      await preloadImage(result.url);
      setIsPhotoLoaded(true);
      setSearchResult(result);

      const x = result.x % 5;
      const z = result.y % 5;
      let y: number | null = null;

      if (modelRef.current) {
        const raycaster = new THREE.Raycaster();
        raycaster.set(
          new THREE.Vector3(x, 100, z),
          new THREE.Vector3(0, -1, 0)
        );
        const hits = raycaster.intersectObject(modelRef.current, true);
        if (hits.length) y = hits[0].point.y;
      }

      if (y === null) throw new Error("Raycast failed");

      setTargetPosition([x, y, z]);
      setShouldAnimate(true);
      setIsResetting(false);

      await donePromise;
    } catch {
      setErrorMessage(t("errors.searchFailed"));
      setTimeout(() => setErrorMessage(""), 5000);
      handleReset();
    }
  };

  return (
    <div className="fixed w-screen h-full bg-background">
      {errorMessage && (
        <div className="fixed top-1/6 left-1/2 transform -translate-x-1/2 z-50 bg-primary/50 border border-primary backdrop-blur-lg text-white px-4 py-2 rounded-2xl animate-in fade-in text-sm slide-in-from-top-2 duration-300 text-center">
          {errorMessage}
        </div>
      )}

      <Header />

      {isModelLoaded && isSplashReady ? (
        <Welcome onTimeout={handleReset} />
      ) : (
        <Splash />
      )}

      <Information
        isVisible={Boolean(searchResult)}
        result={searchResult}
        onPhotoLoaded={() => setIsPhotoLoaded(true)}
      />

      <Search
        query={query}
        setQuery={setQuery}
        onSearch={handleSearch}
        onReset={handleReset}
        isSearchComplete={isSearchComplete}
      />

      {searchResult && (
        <ViewModeSelector viewMode={viewMode} onViewModeChange={setViewMode} />
      )}

      <Canvas
        camera={{ position: INITIAL_CAMERA_POSITION, fov: 40 }}
        onPointerDown={handlePointerDown}
        onPointerUp={handlePointerUp}
      >
        <ModelLights />
        <Model onLoad={() => setIsModelLoaded(true)} modelRef={modelRef} />
        {circleVisible && targetPosition && (
          <Marker position={targetPosition} />
        )}
        <Camera
          targetPosition={targetPosition}
          shouldAnimate={shouldAnimate}
          isResetting={isResetting}
          onAnimationComplete={handleAnimationComplete}
        />
      </Canvas>

      {searchResult && viewMode === "2D" && (
        <div
          className="fixed bg-background inset-0 w-full h-full cursor-pointer animate-in z-30 fade-in duration-500"
          onClick={() => setIsNavigating(!isNavigating)}
        >
          <Image
            src="/left-marked.png"
            alt="2D View"
            fill
            className="object-contain"
            priority
          />
        </div>
      )}
    </div>
  );
}
