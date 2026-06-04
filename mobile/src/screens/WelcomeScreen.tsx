import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image, StatusBar, Platform } from 'react-native';

const THEME = {
  primary: '#18274E',
  background: '#F0F4F8',
  surface: '#FFFFFF',
};

export default function WelcomeScreen({ navigation }: any) {
  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={THEME.primary} />
      
      {/* Cabeçalho Curto igual ao Figma */}
      <View style={styles.topHeader}>
        <Image 
          source={require('../../assets/logo.png')} 
          style={styles.logoImage}
          resizeMode="contain"
        />
      </View>

      {/* Área Centralizada */}
      <View style={styles.centerContent}>
        <TouchableOpacity 
          style={styles.primaryButton} 
          onPress={() => navigation.navigate('Login')}
          activeOpacity={0.8}
        >
          <Text style={styles.primaryButtonText}>Fazer Login</Text>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.secondaryButton} 
          onPress={() => navigation.navigate('SignUp')}
          activeOpacity={0.8}
        >
          <Text style={styles.secondaryButtonText}>Criar Conta</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.background,
  },
  topHeader: {
    backgroundColor: THEME.primary,
    height: Platform.OS === 'ios' ? 200 : 170, // Cabeçalho maior
    width: '100%',
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: Platform.OS === 'ios' ? 40 : 20,
  },
  logoImage: {
    width: 600, // Logo aumentada
    height: 90,
  },
  centerContent: {
    flex: 1,
    justifyContent: 'center', // Centra os botões perfeitamente na vertical
    alignItems: 'center',     // Centra na horizontal
  },
  primaryButton: {
    backgroundColor: THEME.primary,
    width: 240, // Largura controlada para ficar igual ao seu botão desenhado
    height: 55,
    borderRadius: 8,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 6,
    elevation: 4,
  },
  primaryButtonText: {
    color: THEME.surface,
    fontSize: 18,
    fontWeight: 'bold',
  },
  secondaryButton: {
    backgroundColor: 'transparent',
    width: 240,
    height: 55,
    borderRadius: 8,
    borderWidth: 2,
    borderColor: THEME.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: THEME.primary,
    fontSize: 18,
    fontWeight: 'bold',
  },
});