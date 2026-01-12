"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Item, ItemActions, ItemContent } from "@/components/ui/item";

interface TestPanelProps {
  onTest: (x: number, z: number) => void;
  onReset: () => void;
}

export function TestPanel({ onTest, onReset }: TestPanelProps) {
  const [x, setX] = useState<string>("");
  const [z, setZ] = useState<string>("");

  const handleTest = () => {
    const xVal = parseFloat(x);
    const zVal = parseFloat(z);

    if (!isNaN(xVal) && !isNaN(zVal)) {
      onTest(xVal, zVal);
    }
  };

  const handleReset = () => {
    setX("");
    setZ("");
    onReset();
  };

  return (
    <div className="fixed top-20 right-4 z-50 bg-[#3F3F3F]/90 backdrop-blur-xl p-4 border border-[#535353]/80 rounded-2xl w-64 flex flex-col gap-3">
      <h3 className="text-white font-semibold text-sm">Test Panel</h3>
      
      <Item className="rounded-lg p-1.5 border-white/40 bg-white/10">
        <ItemContent className="flex items-center gap-2 w-full">
          <span className="text-white text-xs w-6">X:</span>
          <Input
            type="number"
            step="0.1"
            placeholder="0"
            value={x}
            onChange={(e) => setX(e.target.value)}
            className="bg-transparent border-0 shadow-none text-white placeholder:text-white/40 text-sm"
          />
        </ItemContent>
      </Item>

      <Item className="rounded-lg p-1.5 border-white/40 bg-white/10">
        <ItemContent className="flex items-center gap-2 w-full">
          <span className="text-white text-xs w-6">Z:</span>
          <Input
            type="number"
            step="0.1"
            placeholder="0"
            value={z}
            onChange={(e) => setZ(e.target.value)}
            className="bg-transparent border-0 shadow-none text-white placeholder:text-white/40 text-sm"
          />
        </ItemContent>
      </Item>

      <div className="flex gap-2">
        <Button
          onClick={handleTest}
          disabled={!x || !z}
          className="flex-1 rounded-lg text-xs"
          size="sm"
        >
          Test Et
        </Button>
        <Button
          onClick={handleReset}
          variant="secondary"
          className="flex-1 rounded-lg text-xs"
          size="sm"
        >
          Sıfırla
        </Button>
      </div>
    </div>
  );
}
