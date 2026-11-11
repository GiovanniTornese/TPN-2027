import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ChevronLeft, ChevronRight, Plus, CalendarX2 } from "lucide-react";
import { apiGet } from "@/lib/api";
import { useMe, useStations, useToday } from "@/lib/hooks";
import { fmt, shiftDays, weekDays } from "@/lib/shiftUi";
import type { MonthUsageOut, ShiftOut, StationKey } from "@/lib/types";
import { Button } from "@/components/ui/button";
import ShiftCard from "@/components/ShiftCard";
import ShiftDialog from "@/components/ShiftDialog";
import { cn } from "@/lib/utils";

type View = "day" | "week";

export default function Shifts() {
  const today = useToday();
  const me = useMe();
  const user = me.data;
  const stations = useStations();
  const [view, setView] = useState<View>("day");
  const [picked, setPicked] = useState<string | null>(null);
  const [filter, setFilter] = useState<StationKey>("all");
  const [onlyMine, setOnlyMine] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editing, setEditing] = useState<ShiftOut | null>(null);

  const date = picked ?? today;
  const days = weekDays(date);
  const [rangeStart, rangeEnd] = view === "day" ? [date, date] : [days[0], days[6]];

  const shifts = useQuery({
    queryKey: ["shifts", rangeStart, rangeEnd],
    queryFn: () => apiGet<ShiftOut[]>(`/shifts?start=${rangeStart}&end=${rangeEnd}`),
  });
  const month = date.slice(0, 7);
  const usage = useQuery({
    queryKey: ["usage", month],
    queryFn: () => apiGet<MonthUsageOut>(`/shifts/my-usage?month=${month}`),
    enabled: user?.role === "volunteer",
  });
  const monthFull = (d: string) => !!usage.data && d.slice(0, 7) === usage.data.month && usage.data.used >= usage.data.limit;
  const visible = (shifts.isError ? [] : shifts.data ?? []).filter(
    (s) => (filter === "all" || s.station === filter) && (!onlyMine || s.is_mine),
  );

  const isAdmin = user?.role === "admin";
  const step = view === "day" ? 1 : 7;
  const openNew = () => {
    setEditing(null);
    setDialogOpen(true);
  };
  const openEdit = (s: ShiftOut) => {
    setEditing(s);
    setDialogOpen(true);
  };
  const card = (s: ShiftOut, compact = false) => (
    <ShiftCard
      key={s.id}
      shift={s}
      stationName={stations.nameOf(s.station)}
      user={user}
      isPast={s.date < today}
      monthFull={!s.is_mine && monthFull(s.date)}
      compact={compact}
      onEdit={openEdit}
    />
  );

  return (
    <div className="space-y-5">
      <div className="flex items-end justify-between gap-3">
        <div>
          <p className="text-sm font-medium text-slate-500" data-testid="shifts-period-label">
            {view === "day" ? fmt(date, "EEEE d MMMM") : `${fmt(days[0], "d MMM")} – ${fmt(days[6], "d MMM yyyy")}`}
          </p>
          <h1 className="font-heading text-3xl font-bold tracking-tight md:text-4xl">Turni</h1>
          {user?.role === "volunteer" && usage.data && (
            <p
              className={cn(
                "mt-1 inline-flex rounded-full px-2.5 py-0.5 text-xs font-semibold",
                usage.data.used >= usage.data.limit ? "bg-amber-100 text-amber-900" : "bg-sky-100 text-sky-800",
              )}
              data-testid="month-usage-badge"
            >
              Tuoi turni a {fmt(`${month}-01`, "MMMM")}: {usage.data.used}/{usage.data.limit}
            </p>
          )}
        </div>
        {isAdmin && (
          <Button
            onClick={openNew}
            className="h-11 gap-1.5 rounded-xl bg-slate-900 px-4 text-white hover:bg-slate-800"
            data-testid="shifts-new-button"
          >
            <Plus className="size-4" /> Nuovo turno
          </Button>
        )}
      </div>

      {/* View switch + navigation */}
      <div className="sticky top-[61px] z-20 -mx-4 space-y-3 border-b border-slate-200/70 bg-slate-50/85 px-4 pb-3 pt-1 backdrop-blur-md md:top-0 md:mx-0 md:rounded-2xl md:border md:bg-white/80 md:p-3">
        <div className="flex items-center gap-2">
          <div className="flex rounded-xl bg-slate-200/70 p-1" role="tablist">
            {(["day", "week"] as View[]).map((v) => (
              <button
                key={v}
                role="tab"
                aria-selected={view === v}
                onClick={() => setView(v)}
                data-testid={`view-${v}-tab`}
                className={cn(
                  "min-h-9 rounded-lg px-3.5 text-sm font-semibold transition-colors duration-150",
                  view === v ? "bg-white text-slate-900 shadow-sm" : "text-slate-600",
                )}
              >
                {v === "day" ? "Giorno" : "Settimana"}
              </button>
            ))}
          </div>
          <div className="ml-auto flex items-center gap-1">
            <Button
              variant="outline"
              size="icon"
              className="size-10 rounded-xl"
              aria-label="Precedente"
              onClick={() => setPicked(shiftDays(date, -step))}
              data-testid="nav-prev-button"
            >
              <ChevronLeft className="size-4" />
            </Button>
            <Button
              variant="outline"
              className="h-10 rounded-xl px-3 text-sm"
              onClick={() => setPicked(today)}
              data-testid="nav-today-button"
            >
              Oggi
            </Button>
            <Button
              variant="outline"
              size="icon"
              className="size-10 rounded-xl"
              aria-label="Successivo"
              onClick={() => setPicked(shiftDays(date, step))}
              data-testid="nav-next-button"
            >
              <ChevronRight className="size-4" />
            </Button>
          </div>
        </div>

        {view === "day" && (
          <div className="grid grid-cols-7 gap-1" data-testid="day-strip">
            {days.map((d) => (
              <button
                key={d}
                onClick={() => setPicked(d)}
                data-testid={`day-strip-${d}`}
                className={cn(
                  "flex min-h-14 flex-col items-center justify-center rounded-xl text-xs transition-colors duration-150",
                  d === date ? "bg-slate-900 text-white" : "bg-white text-slate-600 hover:bg-slate-100",
                  d === today && d !== date && "ring-1 ring-sky-400",
                )}
              >
                <span className="uppercase">{fmt(d, "EEEEEE")}</span>
                <span className="font-heading text-lg font-bold leading-none">{fmt(d, "d")}</span>
              </button>
            ))}
          </div>
        )}

        <div className="-mx-1 flex gap-2 overflow-x-auto px-1 pb-0.5" data-testid="station-filter">
          <FilterPill active={filter === "all"} onClick={() => setFilter("all")} testid="filter-all">
            Tutte
          </FilterPill>
          {stations.list.map((s) => (
            <FilterPill
              key={s.key}
              active={filter === s.key}
              onClick={() => setFilter(s.key)}
              testid={`filter-station-${s.key}`}
              activeClass={stations.styleOf(s.key).pillActive}
              dot={stations.styleOf(s.key).dot}
            >
              {s.name}
            </FilterPill>
          ))}
          {user?.role === "volunteer" && (
            <FilterPill active={onlyMine} onClick={() => setOnlyMine(!onlyMine)} testid="filter-mine">
              I miei turni
            </FilterPill>
          )}
        </div>
      </div>

      {shifts.isLoading && (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {[0, 1, 2].map((i) => (
            <div key={i} className="h-48 animate-pulse rounded-2xl bg-slate-200/60" />
          ))}
        </div>
      )}
      {shifts.isError && (
        <p className="rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-500" data-testid="shifts-error">
          Impossibile caricare i turni in questo momento.
        </p>
      )}

      {!shifts.isLoading && !shifts.isError && view === "day" && (
        visible.length === 0 ? (
          <Empty isAdmin={isAdmin} onNew={openNew} />
        ) : (
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3" data-testid="day-shift-list">
            {visible.map((s) => card(s))}
          </div>
        )
      )}

      {!shifts.isLoading && !shifts.isError && view === "week" && (
        <div className="space-y-6 xl:grid xl:grid-cols-7 xl:gap-3 xl:space-y-0" data-testid="week-grid">
          {days.map((d) => {
            const list = visible.filter((s) => s.date === d);
            return (
              <section key={d} data-testid={`week-day-${d}`} className="min-w-0">
                <button
                  onClick={() => {
                    setPicked(d);
                    setView("day");
                  }}
                  className={cn(
                    "mb-2 flex w-full items-baseline gap-2 text-left transition-colors duration-150 hover:text-sky-700",
                    d === today && "text-sky-700",
                  )}
                  data-testid={`week-day-header-${d}`}
                >
                  <span className="font-heading text-lg font-bold capitalize">{fmt(d, "EEEE")}</span>
                  <span className="text-sm text-slate-500">{fmt(d, "d MMM")}</span>
                  <span className="ml-auto text-xs text-slate-400 xl:hidden">{list.length} turni</span>
                </button>
                {list.length === 0 ? (
                  <p className="rounded-xl border border-dashed border-slate-200 px-3 py-4 text-center text-xs text-slate-400">
                    Nessun turno
                  </p>
                ) : (
                  <div className="grid gap-2 sm:grid-cols-2 xl:grid-cols-1">{list.map((s) => card(s, true))}</div>
                )}
              </section>
            );
          })}
        </div>
      )}

      {isAdmin && (
        <ShiftDialog
          open={dialogOpen}
          onOpenChange={setDialogOpen}
          editing={editing}
          defaultDate={date}
          defaultStation={filter === "all" ? undefined : filter}
        />
      )}
    </div>
  );
}

