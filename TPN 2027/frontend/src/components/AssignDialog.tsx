import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Crown, Search, UserRound } from "lucide-react";
import { toast } from "sonner";
import { apiGet, apiPost } from "@/lib/api";
import { errMsg, useMe } from "@/lib/hooks";
import type { AssignIn, ShiftOut, ShiftRole, VolunteerOut } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

interface Props {
  shift: ShiftOut;
  open: boolean;
  onOpenChange: (o: boolean) => void;
}

const canLead = (p: VolunteerOut) => p.gender === "M" && (p.is_team_leader || p.role === "admin");

export default function AssignDialog({ shift, open, onOpenChange }: Props) {
  return (
    <Dialog open={open} onOpenChange={(o) => onOpenChange(o)}>
      {open && <AssignBody shift={shift} onDone={() => onOpenChange(false)} />}
    </Dialog>
  );
}

function AssignBody({ shift, onDone }: { shift: ShiftOut; onDone: () => void }) {
  const qc = useQueryClient();
  const me = useMe();
  const [role, setRole] = useState<ShiftRole>(shift.missing_leader ? "leader" : "member");
  const [q, setQ] = useState("");
  const people = useQuery({
    queryKey: ["volunteers", "assignable"],
    queryFn: () => apiGet<VolunteerOut[]>("/volunteers?include_admins=true"),
  });
  const assign = useMutation({
    mutationFn: (body: AssignIn) => apiPost<ShiftOut>(`/shifts/${shift.id}/assign`, body),
    onSuccess: () => {
      toast.success(role === "leader" ? "Capoturno assegnato" : "Volontario assegnato");
      qc.invalidateQueries({ queryKey: ["shifts"] });
      qc.invalidateQueries({ queryKey: ["volunteers"] });
      onDone();
    },
    onError: (e) => toast.error(errMsg(e)),
  });

  const taken = new Set([shift.leader?.id, ...shift.members.map((m) => m.id)]);
  const list = (people.isError ? [] : people.data ?? [])
    .filter((p) => !taken.has(p.id))
    .filter((p) => (role === "leader" ? canLead(p) : true))
    .filter((p) => `${p.first_name} ${p.last_name}`.toLowerCase().includes(q.toLowerCase()));
  const meUser = me.data;
  const meAssignable = meUser && !taken.has(meUser.id) && (role === "member" || (meUser.gender === "M"));

  return (
    <DialogContent className="max-h-[90dvh] overflow-y-auto sm:max-w-md" data-testid="assign-dialog">
      <DialogHeader>
        <DialogTitle className="font-heading text-xl">Assegna al turno</DialogTitle>
        <DialogDescription>
          {shift.date.split("-").reverse().join("/")} · {shift.start}–{shift.end}. Il limite di 2 turni al mese non si applica.
        </DialogDescription>
      </DialogHeader>
      <div className="flex rounded-xl bg-slate-200/70 p-1">
        {(["leader", "member"] as ShiftRole[]).map((r) => {
          const disabled = r === "leader" ? !shift.missing_leader : shift.free_member_slots === 0;
          return (
            <button
              key={r}
              type="button"
              disabled={disabled}
              onClick={() => setRole(r)}
              data-testid={`assign-role-${r}`}
              className={cn(
                "flex min-h-10 flex-1 items-center justify-center gap-1.5 rounded-lg text-sm font-semibold transition-colors duration-150 disabled:opacity-40",
                role === r ? "bg-white shadow-sm" : "text-slate-600",
              )}
            >
              {r === "leader" ? <><Crown className="size-4" /> Capoturno</> : <><UserRound className="size-4" /> Volontario ({shift.free_member_slots} liberi)</>}
            </button>
          );
        })}
      </div>
      {meAssignable && (
        <Button
          variant="outline"
          className="h-11 w-full"
          disabled={assign.isPending}
          onClick={() => assign.mutate({ user_id: meUser.id, as_role: role })}
          data-testid="assign-me-button"
        >
          Assegna me stesso come {role === "leader" ? "Capoturno" : "Volontario"}
        </Button>
      )}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-slate-400" />
        <Input placeholder="Cerca volontario…" className="h-11 pl-9" value={q} onChange={(e) => setQ(e.target.value)}
          data-testid="assign-search-input" />
      </div>
      {people.isLoading && <div className="h-24 animate-pulse rounded-xl bg-slate-100" />}
      {!people.isLoading && list.length === 0 && (
        <p className="rounded-xl border border-dashed border-slate-200 p-4 text-center text-sm text-slate-500" data-testid="assign-empty">
          {role === "leader" ? "Nessun uomo abilitato come capoturno disponibile." : "Nessun volontario trovato."}
        </p>
      )}
      <ul className="space-y-1.5" data-testid="assign-list">
        {list.map((p) => (
          <li key={p.id}>
            <button
              type="button"
              disabled={assign.isPending}
              onClick={() => assign.mutate({ user_id: p.id, as_role: role })}
              data-testid={`assign-person-${p.id}`}
              className="flex min-h-12 w-full items-center gap-3 rounded-xl border border-slate-200 bg-white px-3 text-left transition-colors duration-150 hover:border-sky-300 hover:bg-sky-50"
            >
              <span className={cn("flex size-8 shrink-0 items-center justify-center rounded-lg text-xs font-bold",
                p.gender === "M" ? "bg-sky-100 text-sky-800" : "bg-rose-100 text-rose-800")}>
                {p.gender === "M" ? "U" : p.gender === "F" ? "D" : "?"}
              </span>
              <span className="min-w-0 flex-1">
                <span className="block truncate text-sm font-semibold">{p.first_name} {p.last_name}</span>
                <span className="block text-xs text-slate-500">
                  {p.role === "admin" ? "Amministratore" : `${p.upcoming_count} turni in programma`}
                  {p.is_team_leader && " · Capoturno"}
                </span>
              </span>
            </button>
          </li>
        ))}
      </ul>
    </DialogContent>
  );
}
