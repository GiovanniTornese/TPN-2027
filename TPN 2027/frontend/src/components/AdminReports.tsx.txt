import type { ReactNode } from "react";
import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { BookOpen, Clock, Lock, MessageSquareText } from "lucide-react";
import { apiGet } from "@/lib/api";
import { useStations } from "@/lib/hooks";
import { fmt, fmtHours } from "@/lib/shiftUi";
import type { AdminReportsOut } from "@/lib/types";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

/** Admin: totals of hours/publications, per-volunteer breakdown, and the private comments. */
export default function AdminReports() {
  const stations = useStations();
  const [month, setMonth] = useState("");
  const q = useQuery({
    queryKey: ["reports", "admin", month],
    queryFn: () => apiGet<AdminReportsOut>(`/reports${month ? `?month=${month}` : ""}`),
  });
  const d = q.isError ? null : q.data;
  const comments = (d?.reports ?? []).filter((r) => r.comment);

  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-end gap-2">
        <div>
          <span className="text-xs text-slate-500">Periodo</span>
          <Input type="month" value={month} onChange={(e) => setMonth(e.target.value)} className="h-11 w-44" data-testid="reports-month-input" />
        </div>
        {month && <Button variant="outline" className="h-11" onClick={() => setMonth("")} data-testid="reports-all-button">Tutto</Button>}
      </div>
      <div className="grid grid-cols-3 gap-2">
        <Big icon={<Clock className="size-4" />} label="Ore totali" value={fmtHours(d?.total_hours ?? 0)} testid="reports-total-hours" />
        <Big icon={<BookOpen className="size-4" />} label="Pubblicazioni" value={String(d?.total_publications ?? 0)} testid="reports-total-publications" />
        <Big icon={<MessageSquareText className="size-4" />} label="Resoconti" value={String(d?.total_reports ?? 0)} testid="reports-total-count" />
      </div>

      <section className="rounded-2xl border border-slate-200 bg-white">
        <h3 className="border-b border-slate-100 px-4 py-3 font-heading font-bold">Per volontario</h3>
        {q.isLoading && <div className="m-4 h-16 animate-pulse rounded-xl bg-slate-100" />}
        {!q.isLoading && !d?.by_volunteer.length && <p className="p-4 text-sm text-slate-500" data-testid="reports-empty">Nessun resoconto inserito.</p>}
        <ul className="divide-y divide-slate-100" data-testid="reports-by-volunteer">
          {d?.by_volunteer.map((v) => (
            <li key={v.user_id} className="flex items-center gap-3 px-4 py-3 text-sm" data-testid={`reports-volunteer-${v.user_id}`}>
              <span className="min-w-0 flex-1 truncate font-semibold">{v.user_name}</span>
              <span className="tabular-nums text-slate-600">{fmtHours(v.hours)} h</span>
              <span className="w-20 text-right tabular-nums text-slate-600">{v.publications} pubbl.</span>
              <span className="hidden w-16 text-right text-xs text-slate-400 sm:block">{v.reports} turni</span>
            </li>
          ))}
        </ul>
      </section>

      <section className="space-y-2">
        <h3 className="flex items-center gap-2 font-heading font-bold"><Lock className="size-4" /> Commenti dei volontari</h3>
        {!comments.length && <p className="text-sm text-slate-500">Nessun commento.</p>}
        {comments.map((r) => (
          <article key={r.id} className="rounded-2xl border border-slate-200 bg-white p-4" data-testid={`report-comment-${r.id}`}>
            <p className="text-xs text-slate-500 capitalize">
              {r.user_name} · {r.date ? fmt(r.date, "EEE d MMM yyyy") : ""} · {r.start}–{r.end} · {stations.nameOf(r.station)} · {fmtHours(r.hours)} h · {r.publications} pubbl.
            </p>
            <p className="mt-1.5 whitespace-pre-line text-sm text-slate-800">{r.comment}</p>
          </article>
        ))}
      </section>
    </div>
  );
}

function Big({ icon, label, value, testid }: { icon: ReactNode; label: string; value: string; testid: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-3">
      <span className="text-slate-400">{icon}</span>
      <p className="mt-1 font-heading text-2xl font-bold tabular-nums" data-testid={testid}>{value}</p>
      <p className="text-xs text-slate-500">{label}</p>
    </div>
  );
}
