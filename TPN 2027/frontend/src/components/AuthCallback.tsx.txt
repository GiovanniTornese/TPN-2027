import { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { toast } from "sonner";
import { apiPost } from "@/lib/api";
import { errMsg } from "@/lib/hooks";
import { beginSession } from "@/lib/session";
import type { GoogleSessionIn, UserPublic } from "@/lib/types";

/** Handles the #session_id=... fragment returned by Emergent Google auth. */
export default function AuthCallback() {
  const location = useLocation();
  const nav = useNavigate();
  const processed = useRef(false);

  useEffect(() => {
    if (processed.current) return;
    processed.current = true;
    const sessionId = new URLSearchParams(location.hash.slice(1)).get("session_id") ?? "";
    apiPost<UserPublic>("/auth/google", { session_id: sessionId } satisfies GoogleSessionIn)
      .then((u) => {
        beginSession();
        const incomplete = u.role === "volunteer" && (!u.gender || !u.phone);
        nav(incomplete ? "/profilo" : "/", { replace: true });
      })
      .catch((e) => {
        toast.error(errMsg(e, "Accesso con Google non riuscito"));
        nav("/login", { replace: true });
      });
  }, [location.hash, nav]);

  return <div className="min-h-dvh bg-slate-50" data-testid="auth-callback" />;
}
