import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Image, StyleSheet, SafeAreaView, ScrollView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';

const StaffLogin = ({ navigation }) => {
  const [staffId, setStaffId] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  const handleLogin = () => {
    navigation.navigate('CommonPortal', { role: 'staff' });
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContainer} keyboardShouldPersistTaps="handled">
        {/* Background decorations */}
        <View style={styles.bgDecor1} />
        <View style={styles.bgDecor2} />

        <View style={styles.container}>
          {/* Brand Header */}
          <View style={styles.logoHeader}>
            <Image
              source={{ uri: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDlZjm4-4-zZtv9Nk2s62FpHayFCQeaQVoAk6bJB658Dwhl_3I0jPbW1SIfwd0cu4I5He7Wl_6sPSjE3J7BLlCwlpg9rvqGECQxJlUf247NQY44YTb_CNTmnTsNCs4uxk4Z214N2LLg_n8SdVk2IYURZ-h9tqntGuUG93vvDjI0rj_7pY33kvUARNYq7sTgB387TFcnkmdSwmDWMWSZbm-rBhajjZRsfFy4K8TMXYtNFY8mqq27tAbtC_USNF1_RPXa6A' }}
              style={styles.logo}
              resizeMode="contain"
            />
            <Text style={styles.brandName}>NEXUS</Text>
            <Text style={styles.portalLabel}>Staff Portal Authentication</Text>
          </View>

          {/* Login Card */}
          <View style={styles.loginCard}>
            <View style={styles.cardHeader}>
              <Text style={styles.cardTitle}>Staff Login</Text>
              <Text style={styles.cardSubtitle}>Access your faculty dashboard and mark attendance.</Text>
            </View>

            {/* Staff ID Field */}
            <View style={styles.fieldGroup}>
              <Text style={styles.label}>Staff ID / Email</Text>
              <View style={styles.inputWrapper}>
                <MaterialIcons name="badge" size={20} color={Colors.outline} style={styles.inputIcon} />
                <TextInput
                  style={styles.input}
                  placeholder="e.g. FAC-2024-001"
                  placeholderTextColor={Colors.outline}
                  value={staffId}
                  onChangeText={setStaffId}
                />
              </View>
            </View>

            {/* Password Field */}
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
                  <MaterialIcons name={showPassword ? 'visibility-off' : 'visibility'} size={20} color={Colors.outline} />
                </TouchableOpacity>
              </View>
            </View>

            {/* Remember Me */}
            <TouchableOpacity style={styles.rememberRow} onPress={() => setRememberMe(!rememberMe)} activeOpacity={0.7}>
              <MaterialIcons
                name={rememberMe ? 'check-box' : 'check-box-outline-blank'}
                size={20}
                color={rememberMe ? Colors.primary : Colors.outlineVariant}
              />
              <Text style={styles.rememberText}>Remember me for 30 days</Text>
            </TouchableOpacity>

            {/* Submit Button */}
            <TouchableOpacity style={styles.submitButton} onPress={handleLogin} activeOpacity={0.8}>
              <Text style={styles.submitButtonText}>Login as Staff</Text>
              <MaterialIcons name="arrow-forward" size={20} color={Colors.onPrimary} />
            </TouchableOpacity>
          </View>

          {/* Footer */}
          <View style={styles.footer}>
            <Text style={styles.footerText}>
              Need help accessing your account?{' '}
              <Text style={styles.footerLinkInline}>Contact Support</Text>
            </Text>
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
    top: -100,
    right: -50,
    width: 350,
    height: 350,
    backgroundColor: Colors.primaryFixed,
    opacity: 0.3,
    borderRadius: 175,
  },
  bgDecor2: {
    position: 'absolute',
    bottom: -100,
    left: -50,
    width: 300,
    height: 300,
    backgroundColor: Colors.secondaryFixed,
    opacity: 0.4,
    borderRadius: 150,
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
    width: 96,
    height: 96,
    marginBottom: 8,
  },
  brandName: {
    ...Typography.headlineLgMobile,
    color: Colors.primary,
  },
  portalLabel: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
    marginTop: 4,
  },
  loginCard: {
    backgroundColor: 'rgba(255, 255, 255, 0.85)',
    borderRadius: 12,
    padding: 24,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.5)',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  cardHeader: {
    marginBottom: 16,
    alignItems: 'center',
  },
  cardTitle: {
    ...Typography.headlineSm,
    color: Colors.onSurface,
  },
  cardSubtitle: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
    marginTop: 4,
    textAlign: 'center',
  },
  fieldGroup: {
    marginBottom: 16,
  },
  label: {
    ...Typography.labelMd,
    color: Colors.onSurface,
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
    backgroundColor: Colors.surfaceContainerLowest,
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
  rememberRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 16,
  },
  rememberText: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
  },
  submitButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: Colors.primary,
    paddingVertical: 10,
    borderRadius: 8,
    gap: 8,
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
  },
  footerText: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
    textAlign: 'center',
  },
  footerLinkInline: {
    ...Typography.labelMd,
    color: Colors.primary,
  },
});

export default StaffLogin;
