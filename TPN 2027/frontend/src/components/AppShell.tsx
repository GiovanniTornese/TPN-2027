import { NavLink, Navigate, Outlet, useLocation } from "react-router-dom";
import { CalendarDays, LogOut, Megaphone, ShieldCheck, UserRound, HeartHandshake } from "lucide-react";
import { useMe, isUnauthorized } from "@/lib/hooks";
import { endSession } from "@/lib/session";
import { cn } from "@/lib/utils";

const NAV = [
  { to: "/", label: "Bacheca", icon: Megaphone, testid: "nav-bacheca", end: true },
  { to: "/turni", label: "Turni", icon: CalendarDays, testid: "nav-turni", end: false },
  { to: "/profilo", label: "Profilo", icon: UserRound, testid: "nav-profilo", end: false },
];
const ADMIN_NAV = { to: "/admin", label: "Gestione", icon: ShieldCheck, testid: "nav-admin", end: false };

export default function AppShell() {
  const me = useMe();
  const loc = useLocation();
  if (me.isError && isUnauthorized(me.error)) return <Navigate to="/login" replace />;
  const user = me.data;
  // Google sign-ups arrive without gender/phone: force profile completion first.
  if (user?.role === "volunteer" && (!user.gender || !user.phone) && loc.pathname !== "/profilo")
    return <Navigate to="/profilo" replace />;
  const items = user?.role === "admin" ? [...NAV, ADMIN_NAV] : NAV;

  return (
    <div className="min-h-dvh bg-slate-50 text-slate-900 md:flex">
      {/* Desktop sidebar */}
      <aside className="hidden md:flex md:w-64 md:flex-col md:border-r md:border-slate-200 md:bg-white md:px-4 md:py-6 sticky top-0 h-dvh">
        <Brand />
        <nav className="mt-8 flex flex-col gap-1">
          {items.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              end={n.end}
              data-testid={`sidebar-${n.testid}`}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors duration-150",
                  isActive ? "bg-sky-50 text-sky-700" : "text-slate-600 hover:bg-slate-100",
                )
              }
            >
              <n.icon className="size-5" />
              {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="mt-auto rounded-xl border border-slate-200 p-3">
          <p className="truncate text-sm font-semibold" data-testid="sidebar-user-name">
            {user ? `${user.first_name} ${user.last_name}`.trim() : "…"}
          </p>
          <p className="text-xs text-slate-500">{user?.role === "admin" ? "Amministratore" : "Volontario"}</p>
          <button
            type="button"
            onClick={() => endSession()}
            data-testid="sidebar-logout-button"
            className="mt-3 flex items-center gap-2 text-sm text-slate-600 transition-colors duration-150 hover:text-red-600"
          >
            <LogOut className="size-4" /> Esci
          </button>
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        {/* Mobile header */}
        <header className="sticky top-0 z-30 flex items-center justify-between border-b border-slate-200/70 bg-white/80 px-4 py-3 backdrop-blur-md md:hidden">
          <Brand />
          <button
            type="button"
            onClick={() => endSession()}
            aria-label="Esci"
            data-testid="header-logout-button"
            className="flex size-11 items-center justify-center rounded-full text-slate-500 transition-colors duration-150 hover:bg-slate-100 hover:text-red-600"
          >
            <LogOut className="size-5" />
          </button>
        </header>

        <main className="mx-auto w-full max-w-6xl flex-1 px-4 pb-28 pt-4 md:px-8 md:pb-10 md:pt-8">
          {me.isLoading ? <div className="h-48 animate-pulse rounded-2xl bg-slate-200/60" /> : <Outlet />}
        </main>
      </div>

      {/* Mobile bottom nav */}
      <nav
        className="fixed inset-x-0 bottom-0 z-40 border-t border-slate-200 bg-white/90 pb-[env(safe-area-inset-bottom)] backdrop-blur-md md:hidden"
        data-testid="bottom-nav"
      >
        <div className="mx-auto flex max-w-md">
          {items.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              end={n.end}
              data-testid={n.testid}
              className={({ isActive }) =>
                cn(
                  "flex min-h-14 flex-1 flex-col items-center justify-center gap-0.5 text-[11px] font-semibold transition-colors duration-150",
                  isActive ? "text-sky-700" : "text-slate-500",
                )
              }
            >
              {({ isActive }) => (
                <>
                  <span
                    className={cn(
                      "flex h-7 w-12 items-center justify-center rounded-full transition-colors duration-150",
                      isActive && "bg-sky-100",
                    )}
                  >
                    <n.icon className="size-5" />
                  </span>
                  {n.label}
                </>
              )}
            </NavLink>
          ))}
        </div>
      </nav>
    </div>
  );
}

export function Brand() {
  return (
    <div className="flex items-center gap-2.5">
      <span className="flex size-9 items-center justify-center rounded-xl bg-slate-900 text-white">
        <HeartHandshake className="size-5" />
      </span>
      <div className="leading-tight">
        <p className="font-heading text-base font-bold tracking-tight">TPN 2027</p>
        <p className="text-[11px] text-slate-500">Pianificazione turni</p>
      </div>
    </div>
  );
}
