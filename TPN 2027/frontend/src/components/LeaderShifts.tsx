import { useQuery } from "@tanstack/react-query";
import { Crown, MessageCircle, Phone } from "lucide-react";
import { apiGet } from "@/lib/api";
import { useStations } from "@/lib/hooks";
import { fmt } from "@/lib/shiftUi";
import type { ShiftOut } from "@/lib/types";
import { cn } from "@/lib/utils";

/** Capoturno view: upcoming shifts he leads, with his volunteers' phone numbers. */
export default function LeaderShifts() {
  const stations = useStations();
  const q = useQuery({ queryKey: ["shifts", "leading"], queryFn: () => apiGet<ShiftOut[]>("/shifts/leading") });
  const items = q.isError ? [] : q.data ?? [];

  return (
    <section className="space-y-3 rounded-2xl border border-slate-200 bg-white p-5" data-testid="leader-shifts">
      <div>
        <h2 className="flex items-center gap-2 font-heading text-lg font-bold">
          <Crown className="size-4 text-amber-500" /> I miei turni da Capoturno
        </h2>
        <p className="text-sm text-slate-500">I prossimi turni che coordini, con i contatti della tua squadra.</p>
      </div>
      {q.isLoading && <div className="h-20 animate-pulse rounded-xl bg-slate-100" />}
      {!q.isLoading && items.length === 0 && (
        <p className="rounded-xl border border-dashed border-slate-200 p-4 text-center text-sm text-slate-500" data-testid="leader-shifts-empty">
          Non sei ancora capoturno in nessun turno futuro.
        </p>
      )}
      <ul className="space-y-3">
        {items.map((s) => {
          const st = stations.styleOf(s.station);
          return (
            <li key={s.id} className="relative overflow-hidden rounded-xl border border-slate-200 p-4 pl-5" data-testid={`leader-shift-${s.id}`}>
              <span className={cn("absolute inset-y-0 left-0 w-1.5", st.bar)} aria-hidden />
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <p className="font-heading font-bold capitalize">
                  {fmt(s.date, "EEEE d MMMM")} · <span className="tabular-nums">{s.start}–{s.end}</span>
                </p>
                <span className={cn("rounded-full border px-2 py-0.5 text-xs font-semibold", st.soft, st.text, st.border)}>
                  {stations.nameOf(s.station)}
                </span>
              </div>
              <ul className="mt-3 space-y-2">
                {s.members.map((m) => (
                  <li key={m.id} className="flex items-center gap-2 text-sm" data-testid={`leader-member-${m.id}`}>
                    <span className="min-w-0 flex-1 truncate font-medium">{m.first_name} {m.last_name}</span>
                    {m.phone && (
                      <>
                        <a
                          href={`tel:${m.phone}`}
                          className="flex min-h-9 items-center gap-1 rounded-lg bg-sky-50 px-2.5 text-sky-800 transition-colors duration-150 hover:bg-sky-100"
                          data-testid={`leader-member-call-${m.id}`}
                        >
                          <Phone className="size-3.5" /> {m.phone}
                        </a>
                        <a
                          href={`https://wa.me/${m.phone.replace(/[^\d]/g, "").replace(/^(?!39)(3\d{8,9})$/, "39$1")}`}
                          target="_blank"
                          rel="noreferrer"
                          aria-label={`WhatsApp ${m.first_name}`}
                          className="flex size-9 items-center justify-center rounded-lg bg-green-50 text-green-700 transition-colors duration-150 hover:bg-green-100"
                          data-testid={`leader-member-whatsapp-${m.id}`}
                        >
                          <MessageCircle className="size-4" />
                        </a>
                      </>
                    )}
                  </li>
                ))}
                {Array.from({ length: s.free_member_slots }, (_, i) => (
                  <li key={`f-${i}`} className="text-sm text-amber-700">Posto volontario ancora libero</li>
                ))}
              </ul>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
