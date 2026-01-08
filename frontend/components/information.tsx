import { useNavigation } from "@/contexts/navigation-context";
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

  const [isExpanded, setIsExpanded] = useState<boolean>(false);

  return (
    <div
      className={clsx(
        "fixed z-45 top-0 right-0 p-4 transition-all duration-500",
        {
          "w-full h-full": isExpanded,
          "w-sm": !isExpanded,
        },
        {
          "translate-x-full": isNavigating || !isSearchComplete,
        }
      )}
    >
      <Card className="border-none w-full h-full py-4 rounded-2xl gap-4">
        <CardHeader className="px-4 gap-1">
          <CardTitle className="text-sm">Sen de Bu Hikâyedesin</CardTitle>
          <CardDescription className="text-xs">
            Türk Hava Yolları’nın 500. uçağında senin bulunduğun alanı 2D olarak
            inceleyebilirsin.
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
            alt="Preview 2D Image"
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