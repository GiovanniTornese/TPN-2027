import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { apiPost } from "@/lib/api";
import { errMsg } from "@/lib/hooks";
import { beginSession } from "@/lib/session";
import type { LoginIn, UserPublic } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import AuthLayout from "@/components/AuthLayout";
import GoogleButton, { OrDivider } from "@/components/GoogleButton";

export default function Login() {
  const nav = useNavigate();
  const [form, setForm] = useState<LoginIn>({ email: "", password: "" });
  const login = useMutation({
    mutationFn: (body: LoginIn) => apiPost<UserPublic>("/auth/login", body),
    onSuccess: () => {
      beginSession();
      nav("/", { replace: true });
    },
    onError: (e) => toast.error(errMsg(e, "Accesso non riuscito")),
  });

  return (
    <AuthLayout title="Bentornato" subtitle="Accedi per consultare e prenotare i tuoi turni.">
      <GoogleButton />
      <OrDivider />
      <form
        className="space-y-4"
        onSubmit={(e) => {
          e.preventDefault();
          login.mutate(form);
        }}
      >
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input
            id="email"
            type="email"
            autoComplete="email"
            required
            className="h-12"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            data-testid="login-email-input"
          />
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input
            id="password"
            type="password"
            autoComplete="current-password"
            required
            className="h-12"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            data-testid="login-password-input"
          />
        </div>
        <Button
          type="submit"
          className="h-12 w-full bg-sky-600 text-base text-white hover:bg-sky-700"
          disabled={login.isPending}
          data-testid="login-submit-button"
        >
          {login.isPending ? "Accesso…" : "Accedi"}
        </Button>
      </form>
      <p className="mt-6 text-center text-sm text-slate-600">
        Nuovo volontario?{" "}
        <Link to="/register" className="font-semibold text-sky-700 hover:underline" data-testid="login-register-link">
          Registrati
        </Link>
      </p>
    </AuthLayout>
  );
}
