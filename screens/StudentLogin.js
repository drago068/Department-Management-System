import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Image, StyleSheet, SafeAreaView, ScrollView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';

const StudentLogin = ({ navigation }) => {
  const [registerNumber, setRegisterNumber] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = () => {
    navigation.navigate('CommonPortal', { role: 'student' });
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContainer} keyboardShouldPersistTaps="handled">
        {/* Background decorations represented as simple views */}
        <View style={styles.bgDecor1} />
        <View style={styles.bgDecor2} />

        <View style={styles.container}>
          {/* Logo Header */}
          <View style={styles.logoHeader}>
            <Image
              source={{ uri: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDSgFolUYApmA7IWd_01YCdc0bZu3WGqImSHYC48VCUHDWbMovVsJpqESPMS89ncNvuRF0e2EmdXaSPufr5dq89c4Ea0A9pY8zwgaw5X3I032ZskkRK4bT53RVeoJ6GKr3Cfkw0yBZIf_PWnx0L_twzM9f0e5-ui7TDz7MjSfKMv-CGHjAQx06OG5Bg21MUD6J32gV93zUqjGzeGV3XT1yk1CCafw9ebZPxQC-huhGRK87FZWCbJsrOo8LHLSgWRAS8qw' }}
              style={styles.logo}
              resizeMode="contain"
            />
            <Text style={styles.brandName}>NEXUS</Text>
            <Text style={styles.portalLabel}>Student Portal Authentication</Text>
          </View>

          {/* Login Card */}
          <View style={styles.loginCard}>
            <View style={styles.cardHeader}>
              <Text style={styles.cardTitle}>Student Login</Text>
              <Text style={styles.cardSubtitle}>Enter your student credentials to access your attendance and portal.</Text>
            </View>

            {/* Register Number */}
            <View style={styles.fieldGroup}>
              <Text style={styles.label}>Register Number</Text>
              <View style={styles.inputWrapper}>
                <MaterialIcons name="badge" size={20} color={Colors.outline} style={styles.inputIcon} />
                <TextInput
                  style={styles.input}
                  placeholder="e.g. STU2024001"
                  placeholderTextColor={Colors.outline}
                  value={registerNumber}
                  onChangeText={setRegisterNumber}
                  autoCapitalize="characters"
                />
              </View>
            </View>

            {/* Password */}
            <View style={styles.fieldGroup}>
              <View style={styles.labelRow}>
                <Text style={styles.label}>Password</Text>
                <TouchableOpacity>
                  <Text style={styles.forgotLink}>Forgot password?</Text>
                </TouchableOpacity>
              </View>
              <View style={styles.inputWrapper}>
                <MaterialIcons name="lock" size={20} color={Colors.outline} style={styles.inputIcon} />
                <TextInput
                  style={styles.input}
                  placeholder="••••••••"
                  placeholderTextColor={Colors.outline}
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry={!showPassword}
                />
                <TouchableOpacity onPress={() => setShowPassword(!showPassword)} style={styles.visibilityButton}>
                  <MaterialIcons
                    name={showPassword ? 'visibility-off' : 'visibility'}
                    size={20}
                    color={Colors.outline}
                  />
                </TouchableOpacity>
              </View>
            </View>

            {/* Submit Button */}
            <TouchableOpacity style={styles.submitButton} onPress={handleLogin} activeOpacity={0.8}>
              <Text style={styles.submitButtonText}>Login as Student</Text>
              <MaterialIcons name="arrow-forward" size={20} color={Colors.onPrimary} />
            </TouchableOpacity>
          </View>

          {/* Footer Links */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>Need help accessing your account?</Text>
            <TouchableOpacity style={styles.footerLink}>
              <MaterialIcons name="support-agent" size={14} color={Colors.primary} />
              <Text style={styles.footerLinkText}>Contact Admin</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: Colors.surface,
  },
  scrollContainer: {
    flexGrow: 1,
    justifyContent: 'center',
  },
  bgDecor1: {
    position: 'absolute',
    top: -50,
    left: -50,
    width: 300,
    height: 200,
    backgroundColor: Colors.primaryFixed,
    opacity: 0.3,
    borderRadius: 150,
  },
  bgDecor2: {
    position: 'absolute',
    bottom: -50,
    right: -50,
    width: 250,
    height: 250,
    backgroundColor: Colors.secondaryFixed,
    opacity: 0.2,
    borderRadius: 125,
  },
  container: {
    paddingHorizontal: 16,
    maxWidth: 420,
    alignSelf: 'center',
    width: '100%',
  },
  logoHeader: {
    alignItems: 'center',
    marginBottom: 24,
  },
  logo: {
    width: 64,
    height: 64,
    borderRadius: 12,
    marginBottom: 16,
  },
  brandName: {
    ...Typography.headlineLgMobile,
    color: Colors.primary,
    textAlign: 'center',
  },
  portalLabel: {
    ...Typography.labelMd,
    color: Colors.secondary,
    marginTop: 4,
    textAlign: 'center',
  },
  loginCard: {
    backgroundColor: Colors.surfaceContainerLowest,
    borderRadius: 12,
    padding: 24,
    borderWidth: 1,
    borderColor: Colors.outlineVariant,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.1,
    shadowRadius: 15,
    elevation: 5,
  },
  cardHeader: {
    marginBottom: 16,
  },
  cardTitle: {
    ...Typography.headlineSm,
    color: Colors.onSurface,
    marginBottom: 4,
  },
  cardSubtitle: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
  },
  fieldGroup: {
    marginBottom: 16,
  },
  label: {
    ...Typography.labelSm,
    color: Colors.onSurfaceVariant,
    marginBottom: 4,
  },
  labelRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  forgotLink: {
    ...Typography.labelSm,
    color: Colors.primary,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    borderWidth: 1,
    borderColor: Colors.outlineVariant,
    borderRadius: 8,
    height: 40,
  },
  inputIcon: {
    paddingLeft: 12,
  },
  input: {
    flex: 1,
    paddingHorizontal: 8,
    ...Typography.bodyMd,
    color: Colors.onSurface,
    height: '100%',
  },
  visibilityButton: {
    paddingRight: 12,
  },
  submitButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: Colors.primary,
    height: 40,
    borderRadius: 8,
    gap: 8,
    marginTop: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  submitButtonText: {
    ...Typography.labelMd,
    color: Colors.onPrimary,
  },
  footer: {
    marginTop: 24,
    alignItems: 'center',
    gap: 8,
  },
  footerText: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
    textAlign: 'center',
  },
  footerLink: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  footerLinkText: {
    ...Typography.labelMd,
    color: Colors.primary,
  },
});

export default StudentLogin;
