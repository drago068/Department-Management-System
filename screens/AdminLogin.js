import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, Image, StyleSheet, SafeAreaView, ScrollView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';

const AdminLogin = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [twoFA, setTwoFA] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberDevice, setRememberDevice] = useState(false);

  const handleLogin = () => {
    navigation.navigate('CommonPortal', { role: 'admin' });
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.scrollContainer} keyboardShouldPersistTaps="handled">
        {/* Background decorations */}
        <View style={styles.bgDecor1} />
        <View style={styles.bgDecor2} />

        <View style={styles.container}>
          {/* Branding Header */}
          <View style={styles.brandHeader}>
            <Image
              source={{ uri: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBtrjPjQd5a2_l9A84VgRqQ1Q0ESjAsOXR-WyXLbLMgjvUOAXLoc86YMon6xSsyMKSz-9CjCNfaVWS9OuQcHYDgVjqYu4o4wkT5bC4ywST3r8n1j8nujITPmY4E3CW8aAJ95_VvsTnwptiUMDDC7sNvnTc91Z_76rICSiW4U43D8qfauToeL4wIO0kNoqpzbhxTizeg-xiS6D2_iuJJzWyCNjcdq6NPB_e1Lzpqhjhk1nwOr1pK-fbXUeSbbV9okX72nw' }}
              style={styles.logo}
              resizeMode="contain"
            />
            <View style={styles.brandRow}>
              <Text style={styles.brandName}>NEXUS</Text>
              <View style={styles.adminBadge}>
                <Text style={styles.adminBadgeText}>ADMIN</Text>
              </View>
            </View>
            <Text style={styles.brandSubtitle}>System-wide governance and management access.</Text>
          </View>

          {/* Login Card */}
          <View style={styles.loginCard}>
            {/* Top gradient bar */}
            <View style={styles.gradientBar} />

            <View style={styles.cardContent}>
              <Text style={styles.cardTitle}>Admin Portal Login</Text>
              <View style={styles.divider} />

              {/* Username */}
              <View style={styles.fieldGroup}>
                <Text style={styles.label}>Admin Username</Text>
                <View style={styles.inputWrapper}>
                  <MaterialIcons name="person" size={20} color={Colors.outline} style={styles.inputIcon} />
                  <TextInput
                    style={styles.input}
                    placeholder="Enter administrator ID"
                    placeholderTextColor={Colors.outline}
                    value={username}
                    onChangeText={setUsername}
                  />
                </View>
              </View>

              {/* Password */}
              <View style={styles.fieldGroup}>
                <Text style={styles.label}>Password</Text>
                <View style={styles.inputWrapper}>
                  <MaterialIcons name="lock" size={20} color={Colors.outline} style={styles.inputIcon} />
                  <TextInput
                    style={styles.input}
                    placeholder="Enter password"
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

              {/* 2FA Code */}
              <View style={styles.fieldGroup}>
                <View style={styles.labelRow}>
                  <Text style={styles.label}>2FA Code</Text>
                  <View style={styles.requiredBadge}>
                    <Text style={styles.requiredBadgeText}>Required for Admin</Text>
                  </View>
                </View>
                <View style={styles.inputWrapper}>
                  <MaterialIcons name="pin" size={20} color={Colors.outline} style={styles.inputIcon} />
                  <TextInput
                    style={[styles.input, { letterSpacing: 4 }]}
                    placeholder="000000"
                    placeholderTextColor={Colors.outline}
                    value={twoFA}
                    onChangeText={setTwoFA}
                    keyboardType="numeric"
                    maxLength={6}
                  />
                </View>
              </View>

              {/* Options Row */}
              <View style={styles.optionsRow}>
                <TouchableOpacity style={styles.rememberRow} onPress={() => setRememberDevice(!rememberDevice)} activeOpacity={0.7}>
                  <MaterialIcons
                    name={rememberDevice ? 'check-box' : 'check-box-outline-blank'}
                    size={20}
                    color={rememberDevice ? Colors.primary : Colors.outlineVariant}
                  />
                  <Text style={styles.rememberText}>Remember this device</Text>
                </TouchableOpacity>
                <TouchableOpacity>
                  <Text style={styles.forgotLink}>Forgot Password?</Text>
                </TouchableOpacity>
              </View>

              {/* Submit Button */}
              <TouchableOpacity style={styles.submitButton} onPress={handleLogin} activeOpacity={0.8}>
                <MaterialIcons name="login" size={20} color={Colors.onPrimary} />
                <Text style={styles.submitButtonText}>Secure Login</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Footer */}
          <View style={styles.footer}>
            <MaterialIcons name="security" size={16} color={Colors.outline} />
            <Text style={styles.footerText}>Connection is encrypted and monitored.</Text>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  scrollContainer: {
    flexGrow: 1,
    justifyContent: 'center',
  },
  bgDecor1: {
    position: 'absolute',
    top: -96,
    left: -96,
    width: 384,
    height: 384,
    backgroundColor: 'rgba(0, 63, 177, 0.05)',
    borderRadius: 192,
  },
  bgDecor2: {
    position: 'absolute',
    bottom: -96,
    right: -96,
    width: 480,
    height: 480,
    backgroundColor: 'rgba(220, 226, 243, 0.2)',
    borderRadius: 240,
  },
  container: {
    paddingHorizontal: 16,
    maxWidth: 440,
    alignSelf: 'center',
    width: '100%',
    gap: 24,
  },
  brandHeader: {
    alignItems: 'center',
    gap: 8,
    marginBottom: 8,
  },
  logo: {
    width: 64,
    height: 64,
    borderRadius: 12,
    marginBottom: 4,
  },
  brandRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  brandName: {
    ...Typography.headlineLgMobile,
    color: Colors.primary,
  },
  adminBadge: {
    backgroundColor: Colors.surfaceVariant,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  adminBadgeText: {
    ...Typography.labelSm,
    color: Colors.onSurfaceVariant,
    letterSpacing: 1,
  },
  brandSubtitle: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
    textAlign: 'center',
    maxWidth: 280,
  },
  loginCard: {
    backgroundColor: Colors.surfaceContainerLowest,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
    borderWidth: 1,
    borderColor: 'rgba(195, 197, 215, 0.4)',
    overflow: 'hidden',
  },
  gradientBar: {
    height: 4,
    backgroundColor: Colors.primary,
  },
  cardContent: {
    padding: 24,
  },
  cardTitle: {
    ...Typography.headlineSm,
    color: Colors.onSurface,
    marginBottom: 16,
  },
  divider: {
    height: 1,
    backgroundColor: 'rgba(195, 197, 215, 0.3)',
    marginBottom: 16,
  },
  fieldGroup: {
    marginBottom: 16,
  },
  label: {
    ...Typography.labelMd,
    color: Colors.onSurfaceVariant,
    marginBottom: 4,
  },
  labelRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  requiredBadge: {
    backgroundColor: Colors.surfaceContainer,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
  },
  requiredBadgeText: {
    ...Typography.labelSm,
    color: Colors.outline,
    fontWeight: '400',
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.surface,
    borderWidth: 1,
    borderColor: Colors.outlineVariant,
    borderRadius: 8,
    height: 44,
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
  optionsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginVertical: 8,
  },
  rememberRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  rememberText: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
  },
  forgotLink: {
    ...Typography.labelMd,
    color: Colors.primary,
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
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
  },
  footerText: {
    ...Typography.bodyMd,
    color: Colors.outline,
  },
});

export default AdminLogin;
