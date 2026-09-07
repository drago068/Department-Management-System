import React from 'react';
import { View, Text, ScrollView, Image, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';
import TopAppBar from '../components/TopAppBar';
import BottomNavBar from '../components/BottomNavBar';

const StudentDashboard = ({ navigation }) => {
  const bottomNavItems = [
    { key: 'home', label: 'Home', icon: 'dashboard' },
    { key: 'attendance', label: 'Attendance', icon: 'how-to-reg' },
    { key: 'history', label: 'History', icon: 'calendar-month' },
    { key: 'profile', label: 'Profile', icon: 'person' },
  ];

  const subjects = [
    { name: 'Data Structures', code: 'CS301', professor: 'Prof. Smith', percentage: 92, color: '#16a34a' },
    { name: 'Algorithms', code: 'CS302', professor: 'Prof. Johnson', percentage: 85, color: Colors.primary },
    { name: 'DBMS', code: 'CS303', professor: 'Prof. Davis', percentage: 78, color: Colors.error, warning: true },
  ];

  return (
    <SafeAreaView style={styles.safeArea}>
      <TopAppBar
        title="Student Portal"
        profileImage="https://lh3.googleusercontent.com/aida-public/AB6AXuDh3ENYoGBBV3bwzJspo81SvX0BWvEf23eyCzngqYJi8Cvhm9IqFDfJMK-_BL37P9EyvAzSBkAdyPSWaHNJHS1p9giuzDzevIiw7Y9b9FeWUmRDkYC0NUqGXjYAbk1fuW-CxWJmGUh15EtLUrm0dk4EwB_vFa1gpTrE-hdF6YhiHf8joIq2cbe9phvQOw1N-_TkQwnHGty6vZEaX2XtroEdA2Mg-yxJSUcQivTuQht1R0DFo2GOPE7e"
      />
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.contentInner}>
          {/* Overall Attendance Card */}
          <View style={styles.overallCard}>
            <Text style={styles.overallLabel}>Overall Attendance</Text>
            {/* Circular Progress (simplified) */}
            <View style={styles.circularContainer}>
              <View style={styles.circularOuter}>
                <View style={styles.circularInner}>
                  <Text style={styles.circularText}>88%</Text>
                </View>
              </View>
            </View>
            <View style={styles.statusBadge}>
              <MaterialIcons name="check-circle" size={16} color="#166534" />
              <Text style={styles.statusText}>Good Standing</Text>
            </View>
          </View>

          {/* Breakdown Cards */}
          <View style={styles.breakdownRow}>
            {/* Present */}
            <View style={styles.breakdownCard}>
              <View style={styles.breakdownHeader}>
                <Text style={styles.breakdownLabel}>Total Present</Text>
                <View style={[styles.breakdownIcon, { backgroundColor: '#dbeafe' }]}>
                  <MaterialIcons name="how-to-reg" size={18} color="#1d4ed8" />
                </View>
              </View>
              <View style={styles.breakdownValue}>
                <Text style={styles.breakdownNumber}>220</Text>
                <Text style={styles.breakdownUnit}>sessions</Text>
              </View>
            </View>

            {/* Absent */}
            <View style={styles.breakdownCard}>
              <View style={styles.breakdownHeader}>
                <Text style={styles.breakdownLabel}>Total Absent</Text>
                <View style={[styles.breakdownIcon, { backgroundColor: '#fee2e2' }]}>
                  <MaterialIcons name="person-off" size={18} color="#b91c1c" />
                </View>
              </View>
              <View style={styles.breakdownValue}>
                <Text style={styles.breakdownNumber}>25</Text>
                <Text style={styles.breakdownUnit}>sessions</Text>
              </View>
            </View>

            {/* On Duty */}
            <View style={styles.breakdownCard}>
              <View style={styles.breakdownHeader}>
                <Text style={styles.breakdownLabel}>On Duty (OD)</Text>
                <View style={[styles.breakdownIcon, { backgroundColor: '#ffedd5' }]}>
                  <MaterialIcons name="assignment-ind" size={18} color="#c2410c" />
                </View>
              </View>
              <View style={styles.breakdownValue}>
                <Text style={styles.breakdownNumber}>5</Text>
                <Text style={styles.breakdownUnit}>sessions</Text>
              </View>
            </View>
          </View>

          {/* Subject Breakdown */}
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Subject Breakdown</Text>
            <TouchableOpacity>
              <Text style={styles.viewAllLink}>View All</Text>
            </TouchableOpacity>
          </View>

          {subjects.map((subject, index) => (
            <View key={index} style={[styles.subjectCard, subject.warning && styles.subjectCardWarning]}>
              {subject.warning && (
                <View style={styles.warningBadge}>
                  <Text style={styles.warningBadgeText}>WARNING</Text>
                </View>
              )}
              <View style={styles.subjectHeader}>
                <View>
                  <Text style={styles.subjectName}>{subject.name}</Text>
                  <Text style={styles.subjectMeta}>{subject.code} • {subject.professor}</Text>
                </View>
                <Text style={[styles.subjectPercentage, { color: subject.color }]}>{subject.percentage}%</Text>
              </View>
              {subject.warning && (
                <Text style={styles.warningText}>Approaching 75% minimum requirement.</Text>
              )}
              <View style={styles.progressBarBg}>
                <View style={[styles.progressBarFill, { width: `${subject.percentage}%`, backgroundColor: subject.color }]} />
              </View>
            </View>
          ))}
        </View>
      </ScrollView>

      <BottomNavBar
        items={bottomNavItems}
        activeItem="home"
        onItemPress={(item) => {
          if (item.key === 'profile') navigation?.navigate('StudentProfile');
          else if (item.key === 'history') navigation?.navigate('AttendanceHistory');
          else if (item.key === 'attendance') navigation?.navigate('StudentAttendanceDetail');
        }}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: Colors.surfaceContainerLow,
  },
  content: {
    flex: 1,
  },
  contentInner: {
    padding: 16,
    paddingBottom: 80,
    gap: 16,
  },
  overallCard: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: Colors.outlineVariant,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  overallLabel: {
    ...Typography.labelMd,
    color: Colors.onSurfaceVariant,
    alignSelf: 'flex-start',
  },
  circularContainer: {
    marginTop: 16,
    marginBottom: 16,
  },
  circularOuter: {
    width: 128,
    height: 128,
    borderRadius: 64,
    borderWidth: 8,
    borderColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: Colors.surfaceContainerHighest,
  },
  circularInner: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  circularText: {
    ...Typography.headlineLg,
    color: Colors.onSurface,
    fontWeight: '700',
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    backgroundColor: '#dcfce7',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 9999,
  },
  statusText: {
    ...Typography.labelSm,
    color: '#166534',
  },
  breakdownRow: {
    flexDirection: 'row',
    gap: 8,
  },
  breakdownCard: {
    flex: 1,
    backgroundColor: Colors.surface,
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: Colors.outlineVariant,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  breakdownHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  breakdownLabel: {
    ...Typography.labelMd,
    color: Colors.onSurfaceVariant,
    flex: 1,
  },
  breakdownIcon: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  breakdownValue: {
    marginTop: 16,
  },
  breakdownNumber: {
    ...Typography.headlineLg,
    color: Colors.onSurface,
    fontWeight: '700',
  },
  breakdownUnit: {
    ...Typography.bodyMd,
    color: Colors.onSurfaceVariant,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 8,
  },
  sectionTitle: {
    ...Typography.headlineSm,
    color: Colors.onSurface,
    fontWeight: '600',
  },
  viewAllLink: {
    ...Typography.labelSm,
    color: Colors.primary,
  },
  subjectCard: {
    backgroundColor: Colors.surface,
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: Colors.outlineVariant,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  subjectCardWarning: {
    backgroundColor: 'rgba(255, 218, 214, 0.2)',
    borderColor: 'rgba(186, 26, 26, 0.3)',
  },
  warningBadge: {
    position: 'absolute',
    top: 0,
    right: 0,
    backgroundColor: Colors.error,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderBottomLeftRadius: 8,
    borderTopRightRadius: 12,
  },
  warningBadgeText: {
    color: Colors.onError,
    fontSize: 10,
    fontWeight: '600',
    letterSpacing: 1,
  },
  subjectHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
  },
  subjectName: {
    ...Typography.labelMd,
    color: Colors.onSurface,
    fontWeight: '600',
  },
  subjectMeta: {
    ...Typography.labelSm,
    color: Colors.onSurfaceVariant,
  },
  subjectPercentage: {
    ...Typography.headlineMd,
    fontWeight: '700',
  },
  warningText: {
    ...Typography.labelSm,
    color: Colors.error,
    marginBottom: 8,
  },
  progressBarBg: {
    width: '100%',
    height: 8,
    backgroundColor: Colors.surfaceContainerHighest,
    borderRadius: 4,
    marginTop: 'auto',
  },
  progressBarFill: {
    height: 8,
    borderRadius: 4,
  },
});

export default StudentDashboard;
