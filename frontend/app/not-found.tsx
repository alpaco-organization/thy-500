"use client";

import { Button } from "@/components/ui/button";
import { useLanguage } from "@/contexts/language-context";
import Image from "next/image";
import Link from "next/link";

export default function NotFound() {
  const { t } = useLanguage();

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
          <h1 className="text-8xl uppercase md:text-9xl font-semibold text-gradient text-center">
            {t("notFound.title")}
          </h1>

          <h2 className="text-lg md:text-xl uppercase tracking-[0.6rem] font-light text-gradient text-center">
            {t("notFound.subtitle")}
          </h2>

          <p className="text-lg md:text-xl font-light text-white text-center max-w-xl">
            {t("notFound.description")}
          </p>
        </div>

        <Link href="/">
          <Button size="lg" className="rounded-full cursor-pointer">
            {t("notFound.home")}
          </Button>
        </Link>
      </div>
    </div>
  );
}
