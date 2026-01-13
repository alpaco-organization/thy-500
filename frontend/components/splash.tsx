"use client";

import { useState, useRef, useEffect } from "react";
import Image from "next/image";

export function Splash() {
  const [videoEnded, setVideoEnded] = useState<boolean>(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleEnded = () => setVideoEnded(true);

    video.addEventListener("ended", handleEnded);

    const safetyTimeout = setTimeout(() => {
      setVideoEnded(true);
    }, 12000);

    return () => {
      video.removeEventListener("ended", handleEnded);
      clearTimeout(safetyTimeout);
    };
  }, []);

  return (
    <div className="fixed inset-0 z-100 flex items-center justify-center bg-background">
      {!videoEnded && (
        <video
          ref={videoRef}
          src="/splash.mp4"
          autoPlay
          muted
          playsInline
          preload="auto"
          className="w-full h-full object-cover"
        />
      )}

      {videoEnded && (
        <div className="relative h-52 w-52">
          <div className="absolute inset-0 rounded-full bg-white/10 animate-ping" />
          <Image
            src="/logo.svg"
            width={200}
            height={50}
            alt="Turkish Airlines 500th Aircraft Logo"
            className="h-24 w-auto animate-in fade-in"
          />
        </div>
      )}
    </div>
  );
}