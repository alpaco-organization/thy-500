import React from "react";

function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <main className="bg-auth bg-center bg-no-repeat bg-cover w-full h-dvh">
      <section className="w-full h-full backdrop-blur-sm flex justify-center items-center p-4">
        {children}
      </section>
    </main>
  );
}

export default AuthLayout;