function FilterPill({
  active,
  onClick,
  children,
  testid,
  activeClass = "bg-slate-900 text-white border-slate-900",
  dot,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
  testid: string;
  activeClass?: string;
  dot?: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      data-testid={testid}
      className={cn(
        "flex min-h-9 shrink-0 items-center gap-1.5 whitespace-nowrap rounded-full border px-3.5 text-sm font-semibold transition-colors duration-150",
        active ? activeClass : "border-slate-200 bg-white text-slate-700 hover:bg-slate-50",
      )}
    >
      {dot && <span className={cn("size-2 rounded-full", active ? "bg-white" : dot)} />}
      {children}
    </button>
  );
}

function Empty({ isAdmin, onNew }: { isAdmin: boolean; onNew: () => void }) {
  return (
    <div className="flex flex-col items-center rounded-3xl border border-dashed border-slate-300 bg-white px-6 py-12 text-center" data-testid="shifts-empty">
      <CalendarX2 className="size-10 text-slate-300" />
      <p className="mt-3 font-heading text-lg font-semibold">Nessun turno in programma</p>
      <p className="mt-1 text-sm text-slate-500">
        {isAdmin ? "Crea il primo turno per questa giornata." : "Prova un altro giorno o un'altra postazione."}
      </p>
      {isAdmin && (
        <Button onClick={onNew} className="mt-4 h-11 bg-sky-600 text-white hover:bg-sky-700" data-testid="shifts-empty-new-button">
          <Plus className="size-4" /> Crea turno
        </Button>
      )}
    </div>
  );
}
