"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Item,
  ItemActions,
  ItemContent,
  ItemDescription,
  ItemGroup,
  ItemSeparator,
  ItemTitle,
} from "@/components/ui/item";
import {
  Pagination,
  PaginationContent,
  PaginationItem,
} from "@/components/ui/pagination";
import useFetch from "@/contexts/fetch-context";
import { useLanguage } from "@/contexts/language-context";
import { clsx } from "clsx";
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  Loader2,
  MessageSquareX,
  Search,
  X,
} from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface FeedbackResult {
  resultId: string;
  personId: string;
  personName: string;
  feedback: string;
  createdAt: string;
}

interface FeedbackResponse {
  data: FeedbackResult[];
  page: number;
  totalPages: number;
  total: number;
}

function Dashboard() {
  const { t } = useLanguage();
  const router = useRouter();
  const { data, loading, fetch: fetchResults } = useFetch("GET", "results/");

  const [searchQuery, setSearchQuery] = useState<string>("");
  const [searchInput, setSearchInput] = useState<string>("");
  const [currentPage, setCurrentPage] = useState<number>(0);

  const response = data as FeedbackResponse | null;
  const feedbacks = response?.data ?? [];
  const totalPages = response?.totalPages ?? 0;
  const total = response?.total ?? 0;

  const doSearch = useCallback(
    (search: string, page: number) => {
      fetchResults({
        params: { search, page },
      });
    },
    [fetchResults],
  );

  const handleSearchSubmit = useCallback(() => {
    setSearchQuery(searchInput);
    setCurrentPage(0);
    doSearch(searchInput, 0);
  }, [searchInput, doSearch]);

  const handleSearchInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setSearchInput(e.target.value);
    },
    [],
  );

  const handleSearchKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Enter") {
        handleSearchSubmit();
      }
    },
    [handleSearchSubmit],
  );

  const handleClearSearch = useCallback(() => {
    setSearchInput("");
    setSearchQuery("");
    setCurrentPage(0);
    doSearch("", 0);
  }, [doSearch]);

  const handlePageChange = useCallback(
    (page: number) => {
      if (currentPage === page) return;

      setCurrentPage(page);
      doSearch(searchQuery, page);
    },
    [searchQuery, doSearch],
  );

  const handlePreviousPage = useCallback(() => {
    if (currentPage > 0) {
      handlePageChange(currentPage - 1);
    }
  }, [currentPage, handlePageChange]);

  const handleNextPage = useCallback(() => {
    if (currentPage < totalPages - 1) {
      handlePageChange(currentPage + 1);
    }
  }, [currentPage, totalPages, handlePageChange]);

  const handleLogout = useCallback(() => {
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    router.push("/auth");
  }, [router]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("tr-TR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  useEffect(() => {
    doSearch("", 0);
  }, []);

  return (
    <>
      <div className="fixed top-4 left-4 z-50">
        <Button size="sm" variant="secondary" onClick={handleLogout} className="rounded-full text-xs">
          {t("auth.logout")}
        </Button>
      </div>
      <article className="max-w-lg h-dvh grid grid-rows-[auto_auto_1fr_auto] w-full pb-4 pt-14 mx-auto gap-4">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-semibold text-gradient">
            {t("dashboard.title")}
          </h1>
          <p className="text-[0.65rem] font-semibold text-white bg-[#010101]/40 border-[#41424F]/80 border-2 px-3 py-1 rounded-full">
            {total} {t("dashboard.feedbacks")}
          </p>
        </div>

        <Item className="rounded-full p-1.5 border-2 border-[#41424F]/80 bg-[#010101]/40">
          <ItemContent className="relative flex items-center pr-4 gap-4 w-full">
            <Input
              type="text"
              placeholder={t("dashboard.searchPlaceholder")}
              value={searchInput}
              onChange={handleSearchInputChange}
              onKeyDown={handleSearchKeyDown}
              className="bg-transparent border-0 shadow-none text-white placeholder:text-[#5B5D6F] capitalize focus-visible:ring-0"
            />
            {searchInput.trim().length > 0 && (
              <X
                className="absolute top-1/2 right-0 -translate-y-1/2 text-white size-3.5 cursor-pointer hover:text-[#5B5D6F] transition-colors"
                onClick={handleClearSearch}
              />
            )}
          </ItemContent>
          <ItemActions>
            <Button
              size="icon"
              className="rounded-full cursor-pointer"
              disabled={loading}
              onClick={handleSearchSubmit}
            >
              {loading ? <Loader2 className="animate-spin" /> : <Search />}
            </Button>
          </ItemActions>
        </Item>

        <div className="w-full h-full flex justify-center items-center gap-1 overflow-auto">
          {loading ? (
            <div className="w-full mb-auto flex flex-col rounded-2xl border-2 border-[#41424F]/80 bg-[#1E1E24]/60 backdrop-blur-xl">
              <ItemGroup>
                {[0, 1, 2, 3, 4].map((_, index) => (
                  <div key={index}>
                    {index > 0 && (
                      <ItemSeparator className="h-2 bg-[#41424F]/50" />
                    )}
                    <Item className="p-4 gap-3 animate-pulse hover:bg-[#41424F]/20 transition-colors">
                      <ItemContent></ItemContent>
                    </Item>
                  </div>
                ))}
              </ItemGroup>
            </div>
          ) : feedbacks.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-16 gap-3">
              <MessageSquareX className="size-12 text-[#41424F]" />
              <p className="text-sm text-[#5B5D6F]">
                {t("dashboard.noResults")}
              </p>
            </div>
          ) : (
            <div className="w-full mb-auto flex flex-col rounded-2xl overflow-hidden border-2 border-[#41424F]/80 bg-[#1E1E24]/60 backdrop-blur-xl">
              <ItemGroup>
                {feedbacks.map((feedback, index) => (
                  <Item
                    key={index}
                    className="p-4 gap-3 hover:bg-[#41424F]/20 transition-colors rounded-none border-b border-[#41424F]/50 last:border-0"
                  >
                    <ItemContent className="gap-4 md:gap-2">
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2">
                          <ItemTitle className="text-white text-sm">
                            {feedback.personName}
                          </ItemTitle>
                          <p className="text-[0.65rem] font-semibold text-white bg-[#010101]/40 border-[#41424F]/80 border-2 px-3 py-1 rounded-full">
                            #{feedback.personId}
                          </p>
                        </div>
                        <p className="text-[#5B5D6F] text-xs">
                          {formatDate(feedback.createdAt)}
                        </p>
                      </div>
                      <ItemDescription className="text-white/70 text-xs leading-relaxed line-clamp-2 whitespace-pre-line">
                        {feedback.feedback}
                      </ItemDescription>
                    </ItemContent>
                  </Item>
                ))}
              </ItemGroup>
            </div>
          )}
        </div>

        {totalPages > 1 && (
          <Pagination>
            <PaginationContent className="gap-2">
              <PaginationItem>
                <Button
                  onClick={handlePreviousPage}
                  variant="secondary"
                  disabled={currentPage === 0}
                  className={clsx("rounded-full pl-2.5", {
                    "pointer-events-none": currentPage === 0,
                  })}
                >
                  <ChevronLeftIcon />
                  Previous
                </Button>
              </PaginationItem>

              {Array.from({ length: totalPages }, (_, i) => i).map((page) => (
                <PaginationItem key={page}>
                  <Button
                    size="icon"
                    onClick={() => handlePageChange(page)}
                    variant={currentPage === page ? "default" : "secondary"}
                    className={clsx("rounded-full", {
                      "pointer-events-none": currentPage === page,
                    })}
                  >
                    {page + 1}
                  </Button>
                </PaginationItem>
              ))}

              <PaginationItem>
                <Button
                  onClick={handleNextPage}
                  variant="secondary"
                  disabled={currentPage === totalPages - 1}
                  className={clsx("rounded-full pr-2.5", {
                    "pointer-events-none": currentPage === totalPages - 1,
                  })}
                >
                  Next
                  <ChevronRightIcon />
                </Button>
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        )}
      </article>
    </>
  );
}

export default Dashboard;
