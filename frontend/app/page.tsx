"use client";

import { Canvas, useThree, useFrame, type RootState } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";
import { useState, useRef, useEffect } from "react";
import { Search } from "@/components/search";
import { Splash } from "@/components/splash";
import { Welcome } from "@/components/welcome";
import { useNavigation } from "@/contexts/navigation-context";
import { useLanguage } from "@/contexts/language-context";
import * as THREE from "three";
import Information from "@/components/information";
import {
  searchPerson,
  ApiError,
  type PersonSearchOut,
  type SearchType,
} from "@/lib/services/search";
import Header from "@/components/header";

const INITIAL_CAMERA_POSITION: [number, number, number] = [54, 8, 33];
const INITIAL_MODEL_POSITION: [number, number, number] = [0, 0, 0];

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

function Model({ onLoad }: { onLoad?: () => void }) {
  const { scene } = useGLTF("/model.glb");

  useEffect(() => {
    onLoad?.();
  }, [onLoad]);

  return <primitive object={scene} position={INITIAL_MODEL_POSITION} />;
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
      targetControlsPos.current = INITIAL_MODEL_POSITION;
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
      minDistance={10}
      maxDistance={80}
    />
  );
}

function CircleMarker({ position }: { position: [number, number, number] }) {
  const meshRef = useRef<THREE.Mesh | null>(null);

  useFrame((state: RootState) => {
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
  const { t } = useLanguage();

  const searchCompleteResolverRef = useRef<null | (() => void)>(null);

  const [targetPosition, setTargetPosition] = useState<
    [number, number, number] | null
  >(null);
  const [shouldAnimate, setShouldAnimate] = useState<boolean>(false);
  const [isResetting, setIsResetting] = useState<boolean>(false);
  const [isModelLoaded, setIsModelLoaded] = useState<boolean>(false);
  const [isSearchComplete, setIsSearchComplete] = useState<boolean>(false);
  const [circleVisible, setCircleVisible] = useState<boolean>(false);
  const [searchResult, setSearchResult] = useState<PersonSearchOut | null>(
    null
  );
  const [isAnimationDone, setIsAnimationDone] = useState<boolean>(false);
  const [isPhotoLoaded, setIsPhotoLoaded] = useState<boolean>(false);
  const [query, setQuery] = useState<string>("");
  const [isSplashReady, setIsSplashReady] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsSplashReady(true);
    }, 5000);

    return () => clearTimeout(timer);
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
  };

  const handleAnimationComplete = () => {
    setIsResetting(false);
    setShouldAnimate(false);
    setIsAnimationDone(true);
  };

  useEffect(() => {
    const ready = Boolean(targetPosition) && isAnimationDone && isPhotoLoaded;
    setCircleVisible(ready);
    setIsSearchComplete(ready);

    if (ready) {
      searchCompleteResolverRef.current?.();
      searchCompleteResolverRef.current = null;
    }
  }, [targetPosition, isAnimationDone, isPhotoLoaded]);

  const handleSearch = async (searchType: SearchType, query: string) => {
    const donePromise = new Promise<void>((resolve) => {
      searchCompleteResolverRef.current = resolve;
    });

    setIsAnimationDone(false);
    setIsPhotoLoaded(false);
    setCircleVisible(false);
    setIsSearchComplete(false);

    try {
      const result = await searchPerson({ searchType, query });
      await preloadImage(result.url);
      setIsPhotoLoaded(true);
      setSearchResult(result);

      // Map 2D coords to the 3D scene: x -> x, y -> z, keep y (height) constant.
      console.log("Search result:", result);
      const coords: [number, number, number] = [result.x % 5, 3, result.y % 5];

      setTargetPosition(coords);
      setShouldAnimate(true);
      setIsResetting(false);

      await donePromise;
    } catch (error: unknown) {
      if (error instanceof ApiError) {
        if (error.status === 404) {
          setErrorMessage(
            t("errors.personNotFound").replace("{query}", query)
          );
        } else {
          // Prefer a stable, translated message; ApiError.message is generic (e.g. "Search failed").
          setErrorMessage(t("errors.searchFailed"));
        }
      } else if (error instanceof Error) {
        // Fallback if something else throws a useful message.
        setErrorMessage(error.message || t("errors.searchFailed"));
      } else {
        setErrorMessage(t("errors.unknown"));
      }
      setTimeout(() => setErrorMessage(""), 5000);
      handleReset();
    }
  };

  const handlePointerDown = () => {
    setIsNavigating(true);
  };

  const handlePointerUp = () => {
    setIsNavigating(false);
  };

  return (
    <div className="fixed w-screen h-full bg-background">
      {errorMessage && (
        <div className="fixed top-1/6 left-1/2 transform -translate-x-1/2 z-50 bg-primary/50 border border-primary backdrop-blur-lg text-white px-4 py-2 rounded-2xl animate-in fade-in text-sm slide-in-from-top-2 duration-300">
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

      <Canvas
        camera={{ position: INITIAL_CAMERA_POSITION, fov: 40 }}
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
