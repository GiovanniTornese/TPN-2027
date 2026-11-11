import type { ReactNode } from "react";
import { useQuery } from "@tanstack/react-query";
import { CheckCircle2, Crown, Users } from "lucide-react";
import { apiGet } from "@/lib/api";
import { useMe, useStations, useToday } from "@/lib/hooks";
import { fmt } from "@/lib/shiftUi";
import type { ShiftOut } from "@/lib/types";
import ShiftCard from "@/components/ShiftCard";

/** Admin view: upcoming shifts still missing the capoturno or volunteers, grouped by day. */
export default function UncoveredShifts() {
  const me = useMe();
  const today = useToday();
  const stations = useStations();
  const q = useQuery({ queryKey: ["shifts", "uncovered"], queryFn: () => apiGet<ShiftOut[]>("/shifts/uncovered") });
  const items = q.isError ? [] : q.data ?? [];
  const noLeader = items.filter((s) => s.missing_leader).length;
  const seats = items.reduce((n, s) => n + s.free_member_slots, 0);
  const days = Array.from(new Set(items.map((s) => s.date)));

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-3 gap-2">
        <Stat icon={<Users className="size-4" />} label="Turni scoperti" value={items.length} testid="uncovered-count" />
        <Stat icon={<Crown className="size-4" />} label="Senza capoturno" value={noLeader} testid="uncovered-no-leader" />
        <Stat icon={<Users className="size-4" />} label="Posti volontario" value={seats} testid="uncovered-seats" />
      </div>
      {q.isLoading && <div className="h-40 animate-pulse rounded-2xl bg-slate-200/60" />}
      {!q.isLoading && items.length === 0 && (
        <div className="flex flex-col items-center rounded-3xl border border-dashed border-green-300 bg-green-50 px-6 py-10 text-center" data-testid="uncovered-empty">
          <CheckCircle2 className="size-10 text-green-600" />
          <p className="mt-3 font-heading text-lg font-semibold text-green-900">Tutti i turni futuri sono coperti</p>
        </div>
      )}
      {days.map((d) => (
        <section key={d} className="space-y-2" data-testid={`uncovered-day-${d}`}>
          <h3 className="flex items-baseline gap-2">
            <span className="font-heading text-lg font-bold capitalize">{fmt(d, "EEEE d MMMM")}</span>
            {d === today && <span className="text-xs font-semibold text-sky-700">Oggi</span>}
          </h3>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {items.filter((s) => s.date === d).map((s) => (
              <ShiftCard key={s.id} shift={s} stationName={stations.nameOf(s.station)} user={me.data} isPast={false} compact />
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}

function Stat({ icon, label, value, testid }: { icon: ReactNode; label: string; value: number; testid: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-3">
      <span className="text-slate-400">{icon}</span>
      <p className="mt-1 font-heading text-2xl font-bold tabular-nums" data-testid={testid}>{value}</p>
      <p className="text-xs leading-tight text-slate-500">{label}</p>
    </div>
  );
}
