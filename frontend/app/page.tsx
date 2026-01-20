"use client";

import Header from "@/components/header";
import Information from "@/components/information";
import { Search } from "@/components/search";
import { Splash } from "@/components/splash";
import { Welcome } from "@/components/welcome";
import { useLanguage } from "@/contexts/language-context";
import { useNavigation } from "@/contexts/navigation-context";
import useFetch from "@/contexts/fetch-context";
import { OrbitControls, useGLTF } from "@react-three/drei";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { useEffect, useRef, useState } from "react";
import type { IPerson, SearchType } from "@/types/person";
import * as THREE from "three";

const INITIAL_CAMERA_POSITION: [number, number, number] = [54, 8, 33];
const CENTER_POSITION: [number, number, number] = [0, 0, 0];
const MARKER_RADIUS = 0.5;

function Model({
  onLoad,
  modelRef,
}: {
  onLoad?: () => void;
  modelRef?: React.MutableRefObject<THREE.Object3D | null>;
}) {
  const { scene } = useGLTF("/model.glb");

  useEffect(() => {
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
      targetControlsPos.current = CENTER_POSITION;
      setIsAnimating(true);
    } else if (shouldAnimate && targetPosition) {
      const [x, y, z] = targetPosition;

      const distance = 2;
      const verticalAngle = Math.PI / 6;

      const horizontalAngle = x < 0 ? Math.PI / 4 + Math.PI : -Math.PI / 4;

      const camX =
        x + distance * Math.cos(verticalAngle) * Math.cos(horizontalAngle);
      const camY = y + distance * Math.sin(verticalAngle);
      const camZ =
        z + distance * Math.cos(verticalAngle) * Math.sin(horizontalAngle);

      targetCameraPos.current = [camX, camY, camZ];
      targetControlsPos.current = targetPosition;
      setIsAnimating(true);
    }
  }, [targetPosition, shouldAnimate, isResetting, camera]);

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
          Math.pow(tz - camera.position.z, 2),
      );

      const distanceToTarget = Math.sqrt(
        Math.pow(cx - controlsRef.current.target.x, 2) +
          Math.pow(cy - controlsRef.current.target.y, 2) +
          Math.pow(cz - controlsRef.current.target.z, 2),
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
      minDistance={2}
      maxDistance={80}
    />
  );
}

function Marker({ position }: { position: [number, number, number] }) {
  return (
    <group position={position}>
      <mesh>
        <sphereGeometry args={[MARKER_RADIUS * 0.6, 32, 32]} />
        <meshBasicMaterial color="#00ff00" transparent opacity={0.3} />
      </mesh>
    </group>
  );
}

function Background() {
  return (
    <video
      autoPlay
      loop
      muted
      playsInline
      className="fixed top-0 left-0 w-full h-full object-cover -z-10"
    >
      <source src="/background.mp4" type="video/mp4" />
    </video>
  );
}

export default function Home() {
  const { setIsNavigating } = useNavigation();
  const { t } = useLanguage();

  const { fetch: doSearch, loading } = useFetch("GET", "search");

  const searchCompleteResolverRef = useRef<null | (() => void)>(null);
  const modelRef = useRef<THREE.Object3D | null>(null);

  const [targetPosition, setTargetPosition] = useState<
    [number, number, number] | null
  >(null);
  const [shouldAnimate, setShouldAnimate] = useState<boolean>(false);
  const [isResetting, setIsResetting] = useState<boolean>(false);
  const [isModelLoaded, setIsModelLoaded] = useState<boolean>(false);
  const [isSearchComplete, setIsSearchComplete] = useState<boolean>(false);
  const [circleVisible, setCircleVisible] = useState<boolean>(false);
  const [searchResult, setSearchResult] = useState<IPerson | null>(null);
  const [isAnimationDone, setIsAnimationDone] = useState<boolean>(false);

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
    setQuery("");
  };

  const handleAnimationComplete = () => {
    setIsResetting(false);
    setShouldAnimate(false);
    setIsAnimationDone(true);
  };

  useEffect(() => {
    const ready = Boolean(targetPosition) && isAnimationDone;

    setCircleVisible(ready);
    setIsSearchComplete(ready);

    if (ready) {
      searchCompleteResolverRef.current?.();
      searchCompleteResolverRef.current = null;
    }
  }, [targetPosition, isAnimationDone]);

  const handleSearch = async (searchType: SearchType, query: string) => {
    setIsAnimationDone(false);
    setCircleVisible(false);
    setIsSearchComplete(false);

    await doSearch({
      params: { searchType, query },
      onSuccess: (result: IPerson) => {
        setSearchResult(result);

        const x = result.x;
        const y = result.y;
        const z = result.z;

        const coords: [number, number, number] = [x, y, z];

        setTargetPosition(coords);
        setShouldAnimate(true);
        setIsResetting(false);

        searchCompleteResolverRef.current?.();
        searchCompleteResolverRef.current = null;
      },
      onError: (error: string) => {
        //TODO: Refactor error handling
        if (error.includes("404")) {
          setErrorMessage(t("errors.personNotFound").replace("{query}", query));
        } else {
          setErrorMessage(error || t("errors.searchFailed"));
        }
        setTimeout(() => setErrorMessage(""), 5000);
        handleReset();
      },
    });
  };

  const handlePointerDown = () => {
    setIsNavigating(true);
  };

  const handlePointerUp = () => {
    setIsNavigating(false);
  };

  return (
    <div className="fixed w-screen h-full bg-pattern bg-cover bg-center bg-no-repeat">
      {/* <Background /> */}
{/* 
      {errorMessage && (
        <div className="fixed top-1/6 left-1/2 transform -translate-x-1/2 z-50 bg-primary/50 border border-primary backdrop-blur-lg text-white px-4 py-2 rounded-2xl animate-in fade-in text-sm slide-in-from-top-2 duration-300 text-center">
          {errorMessage}
        </div>
      )} */}

      <Header />
      {isModelLoaded && isSplashReady ? (
        <Welcome onTimeout={handleReset} />
      ) : (
        <Splash />
      )}

      <Information isVisible={Boolean(false)} result={searchResult} />

      <Search
        loading={loading}
        query={query}
        onChange={(value) => setQuery(value)}
        onSubmit={handleSearch}
        onReset={handleReset}
        isSearchComplete={isSearchComplete}
      />

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
    </div>
  );
}
