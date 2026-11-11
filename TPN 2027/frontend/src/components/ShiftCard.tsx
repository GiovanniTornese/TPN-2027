import { useMutation, useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, ClipboardCheck, Crown, Pencil, Trash2, UserPlus, UserRound, X, CircleAlert, Phone } from "lucide-react";
import { toast } from "sonner";
import { apiDelete, apiPost } from "@/lib/api";
import { errMsg, useStations } from "@/lib/hooks";
import { useState } from "react";
import { needsLabel } from "@/lib/shiftUi";
import AssignDialog from "@/components/AssignDialog";
import ReportDialog from "@/components/ReportDialog";
import type { JoinIn, ShiftOut, ShiftRole, ShiftVolunteer, UserPublic } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface Props {
  shift: ShiftOut;
  stationName: string;
  user: UserPublic | undefined;
  isPast: boolean;
  monthFull?: boolean;
  compact?: boolean;
  onEdit?: (s: ShiftOut) => void;
}

interface RowProps {
  v: ShiftVolunteer;
  leader?: boolean;
  user: UserPublic | undefined;
  compact?: boolean;
  onRemove: (v: ShiftVolunteer) => void;
}

function VolunteerRow({ v, leader, user, compact, onRemove }: RowProps) {
  const isAdmin = user?.role === "admin";
  return (
    <li className="flex items-center gap-2 text-sm" data-testid={`shift-volunteer-${v.id}`}>
      <span
        className={cn(
          "flex size-6 shrink-0 items-center justify-center rounded-full",
          leader ? "bg-slate-900 text-amber-300" : "bg-slate-100 text-slate-600",
        )}
      >
        {leader ? <Crown className="size-3.5" /> : <UserRound className="size-3.5" />}
      </span>
      <span className={cn("truncate", v.id === user?.id && "font-semibold text-sky-700")}>
        {v.first_name} {v.last_name}
        {v.id === user?.id && " (tu)"}
      </span>
      {leader && <span className="shrink-0 text-[11px] font-semibold uppercase tracking-wide text-slate-500">Capoturno</span>}
      {isAdmin && v.phone && (
        <a
          href={`tel:${v.phone}`}
          className="ml-auto flex items-center gap-1 text-xs text-slate-500 hover:text-sky-700"
          data-testid={`shift-volunteer-phone-${v.id}`}
        >
          <Phone className="size-3" />
          {!compact && v.phone}
        </a>
      )}
      {isAdmin && (
        <button
          type="button"
          aria-label="Rimuovi dal turno"
          onClick={() => onRemove(v)}
          className={cn(
            "flex size-7 shrink-0 items-center justify-center rounded-full text-slate-400 transition-colors duration-150 hover:bg-red-50 hover:text-red-600",
            !v.phone && "ml-auto",
          )}
          data-testid={`shift-remove-volunteer-${v.id}`}
        >
          <X className="size-3.5" />
        </button>
      )}
    </li>
  );
}

function FreeRow({ label }: { label: string }) {
  return (
    <li className="flex items-center gap-2 text-sm text-slate-400">
      <span className="flex size-6 items-center justify-center rounded-full border border-dashed border-slate-300">
        <UserRound className="size-3" />
      </span>
      {label}
    </li>
  );
}

