"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Field, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Spinner } from "@/components/ui/spinner";
import useFetch from "@/contexts/fetch-context";
import { useLanguage, LanguageSelector } from "@/contexts/language-context";

function Auth() {
  const [email, setEmail] = useState<string>("admin@alpaco.com");
  const [password, setPassword] = useState<string>("alpacothy500");
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const { fetch: loginFetch } = useFetch("POST", "auth/login");
  const { t } = useLanguage();

  const isDisabled = !email || !password || isLoading;

  const handleAuth = async () => {
    if (isDisabled) return;

    setIsLoading(true);

    await loginFetch({
      params: { email, password },
      onSuccess: (data: { access_token: string; token_type: string }) => {
        document.cookie = `token=${data.access_token}; path=/; max-age=86400`;
        window.location.href = "/dashboard";
      },
      onError: () => {
        setIsLoading(false);
      },
    });
  };

  return (
    <article className="relative">
      <FieldGroup className="flex flex-col gap-6 w-xs">
        <div className="flex flex-col items-center gap-2 text-center w-full">
          <h3 className="text-2xl font-medium text-gradient max-w-sm">
            {t("auth.title")}
          </h3>
          <p className="text-sm font-light text-white max-w-3xs">
            {t("auth.description")}
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email" className="text-xs text-white">
            {t("auth.email")}
          </FieldLabel>
          <Input
            id="email"
            type="email"
            placeholder={t("auth.emailPlaceholder")}
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="text-white placeholder:text-[#5B5D6F] rounded-full p-1.5 px-4 border-2 border-[#41424F]/80 bg-[#010101]/80"
          />
        </Field>
        <Field>
          <FieldLabel htmlFor="password" className="text-xs text-white">
            {t("auth.password")}
          </FieldLabel>
          <Input
            id="password"
            type="password"
            placeholder={t("auth.passwordPlaceholder")}
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="text-white placeholder:text-[#5B5D6F] rounded-full p-1.5 px-4 border-2 border-[#41424F]/80 bg-[#010101]/80"
          />
        </Field>
        <Field>
          <Button
            type="button"
            className="rounded-full"
            disabled={isDisabled}
            onClick={handleAuth}
          >
            {isLoading ? <Spinner /> : t("auth.login")}
          </Button>
        </Field>
      </FieldGroup>
    </article>
  );
}

export default Auth;
