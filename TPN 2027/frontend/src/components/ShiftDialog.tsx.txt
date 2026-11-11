import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Repeat } from "lucide-react";
import { toast } from "sonner";
import { apiPost, apiPut } from "@/lib/api";
import { errMsg, useSlots, useStations } from "@/lib/hooks";
import { addHours } from "@/lib/shiftUi";
import type { ShiftBulkOut, ShiftCreateIn, ShiftIn, ShiftOut, StationKey } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";

interface Props {
  open: boolean;
  onOpenChange: (o: boolean) => void;
  editing: ShiftOut | null;
  defaultDate: string;
  defaultStation?: StationKey;
}

function duration(start: string, end: string): string {
  const [h1, m1] = start.split(":").map(Number);
  const [h2, m2] = end.split(":").map(Number);
  const mins = h2 * 60 + m2 - (h1 * 60 + m1);
  if (mins <= 0) return "";
  const h = Math.floor(mins / 60);
  const m = mins % 60;
  return `${h ? `${h} or${h === 1 ? "a" : "e"}` : ""}${h && m ? " e " : ""}${m ? `${m} min` : ""}`;
}

export default function ShiftDialog(props: Props) {
  // Keyed remount resets the form each time the dialog opens for a different shift.
  return (
    <Dialog open={props.open} onOpenChange={(o) => props.onOpenChange(o)}>
      {props.open && <ShiftForm key={props.editing?.id ?? "new"} {...props} />}
    </Dialog>
  );
}

function ShiftForm({ onOpenChange, editing, defaultDate, defaultStation }: Props) {
  const qc = useQueryClient();
  const stations = useStations();
  const slots = useSlots();
  const [station, setStation] = useState<StationKey>(editing?.station ?? defaultStation ?? stations.list[0]?.key ?? "a");
  const [date, setDate] = useState(editing?.date ?? defaultDate);
  const [start, setStart] = useState(editing?.start ?? "");
  const [end, setEnd] = useState(editing?.end ?? "");
  const [repeat, setRepeat] = useState(false);
  const [until, setUntil] = useState("");

  const save = useMutation({
    mutationFn: async (body: ShiftCreateIn): Promise<number> => {
      if (editing) {
        const upd: ShiftIn = { station: body.station, date: body.date, start: body.start, end: body.end };
        await apiPut<ShiftOut>(`/shifts/${editing.id}`, upd);
        return 1;
      }
      const res = await apiPost<ShiftBulkOut>("/shifts", body);
      if (res.skipped_dates.length) toast.warning(`${res.skipped_dates.length} date saltate: turno già esistente`);
      return res.created.length;
    },
    onSuccess: (n) => {
      toast.success(editing ? "Turno aggiornato" : n > 1 ? `Creati ${n} turni settimanali` : "Turno creato");
      qc.invalidateQueries({ queryKey: ["shifts"] });
      onOpenChange(false);
    },
    onError: (e) => toast.error(errMsg(e)),
  });

  const dur = start && end ? duration(start, end) : "";

  return (
    <DialogContent className="max-h-[90dvh] overflow-y-auto sm:max-w-md" data-testid="shift-dialog">
      <DialogHeader>
        <DialogTitle className="font-heading text-xl">{editing ? "Modifica turno" : "Nuovo turno"}</DialogTitle>
        <DialogDescription>1 Capoturno (uomo) + 2 volontari</DialogDescription>
      </DialogHeader>
      <form
        className="space-y-5"
        onSubmit={(e) => {
          e.preventDefault();
          if (!start || !end) return toast.error("Indica orario di inizio e fine");
          if (end <= start) return toast.error("L'orario di fine deve essere successivo all'inizio");
          if (repeat && !until) return toast.error("Indica fino a quando ripetere il turno");
          save.mutate({ station, date, start, end, repeat_until: repeat ? until : null });
        }}
      >
        <div className="space-y-2">
          <Label>Postazione</Label>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
            {stations.list.map((s) => (
              <button
                type="button"
                key={s.key}
                onClick={() => setStation(s.key)}
                data-testid={`shift-dialog-station-${s.key}`}
                className={cn(
                  "min-h-11 truncate rounded-xl border px-2 text-sm font-semibold transition-colors duration-150",
                  station === s.key ? stations.styleOf(s.key).pillActive : "border-slate-200 bg-white text-slate-700 hover:bg-slate-50",
                )}
              >
                {s.name}
              </button>
            ))}
          </div>
        </div>
        <div className="space-y-2">
          <Label htmlFor="shift-date">Data</Label>
          <Input id="shift-date" type="date" required value={date} onChange={(e) => setDate(e.target.value)}
            className="h-11" data-testid="shift-dialog-date-input" />
        </div>
        <div className="space-y-2">
          <Label>Orario</Label>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <span className="text-xs text-slate-500">Inizio</span>
              <Input type="time" required value={start} onChange={(e) => setStart(e.target.value)} className="h-11"
                data-testid="shift-dialog-start-input" />
            </div>
            <div>
              <span className="text-xs text-slate-500">Fine</span>
              <Input type="time" required value={end} onChange={(e) => setEnd(e.target.value)} className="h-11"
                data-testid="shift-dialog-end-input" />
            </div>
          </div>
          {dur && <p className="text-xs font-medium text-slate-600" data-testid="shift-dialog-duration">Durata: {dur}</p>}
          {(slots.data?.slots.length ?? 0) > 0 && (
            <div className="flex flex-wrap gap-1.5 pt-1">
              <span className="w-full text-xs text-slate-500">Fasce rapide (2 ore)</span>
              {slots.data?.slots.map((s) => (
                <button
                  type="button"
                  key={s}
                  onClick={() => { setStart(s); setEnd(addHours(s, 2)); }}
                  data-testid={`shift-dialog-slot-${s.replace(":", "")}`}
                  className={cn(
                    "min-h-9 rounded-lg border px-2.5 text-xs font-semibold tabular-nums transition-colors duration-150",
                    start === s && end === addHours(s, 2) ? "border-slate-900 bg-slate-900 text-white" : "border-slate-200 bg-white hover:bg-slate-50",
                  )}
                >
                  {s}–{addHours(s, 2)}
                </button>
              ))}
            </div>
          )}
        </div>
        {!editing && (
          <div className="space-y-3 rounded-xl border border-slate-200 p-3">
            <label className="flex items-center gap-2 text-sm font-semibold">
              <Checkbox checked={repeat} onCheckedChange={(c) => setRepeat(c === true)} data-testid="shift-dialog-repeat-checkbox" />
              <Repeat className="size-4" /> Ripeti ogni settimana
            </label>
            {repeat && (
              <div className="space-y-1">
                <Label htmlFor="shift-until">Fino al (compreso)</Label>
                <Input id="shift-until" type="date" min={date} value={until} onChange={(e) => setUntil(e.target.value)}
                  className="h-11" data-testid="shift-dialog-until-input" />
              </div>
            )}
          </div>
        )}
        <DialogFooter>
          <Button type="submit" className="h-11 w-full bg-sky-600 text-white hover:bg-sky-700" disabled={save.isPending}
            data-testid="shift-dialog-submit-button">
            {save.isPending ? "Salvataggio…" : editing ? "Salva modifiche" : repeat ? "Crea turni ripetuti" : "Crea turno"}
          </Button>
        </DialogFooter>
      </form>
    </DialogContent>
  );
}
