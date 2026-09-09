import React from 'react';
import {
  SafeAreaView,
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  ScrollView,
  StatusBar,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialIcons } from '@expo/vector-icons';

const COLLEGE_LOGO =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuANdWs9FsNCaoAEBH-d9jjOGNGHTECsPM5IBwpJZ8hGqWi5BU4XLsXoaZhn9Oj3Tl9ZiK4tWrjXASrpYcWSeB-4H5TuTOP_3_F-HFZDDAoTANGqXUs9Itaneg-eQUPrdgkpGTGMcJaBp7mFQkmNSlvLN2wHxfwOnW9oLojQsVvmLjPbV7DiGhYaNHNlHp7CWp-TtswVdW5UDM4P9f_lTYd9BTzywk-v6kHE3bO2smiq3IZsLXaiXBlsChR7BG6NiYKgDw';

const PROFILE_IMAGE =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuDLMCP8yRlQ0t64bRrmg74ykXVPvsr5Wu0pe7d2NwkXvOlBpvA58cOJaOBG8D9JPBGrg_FO6IWfBxlmEhjWNog-DbQlGX8msgQzxS28oUSjAhY3VkBbDcgFXYKq1NRwZONhHCa7TxdG6fS0f5qgDmtkmdJm9Y44DczH3-ggueFzDOZxl-xDxq0xoUhGVzciGNRHiWjScT0R9LdaDgmLGkWeo-AfeTuo6h1b7CmaX0klr3Ni11bzQYqV';

const BRAND = '#1a56db';

const DetailRow = ({ icon, label, value }) => {
  return (
    <View style={styles.detailRow}>
      <View style={styles.detailLeft}>
        <MaterialIcons name={icon} size={18} color={BRAND} />
        <Text style={styles.detailLabel}>{label}</Text>
      </View>

      <Text
        style={styles.detailValue}
        numberOfLines={1}
        ellipsizeMode="tail"
      >
        {value}
      </Text>
    </View>
  );
};

const BottomNavItem = ({ icon, label, active, onPress }) => {
  if (active) {
    return (
      <TouchableOpacity
        activeOpacity={0.9}
        onPress={onPress}
        style={styles.activeNavItem}
      >
        <MaterialIcons name={icon} size={20} color="#ffffff" />
        <Text style={styles.activeNavText}>{label}</Text>
      </TouchableOpacity>
    );
  }

  return (
    <TouchableOpacity
      activeOpacity={0.7}
      onPress={onPress}
      style={styles.navItem}
    >
      <MaterialIcons name={icon} size={22} color="#64748b" />
      <Text style={styles.navText}>{label}</Text>
    </TouchableOpacity>
  );
};

