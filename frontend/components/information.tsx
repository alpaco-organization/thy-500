import { useNavigation } from "@/contexts/navigation-context";
import { useLanguage } from "@/contexts/language-context";
import clsx from "clsx";
import Image from "next/image";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { PersonSearchOut } from "@/lib/services/search";

function Information({
  isVisible,
  result,
}: {
  isVisible: boolean;
  result: PersonSearchOut | null;
}) {
  const { isNavigating } = useNavigation();
  const { t } = useLanguage();

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
      </Card>
    </div>
  );
}

export default Information;