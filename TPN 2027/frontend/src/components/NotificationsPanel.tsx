import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { BellRing, ClipboardCheck, Crown } from "lucide-react";
import { apiGet } from "@/lib/api";
import { useStations } from "@/lib/hooks";
import { fmt } from "@/lib/shiftUi";
import type { RemindersOut, ShiftOut } from "@/lib/types";
import { Button } from "@/components/ui/button";
import ReportDialog, { useMyReports } from "@/components/ReportDialog";
import { cn } from "@/lib/utils";

/** Home-page notifications: tomorrow's shifts reminder + end-of-shift reports still to fill in. */
export default function NotificationsPanel() {
  const stations = useStations();
  const rem = useQuery({ queryKey: ["shifts", "reminders"], queryFn: () => apiGet<RemindersOut>("/me/reminders") });
  const mine = useMyReports();
  const [reporting, setReporting] = useState<ShiftOut | null>(null);
  const tomorrow = rem.isError ? [] : rem.data?.shifts ?? [];
  const pending = mine.isError ? [] : mine.data?.pending ?? [];
  if (!tomorrow.length && !pending.length) return null;

  return (
    <div className="grid gap-3 md:grid-cols-2" data-testid="notifications-panel">
      {tomorrow.length > 0 && (
        <section className="animate-fade-up rounded-2xl border border-sky-200 bg-gradient-to-br from-sky-50 to-white p-4" data-testid="reminder-card">
          <p className="flex items-center gap-2 font-heading font-bold text-sky-900">
            <BellRing className="size-4" /> Promemoria: domani sei in turno
          </p>
          <ul className="mt-2 space-y-1.5">
            {tomorrow.map((s) => {
              const st = stations.styleOf(s.station);
              return (
                <li key={s.id} className="flex items-center gap-2 text-sm" data-testid={`reminder-shift-${s.id}`}>
                  <span className={cn("size-2 rounded-full", st.dot)} />
                  <span className="font-semibold tabular-nums">{s.start}–{s.end}</span>
                  <span className="truncate text-slate-600">{stations.nameOf(s.station)}</span>
                  {s.my_role === "leader" && (
                    <span className="ml-auto inline-flex items-center gap-1 rounded-full bg-slate-900 px-2 py-0.5 text-[10px] font-semibold text-amber-300">
                      <Crown className="size-2.5" /> Capoturno
                    </span>
                  )}
                </li>
              );
            })}
          </ul>
        </section>
      )}
      {pending.length > 0 && (
        <section className="animate-fade-up rounded-2xl border border-amber-200 bg-gradient-to-br from-amber-50 to-white p-4" data-testid="pending-reports-card">
          <p className="flex items-center gap-2 font-heading font-bold text-amber-900">
            <ClipboardCheck className="size-4" /> Resoconti da inserire ({pending.length})
          </p>
          <ul className="mt-2 space-y-1.5">
            {pending.slice(0, 5).map((s) => (
              <li key={s.id} className="flex items-center gap-2 text-sm">
                <span className="min-w-0 flex-1 truncate capitalize">
                  {fmt(s.date, "EEE d MMM")} · {s.start}–{s.end} · {stations.nameOf(s.station)}
                </span>
                <Button size="sm" className="h-9 shrink-0 bg-amber-500 text-white hover:bg-amber-600" onClick={() => setReporting(s)}
                  data-testid={`pending-report-button-${s.id}`}>
                  Compila
                </Button>
              </li>
            ))}
          </ul>
        </section>
      )}
      {reporting && (
        <ReportDialog shift={reporting} stationName={stations.nameOf(reporting.station)} open
          onOpenChange={(o) => !o && setReporting(null)} />
      )}
    </div>
  );
}
