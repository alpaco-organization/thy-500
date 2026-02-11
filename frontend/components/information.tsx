"use client";

import { useNavigation } from "@/contexts/navigation-context";
import { useLanguage } from "@/contexts/language-context";
import { useNotification } from "@/contexts/notification-context";
import clsx from "clsx";
import { Button } from "@/components/ui/button";
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
import { MessageSquareText } from "lucide-react";
import { Input } from "./ui/input";

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

  const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false);
  const [feedback, setFeedback] = useState<string>("");
  const [fullName, setFullName] = useState<string>("");
  const [personId, setPersonId] = useState<string>("");

  const resetForm = () => {
    setFeedback("");
    setFullName("");
    setPersonId("");
  };

  const handleSubmitFeedback = async () => {
    if (feedback.trim() === "") return;

    const feedbackData: IConfirmationOrFeedback = {
      personId: result?.personId || personId,
      personName: result?.name || fullName,
      feedback: feedback,
    };

    await sendUserConfirmOrFeedback({
      params: feedbackData,
      onSuccess: () => {
        setIsDialogOpen(false);
        resetForm();

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
    resetForm();
  };

  const handleWantToBeFound = () => {
    setIsDialogOpen(true);
  };

  useEffect(() => {
    if (!result) {
      setIsDialogOpen(false);
      resetForm();
      return;
    }
  }, [result]);

  const isValidated =
    !feedback.trim() || (!result && (!fullName.trim() || !personId.trim()));

  return (
    <>
      <div
        className={clsx(
          "fixed z-50 top-0 lg:top-[initial] left-1/2 lg:left-[initial] lg:bottom-4 lg:right-0 flex justify-center -translate-x-1/2 transition-all duration-500",
          {
            "-translate-y-full lg:translate-y-0 lg:translate-x-full":
              isDialogOpen || isNavigating,
            "translate-y-4 lg:translate-y-0 lg:-translate-x-4":
              !isNavigating && !isDialogOpen,
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
            <MessageSquareText className="size-6" />
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
            {!result && (
              <>
                <Input
                  placeholder={t("information.fullNamePlaceholder")}
                  value={fullName}
                  type="text"
                  onChange={(e) => setFullName(e.target.value)}
                  className="rounded-2xl h-auto px-4 py-2 border-2 border-[#41424F]/80! bg-[#010101]/40 text-white placeholder:text-[#5B5D6F] resize-none outline-none"
                />
                <Input
                  placeholder={t("information.personIdPlaceholder")}
                  value={personId}
                  type="number"
                  onChange={(e) => setPersonId(e.target.value)}
                  className="rounded-2xl px-4 py-2 h-auto border-2 border-[#41424F]/80! bg-[#010101]/40 text-white placeholder:text-[#5B5D6F] resize-none outline-none"
                />
              </>
            )}
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
              disabled={isValidated || isSending}
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
