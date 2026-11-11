// src/lib/hooks.ts

export function errMsg(error: unknown): string {
  if (error instanceof Error) return error.message;
  return String(error);
}

// Mock o funzioni di utilità per le stazioni, slot e utente loggato
export function useStations() {
  // Sostituisci con la tua logica o React Query se presente
  return { data: [], isLoading: false, error: null };
}

export function useSlots() {
  return { data: [], isLoading: false, error: null };
}

export function useMe() {
  return { data: null, isLoading: false, error: null };
}

export function useToday() {
  return { data: null, isLoading: false, error: null };
}
