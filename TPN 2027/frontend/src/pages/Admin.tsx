import { useState } from "react";
import { Navigate } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Crown, Pencil, Phone, Plus, Search, Trash2, X } from "lucide-react";
import { Checkbox } from "@/components/ui/checkbox";
import { toast } from "sonner";
import { apiDelete, apiGet, apiPost, apiPut } from "@/lib/api";
import { errMsg, useMe, useSlots, useStations } from "@/lib/hooks";
import type { Gender, SlotsOut, Station, StationIn, VolunteerAdminIn, VolunteerCreateIn, VolunteerOut } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import GenderPicker from "@/components/GenderPicker";
import UncoveredShifts from "@/components/UncoveredShifts";
import AdminReports from "@/components/AdminReports";
import { cn } from "@/lib/utils";

export default function Admin() {
  const me = useMe();
  if (me.data && me.data.role !== "admin") return <Navigate to="/" replace />;
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium text-slate-500">Area amministratori</p>
        <h1 className="font-heading text-3xl font-bold tracking-tight md:text-4xl">Gestione</h1>
      </div>
      <Tabs defaultValue="uncovered">
        <TabsList className="w-full overflow-x-auto sm:w-auto">
          <TabsTrigger value="uncovered" data-testid="admin-tab-uncovered">Scoperti</TabsTrigger>
          <TabsTrigger value="volunteers" data-testid="admin-tab-volunteers">Volontari</TabsTrigger>
          <TabsTrigger value="stations" data-testid="admin-tab-stations">Postazioni</TabsTrigger>
          <TabsTrigger value="slots" data-testid="admin-tab-slots">Orari</TabsTrigger>
          <TabsTrigger value="reports" data-testid="admin-tab-reports">Resoconti</TabsTrigger>
        </TabsList>
        <TabsContent value="uncovered" className="mt-4"><UncoveredShifts /></TabsContent>
        <TabsContent value="volunteers" className="mt-4"><Volunteers /></TabsContent>
        <TabsContent value="stations" className="mt-4"><Stations /></TabsContent>
        <TabsContent value="slots" className="mt-4"><Slots /></TabsContent>
        <TabsContent value="reports" className="mt-4"><AdminReports /></TabsContent>
      </Tabs>
    </div>
  );
}

