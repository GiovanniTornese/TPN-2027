import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { apiPost } from "@/lib/api";
import { errMsg } from "@/lib/hooks";
import { beginSession } from "@/lib/session";
import type { Gender, RegisterIn, UserPublic } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import AuthLayout from "@/components/AuthLayout";
import GoogleButton, { OrDivider } from "@/components/GoogleButton";
import GenderPicker from "@/components/GenderPicker";

export default function Register() {
  const nav = useNavigate();
  const [gender, setGender] = useState<Gender | null>(null);
  const [f, setF] = useState({ first_name: "", last_name: "", phone: "", email: "", password: "" });
  const reg = useMutation({
    mutationFn: (body: RegisterIn) => apiPost<UserPublic>("/auth/register", body),
    onSuccess: () => {
      beginSession();
      toast.success("Registrazione completata!");
      nav("/", { replace: true });
    },
    onError: (e) => toast.error(errMsg(e, "Registrazione non riuscita")),
  });

  const field = (key: keyof typeof f, label: string, type = "text", auto?: string) => (
    <div className="space-y-2">
      <Label htmlFor={`reg-${key}`}>{label}</Label>
      <Input
        id={`reg-${key}`}
        type={type}
        autoComplete={auto}
        required
        minLength={key === "password" ? 6 : undefined}
        className="h-12"
        value={f[key]}
        onChange={(e) => setF({ ...f, [key]: e.target.value })}
        data-testid={`register-${key.replace("_", "-")}-input`}
      />
    </div>
  );

  return (
    <AuthLayout title="Diventa volontario" subtitle="Crea il tuo account per iscriverti ai turni.">
      <GoogleButton label="Registrati con Google" />
      <OrDivider />
      <form
        className="space-y-4"
        onSubmit={(e) => {
          e.preventDefault();
          if (!gender) return toast.error("Seleziona il genere");
          reg.mutate({ ...f, gender });
        }}
      >
        <div className="grid grid-cols-2 gap-3">
          {field("first_name", "Nome", "text", "given-name")}
          {field("last_name", "Cognome", "text", "family-name")}
        </div>
        <div className="space-y-2">
          <Label>Genere</Label>
          <GenderPicker value={gender} onChange={setGender} testidPrefix="register" />
        </div>
        {field("phone", "Telefono", "tel", "tel")}
        {field("email", "Email", "email", "email")}
        {field("password", "Password (min. 6 caratteri)", "password", "new-password")}
        <Button
          type="submit"
          className="h-12 w-full bg-sky-600 text-base text-white hover:bg-sky-700"
          disabled={reg.isPending}
          data-testid="register-submit-button"
        >
          {reg.isPending ? "Registrazione…" : "Crea account"}
        </Button>
      </form>
      <p className="mt-6 text-center text-sm text-slate-600">
        Hai già un account?{" "}
        <Link to="/login" className="font-semibold text-sky-700 hover:underline" data-testid="register-login-link">
          Accedi
        </Link>
      </p>
    </AuthLayout>
  );
}
