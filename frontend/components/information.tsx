"use client";

import { useNavigation } from "@/contexts/navigation-context";
import { useLanguage } from "@/contexts/language-context";
import { useNotification } from "@/contexts/notification-context";
import clsx from "clsx";
import { Button } from "@/components/ui/button";
import { Item, ItemContent } from "@/components/ui/item";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { IPerson } from "@/types/person";
import { useEffect, useState } from "react";
import useFetch from "@/contexts/fetch-context";
import { Spinner } from "./ui/spinner";

const INFORMATION_TIMEOUT = 2000;

interface IConfirmationOrFeedback {
  personId: string;
  personName: string;
  matchCorrect?: boolean;
  feedback?: string;
}

function Information({ result }: { result: IPerson | null }) {
  const { isNavigating } = useNavigation();
  const { t } = useLanguage();
  const { showNotification } = useNotification();

  const { fetch: sendUserConfirmOrFeedback, loading: isSending } = useFetch(
    "POST",
    "results/",
  );

  const [isVisible, setIsVisible] = useState<boolean>(false);
  const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false);
  const [confirmation, setConfirmation] = useState<boolean | null>(null);
  const [feedback, setFeedback] = useState<string>("");

  useEffect(() => {
    if (!result) return;

    const timer = setTimeout(() => {
      setIsVisible(true);
    }, INFORMATION_TIMEOUT);

    return () => clearTimeout(timer);
  }, [result]);

  const handleConfirmation = async (isConfirmed: boolean) => {
    if (!result) return;

    setConfirmation(isConfirmed);

    const confirmationData: IConfirmationOrFeedback = {
      personId: result.personId || "",
      personName: result.name || "",
      matchCorrect: isConfirmed,
    };

    await sendUserConfirmOrFeedback({
      params: confirmationData,
      onSuccess: () => setIsDialogOpen(true),
    });
  };

  const handleSubmitFeedback = async () => {
    if (!result || feedback.trim() === "") return;

    const feedbackData: IConfirmationOrFeedback = {
      personId: result.personId || "",
      personName: result.name || "",
      feedback: feedback,
    };

    await sendUserConfirmOrFeedback({
      params: feedbackData,
      onSuccess: () => {
        setIsDialogOpen(false);
        setIsVisible(false);
        setConfirmation(null);
        setFeedback("");

        showNotification(t("information.thankYouFeedback"), "success");
      },
    });
  };
  const handleCancelDialog = () => {
    setIsDialogOpen(false);
    setFeedback("");
    setConfirmation(null);
    setIsVisible(false);
  };

  return (
    <>
      <div
        className={clsx(
          "fixed z-50 top-0 left-1/2 max-w-md -translate-x-1/2 px-4 transition-all duration-500 w-full",
          {
            "-translate-y-full": isDialogOpen || isNavigating || !isVisible,
            "translate-y-4": isVisible && !isNavigating && !isDialogOpen,
          },
        )}
      >
        <Item className="rounded-2xl p-4 border-2 border-[#41424F]/80 bg-[#1E1E24]/60 backdrop-blur-xl">
          <ItemContent className="flex flex-col gap-6 w-full">
            <div className="flex flex-col gap-2 items-center text-center">
              <h3 className="text-lg md:text-lg font-medium text-gradient max-w-sm">
                {`${t("information.question")}`}
              </h3>
              <p className="text-sm font-light text-white max-w-xs">
                {t("information.instruction")}
              </p>
            </div>

            <div className="grid grid-cols-2 gap-2 items-center">
              <Button
                type="button"
                onClick={() => handleConfirmation(false)}
                variant="secondary"
                className="flex-1 rounded-full"
              >
                {isSending && !confirmation ? (
                  <Spinner className="size-4" />
                ) : (
                  t("information.no")
                )}
              </Button>
              <Button
                type="button"
                onClick={() => handleConfirmation(true)}
                variant="default"
                className="flex-1 rounded-full"
              >
                {isSending && confirmation ? (
                  <Spinner className="size-4" />
                ) : (
                  t("information.yes")
                )}
              </Button>
            </div>
          </ItemContent>
        </Item>
      </div>

      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="bg-[#1E1E24]/60 backdrop-blur-xl p-4 border-2 border-[#41424F]/80 text-white rounded-2xl max-w-sm!">
          <DialogHeader>
            <DialogTitle className="font-semibold text-gradient">
              {t("information.feedbackTitle")}
            </DialogTitle>
            <DialogDescription className="text-white font-light mt-1">
              {t("information.feedbackDescription")}
            </DialogDescription>
          </DialogHeader>
          <div className="grid gap-4">
            <Textarea
              placeholder={t("information.feedbackPlaceholder")}
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
              className="min-h-48 rounded-2xl p-4 border-2 border-[#41424F]/80! bg-[#010101]/40 text-white placeholder:text-[#5B5D6F] resize-none outline-none"
            />
          </div>
          <DialogFooter className="flex gap-2">
            <Button
              type="button"
              variant="secondary"
              onClick={handleCancelDialog}
              className="rounded-full"
            >
              {t("information.cancel")}
            </Button>
            <Button
              type="button"
              onClick={handleSubmitFeedback}
              disabled={!feedback.trim()}
              className="rounded-full"
            >
              {isSending ? (
                <Spinner className="size-4" />
              ) : (
                t("information.submit")
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}

export default Information;
