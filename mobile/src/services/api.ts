import axios from 'axios';
import Constants from 'expo-constants';
import { Platform } from 'react-native';

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

const api = axios.create({
  baseURL: getBaseURL(),
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
