import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Crown, KeyRound, LogOut, Mail, ShieldCheck } from "lucide-react";
import { toast } from "sonner";
import { apiPut } from "@/lib/api";
import { errMsg, useMe } from "@/lib/hooks";
import { endSession } from "@/lib/session";
import type { CredentialsIn, Gender, ProfileIn, UserPublic } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import GenderPicker from "@/components/GenderPicker";
import LeaderShifts from "@/components/LeaderShifts";
import MyStats from "@/components/MyStats";

export default function Profile() {
  const me = useMe();
  const user = me.data;

  return (
    <div className="mx-auto max-w-xl space-y-6">
      <div>
        <p className="text-sm font-medium text-slate-500">Il tuo account</p>
        <h1 className="font-heading text-3xl font-bold tracking-tight md:text-4xl">Profilo</h1>
      </div>

      <div className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5">
        <span className="flex size-14 items-center justify-center rounded-2xl bg-slate-900 font-heading text-xl font-bold text-white">
          {(user?.first_name?.[0] ?? "?").toUpperCase()}
          {(user?.last_name?.[0] ?? "").toUpperCase()}
        </span>
        <div className="min-w-0">
          <p className="truncate font-heading text-lg font-bold" data-testid="profile-name">
            {user ? `${user.first_name} ${user.last_name}`.trim() : "…"}
          </p>
          <p className="flex items-center gap-1 truncate text-sm text-slate-500" data-testid="profile-email">
            <Mail className="size-3.5" /> {user?.email}
          </p>
          <span className="mt-1 inline-flex items-center gap-1 rounded-full bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-700" data-testid="profile-role">
            {user?.role === "admin" ? <><ShieldCheck className="size-3" /> Amministratore</> : "Volontario"}
          </span>
          {user?.is_team_leader && (
            <span className="ml-1 mt-1 inline-flex items-center gap-1 rounded-full bg-slate-900 px-2 py-0.5 text-xs font-semibold text-amber-300" data-testid="profile-leader-badge">
              <Crown className="size-3" /> Capoturno
            </span>
          )}
        </div>
      </div>

      {user?.role === "volunteer" && (!user.gender || !user.phone) && (
        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-900" data-testid="profile-incomplete-banner">
          <p className="font-semibold">Completa il tuo profilo</p>
          <p>Indica genere e telefono per poter vedere e prenotare i turni.</p>
        </div>
      )}

      {user && <MyStats />}

      {user?.is_team_leader && <LeaderShifts />}

      {user && <ProfileForm key={user.id} user={user} />}

      {user && <CredentialsForm key={`${user.id}-${user.email}`} user={user} />}

      <Button
        variant="outline"
        className="h-11 w-full gap-2 text-red-700 hover:bg-red-50"
        onClick={() => endSession()}
        data-testid="profile-logout-button"
      >
        <LogOut className="size-4" /> Esci
      </Button>
    </div>
  );
}

function CredentialsForm({ user }: { user: UserPublic }) {
  const qc = useQueryClient();
  const [email, setEmail] = useState(user.email);
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const save = useMutation({
    mutationFn: (b: CredentialsIn) => apiPut<UserPublic>("/me/credentials", b),
    onSuccess: (u) => {
      qc.setQueryData(["me"], u);
      setCurrent("");
      setNext("");
      toast.success("Credenziali aggiornate");
    },
    onError: (e) => toast.error(errMsg(e)),
  });
  return (
    <form
      className="space-y-4 rounded-2xl border border-slate-200 bg-white p-5"
      onSubmit={(e) => {
        e.preventDefault();
        save.mutate({ email, current_password: current, new_password: next || null });
      }}
      data-testid="credentials-form"
    >
      <div>
        <h2 className="flex items-center gap-2 font-heading text-lg font-bold"><KeyRound className="size-4" /> Credenziali di accesso</h2>
        <p className="text-sm text-slate-500">
          {user.has_password ? "Modifica email e/o password. Serve la password attuale." : "Accedi con Google: puoi impostare anche una password."}
        </p>
      </div>
      <div className="space-y-2">
        <Label htmlFor="c-email">Email</Label>
        <Input id="c-email" type="email" required className="h-11" value={email}
          onChange={(e) => setEmail(e.target.value)} data-testid="credentials-email-input" />
      </div>
      {user.has_password && (
        <div className="space-y-2">
          <Label htmlFor="c-current">Password attuale</Label>
          <Input id="c-current" type="password" required autoComplete="current-password" className="h-11" value={current}
            onChange={(e) => setCurrent(e.target.value)} data-testid="credentials-current-password-input" />
        </div>
      )}
      <div className="space-y-2">
        <Label htmlFor="c-new">Nuova password (lascia vuoto per non cambiarla)</Label>
        <Input id="c-new" type="password" minLength={6} autoComplete="new-password" className="h-11" value={next}
          onChange={(e) => setNext(e.target.value)} data-testid="credentials-new-password-input" />
      </div>
      <Button type="submit" variant="outline" className="h-11 w-full" disabled={save.isPending}
        data-testid="credentials-save-button">
        {save.isPending ? "Salvataggio…" : "Aggiorna credenziali"}
      </Button>
    </form>
  );
}

function ProfileForm({ user }: { user: UserPublic }) {
  const qc = useQueryClient();
  const [f, setF] = useState({ first_name: user.first_name, last_name: user.last_name, phone: user.phone });
  const [gender, setGender] = useState<Gender | null>(user.gender);
  const save = useMutation({
    mutationFn: (b: ProfileIn) => apiPut<UserPublic>("/me", b),
    onSuccess: (u) => {
      qc.setQueryData(["me"], u);
      qc.invalidateQueries({ queryKey: ["shifts"] });
      toast.success("Profilo aggiornato");
    },
    onError: (e) => toast.error(errMsg(e)),
  });

  return (
    <form
      className="space-y-4 rounded-2xl border border-slate-200 bg-white p-5"
      onSubmit={(e) => {
        e.preventDefault();
        if (!gender) return toast.error("Seleziona il genere");
        save.mutate({ ...f, gender });
      }}
      data-testid="profile-form"
    >
      <h2 className="font-heading text-lg font-bold">Dati personali</h2>
      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-2">
          <Label htmlFor="p-first">Nome</Label>
          <Input id="p-first" required className="h-11" value={f.first_name}
            onChange={(e) => setF({ ...f, first_name: e.target.value })} data-testid="profile-first-name-input" />
        </div>
        <div className="space-y-2">
          <Label htmlFor="p-last">Cognome</Label>
          <Input id="p-last" required className="h-11" value={f.last_name}
            onChange={(e) => setF({ ...f, last_name: e.target.value })} data-testid="profile-last-name-input" />
        </div>
      </div>
      <div className="space-y-2">
        <Label>Genere</Label>
        <GenderPicker value={gender} onChange={setGender} testidPrefix="profile" />
      </div>
      <div className="space-y-2">
        <Label htmlFor="p-phone">Telefono</Label>
        <Input id="p-phone" type="tel" required minLength={5} className="h-11" value={f.phone}
          onChange={(e) => setF({ ...f, phone: e.target.value })} data-testid="profile-phone-input" />
      </div>
      <Button type="submit" className="h-11 w-full bg-sky-600 text-white hover:bg-sky-700" disabled={save.isPending}
        data-testid="profile-save-button">
        {save.isPending ? "Salvataggio…" : "Salva profilo"}
      </Button>
    </form>
  );
}
