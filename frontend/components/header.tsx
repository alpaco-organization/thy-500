"use client";

import { LanguageSelector } from "@/contexts/language-context";
import { useNavigation } from "@/contexts/navigation-context";
import Image from "next/image";

function Header() {
  const { isNavigating } = useNavigation();

  return (
    <header
      className="fixed w-full pointer-events-none bg-transparent top-0 left-0 z-35 p-4 transition-transform duration-300 ease-in-out flex justify-between items-start gap-4"
      style={{
        transform: isNavigating ? "translateY(-100%)" : "translateY(0)",
      }}
    >
      <Image
        src="/logo.svg"
        alt="Turkish Airlines 500th Aircraft Logo"
        className="h-10 w-auto"
        width={200}
        height={50}
      />
      <LanguageSelector/>
    </header>
  );
}

export default Header;