const StudentProfile = ({ navigation }) => {
  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar
        barStyle="dark-content"
        backgroundColor="#fafbff"
      />

      <View style={styles.appContainer}>

        {/* ================= TOP BAR ================= */}
        <View style={styles.header}>
          <View style={styles.brandContainer}>
            <TouchableOpacity
              style={{ marginRight: 8, padding: 4 }}
              onPress={() => {
                if (navigation && navigation.canGoBack()) {
                  navigation.goBack();
                } else {
                  navigation?.navigate('StudentDashboard');
                }
              }}
              activeOpacity={0.7}
            >
              <MaterialIcons name="arrow-back" size={24} color="#1e293b" />
            </TouchableOpacity>

            <View style={styles.logoWrapper}>
              <Image
                source={{ uri: COLLEGE_LOGO }}
                style={styles.logo}
                resizeMode="contain"
              />
            </View>

            <Text style={styles.nexusText}>NEXUS</Text>
          </View>

          <TouchableOpacity
            activeOpacity={0.7}
            style={styles.notificationButton}
            onPress={() => navigation?.navigate('Login')}
          >
            <MaterialIcons
              name="logout"
              size={22}
              color="#dc2626"
            />
          </TouchableOpacity>
        </View>

        {/* ================= MAIN CONTENT ================= */}
        <ScrollView
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.scrollContent}
        >
          {/* Section Title */}
          <View style={styles.titleSection}>
            <Text style={styles.pageTitle}>Student Profile</Text>

            <TouchableOpacity
              activeOpacity={0.7}
              style={styles.editButton}
              onPress={() => navigation?.navigate('StudentEditProfile')}
            >
              <MaterialIcons
                name="edit"
                size={16}
                color={BRAND}
              />

              <Text style={styles.editText}>
                Edit Profile
              </Text>
            </TouchableOpacity>
          </View>

          {/* ================= STUDENT CARD ================= */}
          <View style={styles.studentCard}>

            {/* Blue Cover */}
            <LinearGradient
              colors={['#1a56db', '#3b82f6']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.cover}
            >
              {/* Profile Image */}
              <View style={styles.profileImageContainer}>
                <View style={styles.profileImageBorder}>
                  <Image
                    source={{ uri: PROFILE_IMAGE }}
                    style={styles.profileImage}
                    resizeMode="cover"
                  />
                </View>

                {/* Active Indicator */}
                <View style={styles.activeIndicator}>
                  <View style={styles.activeIndicatorInner} />
                </View>
              </View>
            </LinearGradient>

            {/* Student Information */}
            <View style={styles.studentInfo}>

              <Text style={styles.studentName}>
                Aravind Kumar
              </Text>

              <Text style={styles.registerNumber}>
                21AD042
              </Text>

              <View style={styles.departmentPill}>
                <Text style={styles.departmentText}>
                  Department of AI & DS
                </Text>
              </View>

              <Text style={styles.studentMeta}>
                B.Tech • 3rd Year • Semester 6 • Batch 2022–2026
              </Text>

              <View style={styles.divider} />

              {/* Details */}
              <View style={styles.detailsContainer}>

                <DetailRow
                  icon="mail"
                  label="Email"
                  value="aravind.k@suguna.edu"
                />

                <DetailRow
                  icon="call"
                  label="Phone"
                  value="+91 98765 43210"
                />

                <DetailRow
                  icon="school"
                  label="Faculty Mentor"
                  value="Dr. Sarah Williams"
                />

                <DetailRow
                  icon="calendar-today"
                  label="DOB / Blood Group"
                  value="14 Aug 2003 • O+ve"
                />

              </View>
            </View>
          </View>

          {/* ================= PERFORMANCE ================= */}
          <View style={styles.performanceSection}>
            {/* Kept empty because the original HTML section
                contains an empty metrics grid. */}
          </View>

          {/* ================= COURSE ATTENDANCE ================= */}
          <View style={styles.courseSection}>
            {/* Kept empty because the original HTML
                contains no visible course content. */}
          </View>

          {/* ================= QUICK ACTIONS ================= */}
          <View style={styles.servicesSection}>
            {/* The original HTML contains empty quick-action
                placeholders, therefore no visible elements
                are added here. */}
          </View>

          {/* Extra bottom spacing */}
          <View style={{ height: 90 }} />
        </ScrollView>

        {/* ================= BOTTOM NAVIGATION ================= */}
        <View style={styles.bottomNavigation}>

          <BottomNavItem
            icon="dashboard"
            label="Home"
            active={false}
            onPress={() => navigation?.navigate('StudentDashboard')}
          />

          <BottomNavItem
            icon="how-to-reg"
            label="Attendance"
            active={false}
            onPress={() => navigation?.navigate('StudentAttendanceDetail')}
          />

          <BottomNavItem
            icon="calendar-month"
            label="History"
            active={false}
            onPress={() => navigation?.navigate('AttendanceHistory')}
          />

          <BottomNavItem
            icon="person"
            label="Profile"
            active={true}
            onPress={() => {}}
          />

        </View>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  /* ================= ROOT ================= */

  safeArea: {
    flex: 1,
    backgroundColor: '#f8f9fe',
  },

  appContainer: {
    flex: 1,
    width: '100%',
    maxWidth: 420,
    alignSelf: 'center',
    backgroundColor: '#fafbff',
    position: 'relative',
  },

  /* ================= HEADER ================= */

  header: {
    height: 68,
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: 12,

    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',

    backgroundColor: '#fafbff',

    borderBottomWidth: 1,
    borderBottomColor: '#f1f5f9',

    zIndex: 30,
  },

  brandContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },

  logoWrapper: {
    width: 40,
    height: 40,
    borderRadius: 20,

    backgroundColor: '#ffffff',

    padding: 2,

    borderWidth: 2,
    borderColor: 'rgba(37, 99, 235, 0.20)',

    alignItems: 'center',
    justifyContent: 'center',

    overflow: 'hidden',

    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.08,
    shadowRadius: 3,

    elevation: 2,
  },

  logo: {
    width: '100%',
    height: '100%',
  },

  nexusText: {
    marginLeft: 12,

    fontSize: 24,
    fontWeight: '800',

    letterSpacing: -0.5,

    color: '#2563eb',
  },

  notificationButton: {
    width: 42,
    height: 42,

    borderRadius: 21,

    alignItems: 'center',
    justifyContent: 'center',

    position: 'relative',
  },

  notificationDot: {
    position: 'absolute',

    top: 9,
    right: 8,

    width: 10,
    height: 10,

    borderRadius: 5,

    backgroundColor: '#f43f5e',

    borderWidth: 2,
    borderColor: '#ffffff',
  },

  /* ================= SCROLL ================= */

  scrollContent: {
    paddingHorizontal: 20,
    paddingTop: 16,
    paddingBottom: 20,
  },

  /* ================= TITLE ================= */

  titleSection: {
    marginBottom: 16,
  },

  pageTitle: {
    fontSize: 24,
    fontWeight: '700',

    color: '#0f172a',

    letterSpacing: -0.5,

    marginBottom: 12,
  },

  editButton: {
    alignSelf: 'flex-start',

    flexDirection: 'row',
    alignItems: 'center',

    backgroundColor: '#ffffff',

    paddingHorizontal: 16,
    paddingVertical: 8,

    borderRadius: 12,

    borderWidth: 1,
    borderColor: '#e2e8f0',

    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.04,
    shadowRadius: 2,

    elevation: 1,
  },

  editText: {
    marginLeft: 8,

    fontSize: 12,
    fontWeight: '600',

    color: '#334155',
  },

  /* ================= STUDENT CARD ================= */

  studentCard: {
    backgroundColor: '#ffffff',

    borderRadius: 24,

    overflow: 'hidden',

    borderWidth: 1,
    borderColor: 'rgba(226, 232, 240, 0.8)',

    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.04,
    shadowRadius: 10,

    elevation: 2,
  },

  cover: {
    height: 96,

    position: 'relative',

    alignItems: 'center',
    justifyContent: 'flex-end',
  },

  profileImageContainer: {
    position: 'absolute',

    bottom: -40,

    alignItems: 'center',
    justifyContent: 'center',
  },

  profileImageBorder: {
    width: 96,
    height: 96,

    borderRadius: 48,

    padding: 4,

    backgroundColor: '#ffffff',

    borderWidth: 4,
    borderColor: '#ffffff',

    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 3,
    },
    shadowOpacity: 0.12,
    shadowRadius: 6,

    elevation: 4,

    overflow: 'hidden',
  },

  profileImage: {
    width: '100%',
    height: '100%',

    borderRadius: 48,
  },

  activeIndicator: {
    position: 'absolute',

    right: 2,
    bottom: 3,

    width: 20,
    height: 20,

    borderRadius: 10,

    backgroundColor: '#10b981',

    borderWidth: 2,
    borderColor: '#ffffff',

    alignItems: 'center',
    justifyContent: 'center',
  },

  activeIndicatorInner: {
    width: 6,
    height: 6,

    borderRadius: 3,

    backgroundColor: '#ffffff',
  },

  /* ================= STUDENT INFO ================= */

  studentInfo: {
    paddingHorizontal: 24,
    paddingTop: 48,
    paddingBottom: 24,

    alignItems: 'center',
  },

  studentName: {
    fontSize: 20,
    fontWeight: '700',

    color: '#0f172a',

    lineHeight: 25,

    textAlign: 'center',
  },

  registerNumber: {
    marginTop: 2,

    fontSize: 14,
    fontWeight: '700',

    color: '#2563eb',

    letterSpacing: 0.7,
  },

  departmentPill: {
    marginTop: 10,

    paddingHorizontal: 14,
    paddingVertical: 4,

    borderRadius: 999,

    backgroundColor: '#e8ecf8',
  },

  departmentText: {
    fontSize: 12,
    fontWeight: '600',

    color: '#1a56db',
  },

  studentMeta: {
    marginTop: 8,

    fontSize: 11,
    fontWeight: '500',

    color: '#64748b',

    textAlign: 'center',
  },

  divider: {
    width: '100%',

    height: 1,

    backgroundColor: '#f1f5f9',

    marginVertical: 16,
  },

  /* ================= DETAILS ================= */

  detailsContainer: {
    width: '100%',
  },

  detailRow: {
    width: '100%',

    minHeight: 34,

    paddingHorizontal: 12,
    paddingVertical: 6,

    borderRadius: 12,

    backgroundColor: '#f3f3fe',

    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',

    marginBottom: 10,
  },

  detailLeft: {
    flexDirection: 'row',
    alignItems: 'center',

    flexShrink: 1,
  },

  detailLabel: {
    marginLeft: 10,

    fontSize: 12,
    fontWeight: '500',

    color: '#64748b',
  },

  detailValue: {
    marginLeft: 10,

    flexShrink: 1,

    maxWidth: 190,

    fontSize: 12,
    fontWeight: '600',

    color: '#1e293b',

    textAlign: 'right',
  },

  /* ================= EMPTY SECTIONS ================= */

  performanceSection: {
    marginTop: 14,
  },

  courseSection: {
    marginTop: 4,
  },

  servicesSection: {
    marginTop: 4,
  },

  /* ================= BOTTOM NAV ================= */

  bottomNavigation: {
    position: 'absolute',

    left: 0,
    right: 0,
    bottom: 0,

    height: 64,

    backgroundColor: '#ffffff',

    borderTopWidth: 1,
    borderTopColor: 'rgba(226, 232, 240, 0.8)',

    paddingHorizontal: 16,
    paddingVertical: 8,

    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',

    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: -4,
    },
    shadowOpacity: 0.04,
    shadowRadius: 10,

    elevation: 8,

    zIndex: 40,
  },

  navItem: {
    width: 60,
    height: 48,

    alignItems: 'center',
    justifyContent: 'center',

    paddingVertical: 4,
  },

  navText: {
    marginTop: 2,

    fontSize: 10,
    fontWeight: '500',

    color: '#64748b',
  },

  emptyNavItem: {
    width: 60,
    height: 48,
  },

  activeNavItem: {
    width: 64,
    height: 48,

    borderRadius: 24,

    backgroundColor: '#1a56db',

    alignItems: 'center',
    justifyContent: 'center',

    shadowColor: '#1a56db',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.30,
    shadowRadius: 6,

    elevation: 5,
  },

  activeNavText: {
    marginTop: -1,

    fontSize: 10,
    fontWeight: '600',

    color: '#ffffff',
  },
});

export default StudentProfile;
