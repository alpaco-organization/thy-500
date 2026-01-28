import Image from "next/image";

export function Splash() {
  return (
    <dialog className="group fixed left-0 top-0 z-100 flex h-full w-full items-center justify-center bg-background data-[state=hide]:animate-out fade-out duration-1000 fill-mode-forwards">
      <div className="relative h-52 w-52 scale-75 md:scale-100">
        <div className="absolute inset-0 rounded-full bg-white/10 animate-ping duration-1000" />
        <div className="absolute inset-0 flex items-center justify-center rounded-lg">
          <Image
            src="/logo.svg"
            width={200}
            height={50}
            alt="Turkish Airlines 500th Aircraft Logo"
            className="w-auto h-20 animate-in fade-in duration-500 group-data-[state=hide]:animate-out fade-out fill-mode-forwards"
          />
        </div>
      </div>
    </dialog>
  );
}

export default Splash;
