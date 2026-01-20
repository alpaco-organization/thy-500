"use client";

import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { useLanguage } from "@/contexts/language-context";
import { clsx } from "clsx";
import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";

const STORAGE_KEY = "welcome_approved";
const INACTIVITY_TIMEOUT = 5000;
const appMode = process.env.NEXT_PUBLIC_APP_MODE || "default";

interface WelcomeProps {
  onTimeout: () => void;
}

export function Welcome({ onTimeout }: WelcomeProps) {
  const { t } = useLanguage();

  const isAgreementsExist =
    Boolean(process.env.NEXT_PUBLIC_GDPR_URL) &&
    Boolean(process.env.NEXT_PUBLIC_PRIVACY_POLICY_URL);

  const [isVisible, setIsVisible] = useState<boolean>(true);
  const [isApproved, setIsApproved] = useState<boolean>(
    isAgreementsExist ? false : true
  );
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
        setIsApproved(isAgreementsExist ? false : true);
        onTimeout();
      }
    }, INACTIVITY_TIMEOUT);
  }, [isAgreementsExist, onTimeout, appMode]);

  useEffect(() => {
    if (appMode !== "kiosk") return;

    const handleUserActivity = () => {
      lastInteractionTimeRef.current = Date.now();
      if (!isVisible) {
        startInactivityTimer();
      }
    };

    const events = ['click', 'keydown', 'scroll', 'touchstart', 'mousemove'];
    
    events.forEach(event => {
      window.addEventListener(event, handleUserActivity);
    });

    if (!isVisible) {
      startInactivityTimer();
    }

    return () => {
      events.forEach(event => {
        window.removeEventListener(event, handleUserActivity);
      });
      
      if (inactivityTimerRef.current) {
        clearTimeout(inactivityTimerRef.current);
      }
    };
  }, [isVisible, startInactivityTimer, appMode]);

  const handleApprove = () => {
    if (isAgreementsExist && !isApproved) return;

    if (isAgreementsExist && appMode === "default") {
      localStorage.setItem(STORAGE_KEY, "true");
    }

    setIsVisible(false);
  };

  if (appMode === "default" && localStorage.getItem(STORAGE_KEY) === "true")
    return null;

  return (
    <div
      className="fixed inset-0 z-100 flex flex-col items-center justify-center backdrop-blur-md bg-background/80 transition-opacity duration-500 data-[state=show]:animate-in fade-in data-[state=hide]:animate-out fade-out fill-mode-forwards data-[state=hide]:pointer-events-none data-[state=hide]:-z-1 px-4"
      data-state={isVisible ? "show" : "hide"}
    >
      <div className="flex flex-col items-center gap-8 pointer-events-auto">
        <Image
          src="/logo.svg"
          width={200}
          height={50}
          alt="Turkish Airlines 500th Aircraft Logo"
          className="w-auto h-12"
          priority
        />

        <div className="flex flex-col items-center gap-3 text-center">
          <h2 className="text-lg md:text-xl uppercase tracking-[0.6rem] font-light text-gradient text-center">
            {t("welcome.subtitle")}
          </h2>

          <h1 className="text-5xl leading-[1.15] uppercase md:text-6xl font-semibold text-gradient text-center max-w-3xl">
            {t("welcome.title")}
          </h1>
          <p className="text-lg md:text-xl font-light text-white text-center max-w-xl">
            {t("welcome.description")}
          </p>
        </div>

        <div className="flex flex-col gap-6 items-center w-full">
          {isAgreementsExist && (
            <div className="border-gradient rounded-2xl sm:rounded-full">
              <div className="flex items-start space-x-3 bg-background/90 border backdrop-blur-lg border-gold/40 py-4 px-6 rounded-2xl sm:rounded-full max-w-xl">
                <Checkbox
                  id="terms"
                  checked={isApproved}
                  onCheckedChange={(checked: boolean) =>
                    setIsApproved(checked === true)
                  }
                  className="mt-1"
                />
                <Label
                  htmlFor="terms"
                  className="text-sm flex-wrap text-white cursor-pointer leading-relaxed"
                >
                  {t("welcome.terms").split("{gdpr}")[0]}

                  <Link
                    href={process.env.NEXT_PUBLIC_GPDR_URL || "#"}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline underline-offset-4 hover:opacity-80 transition-colors"
                  >
                    {t("welcome.gdpr")}
                  </Link>

                  {t("welcome.terms").split("{gdpr}")[1].split("{privacy}")[0]}

                  <Link
                    href={process.env.NEXT_PUBLIC_PRIVACY_POLICY_URL || "#"}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline underline-offset-4 hover:opacity-80 transition-colors"
                  >
                    {t("welcome.privacy")}
                  </Link>

                  {t("welcome.terms").split("{privacy}")[1]}
                </Label>
              </div>
            </div>
          )}

          <Button
            onClick={handleApprove}
            size="lg"
            className={clsx("rounded-full", {
              "cursor-pointer": isApproved,
            })}
            disabled={isAgreementsExist && !isApproved}
          >
            {t("welcome.continue")}
          </Button>
        </div>
      </div>
    </div>
  );
}
