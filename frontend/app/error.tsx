"use client";

import { Button } from "@/components/ui/button";
import { useLanguage } from "@/contexts/language-context";
import Image from "next/image";
import { useEffect } from "react";

interface ErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function Error({ error, reset }: ErrorProps) {
  const { t } = useLanguage();

  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="fixed inset-0 z-100 flex flex-col items-center justify-center backdrop-blur-md bg-background/80 px-4">
      <div className="flex flex-col items-center gap-8 pointer-events-auto">
        <Image
          src="/logo.svg"
          width={200}
          height={50}
          alt="Turkish Airlines 500th Aircraft Logo"
          className="w-auto h-10"
          priority
        />

        <div className="flex flex-col items-center gap-3 text-center">
          <h1 className="text-8xl md:text-9xl font-semibold text-gradient text-center">
            {t("error.title")}
          </h1>

          <h2 className="text-lg md:text-xl uppercase tracking-[0.6rem] font-light text-gradient text-center">
            {t("error.subtitle")}
          </h2>

          <p className="text-lg md:text-xl font-light text-white text-center max-w-xl">
            {t("error.description")}
          </p>
        </div>

        <Button
          onClick={reset}
          size="lg"
          className="rounded-full cursor-pointer"
        >
          {t("error.retry")}
        </Button>
      </div>
    </div>
  );
}
