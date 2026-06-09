import React, { useState } from 'react';
import { 
  View, 
  Text, 
  TextInput, 
  TouchableOpacity, 
  StyleSheet, 
  KeyboardAvoidingView, 
  Platform, 
  StatusBar, 
  Image, 
  ScrollView,
  Alert,
  ActivityIndicator
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as SecureStore from 'expo-secure-store';
import api from '../services/api';
import { useAuthStore } from '../store/authStore';

const THEME = {
  primary: '#18274E',    
  background: '#F0F4F8', 
  surface: '#FFFFFF',    
  textDark: '#000000',   
  textLight: '#9CA3AF',  
  border: '#D1D5DB',     
};

export default function LoginScreen({ navigation }: any) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // ---> PUXANDO A FUNÇÃO DE LOGIN DO ZUSTAND <---
  const loginAction = useAuthStore((state) => state.login);

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Atenção', 'Por favor, preencha o Usuário e a Senha.');
      return;
    }

    setIsLoading(true);

    try {
      // Disparo para o seu back-end em Python
      const response = await api.post('/auth/login/', {
        username: username,
        password: password,
      });

      // Extrai a resposta da API
      const token = response.data.token;
      const user = response.data.user;

      // Mantém os dados guardados fisicamente no celular (útil para o futuro, para não deslogar ao fechar o app)
      await SecureStore.setItemAsync('userToken', token);
      await SecureStore.setItemAsync('userData', JSON.stringify(user));

      setUsername('');
      setPassword('');
      
      // ---> A MÁGICA ACONTECE AQUI <---
      // Disparamos o estado global. O AppNavigator escutará isso imediatamente
      // destruindo esta tela e montando a DashboardScreen instantaneamente.
      loginAction(token, {
        id: user.id.toString(),
        name: user.first_name || user.username,
        team: user.operator_profile?.team_name || 'Sem Equipe'
      });

    } catch (error: any) {
      console.error('Erro no login:', error);
      
      if (error.response && error.response.status === 401) {
        Alert.alert('Erro', 'Usuário ou senha incorretos.');
      } else {
        Alert.alert('Erro de Conexão', 'Não foi possível conectar ao servidor. Verifique se o backend está rodando na porta 8000.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={THEME.primary} />

      <View style={styles.topHeader}>
        <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
          <Ionicons name="arrow-back" size={28} color={THEME.surface} />
        </TouchableOpacity>

        <Image source={require('../../assets/logo.png')} style={styles.logoImage} resizeMode="contain" />
      </View>

      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : undefined} style={styles.keyboardContainer}>
        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false} keyboardShouldPersistTaps="handled">
          <View style={styles.card}>
            <Text style={styles.title}>Login</Text>

            <View style={styles.inputContainer}>
              <Ionicons name="person" size={20} color={THEME.textLight} style={styles.inputIcon} />
              <TextInput style={styles.input} placeholder="Usuário" placeholderTextColor={THEME.textLight} value={username} onChangeText={setUsername} autoCapitalize="none" />
            </View>

            <View style={styles.inputContainer}>
              <Ionicons name="lock-closed" size={20} color={THEME.textLight} style={styles.inputIcon} />
              <TextInput style={styles.input} placeholder="Senha" placeholderTextColor={THEME.textLight} value={password} onChangeText={setPassword} secureTextEntry={true} />
            </View>

            <TouchableOpacity 
              style={styles.button} 
              onPress={handleLogin} 
              activeOpacity={0.8}
              disabled={isLoading} 
            >
              {isLoading ? (
                <ActivityIndicator size="small" color={THEME.surface} />
              ) : (
                <Text style={styles.buttonText}>Entrar</Text>
              )}
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: THEME.background },
  topHeader: { backgroundColor: THEME.primary, height: '35%', width: '100%', position: 'absolute', top: 0, alignItems: 'center', paddingTop: Platform.OS === 'ios' ? 60 : 80 },
  backButton: { position: 'absolute', top: Platform.OS === 'ios' ? 50 : 60, left: 20, zIndex: 10, padding: 10 },
  logoImage: { width: 500, height: 100, marginTop: 10 },
  keyboardContainer: { flex: 1 },
  scrollContent: { flexGrow: 1, justifyContent: 'center', paddingBottom: 40 },
  card: { backgroundColor: THEME.surface, width: '85%', alignSelf: 'center', borderRadius: 16, padding: 24, marginTop: 80, shadowColor: '#000', shadowOffset: { width: 0, height: 8 }, shadowOpacity: 0.1, shadowRadius: 12, elevation: 6 },
  title: { fontSize: 24, fontWeight: 'bold', color: THEME.textDark, textAlign: 'center', marginBottom: 30 },
  inputContainer: { flexDirection: 'row', alignItems: 'center', borderWidth: 1.5, borderColor: THEME.border, borderRadius: 8, paddingHorizontal: 14, height: 55, marginBottom: 16, backgroundColor: THEME.surface },
  inputIcon: { marginRight: 12 },
  input: { flex: 1, fontSize: 16, color: THEME.textDark },
  button: { backgroundColor: THEME.primary, height: 55, borderRadius: 8, justifyContent: 'center', alignItems: 'center', marginTop: 10 },
  buttonText: { color: THEME.surface, fontSize: 18, fontWeight: 'bold' },
});