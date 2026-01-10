"use client";

export function Splash() {
  return (
    <dialog className="group fixed left-0 top-0 z-100 flex h-full w-full items-center justify-center bg-background data-[state=hide]:animate-out fade-out duration-1000 fill-mode-forwards">
      <video
        src="/splash.mp4"
        autoPlay
        muted
        playsInline
        className="w-full h-full object-cover animate-in fade-in duration-500 group-data-[state=hide]:animate-out fade-out fill-mode-forwards"
      />
    </dialog>
  );
}

export default Splash;
