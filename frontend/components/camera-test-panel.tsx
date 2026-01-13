"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";

interface CameraTestPanelProps {
  onCameraPositionChange: (position: [number, number, number]) => void;
  onTextureSizeChange?: (width: number, height: number) => void;
  onScannerCornersChange?: (corners: [number, number, number][]) => void;
}

export function CameraTestPanel({
  onCameraPositionChange,
  onTextureSizeChange,
  onScannerCornersChange,
}: CameraTestPanelProps) {
  const [xValue, setXValue] = useState(60);
  const [yValue, setYValue] = useState(3.5);
  const [zValue, setZValue] = useState(22.7);
  const [side, setSide] = useState<"left" | "right" | null>(null);
  const [textureWidth, setTextureWidth] = useState(20);
  const [textureHeight, setTextureHeight] = useState(30);

  // Scanner'dan gelen köşe koordinatları
  const scannerCorners: [number, number, number][] = [
    [-12.139593601226807, 7.520079430066275, -29.36063027381897], // Sol Ön
    [31.967596483230594, 7.520079430066275, -29.36063027381897], // Sağ Ön
    [31.967596483230594, 7.520079430066275, 31.038380575180057], // Sağ Arka
    [-12.139593601226807, 7.520079430066275, 31.038380575180057], // Sol Arka
  ];

  // Scanner köşelerini parent'a bildir
  useEffect(() => {
    onScannerCornersChange?.(scannerCorners);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const updateCameraPosition = (
    newX?: number,
    newY?: number,
    newZ?: number
  ) => {
    const finalX = newX !== undefined ? newX : xValue;
    const finalY = newY !== undefined ? newY : yValue;
    const finalZ = newZ !== undefined ? newZ : zValue;

    onCameraPositionChange([finalX, finalY, finalZ]);
  };

  const handleLeftSide = () => {
    setSide("left");
    setXValue(-35);
    // Uçağın solundan bakış açısı - X negatif tarafta
    const position: [number, number, number] = [-35, yValue, zValue];
    onCameraPositionChange(position);
  };

  const handleRightSide = () => {
    setSide("right");
    setXValue(35);
    // Uçağın sağından bakış açısı - X pozitif tarafta
    const position: [number, number, number] = [35, yValue, zValue];
    onCameraPositionChange(position);
  };

  const handleXChange = (value: string) => {
    const newX = parseFloat(value) || 0;
    setXValue(newX);
    setSide(null); // Manuel X değişikliğinde side'ı sıfırla
    updateCameraPosition(newX, undefined, undefined);
  };

  const handleYChange = (value: string) => {
    const newY = parseFloat(value) || 0;
    setYValue(newY);
    updateCameraPosition(undefined, newY, undefined);
  };

  const handleZChange = (value: string) => {
    const newZ = parseFloat(value) || 0;
    setZValue(newZ);
    updateCameraPosition(undefined, undefined, newZ);
  };

  return null;

  return (
    <Card className="fixed bottom-4 right-4 z-50 p-4 bg-background/95 backdrop-blur-sm border shadow-lg min-w-[280px]">
      <div className="space-y-4">
        <div className="font-semibold text-sm mb-2 text-white">
          Kamera Test Paneli
        </div>

        <div className="space-y-2">
          <Label htmlFor="x-value" className="text-xs text-white">
            X Değeri: {xValue.toFixed(2)}
          </Label>
          <div className="flex gap-2">
            <Input
              id="x-value"
              type="number"
              value={xValue}
              onChange={(e) => handleXChange(e.target.value)}
              step={0.1}
              className="h-8 text-xs"
            />
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleXChange(String(xValue - 1))}
              className="h-8 px-2"
            >
              -1
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleXChange(String(xValue + 1))}
              className="h-8 px-2"
            >
              +1
            </Button>
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="y-value" className="text-xs text-white">
            Y Değeri: {yValue.toFixed(2)}
          </Label>
          <div className="flex gap-2">
            <Input
              id="y-value"
              type="number"
              value={yValue}
              onChange={(e) => handleYChange(e.target.value)}
              step={0.1}
              className="h-8 text-xs"
            />
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleYChange(String(yValue - 1))}
              className="h-8 px-2"
            >
              -1
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleYChange(String(yValue + 1))}
              className="h-8 px-2"
            >
              +1
            </Button>
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="z-value" className="text-xs text-white">
            Z Değeri: {zValue.toFixed(2)}
          </Label>
          <div className="flex gap-2">
            <Input
              id="z-value"
              type="number"
              value={zValue}
              onChange={(e) => handleZChange(e.target.value)}
              step={0.1}
              className="h-8 text-xs"
            />
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleZChange(String(zValue - 1))}
              className="h-8 px-2"
            >
              -1
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={() => handleZChange(String(zValue + 1))}
              className="h-8 px-2"
            >
              +1
            </Button>
          </div>
        </div>

        <div className="space-y-2">
          <Label className="text-xs text-white">2D Görünüm Açıları</Label>
          <div className="flex gap-2">
            <Button
              size="sm"
              variant={side === "left" ? "default" : "secondary"}
              onClick={handleLeftSide}
              className="flex-1 text-xs"
            >
              Sol Taraf
            </Button>
            <Button
              size="sm"
              variant={side === "right" ? "default" : "secondary"}
              onClick={handleRightSide}
              className="flex-1 text-xs"
            >
              Sağ Taraf
            </Button>
          </div>
        </div>

        <div className="space-y-2 pt-2 border-t border-white/20">
          <Label className="text-xs text-white">Texture Boyutları</Label>
          <div className="grid grid-cols-2 gap-2">
            <div className="space-y-1">
              <Label htmlFor="texture-width" className="text-xs text-white">
                Genişlik: {textureWidth}
              </Label>
              <Input
                id="texture-width"
                type="number"
                value={textureWidth}
                onChange={(e) => {
                  const val = parseFloat(e.target.value) || 0;
                  setTextureWidth(val);
                  onTextureSizeChange?.(val, textureHeight);
                }}
                step={0.5}
                className="h-8 text-xs"
              />
            </div>
            <div className="space-y-1">
              <Label htmlFor="texture-height" className="text-xs text-white">
                Yükseklik: {textureHeight}
              </Label>
              <Input
                id="texture-height"
                type="number"
                value={textureHeight}
                onChange={(e) => {
                  const val = parseFloat(e.target.value) || 0;
                  setTextureHeight(val);
                  onTextureSizeChange?.(textureWidth, val);
                }}
                step={0.5}
                className="h-8 text-xs"
              />
            </div>
          </div>
        </div>

        <div className="text-xs text-white pt-2 border-t border-white/20">
          {side && `Aktif: ${side === "left" ? "Sol" : "Sağ"} taraf`}
          {side && <br />}
          Pozisyon: [{xValue.toFixed(2)}, {yValue.toFixed(2)},{" "}
          {zValue.toFixed(2)}]
        </div>
      </div>
    </Card>
  );
}
