import { create } from 'zustand';

// Definimos o formato dos dados do operador
export interface Operator {
  id: string;
  name: string;
  team: string; // ex: "Turno A"
}

// Definimos o formato do nosso estado global
interface AuthState {
  token: string | null;
  user: Operator | null;
  login: (token: string, user: Operator) => void;
  logout: () => void;
}

// Criamos o cofre (store)
export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  
  // Função para guardar os dados quando o login tem sucesso
  login: (token, user) => set({ token, user }),
  
  // Função para apagar os dados quando a sessão expira ou o utilizador sai
  logout: () => set({ token: null, user: null }),
}));