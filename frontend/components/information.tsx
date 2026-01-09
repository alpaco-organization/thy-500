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

function Information({ isSearchComplete }: { isSearchComplete: boolean }) {
  const { isNavigating } = useNavigation();
  const { t } = useLanguage();

  const [isExpanded, setIsExpanded] = useState<boolean>(false);

  return (
    <div
      className={clsx(
        "fixed z-50 right-0 p-4 transition-all duration-500",
        {
          "w-full top-0 h-full": isExpanded,
          "w-sm top-12": !isExpanded,
        },
        {
          "translate-x-full": isNavigating || !isSearchComplete,
        }
      )}
    >
      <Card className="border-none w-full h-full py-4 rounded-2xl gap-4">
        <CardHeader className="px-4 gap-1">
          <CardTitle className="text-sm">{t("information.title")}</CardTitle>
          <CardDescription className="text-xs">
            {t("information.description")}
          </CardDescription>
          <CardAction>
            <Button
              variant="secondary"
              onClick={() => setIsExpanded(!isExpanded)}
              size="icon-sm"
            >
              {isExpanded ? (
                <Minimize className="size-4" />
              ) : (
                <Maximize className="size-4" />
              )}
            </Button>
          </CardAction>
        </CardHeader>
        <CardContent className="overflow-hidden px-4">
          <Image
            src="/preview.png"
            alt={t("information.imageAlt")}
            width={500}
            height={500}
            className="w-full h-full object-cover object-center rounded-xl border border-border"
          />
        </CardContent>
      </Card>
    </div>
  );
}

export default Information;