/* ---------------- Volontari ---------------- */
function Volunteers() {
  const qc = useQueryClient();
  const list = useQuery({ queryKey: ["volunteers"], queryFn: () => apiGet<VolunteerOut[]>("/volunteers") });
  const [q, setQ] = useState("");
  const [gFilter, setGFilter] = useState<Gender | "all">("all");
  const [editing, setEditing] = useState<VolunteerOut | null>(null);
  const [creating, setCreating] = useState(false);

  const del = useMutation({
    mutationFn: (id: string) => apiDelete(`/volunteers/${id}`),
    onSuccess: () => {
      toast.success("Volontario eliminato");
      qc.invalidateQueries({ queryKey: ["volunteers"] });
      qc.invalidateQueries({ queryKey: ["shifts"] });
    },
    onError: (e) => toast.error(errMsg(e)),
  });

  const all = list.isError ? [] : list.data ?? [];
  const items = all.filter((v) => {
    const s = `${v.first_name} ${v.last_name} ${v.email} ${v.phone}`.toLowerCase();
    return s.includes(q.toLowerCase()) && (gFilter === "all" || v.gender === gFilter);
  });
  const men = all.filter((v) => v.gender === "M").length;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-3 gap-2">
        <Stat label="Volontari" value={all.length} testid="stat-total" />
        <Stat label="Uomini" value={men} testid="stat-men" />
        <Stat label="Donne" value={all.length - men} testid="stat-women" />
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <div className="relative min-w-0 flex-1">
          <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
          <Input placeholder="Cerca per nome, email, telefono…" className="h-11 pl-9" value={q}
            onChange={(e) => setQ(e.target.value)} data-testid="volunteers-search-input" />
        </div>
        <div className="flex rounded-xl bg-slate-200/70 p-1">
          {(["all", "M", "F"] as const).map((g) => (
            <button key={g} onClick={() => setGFilter(g)} data-testid={`volunteers-filter-${g}`}
              className={cn("min-h-9 rounded-lg px-3 text-sm font-semibold transition-colors duration-150",
                gFilter === g ? "bg-white shadow-sm" : "text-slate-600")}>
              {g === "all" ? "Tutti" : g === "M" ? "Uomini" : "Donne"}
            </button>
          ))}
        </div>
        <Button onClick={() => setCreating(true)} className="h-11 gap-1.5 bg-slate-900 text-white hover:bg-slate-800"
          data-testid="volunteers-add-button">
          <Plus className="size-4" /> Aggiungi
        </Button>
      </div>

      {list.isLoading && <div className="h-24 animate-pulse rounded-2xl bg-slate-200/60" />}
      {!list.isLoading && items.length === 0 && (
        <p className="rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center text-sm text-slate-500" data-testid="volunteers-empty">
          Nessun volontario trovato.
        </p>
      )}
      <div className="grid gap-2 md:grid-cols-2" data-testid="volunteers-list">
        {items.map((v) => (
          <div key={v.id} className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white p-4" data-testid={`volunteer-row-${v.id}`}>
            <span className={cn("flex size-11 shrink-0 items-center justify-center rounded-xl text-sm font-bold",
              v.gender === "M" ? "bg-sky-100 text-sky-800" : "bg-rose-100 text-rose-800")}>
              {v.gender === "M" ? "U" : "D"}
            </span>
            <div className="min-w-0 flex-1">
              <p className="flex items-center gap-1.5 truncate font-semibold" data-testid="volunteer-name">
                {v.first_name} {v.last_name}
                {v.is_team_leader && (
                  <span className="inline-flex items-center gap-0.5 rounded-full bg-slate-900 px-1.5 py-0.5 text-[10px] font-semibold text-amber-300" data-testid={`volunteer-leader-badge-${v.id}`}>
                    <Crown className="size-2.5" /> Capoturno
                  </span>
                )}
                {(!v.gender || !v.phone) && (
                  <span className="rounded-full bg-amber-100 px-1.5 py-0.5 text-[10px] font-semibold text-amber-900">Profilo incompleto</span>
                )}
              </p>
              <p className="truncate text-xs text-slate-500">{v.email}</p>
              <div className="mt-1 flex flex-wrap items-center gap-x-3 gap-y-0.5 text-xs text-slate-600">
                <a href={`tel:${v.phone}`} className="flex items-center gap-1 hover:text-sky-700"><Phone className="size-3" />{v.phone}</a>
                <span data-testid="volunteer-shift-count">{v.upcoming_count} prossimi · {v.shift_count} totali</span>
              </div>
            </div>
            <Button variant="ghost" size="icon-sm" aria-label="Modifica" onClick={() => setEditing(v)} data-testid={`volunteer-edit-${v.id}`}>
              <Pencil className="size-4" />
            </Button>
            <Button variant="ghost" size="icon-sm" aria-label="Elimina" className="text-red-600 hover:bg-red-50"
              onClick={() => window.confirm(`Eliminare ${v.first_name} ${v.last_name}? Verrà rimosso da tutti i turni.`) && del.mutate(v.id)}
              data-testid={`volunteer-delete-${v.id}`}>
              <Trash2 className="size-4" />
            </Button>
          </div>
        ))}
      </div>

      <Dialog open={!!editing || creating} onOpenChange={(o) => { if (!o) { setEditing(null); setCreating(false); } }}>
        {(editing || creating) && (
          <VolunteerForm key={editing?.id ?? "new"} editing={editing}
            onDone={() => { setEditing(null); setCreating(false); }} />
        )}
      </Dialog>
    </div>
  );
}

function Stat({ label, value, testid }: { label: string; value: number; testid: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-3">
      <p className="font-heading text-2xl font-bold tabular-nums" data-testid={testid}>{value}</p>
      <p className="text-xs text-slate-500">{label}</p>
    </div>
  );
}

