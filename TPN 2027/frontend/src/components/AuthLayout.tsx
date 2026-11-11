import type { ReactNode } from "react";
import { Brand } from "@/components/AppShell";

export default function AuthLayout({ title, subtitle, children }: { title: string; subtitle: string; children: ReactNode }) {
  return (
    <div className="relative min-h-dvh overflow-hidden bg-slate-50">
      <div aria-hidden className="pointer-events-none absolute -left-24 -top-24 size-72 rounded-full bg-emerald-200/50 blur-3xl" />
      <div aria-hidden className="pointer-events-none absolute -right-20 top-40 size-72 rounded-full bg-indigo-200/50 blur-3xl" />
      <div aria-hidden className="pointer-events-none absolute bottom-0 left-1/3 size-72 rounded-full bg-amber-200/40 blur-3xl" />
      <div className="relative mx-auto flex min-h-dvh max-w-md flex-col px-5 py-8">
        <Brand />
        <div className="mt-10 sm:mt-16">
          <h1 className="font-heading text-4xl font-bold tracking-tight">{title}</h1>
          <p className="mt-2 text-slate-600">{subtitle}</p>
        </div>
        <div className="animate-fade-up mt-8 rounded-3xl border border-white/60 bg-white/80 p-6 shadow-[0_20px_50px_-20px_rgba(15,23,42,0.25)] backdrop-blur-xl">
          {children}
        </div>
      </div>
    </div>
  );
}
