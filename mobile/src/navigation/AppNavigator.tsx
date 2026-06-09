import React, { useEffect, useState } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import * as SecureStore from 'expo-secure-store';

// Importamos o cofre de estado (Zustand)
import { useAuthStore } from '../store/authStore';

// Telas de Autenticação (Deslogado)
import WelcomeScreen from '../screens/WelcomeScreen';
import LoginScreen from '../screens/LoginScreen';
import SignUpScreen from '../screens/SignUpScreen';

// Tela Operacional Principal (Logado)
import DashboardScreen from '../screens/DashboardScreen';

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  const token = useAuthStore((state) => state.token);
  const loginAction = useAuthStore((state) => state.login);
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);

  useEffect(() => {
    const checkPersistedAuth = async () => {
      try {
        // Tentamos ler o token e os dados salvos fisicamente no dispositivo
        const savedToken = await SecureStore.getItemAsync('userToken');
        const savedUserData = await SecureStore.getItemAsync('userData');

        if (savedToken && savedUserData) {
          const parsedUser = JSON.parse(savedUserData);
          
          // Se os dados existirem, restauramos a sessão no Zustand automaticamente
          loginAction(savedToken, {
            id: parsedUser.id.toString(),
            name: parsedUser.first_name || parsedUser.username,
            team: parsedUser.operator_profile?.team_name || 'Sem Equipe',
          });
        }
      } catch (error) {
        console.error('Erro ao restaurar sessão persistida:', error);
      } finally {
        // Finaliza a verificação inicial e renderiza as telas corretas
        setIsCheckingAuth(false);
      }
    };

    checkPersistedAuth();
  }, [loginAction]);

  // Enquanto estiver a verificar o SecureStore, exibe um indicador de carregamento limpo
  if (isCheckingAuth) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#18274E" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {token ? (
          // ===== FLUXO LOGADO (OPERADOR) =====
          <Stack.Screen name="Dashboard" component={DashboardScreen} />
        ) : (
          // ===== FLUXO DESLOGADO (PÚBLICO) =====
          <>
            <Stack.Screen name="Welcome" component={WelcomeScreen} />
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="SignUp" component={SignUpScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F0F4F8',
  },
});