export default function ShiftCard({ shift, stationName, user, isPast, monthFull, compact, onEdit }: Props) {
  const qc = useQueryClient();
  const st = useStations().styleOf(shift.station);
  const [assignOpen, setAssignOpen] = useState(false);
  const [reportOpen, setReportOpen] = useState(false);
  const isAdmin = user?.role === "admin";
  const invalidate = () => {
    qc.invalidateQueries({ queryKey: ["shifts"] });
    qc.invalidateQueries({ queryKey: ["usage"] });
  };

  const join = useMutation({
    mutationFn: (as_role: ShiftRole) => apiPost<ShiftOut>(`/shifts/${shift.id}/join`, { as_role } satisfies JoinIn),
    onSuccess: (_, role) => {
      toast.success(role === "leader" ? "Iscritto come Capoturno" : "Iscrizione confermata");
      invalidate();
    },
    onError: (e) => {
      toast.error(errMsg(e));
      invalidate();
    },
  });
  const leave = useMutation({
    mutationFn: () => apiPost<ShiftOut>(`/shifts/${shift.id}/leave`),
    onSuccess: () => {
      toast.success("Iscrizione annullata");
      invalidate();
    },
    onError: (e) => toast.error(errMsg(e)),
  });
  const remove = useMutation({
    mutationFn: (uid: string) => apiDelete<ShiftOut>(`/shifts/${shift.id}/volunteers/${uid}`),
    onSuccess: () => {
      toast.success("Volontario rimosso dal turno");
      invalidate();
    },
    onError: (e) => toast.error(errMsg(e)),
  });
  const del = useMutation({
    mutationFn: () => apiDelete(`/shifts/${shift.id}`),
    onSuccess: () => {
      toast.success("Turno eliminato");
      invalidate();
    },
    onError: (e) => toast.error(errMsg(e)),
  });
  const onRemove = (v: ShiftVolunteer) => {
    if (window.confirm(`Rimuovere ${v.first_name} da questo turno?`)) remove.mutate(v.id);
  };

  const canLead = user?.role === "volunteer" && user.gender === "M" && user.is_team_leader;
  let blockedReason = "";
  if (!shift.is_mine) {
    if (isPast) blockedReason = "Turno passato";
    else if (shift.is_complete) blockedReason = "Completo";
    else if (!user?.gender || !user.phone) blockedReason = "Completa il profilo";
    else if (monthFull) blockedReason = "Limite 2 turni/mese raggiunto";
    else if (shift.free_member_slots === 0 && !canLead) blockedReason = "Resta solo il posto Capoturno";
  }
  const showLeadButton = !blockedReason && canLead && shift.missing_leader;
  const showMemberButton = !blockedReason && shift.free_member_slots > 0;

  return (
    <article
      data-testid={`shift-card-${shift.id}`}
      className={cn(
        "animate-fade-up relative overflow-hidden rounded-2xl border bg-white shadow-[0_1px_2px_rgba(15,23,42,0.04),0_8px_24px_-12px_rgba(15,23,42,0.12)] transition-shadow duration-200 hover:shadow-[0_2px_4px_rgba(15,23,42,0.06),0_16px_32px_-12px_rgba(15,23,42,0.18)]",
        shift.is_mine ? "border-sky-300 ring-2 ring-sky-100" : "border-slate-200",
        isPast && "opacity-70",
      )}
    >
      <span className={cn("absolute inset-y-0 left-0 w-1.5", st.bar)} aria-hidden />
      <div className={cn("pl-5 pr-4", compact ? "py-3" : "py-4")}>
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <p
              className={cn("font-heading font-bold tracking-tight tabular-nums", compact ? "text-base" : "text-xl")}
              data-testid="shift-time"
            >
              {shift.start}–{shift.end}
            </p>
            <span
              className={cn(
                "mt-1 inline-flex max-w-full items-center gap-1.5 truncate rounded-full border px-2 py-0.5 text-xs font-semibold",
                st.soft,
                st.text,
                st.border,
              )}
              data-testid="shift-station-badge"
            >
              <span className={cn("size-1.5 rounded-full", st.dot)} />
              {stationName}
            </span>
          </div>
          {isAdmin && onEdit && (
            <div className="flex shrink-0 gap-1">
              <Button variant="ghost" size="icon-sm" aria-label="Modifica turno" onClick={() => onEdit(shift)} data-testid="shift-edit-button">
                <Pencil className="size-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon-sm"
                aria-label="Elimina turno"
                className="text-red-600 hover:bg-red-50 hover:text-red-700"
                onClick={() => {
                  if (window.confirm("Eliminare questo turno? Le iscrizioni verranno perse.")) del.mutate();
                }}
                data-testid="shift-delete-button"
              >
                <Trash2 className="size-4" />
              </Button>
            </div>
          )}
        </div>

        <div
          className={cn(
            "mt-3 inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1 text-xs font-semibold",
            shift.is_complete ? "bg-green-100 text-green-900" : "bg-amber-100 text-amber-900",
          )}
          data-testid="shift-status"
          aria-label={shift.is_complete ? "Turno completo" : "Turno incompleto"}
        >
          {shift.is_complete ? (
            <>
              <CheckCircle2 className="size-3.5" /> Completo
            </>
          ) : (
            <>
              <CircleAlert className="size-3.5" />
              Incompleto · {shift.free_slots} {shift.free_slots === 1 ? "posto libero" : "posti liberi"} ·{" "}
              {needsLabel(shift.missing_leader, shift.free_member_slots)}
            </>
          )}
        </div>

        <ul className="mt-3 space-y-1.5" data-testid="shift-volunteers">
          {shift.leader ? (
            <VolunteerRow v={shift.leader} leader user={user} compact={compact} onRemove={onRemove} />
          ) : (
            <FreeRow label="Posto libero · Capoturno (uomo)" />
          )}
          {shift.members.map((v) => (
            <VolunteerRow key={v.id} v={v} user={user} compact={compact} onRemove={onRemove} />
          ))}
          {Array.from({ length: shift.free_member_slots }, (_, i) => (
            <FreeRow key={`f-${i}`} label="Posto libero · Volontario" />
          ))}
        </ul>

        {(isAdmin && !shift.is_complete) || (shift.is_mine && shift.has_ended) ? (
          <div className="mt-4 flex flex-col gap-2">
            {isAdmin && !shift.is_complete && (
              <Button
                variant="outline"
                className="h-11 w-full gap-1.5 border-sky-200 text-sky-800 transition-colors duration-150 hover:bg-sky-50"
                onClick={() => setAssignOpen(true)}
                data-testid="shift-assign-button"
              >
                <UserPlus className="size-4" /> Assegna
              </Button>
            )}
            {shift.is_mine && shift.has_ended && (
              <Button
                className={cn(
                  "h-11 w-full gap-1.5 transition-colors duration-150",
                  shift.my_report_done ? "bg-green-100 text-green-900 hover:bg-green-200" : "bg-amber-500 text-white hover:bg-amber-600",
                )}
                onClick={() => setReportOpen(true)}
                data-testid="shift-report-button"
              >
                <ClipboardCheck className="size-4" /> {shift.my_report_done ? "Resoconto inviato · modifica" : "Inserisci resoconto"}
              </Button>
            )}
          </div>
        ) : null}
        {isAdmin && <AssignDialog shift={shift} open={assignOpen} onOpenChange={setAssignOpen} />}
        {shift.is_mine && <ReportDialog shift={shift} stationName={stationName} open={reportOpen} onOpenChange={setReportOpen} />}

        {user?.role === "volunteer" && !(shift.is_mine && shift.has_ended) && (
          <div className="mt-4 space-y-2">
            {shift.is_mine ? (
              <Button
                variant="outline"
                className="h-11 w-full border-red-200 text-red-700 transition-colors duration-150 hover:bg-red-50"
                disabled={leave.isPending || isPast}
                onClick={() => leave.mutate()}
                data-testid="shift-leave-button"
              >
                {leave.isPending ? "Annullamento…" : "Annulla iscrizione"}
              </Button>
            ) : blockedReason ? (
              <Button disabled className="h-11 w-full" data-testid="shift-join-button">
                {blockedReason}
              </Button>
            ) : (
              <>
                {showLeadButton && (
                  <Button
                    className="h-11 w-full gap-1.5 bg-slate-900 text-white transition-colors duration-150 hover:bg-slate-800"
                    disabled={join.isPending}
                    onClick={() => join.mutate("leader")}
                    data-testid="shift-join-leader-button"
                  >
                    <Crown className="size-4 text-amber-300" /> Iscriviti come Capoturno
                  </Button>
                )}
                {showMemberButton && (
                  <Button
                    className="h-11 w-full bg-sky-600 text-white transition-colors duration-150 hover:bg-sky-700"
                    disabled={join.isPending}
                    onClick={() => join.mutate("member")}
                    data-testid="shift-join-button"
                  >
                    {join.isPending ? "Iscrizione…" : showLeadButton ? "Iscriviti come volontario" : "Iscriviti"}
                  </Button>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </article>
  );
}
