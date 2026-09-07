import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet, SafeAreaView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';

const LoginPage = ({ navigation }) => {
  const [selectedRole, setSelectedRole] = useState('student');

  const roles = [
    { key: 'student', label: 'Student', icon: 'school' },
    { key: 'staff', label: 'Staff', icon: 'badge' },
    { key: 'admin', label: 'Admin', icon: 'shield' },
  ];

  const handleRoleSelect = (role) => {
    setSelectedRole(role);
  };

  const handleNavigate = () => {
    if (selectedRole === 'student') {
      navigation.navigate('StudentLogin');
    } else if (selectedRole === 'staff') {
      navigation.navigate('StaffLogin');
    } else if (selectedRole === 'admin') {
      navigation.navigate('AdminLogin');
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <View style={styles.card}>
          {/* Top Bar */}
          <View style={styles.topBar} />

          <View style={styles.cardContent}>
            {/* Header */}
            <View style={styles.header}>
              <Image
                source={{ uri: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCuTmzG4MrHYhMnP2grVN00u-OdNw6Mv03BP0zE4CaipaR2PwVW7WK5DuOOKfBMOLQ9dGI46knXfp187V7ahhpYeBMbw9zhkp8iBG36nANSNFr0DpnZ1C8GjHW6DF8VltLWbkxXeA51SvsCaUPvb8RUTHPpFvPvO_BNMgiNF8sPg8rnL1MIyatYCyKhQab_X8JvNJ258Oj0WkbmpgVfx-WYXjoQh-XeKZtAyV6ZLWb1Rt0tEiotkyE2B7M-50NGgKzbUQ' }}
                style={styles.logo}
                resizeMode="contain"
              />
              <Text style={styles.brandName}>NEXUS</Text>
              <Text style={styles.brandSubtitle}>Attendance Management System</Text>
            </View>

            {/* Title */}
            <Text style={styles.welcomeTitle}>Welcome to NEXUS</Text>

            {/* Role Selection */}
            <Text style={styles.roleLabel}>Please select your role to get started</Text>
            <View style={styles.roleGrid}>
              {roles.map((role) => {
                const isSelected = selectedRole === role.key;
                return (
                  <TouchableOpacity
                    key={role.key}
                    style={[styles.roleCard, isSelected && styles.roleCardSelected]}
                    onPress={() => handleRoleSelect(role.key)}
                    activeOpacity={0.7}
                  >
                    <MaterialIcons
                      name={role.icon}
                      size={28}
                      color={isSelected ? Colors.primary : Colors.onSurfaceVariant}
                    />
                    <Text style={[styles.roleText, isSelected && styles.roleTextSelected]}>
                      {role.label}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>

            {/* Navigate Button */}
            <TouchableOpacity style={styles.continueButton} onPress={handleNavigate} activeOpacity={0.8}>
              <Text style={styles.continueButtonText}>Continue</Text>
              <MaterialIcons name="arrow-forward" size={20} color={Colors.onPrimary} />
            </TouchableOpacity>

            {/* Footer */}
            <View style={styles.footer}>
              <View style={styles.footerDivider} />
              <View style={styles.footerContent}>
                <MaterialIcons name="help-outline" size={14} color={Colors.onSurfaceVariant} />
                <Text style={styles.footerText}>
                  Need help?{' '}
                  <Text style={styles.footerLink}>Contact Dept. Admin</Text>
                </Text>
              </View>
            </View>
          </View>
        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  card: {
    width: '100%',
    maxWidth: 420,
    backgroundColor: Colors.surfaceContainerLowest,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
    borderWidth: 1,
    borderColor: 'rgba(195, 197, 215, 0.3)',
    overflow: 'hidden',
  },
  topBar: {
    height: 8,
    backgroundColor: Colors.primary,
    width: '100%',
  },
  cardContent: {
    padding: 24,
  },
  header: {
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
    textAlign: 'center',
  },
  brandSubtitle: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
    marginTop: 4,
  },
  welcomeTitle: {
    ...Typography.headlineSm,
    color: Colors.onSurface,
    textAlign: 'center',
    marginBottom: 24,
  },
  roleLabel: {
    ...Typography.labelMd,
    color: Colors.onSurface,
    marginBottom: 8,
  },
  roleGrid: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 24,
  },
  roleCard: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 24,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: Colors.outlineVariant,
    backgroundColor: Colors.surface,
  },
  roleCardSelected: {
    borderWidth: 2,
    borderColor: Colors.primary,
    backgroundColor: 'rgba(219, 225, 255, 0.1)',
  },
  roleText: {
    fontSize: 14,
    fontWeight: '500',
    color: Colors.onSurfaceVariant,
    marginTop: 8,
  },
  roleTextSelected: {
    color: Colors.primary,
  },
  continueButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: Colors.primary,
    paddingVertical: 12,
    borderRadius: 8,
    gap: 8,
    marginBottom: 16,
  },
  continueButtonText: {
    ...Typography.labelMd,
    color: Colors.onPrimary,
  },
  footer: {
    marginTop: 8,
  },
  footerDivider: {
    height: 1,
    backgroundColor: 'rgba(195, 197, 215, 0.3)',
    marginBottom: 16,
  },
  footerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  footerText: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
  },
  footerLink: {
    color: Colors.primary,
    fontWeight: '500',
  },
});

export default LoginPage;
