import { addDays, format, parseISO, startOfWeek } from "date-fns";
import { it } from "date-fns/locale";

export interface StationStyle { bar: string; soft: string; text: string; border: string; dot: string; pillActive: string }

// Literal class strings so Tailwind can see them.
export const COLOR_STYLES: Record<string, StationStyle> = {
  emerald: { bar: "bg-emerald-500", soft: "bg-emerald-50", text: "text-emerald-800", border: "border-emerald-200", dot: "bg-emerald-500", pillActive: "bg-emerald-600 text-white border-emerald-600" },
  indigo: { bar: "bg-indigo-500", soft: "bg-indigo-50", text: "text-indigo-800", border: "border-indigo-200", dot: "bg-indigo-500", pillActive: "bg-indigo-600 text-white border-indigo-600" },
  amber: { bar: "bg-amber-500", soft: "bg-amber-50", text: "text-amber-900", border: "border-amber-200", dot: "bg-amber-500", pillActive: "bg-amber-500 text-white border-amber-500" },
  rose: { bar: "bg-rose-500", soft: "bg-rose-50", text: "text-rose-800", border: "border-rose-200", dot: "bg-rose-500", pillActive: "bg-rose-600 text-white border-rose-600" },
  cyan: { bar: "bg-cyan-500", soft: "bg-cyan-50", text: "text-cyan-900", border: "border-cyan-200", dot: "bg-cyan-500", pillActive: "bg-cyan-600 text-white border-cyan-600" },
  violet: { bar: "bg-violet-500", soft: "bg-violet-50", text: "text-violet-800", border: "border-violet-200", dot: "bg-violet-500", pillActive: "bg-violet-600 text-white border-violet-600" },
  lime: { bar: "bg-lime-500", soft: "bg-lime-50", text: "text-lime-900", border: "border-lime-200", dot: "bg-lime-500", pillActive: "bg-lime-600 text-white border-lime-600" },
  orange: { bar: "bg-orange-500", soft: "bg-orange-50", text: "text-orange-900", border: "border-orange-200", dot: "bg-orange-500", pillActive: "bg-orange-500 text-white border-orange-500" },
  fuchsia: { bar: "bg-fuchsia-500", soft: "bg-fuchsia-50", text: "text-fuchsia-800", border: "border-fuchsia-200", dot: "bg-fuchsia-500", pillActive: "bg-fuchsia-600 text-white border-fuchsia-600" },
  teal: { bar: "bg-teal-500", soft: "bg-teal-50", text: "text-teal-800", border: "border-teal-200", dot: "bg-teal-500", pillActive: "bg-teal-600 text-white border-teal-600" },
};
export const styleFor = (color?: string): StationStyle => COLOR_STYLES[color ?? ""] ?? COLOR_STYLES.emerald;

export const iso = (d: Date) => format(d, "yyyy-MM-dd");
export const shiftDays = (date: string, n: number) => iso(addDays(parseISO(date), n));
export const weekStart = (date: string) => iso(startOfWeek(parseISO(date), { weekStartsOn: 1 }));
export const weekDays = (date: string) => {
  const start = weekStart(date);
  return Array.from({ length: 7 }, (_, i) => shiftDays(start, i));
};
export const fmt = (date: string, pattern: string) => format(parseISO(date), pattern, { locale: it });

export function needsLabel(missingLeader: boolean, freeMembers: number): string {
  const parts: string[] = [];
  if (missingLeader) parts.push("il Capoturno");
  if (freeMembers > 0) parts.push(`${freeMembers} ${freeMembers === 1 ? "volontario" : "volontari"}`);
  return parts.length ? `Serve ${parts.join(" e ")}` : "";
}

export const fmtHours = (h: number) => h.toLocaleString("it-IT", { maximumFractionDigits: 1 });
export function addHours(start: string, n: number): string {
  const [h, m] = start.split(":").map(Number);
  return `${String(Math.min(h + n, 23)).padStart(2, "0")}:${String(h + n > 23 ? 59 : m).padStart(2, "0")}`;
}
