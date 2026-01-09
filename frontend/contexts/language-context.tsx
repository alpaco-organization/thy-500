"use client";

import { Button } from "@/components/ui/button";
import translation from "@/data/translation.json";
import { clsx } from "clsx";
import { createContext, useContext, useEffect, useState } from "react";

interface LanguageContextTypes {
  currentLanguage: string;
  languages: Record<string, string>;
  changeLanguage: (languageCode: string) => void;
  t: (path: string) => string;
}

const LanguageContextDefaultValues: LanguageContextTypes = {
  currentLanguage: "tr",
  languages: { en: "English", tr: "Türkçe" },
  changeLanguage: () => {},
  t: () => "",
};

const LanguageContext = createContext<LanguageContextTypes>(
  LanguageContextDefaultValues
);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const languages = LanguageContextDefaultValues.languages;

  const [currentLanguage, setCurrentLanguage] = useState<string>(
    LanguageContextDefaultValues.currentLanguage
  );

  const changeLanguage = (languageCode: string) => {
    setCurrentLanguage(languageCode);
  };

  const t = (path: string): string => {
    const keys = path.split(".");
    let value: any = translation[currentLanguage as keyof typeof translation];

    for (const key of keys) {
      if (value && typeof value === "object" && key in value) {
        value = value[key];
      } else {
        return path;
      }
    }

    return typeof value === "string" ? value : path;
  };

  useEffect(() => {
    document.documentElement.setAttribute("lang", currentLanguage);
  }, [currentLanguage]);

  const value = {
    currentLanguage,
    languages,
    changeLanguage,
    t,
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}

export function LanguageSelector() {
  const { languages, currentLanguage, changeLanguage } = useLanguage();

  return (
    <div className="flex items-center gap-1.5 pointer-events-auto">
      {Object.entries(languages).map(([key, _]) => (
        <Button
         key={key}
          type="button"
          size="sm"
          onClick={() => changeLanguage(key)}
          variant={currentLanguage === key ? "default" : "secondary"}
          className={clsx("rounded-full text-xs", {
            "cursor-pointer": currentLanguage !== key,
          })}
        >
          {key.toUpperCase()}
        </Button>
      ))}
    </div>
  );
}
