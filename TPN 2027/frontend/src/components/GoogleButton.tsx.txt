import { SiGoogle } from "@icons-pack/react-simple-icons";
import { Button } from "@/components/ui/button";

export default function GoogleButton({ label = "Continua con Google" }: { label?: string }) {
  const go = () => {
    // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    const redirectUrl = window.location.origin + "/";
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };
  return (
    <Button
      type="button"
      variant="outline"
      onClick={go}
      className="h-12 w-full gap-2 bg-white text-base"
      data-testid="google-login-button"
    >
      <SiGoogle size={18} color="#4285F4" /> {label}
    </Button>
  );
}

export function OrDivider() {
  return (
    <div className="my-5 flex items-center gap-3 text-xs text-slate-400">
      <span className="h-px flex-1 bg-slate-200" /> oppure <span className="h-px flex-1 bg-slate-200" />
    </div>
  );
}
