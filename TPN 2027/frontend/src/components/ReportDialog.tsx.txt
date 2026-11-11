import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Lock } from "lucide-react";
import { toast } from "sonner";
import { apiGet, apiPut } from "@/lib/api";
import { errMsg } from "@/lib/hooks";
import { fmt } from "@/lib/shiftUi";
import type { MyReportsOut, ReportIn, ReportOut, ShiftOut } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";

const HOURS = [0.5, 1, 1.5, 2];

interface Props {
  shift: ShiftOut;
  stationName: string;
  open: boolean;
  onOpenChange: (o: boolean) => void;
}

export function useMyReports() {
  return useQuery({ queryKey: ["reports", "me"], queryFn: () => apiGet<MyReportsOut>("/reports/me") });
}

export default function ReportDialog({ shift, stationName, open, onOpenChange }: Props) {
  const mine = useMyReports();
  const existing = mine.data?.reports.find((r) => r.shift_id === shift.id);
  return (
    <Dialog open={open} onOpenChange={(o) => onOpenChange(o)}>
      {open && !mine.isLoading && (
        <ReportForm key={existing?.id ?? "new"} shift={shift} stationName={stationName} existing={existing} onDone={() => onOpenChange(false)} />
      )}
    </Dialog>
  );
}

function ReportForm({ shift, stationName, existing, onDone }: {
  shift: ShiftOut; stationName: string; existing?: ReportOut; onDone: () => void;
}) {
  const qc = useQueryClient();
  const [hours, setHours] = useState<number>(existing?.hours ?? 2);
  const [pubs, setPubs] = useState(String(existing?.publications ?? 0));
  const [comment, setComment] = useState(existing?.comment ?? "");
  const save = useMutation({
    mutationFn: (b: ReportIn) => apiPut<ReportOut>(`/shifts/${shift.id}/report`, b),
    onSuccess: () => {
      toast.success("Resoconto salvato, grazie!");
      qc.invalidateQueries({ queryKey: ["reports"] });
      qc.invalidateQueries({ queryKey: ["shifts"] });
      onDone();
    },
    onError: (e) => toast.error(errMsg(e)),
  });

  return (
    <DialogContent className="max-h-[90dvh] overflow-y-auto sm:max-w-md" data-testid="report-dialog">
      <DialogHeader>
        <DialogTitle className="font-heading text-xl">Resoconto del turno</DialogTitle>
        <DialogDescription className="capitalize">
          {fmt(shift.date, "EEEE d MMMM")} · {shift.start}–{shift.end} · {stationName}
        </DialogDescription>
      </DialogHeader>
      <form
        className="space-y-5"
        onSubmit={(e) => {
          e.preventDefault();
          const n = Number(pubs);
          if (!Number.isInteger(n) || n < 0) return toast.error("Numero di pubblicazioni non valido");
          save.mutate({ hours, publications: n, comment });
        }}
      >
        <div className="space-y-2">
          <Label>Ore svolte</Label>
          <div className="grid grid-cols-4 gap-2">
            {HOURS.map((h) => (
              <button
                key={h}
                type="button"
                onClick={() => setHours(h)}
                data-testid={`report-hours-${String(h).replace(".", "-")}`}
                className={cn(
                  "min-h-12 rounded-xl border text-base font-bold tabular-nums transition-colors duration-150",
                  hours === h ? "border-slate-900 bg-slate-900 text-white" : "border-slate-200 bg-white hover:bg-slate-50",
                )}
              >
                {h.toLocaleString("it-IT")}
              </button>
            ))}
          </div>
        </div>
        <div className="space-y-2">
          <Label htmlFor="report-pubs">Pubblicazioni lasciate</Label>
          <Input id="report-pubs" type="number" inputMode="numeric" min={0} step={1} required className="h-12 text-lg"
            value={pubs} onChange={(e) => setPubs(e.target.value)} data-testid="report-publications-input" />
        </div>
        <div className="space-y-2">
          <Label htmlFor="report-comment">Commento (facoltativo)</Label>
          <Textarea id="report-comment" rows={3} value={comment} onChange={(e) => setComment(e.target.value)}
            placeholder="Esperienze, problemi, segnalazioni…" data-testid="report-comment-input" />
          <p className="flex items-center gap-1 text-xs text-slate-500"><Lock className="size-3" /> Visibile solo agli amministratori</p>
        </div>
        <Button type="submit" className="h-12 w-full bg-sky-600 text-white hover:bg-sky-700" disabled={save.isPending}
          data-testid="report-submit-button">
          {save.isPending ? "Salvataggio…" : existing ? "Aggiorna resoconto" : "Invia resoconto"}
        </Button>
      </form>
    </DialogContent>
  );
}
