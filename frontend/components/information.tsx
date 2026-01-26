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
import { MessageSquare } from "lucide-react";

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
    if (!result) {
      setIsVisible(false);
      setIsDialogOpen(false);
      setConfirmation(null);
      setFeedback("");
      return;
    }

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

  const handleDialogOpenChange = (open: boolean) => {
    setIsDialogOpen(open);

    if (open) return;

    handleCancelDialog();
  };

  const handleCancelDialog = () => {
    setIsDialogOpen(false);
    setFeedback("");
    setConfirmation(null);
    setIsVisible(false);
  };

  const handleWantToBeFound = () => {
    setIsDialogOpen(true);
  };

  return (
    <>
      <div
        className={clsx(
          "fixed z-50 top-0 left-1/2 flex justify-center -translate-x-1/2 px-4 transition-all duration-500",
          {
            "-translate-y-full": isDialogOpen || isNavigating || !isVisible,
            "translate-y-4": isVisible && !isNavigating && !isDialogOpen,
          },
        )}
      >
        <div className="bg-[#1E1E24]/80 border-2 backdrop-blur-xl border-[#41424F]/80 rounded-full p-2">
          <Button
            type="button"
            onClick={handleWantToBeFound}
            variant="default"
            size="icon"
            className="rounded-full w-14 h-14 animate-pulse-glow hover:animate-none hover:scale-110 transition-all duration-200"
          >
            <MessageSquare className="w-6 h-6" />
          </Button>
        </div>
      </div>

      <Dialog open={isDialogOpen} onOpenChange={handleDialogOpenChange}>
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
