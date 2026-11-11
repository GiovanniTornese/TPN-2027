import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import AppShell from "@/components/AppShell";
import AuthCallback from "@/components/AuthCallback";
import Login from "@/pages/Login";
import Register from "@/pages/Register";
import Shifts from "@/pages/Shifts";
import Board from "@/pages/Board";
import Profile from "@/pages/Profile";
import Admin from "@/pages/Admin";

// One <Route> per page in src/pages; BrowserRouter already wraps this in main.tsx.
export default function App() {
  const location = useLocation();
  // Google auth returns with #session_id=… — process it before any protected route checks /auth/me.
  if (location.hash?.includes("session_id=")) return <AuthCallback />;
  return (
    <>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route element={<AppShell />}>
          <Route path="/" element={<Board />} />
          <Route path="/turni" element={<Shifts />} />
          <Route path="/profilo" element={<Profile />} />
          <Route path="/admin" element={<Admin />} />
        </Route>
        <Route path="/bacheca" element={<Navigate to="/" replace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <Toaster richColors position="bottom-right" mobileOffset={{ bottom: 84 }} />
    </>
  );
}
