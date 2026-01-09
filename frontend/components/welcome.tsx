"use client";

import Image from "next/image";
import { useEffect, useState, useRef, useCallback } from "react";
import { useLanguage } from "@/contexts/language-context";
import { Hand } from "lucide-react";

interface WelcomeProps {
  isModelLoaded: boolean;
  isUserInteracting: boolean;
  onInteraction: () => void;
}

export function Welcome({
  isModelLoaded,
  isUserInteracting,
  onInteraction,
}: WelcomeProps) {
  const { t } = useLanguage();
  const [isVisible, setIsVisible] = useState(false);
  const inactivityTimerRef = useRef<NodeJS.Timeout | null>(null);
  const lastInteractionTimeRef = useRef<number>(Date.now());

  useEffect(() => {
    if (isModelLoaded) {
      setIsVisible(true);
      lastInteractionTimeRef.current = Date.now();
    }
  }, [isModelLoaded]);

  const startInactivityTimer = useCallback(() => {
    if (inactivityTimerRef.current) {
      clearTimeout(inactivityTimerRef.current);
    }

    inactivityTimerRef.current = setTimeout(() => {
      const now = Date.now();
      const timeSinceLastInteraction = now - lastInteractionTimeRef.current;

      if (timeSinceLastInteraction >= 30000) {
        setIsVisible(true);
      }
    }, 30000);
  }, []);

  useEffect(() => {
    if (!isModelLoaded) return;

    if (isUserInteracting) {
      setIsVisible(false);
      lastInteractionTimeRef.current = Date.now();

      if (inactivityTimerRef.current) {
        clearTimeout(inactivityTimerRef.current);
        inactivityTimerRef.current = null;
      }
    } else if (!isVisible) {
      startInactivityTimer();
    }

    return () => {
      if (inactivityTimerRef.current) {
        clearTimeout(inactivityTimerRef.current);
      }
    };
  }, [isModelLoaded, isUserInteracting, isVisible, startInactivityTimer]);

  useEffect(() => {
    if (!isModelLoaded || isVisible) return;

    const handleInteraction = () => {
      lastInteractionTimeRef.current = Date.now();
      startInactivityTimer();
    };

    window.addEventListener("mousemove", handleInteraction);
    window.addEventListener("touchmove", handleInteraction);
    window.addEventListener("mousedown", handleInteraction);
    window.addEventListener("touchstart", handleInteraction);

    return () => {
      window.removeEventListener("mousemove", handleInteraction);
      window.removeEventListener("touchmove", handleInteraction);
      window.removeEventListener("mousedown", handleInteraction);
      window.removeEventListener("touchstart", handleInteraction);
    };
  }, [isModelLoaded, isVisible, startInactivityTimer]);

  return (
    <div
      className="fixed inset-0 z-100 pointer-events-none flex flex-col items-center justify-center backdrop-blur-md bg-background/80 transition-opacity duration-500 data-[state=show]:animate-in fade-in data-[state=hide]:animate-out fade-out fill-mode-forwards"
      onClick={onInteraction}
      onTouchStart={onInteraction}
      data-state={isVisible ? "show" : "hide"}
    >
      <div className="flex flex-col items-center gap-8 px-4">
        <Image
          src="/logo.svg"
          width={200}
          height={50}
          alt="Turkish Airlines 500th Aircraft Logo"
          className="w-auto h-16"
          priority
        />

        <h1 className="text-3xl md:text-4xl max-w-lg font-semibold text-white text-center">
          {t("welcome.title")}
        </h1>

        <div className="flex flex-col gap-6 items-center">
          <p className="text-lg md:text-xl text-white/90 text-center max-w-lg">
            {t("welcome.description")}
          </p>

          <div className="flex flex-col items-center">
            <Hand className="size-8 text-white animate-slide-right" />
          </div>
        </div>
      </div>
    </div>
  );
}
