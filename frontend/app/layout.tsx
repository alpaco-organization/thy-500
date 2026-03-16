import { LanguageProvider } from "@/contexts/language-context";
import { NavigationProvider } from "@/contexts/navigation-context";
import { TooltipProvider } from "@/components/ui/tooltip";
import type { Metadata } from "next";
import { Red_Hat_Display } from "next/font/google";
import "./globals.css";
import { NotificationProvider } from "@/contexts/notification-context";

const redHat = Red_Hat_Display({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700", "800", "900"],
  variable: "--font-red-hat",
});

export const metadata: Metadata = {
  title: "Turkish Airlines 500th Aircraft - TK Aile'de Sen de Varsın",
  description:
    "Türk Hava Yolları'nın 500. uçağı üzerinde yer alan binlerce fotoğraf arasından kendi fotoğrafını keşfet. Discover your photo among thousands of photos on Turkish Airlines' 500th aircraft.",
  icons: {
    icon: "/thy-logo.png",
  },
  viewport: {
    width: "device-width",
    initialScale: 1,
    interactiveWidget: "resizes-content",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html>
      <body className={redHat.variable}>
        <NotificationProvider>
          <LanguageProvider>
            <TooltipProvider>
              <NavigationProvider>{children}</NavigationProvider>
            </TooltipProvider>
          </LanguageProvider>
        </NotificationProvider>
      </body>
    </html>
  );
}
