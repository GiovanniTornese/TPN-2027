import { useQuery } from "@tanstack/react-query";
import { ApiError, apiGet } from "@/lib/api";
import { styleFor } from "@/lib/shiftUi";
import type { SlotsOut, Station, StationKey, TodayOut, UserPublic } from "@/lib/types";

export const DEFAULT_STATIONS: Station[] = [
  { key: "a", name: "Postazione A", color: "emerald", archived: false },
  { key: "b", name: "Postazione B", color: "indigo", archived: false },
  { key: "c", name: "Postazione C", color: "amber", archived: false },
];

export function useMe() {
  return useQuery({
    queryKey: ["me"],
    queryFn: () => apiGet<UserPublic>("/auth/me"),
    retry: false,
  });
}

export function useStations() {
  const q = useQuery({ queryKey: ["stations"], queryFn: () => apiGet<Station[]>("/stations") });
  const all = q.data && q.data.length ? q.data : DEFAULT_STATIONS;
  const list = all.filter((s) => !s.archived);
  const nameOf = (k: StationKey) => all.find((s) => s.key === k)?.name ?? "Postazione";
  const styleOf = (k: StationKey) => styleFor(all.find((s) => s.key === k)?.color);
  return { ...q, all, list, nameOf, styleOf };
}

export function useSlots() {
  return useQuery({ queryKey: ["slots"], queryFn: () => apiGet<SlotsOut>("/settings/slots") });
}

function localToday(): string {
  const d = new Date();
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

/** Server-anchored "today" (Europe/Rome); falls back to the device date only if the API is unreachable. */
export function useToday(): string {
  const q = useQuery({ queryKey: ["today"], queryFn: () => apiGet<TodayOut>("/today"), staleTime: 60_000 });
  return q.data?.today ?? localToday();
}

export function errMsg(e: unknown, fallback = "Si è verificato un errore"): string {
  if (e instanceof ApiError) {
    const body = e.body as { detail?: unknown } | null;
    if (body && typeof body.detail === "string") return body.detail;
    if (body && Array.isArray(body.detail)) return "Dati non validi: controlla i campi inseriti";
  }
  return fallback;
}

export function isUnauthorized(e: unknown): boolean {
  return e instanceof ApiError && e.status === 401;
}
