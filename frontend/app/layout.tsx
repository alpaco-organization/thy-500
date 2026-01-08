import type { Metadata } from "next";
import Header from "@/components/header";
import { NavigationProvider } from "@/contexts/navigation-context";
import "./globals.css";

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
        <NavigationProvider>
          <Header />
          {children}
        </NavigationProvider>
      </body>
    </html>
  );
}
