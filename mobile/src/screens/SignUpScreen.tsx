import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, KeyboardAvoidingView, Platform, StatusBar, Image, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

const THEME = {
  primary: '#18274E',    
  background: '#F0F4F8', 
  surface: '#FFFFFF',    
  textDark: '#000000',   
  textLight: '#9CA3AF',  
  border: '#D1D5DB',     
};

export default function SignUpScreen({ navigation }: any) {
  const [name, setName] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  const handleSignUp = () => {
    console.log('Registo para:', name);
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

      {/* Ajuste do comportamento do teclado (adicionado 'height' e offset) */}
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'} 
        keyboardVerticalOffset={Platform.OS === 'ios' ? 0 : 20}
        style={styles.keyboardContainer}
      >
        <ScrollView 
          contentContainerStyle={styles.scrollContent} 
          showsVerticalScrollIndicator={false} 
          keyboardShouldPersistTaps="handled"
        >
          
          <View style={styles.card}>
            <Text style={styles.title}>Criar Nova Conta</Text>

            <View style={styles.inputContainer}>
              <Ionicons name="id-card" size={20} color={THEME.textLight} style={styles.inputIcon} />
              <TextInput style={styles.input} placeholder="Nome completo" placeholderTextColor={THEME.textLight} value={name} onChangeText={setName} />
            </View>

            <View style={styles.inputContainer}>
              <Ionicons name="person" size={20} color={THEME.textLight} style={styles.inputIcon} />
              <TextInput style={styles.input} placeholder="Usuário" placeholderTextColor={THEME.textLight} value={username} onChangeText={setUsername} autoCapitalize="none" />
            </View>

            <TouchableOpacity style={styles.inputContainer} activeOpacity={0.7}>
              <Ionicons name="people" size={20} color={THEME.textLight} style={styles.inputIcon} />
              <Text style={[styles.input, { color: THEME.textLight }]}>Selecione a equipe</Text>
              <Ionicons name="chevron-down" size={20} color={THEME.textLight} />
            </TouchableOpacity>

            <View style={styles.inputContainer}>
              <Ionicons name="lock-closed" size={20} color={THEME.textLight} style={styles.inputIcon} />
              <TextInput style={styles.input} placeholder="Senha" placeholderTextColor={THEME.textLight} value={password} onChangeText={setPassword} secureTextEntry={true} />
            </View>

            <View style={styles.inputContainer}>
              <Ionicons name="checkmark-circle" size={20} color={THEME.textLight} style={styles.inputIcon} />
              <TextInput style={styles.input} placeholder="Confirmar Senha" placeholderTextColor={THEME.textLight} value={confirmPassword} onChangeText={setConfirmPassword} secureTextEntry={true} />
            </View>

            <TouchableOpacity style={styles.button} onPress={handleSignUp} activeOpacity={0.8}>
              <Text style={styles.buttonText}>Registar</Text>
            </TouchableOpacity>
          </View>

        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: THEME.background },
  topHeader: { backgroundColor: THEME.primary, height: Platform.OS === 'ios' ? 130 : 110, width: '100%', justifyContent: 'center', alignItems: 'center', paddingTop: Platform.OS === 'ios' ? 40 : 20 },
  backButton: { position: 'absolute', left: 20, bottom: 25, zIndex: 10, padding: 5 },
  logoImage: { width: 500, height: 55 },
  keyboardContainer: { flex: 1 },
  scrollContent: { 
    flexGrow: 1, 
    justifyContent: 'center', 
    paddingTop: 20,
    paddingBottom: 120 // <-- MÁGICA AQUI: Dá espaço para o formulário subir por cima do teclado
  },
  card: { backgroundColor: THEME.surface, width: '85%', alignSelf: 'center', borderRadius: 16, padding: 24, shadowColor: '#000', shadowOffset: { width: 0, height: 8 }, shadowOpacity: 0.1, shadowRadius: 12, elevation: 6 },
  title: { fontSize: 24, fontWeight: 'bold', color: THEME.textDark, textAlign: 'center', marginBottom: 30 },
  inputContainer: { flexDirection: 'row', alignItems: 'center', borderWidth: 1.5, borderColor: THEME.border, borderRadius: 8, paddingHorizontal: 14, height: 55, marginBottom: 16, backgroundColor: THEME.surface },
  inputIcon: { marginRight: 12 },
  input: { flex: 1, fontSize: 16, color: THEME.textDark },
  button: { backgroundColor: THEME.primary, height: 55, borderRadius: 8, justifyContent: 'center', alignItems: 'center', marginTop: 10 },
  buttonText: { color: THEME.surface, fontSize: 18, fontWeight: 'bold' },
});