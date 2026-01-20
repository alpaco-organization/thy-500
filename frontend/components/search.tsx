"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Item, ItemActions, ItemContent } from "@/components/ui/item";
import { useLanguage } from "@/contexts/language-context";
import { useNavigation } from "@/contexts/navigation-context";
import clsx from "clsx";
import { Loader2, Search as SearchIcon, X } from "lucide-react";
import Image from "next/image";
import { useState } from "react";

type SearchType = "identity" | "fullName";

interface SearchProps {
  loading?: boolean;
  query: string;
  isSearchComplete?: boolean;
  onChange: (query: string) => void;
  onSubmit: (searchType: SearchType, query: string) => Promise<void>;
  onReset?: () => void;
}

export function Search({
  query,
  onChange,
  onSubmit,
  onReset,
  isSearchComplete = false,
  loading = false,
}: SearchProps) {
  const { isNavigating } = useNavigation();
  const { t } = useLanguage();

  const [searchType, setSearchType] = useState<SearchType>("fullName");
  const [isFocused, setIsFocused] = useState<boolean>(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    await onSubmit(searchType, query.trim());
  };

  const handleReset = () => {
    onReset?.();
  };
  
  const handleClear = () => {
    if (loading || isSearchComplete) return;

    onChange("");
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <>
      {isFocused && query && (
        <div className="fixed top-1/12 left-1/2 -translate-x-1/2 z-50 border-2 border-[#41424F]/80 bg-[#010101]/40 backdrop-blur-xl rounded-full px-6 py-2 animate-in fade-in slide-in-from-top-2 duration-300">
          <p className="capitalize text-white text-sm font-medium">{query}</p>
        </div>
      )}
      <div
        className={clsx(
          "fixed bottom-0 bg-[#1E1E24]/60 backdrop-blur-xl p-4 border-2 border-b-0 border-[#41424F]/80 rounded-t-3xl left-1/2 z-40 w-full md:max-w-lg flex px-4 flex-col gap-3 transition-transform duration-300 ease-in-out translate-x-[-50%]",
          isNavigating ? "translate-y-[calc(100%+1rem)]" : "translate-y-0",
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

        <Item className="rounded-full p-1.5 border-2 border-[#41424F]/80 bg-[#010101]/40">
          <ItemContent className="relative flex items-center pr-4 gap-4 w-full">
            <Input
              type={searchType === "identity" ? "number" : "text"}
              placeholder={
                searchType === "identity"
                  ? t("search.identityNumberPlaceholder")
                  : t("search.fullNamePlaceholder")
              }
              value={query}
              onChange={(e) => onChange(e.target.value)}
              onKeyDown={handleKeyDown}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setIsFocused(false)}
              disabled={loading || isSearchComplete}
              className="bg-transparent capitalize border-0 shadow-none text-white placeholder:text-[#5B5D6F]"
            />
            {query.trim().length > 0 && (
              <X
                data-disabled={loading || isSearchComplete}
                className="absolute top-1/2 right-0 -translate-y-1/2 text-white size-3.5 cursor-pointer hover:text-[#5B5D6F] transition-colors data-[disabled=true]:cursor-not-allowed data-[disabled=true]:text-[#5B5D6F]"
                onClick={handleClear}
              />
            )}
          </ItemContent>
          <ItemActions>
            {isSearchComplete && !loading ? (
              <Button className="rounded-full" onClick={handleReset}>
                {t("search.reset")}
              </Button>
            ) : (
              <Button
                size="icon"
                onClick={handleSearch}
                disabled={loading || !query.trim()}
                className="rounded-full cursor-pointer disabled:cursor-default"
              >
                {loading ? (
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
