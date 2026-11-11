import { BookOpen, Clock, ClipboardCheck } from "lucide-react";
import { fmtHours } from "@/lib/shiftUi";
import { useMyReports } from "@/components/ReportDialog";

/** Volunteer's own counters (hours + publications) from submitted end-of-shift reports. */
export default function MyStats() {
  const q = useMyReports();
  const d = q.isError ? null : q.data;
  const items = [
    { icon: <Clock className="size-4" />, label: "Ore totali", value: fmtHours(d?.total_hours ?? 0), testid: "stats-hours" },
    { icon: <BookOpen className="size-4" />, label: "Pubblicazioni", value: String(d?.total_publications ?? 0), testid: "stats-publications" },
    { icon: <ClipboardCheck className="size-4" />, label: "Turni svolti", value: String(d?.reports.length ?? 0), testid: "stats-reports" },
  ];
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5" data-testid="my-stats">
      <h2 className="font-heading text-lg font-bold">Il mio contatore</h2>
      <div className="mt-3 grid grid-cols-3 gap-2">
        {items.map((i) => (
          <div key={i.label} className="rounded-xl bg-slate-50 p-3">
            <span className="text-slate-400">{i.icon}</span>
            <p className="mt-1 font-heading text-2xl font-bold tabular-nums" data-testid={i.testid}>{q.isLoading ? "…" : i.value}</p>
            <p className="text-xs leading-tight text-slate-500">{i.label}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
