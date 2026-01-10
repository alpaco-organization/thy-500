import type { Metadata } from "next";
import { NavigationProvider } from "@/contexts/navigation-context";
import { Red_Hat_Display } from 'next/font/google';
import "./globals.css";
import { LanguageProvider } from "@/contexts/language-context";

const redHat = Red_Hat_Display({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700', '800', '900'],
  variable: '--font-red-hat',
})

export const metadata: Metadata = {
  title: "Turkish Airlines 500th Aircraft - TK Aile'de Sen de Varsın",
  description: "Türk Hava Yolları'nın 500. uçağı üzerinde yer alan binlerce fotoğraf arasından kendi fotoğrafını keşfet. Discover your photo among thousands of photos on Turkish Airlines' 500th aircraft.",
  icons: {
    icon: '/thy-500.png',
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
        <LanguageProvider>
          <NavigationProvider>
            {children}
          </NavigationProvider>
        </LanguageProvider>
      </body>
    </html>
  );
}
