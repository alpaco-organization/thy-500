"use client";

import Image from "next/image";
import { useEffect, useState, useRef, useCallback } from "react";
import { useLanguage } from "@/contexts/language-context";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { useNavigation } from "@/contexts/navigation-context";
import { clsx } from "clsx";
import Link from "next/link";

const STORAGE_KEY = "welcome_approved";
const INACTIVITY_TIMEOUT = 30000;
const appMode = process.env.NEXT_PUBLIC_APP_MODE || "default";

interface WelcomeProps {
  onTimeout: () => void;
}

export function Welcome({ onTimeout }: WelcomeProps) {
  const { t } = useLanguage();
  const { isNavigating } = useNavigation();

  const [isVisible, setIsVisible] = useState<boolean>(
    appMode === "default" && localStorage.getItem(STORAGE_KEY) === "true"
      ? false
      : true
  );
  const [isApproved, setIsApproved] = useState<boolean>(false);
  const inactivityTimerRef = useRef<NodeJS.Timeout | null>(null);

  const lastInteractionTimeRef = useRef<number>(Date.now());

  useEffect(() => {
    if (appMode === "default") {
      const approved = localStorage.getItem(STORAGE_KEY);

      if (approved === "true") {
        setIsVisible(false);
        return;
      }
    }

    setIsVisible(true);
    lastInteractionTimeRef.current = Date.now();
  }, [appMode]);

  const startInactivityTimer = useCallback(() => {
    if (appMode !== "kiosk") return;

    if (inactivityTimerRef.current) {
      clearTimeout(inactivityTimerRef.current);
    }

    inactivityTimerRef.current = setTimeout(() => {
      const now = Date.now();
      const timeSinceLastInteraction = now - lastInteractionTimeRef.current;

      if (timeSinceLastInteraction >= INACTIVITY_TIMEOUT) {
        setIsVisible(true);
        setIsApproved(false);
        onTimeout();
      }
    }, INACTIVITY_TIMEOUT);
  }, [appMode]);

  useEffect(() => {
    if (isNavigating) {
      if (appMode !== "kiosk") {
        setIsVisible(false);
      }
      lastInteractionTimeRef.current = Date.now();

      if (inactivityTimerRef.current) {
        clearTimeout(inactivityTimerRef.current);
        inactivityTimerRef.current = null;
      }
    } else if (!isVisible && appMode === "kiosk") {
      lastInteractionTimeRef.current = Date.now();
      startInactivityTimer();
    }

    return () => {
      if (inactivityTimerRef.current) {
        clearTimeout(inactivityTimerRef.current);
      }
    };
  }, [isNavigating, isVisible, startInactivityTimer, appMode]);

  const handleApprove = () => {
    if (!isApproved) return;

    if (appMode === "default") {
      localStorage.setItem(STORAGE_KEY, "true");
    }

    setIsVisible(false);
  };

  if (appMode === "default" && localStorage.getItem(STORAGE_KEY) === "true")
    return null;

  return (
    <div
      className="fixed inset-0 z-100 flex flex-col items-center justify-center backdrop-blur-md bg-background/80 transition-opacity duration-500 data-[state=show]:animate-in fade-in data-[state=hide]:animate-out fade-out fill-mode-forwards data-[state=hide]:pointer-events-none data-[state=hide]:-z-1"
      data-state={isVisible ? "show" : "hide"}
    >
      <div className="flex flex-col items-center gap-8 px-4 max-w-2xl pointer-events-auto">
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

        <div className="flex flex-col gap-6 items-center w-full">
          <p className="text-lg md:text-xl text-white/90 text-center max-w-lg">
            {t("welcome.description")}
          </p>

          <div className="flex items-center space-x-3 bg-white/10 p-4 rounded-lg w-full max-w-lg">
            <Checkbox
              id="terms"
              checked={isApproved}
              onCheckedChange={(checked: boolean) =>
                setIsApproved(checked === true)
              }
            />
            <Label
              htmlFor="terms"
              className="text-sm text-white cursor-pointer leading-relaxed"
            >
              {t("welcome.terms").split("{gdpr}")[0]}

              <Link
                href="/gdpr"
                className="underline underline-offset-4 hover:opacity-80 transition-colors"
              >
                {t("welcome.gdpr")}
              </Link>

              {t("welcome.terms").split("{gdpr}")[1].split("{privacy}")[0]}

              <Link
                href="/privacy"
                className="underline underline-offset-4 hover:opacity-80 transition-colors"
              >
                {t("welcome.privacy")}
              </Link>

              {t("welcome.terms").split("{privacy}")[1]}
            </Label>
          </div>

          <Button
            onClick={handleApprove}
            size="lg"
            className={clsx("rounded-full", {
              "cursor-pointer": isApproved,
            })}
            disabled={!isApproved}
          >
            {t("welcome.continue")}
          </Button>
        </div>
      </div>
    </div>
  );
}
