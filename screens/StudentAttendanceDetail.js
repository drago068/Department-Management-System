import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';
import TopAppBar from '../components/TopAppBar';
import BottomNavBar from '../components/BottomNavBar';

const StudentAttendanceDetail = ({ navigation }) => {
  const [selectedSubject, setSelectedSubject] = useState('all');

  const subjects = [
    { key: 'all', label: 'All Subjects' },
    { key: 'cs301', label: 'CS301' },
    { key: 'cs302', label: 'CS302' },
    { key: 'cs303', label: 'CS303' },
  ];

  const attendanceLog = [
    { date: 'Sep 6, 2024', subject: 'Data Structures (CS301)', period: 'Period 1', status: 'present' },
    { date: 'Sep 6, 2024', subject: 'Algorithms (CS302)', period: 'Period 2', status: 'present' },
    { date: 'Sep 6, 2024', subject: 'DBMS (CS303)', period: 'Period 3', status: 'absent' },
    { date: 'Sep 5, 2024', subject: 'Data Structures (CS301)', period: 'Period 1', status: 'present' },
    { date: 'Sep 5, 2024', subject: 'Algorithms (CS302)', period: 'Period 2', status: 'present' },
    { date: 'Sep 5, 2024', subject: 'DBMS (CS303)', period: 'Period 3', status: 'od' },
    { date: 'Sep 4, 2024', subject: 'Data Structures (CS301)', period: 'Period 1', status: 'present' },
    { date: 'Sep 4, 2024', subject: 'Algorithms (CS302)', period: 'Period 2', status: 'absent' },
    { date: 'Sep 4, 2024', subject: 'DBMS (CS303)', period: 'Period 3', status: 'present' },
  ];

  const subjectStats = [
    { name: 'Data Structures', code: 'CS301', present: 42, total: 45, percentage: 93 },
    { name: 'Algorithms', code: 'CS302', present: 38, total: 45, percentage: 84 },
    { name: 'DBMS', code: 'CS303', present: 35, total: 45, percentage: 78 },
  ];

  const statusConfig = {
    present: { bg: '#dcfce7', text: '#166534', label: 'Present', icon: 'check-circle' },
    absent: { bg: '#fee2e2', text: '#b91c1c', label: 'Absent', icon: 'cancel' },
    od: { bg: '#ffedd5', text: '#c2410c', label: 'OD', icon: 'assignment-ind' },
  };

  const bottomNavItems = [
    { key: 'home', label: 'Home', icon: 'dashboard' },
    { key: 'attendance', label: 'Attendance', icon: 'how-to-reg' },
    { key: 'history', label: 'History', icon: 'calendar-month' },
    { key: 'profile', label: 'Profile', icon: 'person' },
  ];

  return (
    <SafeAreaView style={styles.safeArea}>
      <TopAppBar title="Attendance Detail" />
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.contentInner}>
          {/* Page Header */}
          <View>
            <Text style={styles.pageTitle}>Attendance Details</Text>
            <Text style={styles.pageSubtitle}>Your detailed attendance records by subject and date.</Text>
          </View>

          {/* Subject-wise Summary */}
          <View style={styles.summarySection}>
            <Text style={styles.sectionTitle}>Subject Summary</Text>
            {subjectStats.map((subj, index) => (
              <View key={index} style={styles.subjectSummaryCard}>
                <View style={styles.subjectSummaryHeader}>
                  <View>
                    <Text style={styles.subjectName}>{subj.name}</Text>
                    <Text style={styles.subjectCode}>{subj.code}</Text>
                  </View>
                  <Text style={[styles.subjectPercentage, { color: subj.percentage >= 75 ? '#16a34a' : Colors.error }]}>
                    {subj.percentage}%
                  </Text>
                </View>
                <View style={styles.subjectStatsRow}>
                  <Text style={styles.subjectStatText}>{subj.present}/{subj.total} sessions</Text>
                </View>
                <View style={styles.progressBarBg}>
                  <View style={[styles.progressBarFill, {
                    width: `${subj.percentage}%`,
                    backgroundColor: subj.percentage >= 75 ? '#22c55e' : Colors.error,
                  }]} />
                </View>
              </View>
            ))}
          </View>

          {/* Subject Filter */}
          <View style={styles.filterRow}>
            {subjects.map((s) => (
              <TouchableOpacity
                key={s.key}
                style={[styles.filterChip, selectedSubject === s.key && styles.filterChipActive]}
                onPress={() => setSelectedSubject(s.key)}
              >
                <Text style={[styles.filterText, selectedSubject === s.key && styles.filterTextActive]}>{s.label}</Text>
              </TouchableOpacity>
            ))}
          </View>

          {/* Attendance Log */}
          <View style={styles.logCard}>
            <Text style={styles.sectionTitle}>Daily Log</Text>
            {attendanceLog.map((entry, index) => {
              const sc = statusConfig[entry.status];
              return (
                <View key={index} style={styles.logEntry}>
                  <View style={styles.logLeft}>
                    <Text style={styles.logDate}>{entry.date}</Text>
                    <Text style={styles.logSubject}>{entry.subject}</Text>
                    <Text style={styles.logPeriod}>{entry.period}</Text>
                  </View>
                  <View style={[styles.logStatusBadge, { backgroundColor: sc.bg }]}>
                    <MaterialIcons name={sc.icon} size={14} color={sc.text} />
                    <Text style={[styles.logStatusText, { color: sc.text }]}>{sc.label}</Text>
                  </View>
                </View>
              );
            })}
          </View>
        </View>
      </ScrollView>
      <BottomNavBar items={bottomNavItems} activeItem="attendance" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: Colors.background },
  content: { flex: 1 },
  contentInner: { padding: 16, paddingBottom: 80, gap: 16 },
  pageTitle: { ...Typography.headlineLgMobile, color: Colors.onBackground },
  pageSubtitle: { ...Typography.bodyMd, color: Colors.onSurfaceVariant, marginTop: 4 },
  sectionTitle: { ...Typography.headlineSm, color: Colors.onSurface, marginBottom: 8 },
  summarySection: {
    backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, padding: 16,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)', gap: 12,
  },
  subjectSummaryCard: {
    padding: 12, borderRadius: 8, backgroundColor: Colors.surfaceContainerLow, gap: 8,
  },
  subjectSummaryHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  subjectName: { ...Typography.labelMd, color: Colors.onSurface, fontWeight: '600' },
  subjectCode: { ...Typography.labelSm, color: Colors.onSurfaceVariant, fontWeight: '400' },
  subjectPercentage: { ...Typography.headlineMd, fontWeight: '700' },
  subjectStatsRow: { flexDirection: 'row' },
  subjectStatText: { ...Typography.bodyMd, color: Colors.onSurfaceVariant, fontSize: 12 },
  progressBarBg: { height: 6, backgroundColor: Colors.surfaceContainerHighest, borderRadius: 3 },
  progressBarFill: { height: 6, borderRadius: 3 },
  filterRow: { flexDirection: 'row', gap: 8, flexWrap: 'wrap' },
  filterChip: {
    paddingHorizontal: 14, paddingVertical: 6, borderRadius: 9999,
    backgroundColor: Colors.surfaceContainerLow, borderWidth: 1, borderColor: Colors.outlineVariant,
  },
  filterChipActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  filterText: { ...Typography.labelSm, color: Colors.onSurfaceVariant },
  filterTextActive: { color: Colors.onPrimary },
  logCard: {
    backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, padding: 16,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)', gap: 8,
  },
  logEntry: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: 'rgba(195,197,215,0.2)',
  },
  logLeft: { flex: 1 },
  logDate: { ...Typography.labelSm, color: Colors.onSurfaceVariant, fontWeight: '400' },
  logSubject: { ...Typography.labelMd, color: Colors.onSurface, marginTop: 2 },
  logPeriod: { ...Typography.bodyMd, color: Colors.onSurfaceVariant, fontSize: 12, marginTop: 2 },
  logStatusBadge: {
    flexDirection: 'row', alignItems: 'center', gap: 4,
    paddingHorizontal: 10, paddingVertical: 4, borderRadius: 9999,
  },
  logStatusText: { fontSize: 12, fontWeight: '500' },
});

export default StudentAttendanceDetail;
