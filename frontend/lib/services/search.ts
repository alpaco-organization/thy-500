export type SearchType = "identity" | "fullName";

export interface PersonSearchOut {
  personId: string;
  name: string;
  grid_filename?: string | null;
  row?: number | null;
  column?: number | null;
  x: number;
  y: number;
  url: string;
}

export class ApiError extends Error {
  status: number;
  detail?: unknown;

  constructor(message: string, status: number, detail?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

async function readJsonSafe(res: Response): Promise<any> {
  const text = await res.text();
  if (!text) return undefined;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export async function searchPerson(params: {
  searchType: SearchType;
  query: string;
}): Promise<PersonSearchOut> {
  const queryTrimmed = params.query.trim();
  if (!queryTrimmed) {
    throw new ApiError("Query is required", 400);
  }

  const url = new URL("/api/search", window.location.origin);
  url.searchParams.set("searchType", params.searchType);
  url.searchParams.set("query", queryTrimmed);

  const res = await fetch(url.toString(), {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
  });

  if (!res.ok) {
    const detail = await readJsonSafe(res);
    throw new ApiError("Search failed", res.status, detail);
  }

  const data = (await res.json()) as PersonSearchOut;
  return data;
}