function VolunteerForm({ editing, onDone }: { editing: VolunteerOut | null; onDone: () => void }) {
  const qc = useQueryClient();
  const [f, setF] = useState({
    first_name: editing?.first_name ?? "", last_name: editing?.last_name ?? "",
    phone: editing?.phone ?? "", email: editing?.email ?? "", password: "",
  });
  const [gender, setGender] = useState<Gender | null>(editing?.gender ?? null);
  const [leader, setLeader] = useState(editing?.is_team_leader ?? false);
  const save = useMutation({
    mutationFn: (g: Gender) => {
      const base: VolunteerAdminIn = {
        first_name: f.first_name, last_name: f.last_name, phone: f.phone, gender: g, is_team_leader: leader && g === "M",
        email: editing ? f.email : null, new_password: editing && f.password ? f.password : null,
      };
      if (editing) return apiPut<VolunteerOut>(`/volunteers/${editing.id}`, base);
      const body: VolunteerCreateIn = { ...base, email: f.email, password: f.password };
      return apiPost<VolunteerOut>("/volunteers", body);
    },
    onSuccess: () => {
      toast.success(editing ? "Volontario aggiornato" : "Volontario aggiunto");
      qc.invalidateQueries({ queryKey: ["volunteers"] });
      qc.invalidateQueries({ queryKey: ["shifts"] });
      onDone();
    },
    onError: (e) => toast.error(errMsg(e)),
  });
  const input = (key: keyof typeof f, label: string, type = "text") => (
    <div className="space-y-2">
      <Label htmlFor={`v-${key}`}>{label}</Label>
      <Input id={`v-${key}`} type={type} required={!(editing && key === "password")} minLength={key === "password" ? 6 : undefined} className="h-11"
        value={f[key]} onChange={(e) => setF({ ...f, [key]: e.target.value })}
        data-testid={`volunteer-form-${key.replace("_", "-")}-input`} />
    </div>
  );
  return (
    <DialogContent className="sm:max-w-md" data-testid="volunteer-dialog">
      <DialogHeader>
        <DialogTitle className="font-heading text-xl">{editing ? "Modifica volontario" : "Nuovo volontario"}</DialogTitle>
        <DialogDescription>{editing ? editing.email : "Crea un account volontario"}</DialogDescription>
      </DialogHeader>
      <form className="space-y-4" onSubmit={(e) => {
        e.preventDefault();
        if (!gender) return toast.error("Seleziona il genere");
        save.mutate(gender);
      }}>
        <div className="grid grid-cols-2 gap-3">{input("first_name", "Nome")}{input("last_name", "Cognome")}</div>
        <div className="space-y-2"><Label>Genere</Label><GenderPicker value={gender} onChange={setGender} testidPrefix="volunteer-form" /></div>
        <label className={cn("flex items-center gap-2 rounded-xl border border-slate-200 p-3 text-sm", gender !== "M" && "opacity-50")}>
          <Checkbox checked={leader && gender === "M"} disabled={gender !== "M"}
            onCheckedChange={(c) => setLeader(c === true)} data-testid="volunteer-form-leader-checkbox" />
          <span>
            <span className="flex items-center gap-1 font-semibold"><Crown className="size-3.5" /> Abilitato come Capoturno</span>
            <span className="text-xs text-slate-500">Solo per volontari uomini</span>
          </span>
        </label>
        {input("phone", "Telefono", "tel")}
        {input("email", editing ? "Email di accesso" : "Email", "email")}
        {input("password", editing ? "Nuova password (lascia vuoto per non cambiarla)" : "Password iniziale", "password")}
        <Button type="submit" className="h-11 w-full bg-sky-600 text-white hover:bg-sky-700" disabled={save.isPending}
          data-testid="volunteer-form-submit-button">
          {save.isPending ? "Salvataggio…" : "Salva"}
        </Button>
      </form>
    </DialogContent>
  );
}

/* ---------------- Postazioni ---------------- */
function Stations() {
  const qc = useQueryClient();
  const stations = useStations();
  const [name, setName] = useState("");
  const add = useMutation({
    mutationFn: (b: StationIn) => apiPost<Station>("/stations", b),
    onSuccess: () => {
      toast.success("Postazione creata");
      setName("");
      qc.invalidateQueries({ queryKey: ["stations"] });
    },
    onError: (e) => toast.error(errMsg(e)),
  });
  return (
    <div className="space-y-4">
      <form className="flex max-w-xl gap-2" onSubmit={(e) => { e.preventDefault(); if (name.trim()) add.mutate({ name: name.trim() }); }}>
        <Input placeholder="Nome nuova postazione" value={name} maxLength={40} onChange={(e) => setName(e.target.value)}
          className="h-11" data-testid="station-new-input" />
        <Button type="submit" className="h-11 gap-1.5 bg-slate-900 text-white hover:bg-slate-800" disabled={add.isPending || !name.trim()}
          data-testid="station-add-button">
          <Plus className="size-4" /> Crea
        </Button>
      </form>
      <div className="grid gap-3 md:grid-cols-3">
        {stations.list.map((s) => <StationEditor key={`${s.key}-${s.name}`} station={s} canDelete={stations.list.length > 1} />)}
      </div>
    </div>
  );
}

