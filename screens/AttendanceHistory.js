import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';
import TopAppBar from '../components/TopAppBar';
import BottomNavBar from '../components/BottomNavBar';

const AttendanceHistory = ({ navigation }) => {
  const [selectedMonth, setSelectedMonth] = useState('September');

  const months = ['August', 'September', 'October'];

  const historyData = [
    { date: 'Sep 6, 2024', day: 'Friday', entries: [
      { course: 'CS-101: Data Structures', period: 'Period 1', present: 38, total: 40, staff: 'Dr. Priya Sharma' },
      { course: 'CS-305: Algorithms', period: 'Period 2', present: 42, total: 45, staff: 'Prof. Arjun Patel' },
    ]},
    { date: 'Sep 5, 2024', day: 'Thursday', entries: [
      { course: 'MA-201: Linear Algebra', period: 'Period 1', present: 35, total: 40, staff: 'Dr. Sneha Gupta' },
      { course: 'PH-301: Quantum Physics', period: 'Period 3', present: 22, total: 25, staff: 'Dr. Vikram Singh' },
      { course: 'CS-Lab: Python', period: 'Lab', present: 20, total: 20, staff: 'Prof. Meera Nair' },
    ]},
    { date: 'Sep 4, 2024', day: 'Wednesday', entries: [
      { course: 'CS-101: Data Structures', period: 'Period 1', present: 37, total: 40, staff: 'Dr. Priya Sharma' },
      { course: 'ENG-101: Technical Writing', period: 'Period 4', present: 28, total: 30, staff: 'Prof. Karthik R.' },
    ]},
  ];

  const bottomNavItems = [
    { key: 'home', label: 'Home', icon: 'dashboard' },
    { key: 'attendance', label: 'Attendance', icon: 'how-to-reg' },
    { key: 'history', label: 'History', icon: 'calendar-month' },
    { key: 'profile', label: 'Profile', icon: 'person' },
  ];

  return (
    <SafeAreaView style={styles.safeArea}>
      <TopAppBar title="Attendance History" />
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.contentInner}>
          {/* Page Header */}
          <View>
            <Text style={styles.pageTitle}>Attendance History</Text>
            <Text style={styles.pageSubtitle}>View past attendance records by date.</Text>
          </View>

          {/* Month Selector */}
          <View style={styles.monthRow}>
            {months.map((m) => (
              <TouchableOpacity
                key={m}
                style={[styles.monthChip, selectedMonth === m && styles.monthChipActive]}
                onPress={() => setSelectedMonth(m)}
              >
                <Text style={[styles.monthText, selectedMonth === m && styles.monthTextActive]}>{m}</Text>
              </TouchableOpacity>
            ))}
          </View>

          {/* Summary Stats */}
          <View style={styles.summaryRow}>
            <View style={styles.summaryCard}>
              <Text style={styles.summaryValue}>94%</Text>
              <Text style={styles.summaryLabel}>Avg. Attendance</Text>
            </View>
            <View style={styles.summaryCard}>
              <Text style={styles.summaryValue}>18</Text>
              <Text style={styles.summaryLabel}>Working Days</Text>
            </View>
            <View style={styles.summaryCard}>
              <Text style={styles.summaryValue}>42</Text>
              <Text style={styles.summaryLabel}>Sessions</Text>
            </View>
          </View>

          {/* History by Date */}
          {historyData.map((dateGroup, index) => (
            <View key={index} style={styles.dateGroup}>
              <View style={styles.dateHeader}>
                <View style={styles.dateIconWrap}>
                  <MaterialIcons name="calendar-today" size={16} color={Colors.primary} />
                </View>
                <View>
                  <Text style={styles.dateTitle}>{dateGroup.date}</Text>
                  <Text style={styles.dateDay}>{dateGroup.day}</Text>
                </View>
              </View>

              {dateGroup.entries.map((entry, eIdx) => {
                const percentage = Math.round((entry.present / entry.total) * 100);
                return (
                  <View key={eIdx} style={styles.entryCard}>
                    <View style={styles.entryHeader}>
                      <View style={{ flex: 1 }}>
                        <Text style={styles.entryCourse}>{entry.course}</Text>
                        <Text style={styles.entryMeta}>{entry.period} • {entry.staff}</Text>
                      </View>
                      <View style={styles.entryStats}>
                        <Text style={styles.entryCount}>{entry.present}/{entry.total}</Text>
                        <Text style={[styles.entryPercentage, { color: percentage >= 75 ? '#16a34a' : Colors.error }]}>{percentage}%</Text>
                      </View>
                    </View>
                    <View style={styles.progressBarBg}>
                      <View style={[styles.progressBarFill, { width: `${percentage}%`, backgroundColor: percentage >= 75 ? '#22c55e' : Colors.error }]} />
                    </View>
                  </View>
                );
              })}
            </View>
          ))}
        </View>
      </ScrollView>
      <BottomNavBar items={bottomNavItems} activeItem="history" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: Colors.background },
  content: { flex: 1 },
  contentInner: { padding: 16, paddingBottom: 80, gap: 16 },
  pageTitle: { ...Typography.headlineLgMobile, color: Colors.onBackground },
  pageSubtitle: { ...Typography.bodyMd, color: Colors.onSurfaceVariant, marginTop: 4 },
  monthRow: { flexDirection: 'row', gap: 8 },
  monthChip: {
    paddingHorizontal: 16, paddingVertical: 8, borderRadius: 9999,
    backgroundColor: Colors.surfaceContainerLow, borderWidth: 1, borderColor: Colors.outlineVariant,
  },
  monthChipActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  monthText: { ...Typography.labelSm, color: Colors.onSurfaceVariant },
  monthTextActive: { color: Colors.onPrimary },
  summaryRow: { flexDirection: 'row', gap: 8 },
  summaryCard: {
    flex: 1, backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, padding: 12, alignItems: 'center',
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)',
  },
  summaryValue: { ...Typography.headlineMd, color: Colors.primary, fontWeight: '700' },
  summaryLabel: { ...Typography.labelSm, color: Colors.onSurfaceVariant, marginTop: 4, textAlign: 'center' },
  dateGroup: { gap: 8 },
  dateHeader: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 4 },
  dateIconWrap: {
    width: 36, height: 36, borderRadius: 18, backgroundColor: 'rgba(0,63,177,0.1)',
    alignItems: 'center', justifyContent: 'center',
  },
  dateTitle: { ...Typography.labelMd, color: Colors.onSurface, fontWeight: '600' },
  dateDay: { ...Typography.labelSm, color: Colors.onSurfaceVariant, fontWeight: '400' },
  entryCard: {
    backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, padding: 16,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)', gap: 12, marginLeft: 18,
    borderLeftWidth: 2, borderLeftColor: Colors.primaryFixed,
  },
  entryHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  entryCourse: { ...Typography.labelMd, color: Colors.onSurface, fontWeight: '600' },
  entryMeta: { ...Typography.bodyMd, color: Colors.onSurfaceVariant, fontSize: 12, marginTop: 2 },
  entryStats: { alignItems: 'flex-end' },
  entryCount: { ...Typography.labelMd, color: Colors.onSurface },
  entryPercentage: { ...Typography.labelSm, marginTop: 2 },
  progressBarBg: { height: 6, backgroundColor: Colors.surfaceContainerHighest, borderRadius: 3 },
  progressBarFill: { height: 6, borderRadius: 3 },
});

export default AttendanceHistory;
