import { useNavigation } from "@/contexts/navigation-context";
import { useLanguage } from "@/contexts/language-context";
import clsx from "clsx";
import { useState } from "react";
import Image from "next/image";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Maximize, Minimize } from "lucide-react";
import type { PersonSearchOut } from "@/lib/services/search";

const GRID_COLUMNS = 14;
const GRID_ROWS = 11;

function Information({
  isVisible,
  result,
  onPhotoLoaded,
}: {
  isVisible: boolean;
  result: PersonSearchOut | null;
  onPhotoLoaded?: () => void;
}) {
  const { isNavigating } = useNavigation();
  const { t } = useLanguage();

  const frameStyle = (() => {
    const row = result?.row;
    const column = result?.column;
    if (typeof row !== "number" || typeof column !== "number") return undefined;
    if (row < 0 || row >= GRID_ROWS || column < 0 || column >= GRID_COLUMNS) {
      return undefined;
    }

    const leftPct = (column / GRID_COLUMNS) * 100;
    const topPct = (row / GRID_ROWS) * 100;
    const widthPct = (1 / GRID_COLUMNS) * 100;
    const heightPct = (1 / GRID_ROWS) * 100;

    return {
      left: `${leftPct}%`,
      top: `${topPct}%`,
      width: `${widthPct}%`,
      height: `${heightPct}%`,
    } as const;
  })();

  return (
    <div
      className={clsx(
        "fixed z-50 top-12 right-0 p-4 transition-all duration-500",
        {
          "translate-x-full": isNavigating || !isVisible,
        }
      )}
    >
      <Card className="w-full h-full pt-4 pb-0 rounded-2xl gap-4 overflow-hidden bg-[#3F3F3F]/40 backdrop-blur-xl border border-[#535353]/80">
        <CardHeader className="px-4 gap-1 items-center text-center">
          <CardTitle className="text-md text-white">
            {result?.name
              ? `${t("information.title")}, ${result.name}`
              : t("information.title")}
          </CardTitle>
        </CardHeader>
        <CardContent className="overflow-hidden px-0">
          <div className="relative">
            <Image
              src={result?.url || "/preview.png"}
              alt=""
              width={500}
              height={500}
              className="w-full max-w-2xs h-full object-cover object-center rounded-xl"
              unoptimized={Boolean(result?.url)}
              onLoadingComplete={() => {
                if (result?.url) onPhotoLoaded?.();
              }}
            />

            {frameStyle && (
              <div
                className="pointer-events-none absolute border-3 border-white -translate-y-1"
                style={frameStyle}
              />
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default Information;
