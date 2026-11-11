import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { format } from "date-fns";
import { it } from "date-fns/locale";
import { Megaphone, Pin, Trash2 } from "lucide-react";
import { toast } from "sonner";
import { apiDelete, apiGet, apiPost } from "@/lib/api";
import { errMsg, useMe } from "@/lib/hooks";
import type { Announcement, AnnouncementIn } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Checkbox } from "../components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import NotificationsPanel from "@/components/NotificationsPanel";

export default function Board() {
  const me = useMe();
  const qc = useQueryClient();
  const isAdmin = me.data?.role === "admin";
  const list = useQuery({ queryKey: ["announcements"], queryFn: () => apiGet<Announcement[]>("/announcements") });
  const [form, setForm] = useState<AnnouncementIn>({ title: "", body: "", pinned: false });

  const create = useMutation({
    mutationFn: (b: AnnouncementIn) => apiPost<Announcement>("/announcements", b),
    onSuccess: () => {
      toast.success("Avviso pubblicato");
      setForm({ title: "", body: "", pinned: false });
      qc.invalidateQueries({ queryKey: ["announcements"] });
    },
    onError: (e) => toast.error(errMsg(e)),
  });
  const del = useMutation({
    mutationFn: (id: string) => apiDelete(`/announcements/${id}`),
    onSuccess: () => {
      toast.success("Avviso eliminato");
      qc.invalidateQueries({ queryKey: ["announcements"] });
    },
    onError: (e) => toast.error(errMsg(e)),
  });

  const items = list.isError ? [] : list.data ?? [];

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium text-slate-500">Comunicazioni dell'associazione</p>
        <h1 className="font-heading text-3xl font-bold tracking-tight md:text-4xl">Bacheca Avvisi</h1>
      </div>

      <NotificationsPanel />

      <div className={cn("grid gap-6", isAdmin && "lg:grid-cols-[minmax(0,1fr)_380px]")}>
        <div className="space-y-3 lg:order-1" data-testid="announcements-list">
          {list.isLoading && <div className="h-32 animate-pulse rounded-2xl bg-slate-200/60" />}
          {!list.isLoading && items.length === 0 && (
            <div className="flex flex-col items-center rounded-3xl border border-dashed border-slate-300 bg-white px-6 py-12 text-center" data-testid="announcements-empty">
              <Megaphone className="size-10 text-slate-300" />
              <p className="mt-3 font-heading text-lg font-semibold">Nessun avviso</p>
              <p className="mt-1 text-sm text-slate-500">Le comunicazioni pubblicate appariranno qui.</p>
            </div>
          )}
          {items.map((a) => (
            <article
              key={a.id}
              data-testid={`announcement-${a.id}`}
              className={cn(
                "animate-fade-up rounded-2xl border bg-white p-5 shadow-[0_8px_24px_-14px_rgba(15,23,42,0.18)]",
                a.pinned ? "border-sky-200 bg-gradient-to-br from-sky-50 to-white" : "border-slate-200",
              )}
            >
              <div className="flex items-start gap-3">
                <div className="min-w-0 flex-1">
                  {a.pinned && (
                    <span className="mb-2 inline-flex items-center gap-1 rounded-full bg-sky-600 px-2 py-0.5 text-[11px] font-semibold text-white">
                      <Pin className="size-3" /> In evidenza
                    </span>
                  )}
                  <h2 className="font-heading text-lg font-bold leading-snug" data-testid="announcement-title">
                    {a.title}
                  </h2>
                  <p className="mt-0.5 text-xs text-slate-500">
                    {a.author_name} · {format(new Date(a.created_at), "d MMMM yyyy, HH:mm", { locale: it })}
                  </p>
                </div>
                {isAdmin && (
                  <Button
                    variant="ghost"
                    size="icon-sm"
                    className="text-red-600 hover:bg-red-50"
                    aria-label="Elimina avviso"
                    onClick={() => window.confirm("Eliminare questo avviso?") && del.mutate(a.id)}
                    data-testid={`announcement-delete-${a.id}`}
                  >
                    <Trash2 className="size-4" />
                  </Button>
                )}
              </div>
              <p className="mt-3 whitespace-pre-line text-[15px] leading-relaxed text-slate-700" data-testid="announcement-body">
                {a.body}
              </p>
            </article>
          ))}
        </div>

        {isAdmin && (
          <form
            className="h-fit space-y-4 rounded-2xl border border-slate-200 bg-white p-5 lg:sticky lg:top-8 lg:order-2"
            onSubmit={(e) => {
              e.preventDefault();
              create.mutate(form);
            }}
            data-testid="announcement-form"
          >
            <h2 className="font-heading text-lg font-bold">Nuovo avviso</h2>
            <div className="space-y-2">
              <Label htmlFor="ann-title">Titolo</Label>
              <Input
                id="ann-title"
                required
                className="h-11"
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                data-testid="announcement-title-input"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="ann-body">Messaggio</Label>
              <Textarea
                id="ann-body"
                required
                rows={5}
                value={form.body}
                onChange={(e) => setForm({ ...form, body: e.target.value })}
                data-testid="announcement-body-input"
              />
            </div>
            <label className="flex items-center gap-2 text-sm">
              <Checkbox
                checked={form.pinned}
                onCheckedChange={(c: any) => setForm({ ...form, pinned: c === true })}
                data-testid="announcement-pinned-checkbox"
              />
              Metti in evidenza
            </label>
            <Button
              type="submit"
              className="h-11 w-full bg-sky-600 text-white hover:bg-sky-700"
              disabled={create.isPending}
              data-testid="announcement-submit-button"
            >
              {create.isPending ? "Pubblicazione…" : "Pubblica"}
            </Button>
          </form>
        )}
      </div>
    </div>
  );
}
