import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

function getInternalApiBaseUrl(): string {
  const base = process.env.INTERNAL_API_BASE_URL;
  console.log("INTERNAL_API_BASE_URL:", base);
  if (!base) {
    throw new Error("INTERNAL_API_BASE_URL is not configured");
  }
  return base;
}

export async function GET(req: Request) {
  try {
    const url = new URL(req.url);
    const searchType = url.searchParams.get("searchType") || "";
    const query = url.searchParams.get("query") || "";

    const upstream = new URL("/api/search", getInternalApiBaseUrl());
    upstream.searchParams.set("searchType", searchType);
    upstream.searchParams.set("query", query);

    const res = await fetch(upstream.toString(), {
      method: "GET",
      headers: { Accept: "application/json" },
      cache: "no-store",
    });

    const contentType = res.headers.get("content-type") || "";
    const body = contentType.includes("application/json")
      ? await res.json()
      : await res.text();

    return NextResponse.json(body, { status: res.status });
  } catch (e: unknown) {
    const message = e instanceof Error ? e.message : "Upstream request failed";
    return NextResponse.json(
      { detail: message },
      { status: 502 }
    );
  }
}
