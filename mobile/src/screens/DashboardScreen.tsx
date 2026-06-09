import React from 'react';
import { View, Text, Button, StyleSheet, SafeAreaView } from 'react-native';
import * as SecureStore from 'expo-secure-store';
import { useAuthStore } from '../store/authStore';

export default function DashboardScreen() {
  const { user, logout } = useAuthStore();

  const handleLogout = async () => {
    try {
      // Remove os dados físicos para evitar o auto-login ao reabrir o app
      await SecureStore.deleteItemAsync('userToken');
      await SecureStore.deleteItemAsync('userData');
    } catch (error) {
      console.error('Erro ao remover dados de autenticação:', error);
    } finally {
      // Limpa o estado global do Zustand para redirecionar o utilizador
      logout();
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        <Text style={styles.title}>Painel de Operador</Text>
        
        <Text style={styles.subtitle}>
          Olá, {user?.name || 'Operador'}!
        </Text>
        
        {user?.team && (
          <Text style={styles.team}>Equipe: {user.team}</Text>
        )}

        <View style={styles.actionContainer}>
          <Text style={styles.info}>
            A carga inicial de dados da estação será exibida aqui.
          </Text>
          
          <View style={styles.buttonWrapper}>
            <Button 
              title="Sair do Turno (Logout)" 
              onPress={handleLogout} 
              color="#FF3B30" 
            />
          </View>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  content: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  subtitle: {
    fontSize: 20,
    marginBottom: 5,
    color: '#18274E',
  },
  team: {
    fontSize: 16,
    color: '#666',
    marginBottom: 40,
  },
  actionContainer: {
    width: '100%',
    backgroundColor: '#FFF',
    padding: 20,
    borderRadius: 10,
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  info: {
    textAlign: 'center',
    color: '#888',
    marginBottom: 20,
  },
  buttonWrapper: {
    width: '100%',
  }
});