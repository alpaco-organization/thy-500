import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://thy500-backend:8000";

const TOKEN_COOKIE = "token";

function redirectToAuth(request: NextRequest) {
  const url = request.nextUrl.clone();
  url.pathname = "/auth";

  const response = NextResponse.redirect(url);
  response.cookies.delete(TOKEN_COOKIE);

  return response;
}

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (
    pathname.startsWith("/auth") ||
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api") ||
    pathname.includes(".")
  ) {
    return NextResponse.next();
  }

  const token = request.cookies.get(TOKEN_COOKIE)?.value;
  if (!token) return redirectToAuth(request);

  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/verify`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      cache: "no-store",
    });

    if (!response.ok) return redirectToAuth(request);

    const userData = await response.json();

    const headers = new Headers(request.headers);
    headers.set("x-user-id", userData.userId);
    headers.set("x-user-email", userData.email);
    headers.set("x-user-role", userData.role);

    return NextResponse.next({
      request: { headers },
    });
  } catch {
    return redirectToAuth(request);
  }
}

export const config = {
  matcher: ["/dashboard/:path*"],
};