function StationEditor({ station, canDelete }: { station: Station; canDelete: boolean }) {
  const qc = useQueryClient();
  const [name, setName] = useState(station.name);
  const st = useStations().styleOf(station.key);
  const save = useMutation({
    mutationFn: (n: string) => apiPut<Station>(`/stations/${station.key}`, { name: n } satisfies StationIn),
    onSuccess: () => {
      toast.success("Nome postazione aggiornato");
      qc.invalidateQueries({ queryKey: ["stations"] });
    },
    onError: (e) => toast.error(errMsg(e)),
  });
  const del = useMutation({
    mutationFn: () => apiDelete(`/stations/${station.key}`),
    onSuccess: () => {
      toast.success("Postazione eliminata");
      qc.invalidateQueries({ queryKey: ["stations"] });
    },
    onError: (e) => toast.error(errMsg(e)),
  });
  return (
    <form className={cn("space-y-3 rounded-2xl border p-4", st.soft, st.border)}
      onSubmit={(e) => { e.preventDefault(); save.mutate(name.trim()); }}
      data-testid={`station-form-${station.key}`}>
      <div className="flex items-center gap-2">
        <span className={cn("size-3 rounded-full", st.dot)} />
        <p className={cn("flex-1 text-xs font-bold uppercase tracking-wider", st.text)}>Postazione</p>
        {canDelete && (
          <Button type="button" variant="ghost" size="icon-sm" aria-label="Elimina postazione" className="text-red-600 hover:bg-red-50"
            onClick={() => window.confirm(`Eliminare la postazione "${station.name}"?`) && del.mutate()}
            data-testid={`station-delete-button-${station.key}`}>
            <Trash2 className="size-4" />
          </Button>
        )}
      </div>
      <Input value={name} required maxLength={40} onChange={(e) => setName(e.target.value)} className="h-11 bg-white"
        data-testid={`station-name-input-${station.key}`} />
      <Button type="submit" disabled={save.isPending || !name.trim() || name === station.name}
        className="h-10 w-full bg-slate-900 text-white hover:bg-slate-800" data-testid={`station-save-button-${station.key}`}>
        Salva nome
      </Button>
    </form>
  );
}

/* ---------------- Orari ---------------- */
function Slots() {
  const slots = useSlots();
  if (slots.isLoading) return <div className="h-24 animate-pulse rounded-2xl bg-slate-200/60" />;
  return <SlotsEditor key={(slots.data?.slots ?? []).join(",")} initial={slots.data?.slots ?? []} />;
}

function SlotsEditor({ initial }: { initial: string[] }) {
  const qc = useQueryClient();
  const [list, setList] = useState<string[]>(initial);
  const [next, setNext] = useState("");
  const save = useMutation({
    mutationFn: (s: string[]) => apiPut<SlotsOut>("/settings/slots", { slots: s }),
    onSuccess: () => {
      toast.success("Fasce orarie salvate");
      qc.invalidateQueries({ queryKey: ["slots"] });
    },
    onError: (e) => toast.error(errMsg(e)),
  });
  const add = () => {
    if (!/^([01]\d|2[0-1]):[0-5]\d$/.test(next)) return toast.error("Orario non valido (ultimo inizio 21:00)");
    setList(Array.from(new Set([...list, next])).sort());
    setNext("");
  };
  const end = (s: string) => `${String(Number(s.slice(0, 2)) + 2).padStart(2, "0")}${s.slice(2)}`;
  return (
    <div className="max-w-xl space-y-4 rounded-2xl border border-slate-200 bg-white p-5">
      <div>
        <h2 className="font-heading text-lg font-bold">Fasce rapide</h2>
        <p className="text-sm text-slate-500">Scorciatoie da 2 ore proposte quando crei un turno. Puoi comunque scegliere qualsiasi orario.</p>
      </div>
      <div className="flex flex-wrap gap-2" data-testid="slots-list">
        {list.map((s) => (
          <span key={s} className="inline-flex items-center gap-1 rounded-full border border-slate-200 bg-slate-50 py-1 pl-3 pr-1 text-sm font-semibold tabular-nums" data-testid={`slot-chip-${s.replace(":", "")}`}>
            {s}–{end(s)}
            <button type="button" aria-label={`Rimuovi ${s}`} onClick={() => setList(list.filter((x) => x !== s))}
              className="flex size-7 items-center justify-center rounded-full text-slate-400 transition-colors duration-150 hover:bg-red-50 hover:text-red-600"
              data-testid={`slot-remove-${s.replace(":", "")}`}>
              <X className="size-3.5" />
            </button>
          </span>
        ))}
        {list.length === 0 && <p className="text-sm text-slate-500">Nessuna fascia.</p>}
      </div>
      <div className="flex gap-2">
        <Input type="time" value={next} onChange={(e) => setNext(e.target.value)} className="h-11 w-36" data-testid="slot-new-input" />
        <Button type="button" variant="outline" className="h-11" onClick={add} data-testid="slot-add-button">
          <Plus className="size-4" /> Aggiungi
        </Button>
      </div>
      <Button className="h-11 w-full bg-sky-600 text-white hover:bg-sky-700" disabled={save.isPending || list.length === 0}
        onClick={() => save.mutate(list)} data-testid="slots-save-button">
        Salva fasce orarie
      </Button>
    </div>
  );
}
