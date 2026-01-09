import type { Metadata } from "next";
import { NavigationProvider } from "@/contexts/navigation-context";
import "./globals.css";
import { LanguageProvider } from "@/contexts/language-context";

export const metadata: Metadata = {
  title: "",
  description: "",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr">
      <body>
        <LanguageProvider>
          <NavigationProvider>
            {children}
          </NavigationProvider>
        </LanguageProvider>
      </body>
    </html>
  );
}
