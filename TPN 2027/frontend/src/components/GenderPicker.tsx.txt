import type { Gender } from "@/lib/types";
import { cn } from "@/lib/utils";

export default function GenderPicker({
  value,
  onChange,
  testidPrefix,
}: {
  value: Gender | null;
  onChange: (g: Gender) => void;
  testidPrefix: string;
}) {
  const opts: { v: Gender; label: string; active: string }[] = [
    { v: "M", label: "Uomo", active: "border-sky-600 bg-sky-50 text-sky-800 ring-2 ring-sky-100" },
    { v: "F", label: "Donna", active: "border-rose-500 bg-rose-50 text-rose-800 ring-2 ring-rose-100" },
  ];
  return (
    <div className="grid grid-cols-2 gap-2" role="radiogroup" aria-label="Genere">
      {opts.map((o) => (
        <button
          key={o.v}
          type="button"
          role="radio"
          aria-checked={value === o.v}
          onClick={() => onChange(o.v)}
          data-testid={`${testidPrefix}-gender-${o.v === "M" ? "uomo" : "donna"}`}
          className={cn(
            "min-h-12 rounded-xl border text-sm font-semibold transition-[color,background-color,border-color,box-shadow] duration-150",
            value === o.v ? o.active : "border-slate-200 bg-white text-slate-700 hover:bg-slate-50",
          )}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}
