"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Item, ItemActions, ItemContent } from "@/components/ui/item";
import { useLanguage } from "@/contexts/language-context";
import { useNavigation } from "@/contexts/navigation-context";
import clsx from "clsx";
import { Loader2, Search as SearchIcon } from "lucide-react";
import Image from "next/image";
import { useState } from "react";

type SearchType = "identity" | "fullName";

interface SearchProps {
  query: string;
  setQuery: (query: string) => void;
  onSearch: (searchType: SearchType, query: string) => Promise<void>;
  onReset?: () => void;
  isSearchComplete?: boolean;
}

export function Search({
  query,
  setQuery,
  onSearch,
  onReset,
  isSearchComplete = false,
}: SearchProps) {
  const { isNavigating } = useNavigation();
  const { t } = useLanguage();

  const [searchType, setSearchType] = useState<SearchType>("fullName");
  const [isLoading, setIsLoading] = useState(false);
  const [isFocused, setIsFocused] = useState(false);

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
    setIsLoading(false);
    onReset?.();
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <>
      {isFocused && query && (
        <div className="fixed top-[15%] left-1/2 -translate-x-1/2 z-50 bg-[#3F3F3F]/40 backdrop-blur-xl border border-white/40 rounded-full px-6 py-2 animate-in fade-in slide-in-from-top-2 duration-300">
          <p className="capitalize text-white text-sm font-medium">{query}</p>
        </div>
      )}
      <div
        className={clsx(
          "fixed bottom-0 bg-[#3F3F3F]/40 backdrop-blur-xl p-4 border border-b-0 border-[#535353]/80 rounded-t-3xl left-1/2 z-40 w-full md:max-w-lg flex px-4 flex-col gap-3 transition-transform duration-300 ease-in-out translate-x-[-50%]",
          isNavigating ? "translate-y-[calc(100%+1rem)]" : "translate-y-0"
        )}
      >
        <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-6 justify-center">
          <Button
            type="button"
            size="sm"
            onClick={() => setSearchType("fullName")}
            variant={searchType === "fullName" ? "default" : "secondary"}
            className={clsx("rounded-full text-xs", {
              "cursor-pointer": searchType !== "fullName",
            })}
          >
            {t("search.fullName")}
          </Button>
          <p className="text-xs italic text-white">{t("search.or")}</p>
          <Button
            type="button"
            size="sm"
            onClick={() => setSearchType("identity")}
            variant={searchType === "identity" ? "default" : "secondary"}
            className={clsx("rounded-full text-xs", {
              "cursor-pointer": searchType !== "identity",
            })}
          >
            <Image
              src="/thy-logo.png"
              alt="THY Logo"
              width={50}
              height={50}
              className="inline-block size-4"
            />
            {t("search.identityNumber")}
          </Button>
        </div>

        <Item className="rounded-full p-1.5 border-white/40 bg-white/10">
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
              onKeyDown={handleKeyDown}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              disabled={isLoading || isSearchComplete}
              className="bg-transparent capitalize border-0 shadow-non text-white placeholder:text-white/40"
            />
          </ItemContent>
          <ItemActions>
            {isSearchComplete && !isLoading ? (
              <Button className="rounded-full" onClick={handleReset}>
                {t("search.reset")}
              </Button>
            ) : (
              <Button
                size="icon"
                onClick={handleSearch}
                disabled={isLoading || !query.trim()}
                className="rounded-full cursor-pointer disabled:cursor-default"
              >
                {isLoading ? (
                  <Loader2 className="animate-spin" />
                ) : (
                  <SearchIcon />
                )}
              </Button>
            )}
          </ItemActions>
        </Item>
      </div>
    </>
  );
}
