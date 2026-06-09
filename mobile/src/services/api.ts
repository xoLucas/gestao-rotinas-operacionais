import axios from 'axios';
import Constants from 'expo-constants';
import { Platform } from 'react-native';
import { useAuthStore } from '../store/authStore';

const API_PORT = 8000;

const normalizeBaseURL = (url: string) => url.replace(/\/$/, '');

const getExpoHost = () => {
  const hostUri =
    Constants.expoConfig?.hostUri ||
    (Constants as any).manifest?.debuggerHost ||
    (Constants as any).manifest?.hostUri ||
    (Constants as any).manifest2?.extra?.expoClient?.hostUri;

  return hostUri?.replace(/^https?:\/\//, '').split(':')[0];
};

const getBaseURL = () => {
  const configuredBaseURL = process.env.EXPO_PUBLIC_API_URL || Constants.expoConfig?.extra?.apiUrl;

  if (configuredBaseURL) {
    return normalizeBaseURL(configuredBaseURL);
  }

  const expoHost = getExpoHost();
  const isAndroidLoopback = Platform.OS === 'android' && (!expoHost || expoHost === 'localhost' || expoHost === '127.0.0.1');
  const host = isAndroidLoopback ? '10.0.2.2' : expoHost || 'localhost';

  return `http://${host}:${API_PORT}/api`;
};

// SUA INSTÂNCIA ORIGINAL MANTIDA INTACTA
const api = axios.create({
  baseURL: getBaseURL(),
  headers: {
    'Content-Type': 'application/json',
  },
});

// === ADICIONAR A PARTIR DAQUI: INTERCEPTORS ===

// 1. Interceptor de Requisição (Injeta o Token)
api.interceptors.request.use(
  async (config) => {
    // Agora vamos buscar o token real ao nosso estado do Zustand!
    const token = useAuthStore.getState().token; 

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 2. Interceptor de Resposta (Tratamento de Sessão Expirada)
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      console.log('Sessão expirada ou token inválido. Redirecionando para login...');
      // Forçamos o logout global: o token é apagado e o utilizador volta ao ecrã de login
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);

export default api;