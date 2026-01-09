"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search as SearchIcon, Loader2, User, IdCard, RotateCcw } from "lucide-react";
import { Item, ItemActions, ItemContent } from "@/components/ui/item";
import { useNavigation } from "@/contexts/navigation-context";
import { useLanguage } from "@/contexts/language-context";
import clsx from "clsx";

type SearchType = "identity" | "fullName";

interface SearchProps {
  onSearch: (searchType: SearchType, query: string) => Promise<void>;
  onReset?: () => void;
  isSearchComplete?: boolean;
}

export function Search({
  onSearch,
  onReset,
  isSearchComplete = false,
}: SearchProps) {
  const { isNavigating } = useNavigation();
  const { t } = useLanguage();

  const [searchType, setSearchType] = useState<SearchType>("fullName");
  const [query, setQuery] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsLoading(true);

    try {
      await onSearch(searchType, query.trim());
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setQuery("");
    setIsLoading(false);
    onReset?.();
  };

  return (
    <div
      className={clsx(
        "fixed bottom-4 left-1/2 z-40 w-full max-w-lg flex flex-col gap-3 transition-transform duration-300 ease-in-out translate-x-[-50%]",
        isNavigating ? "translate-y-[calc(100%+1rem)]" : "translate-y-0"
      )}
    >
      <div className="flex items-center gap-3 justify-start">
        <Button
          type="button"
          size="sm"
          onClick={() => setSearchType("fullName")}
          variant={searchType === "fullName" ? "default" : "secondary"}
          className={clsx("rounded-full text-xs", {
            "cursor-pointer": searchType !== "fullName",
          })}
        >
          <User className="size-4" />
          {t("search.fullName")}
        </Button>
        <Button
          type="button"
          size="sm"
          onClick={() => setSearchType("identity")}
          variant={searchType === "identity" ? "default" : "secondary"}
          className={clsx("rounded-full text-xs", {
            "cursor-pointer": searchType !== "identity",
          })}
        >
          <IdCard className="size-5" />
          {t("search.identityNumber")}
        </Button>
      </div>

      <Item className="bg-white rounded-full p-1.5">
        <ItemContent className="flex items-center gap-4 w-full">
          <Input
            type={searchType === "identity" ? "number" : "text"}
            placeholder={
              searchType === "identity"
                ? t("search.identityNumberPlaceholder")
                : t("search.fullNamePlaceholder")
            }
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading || isSearchComplete}
            className="bg-transparent border-0 shadow-none"
          />
        </ItemContent>
        <ItemActions>
          {isSearchComplete && !isLoading ? (
            <Button size="icon" className="rounded-full" onClick={handleReset}>
              <RotateCcw />
            </Button>
          ) : (
            <Button
              size="icon"
              className="rounded-full"
              onClick={handleSearch}
              disabled={isLoading || !query.trim()}
            >
              {isLoading ? <Loader2 className="animate-spin" /> : <SearchIcon />}
            </Button>
          )}
        </ItemActions>
      </Item>
    </div>
  );
}
