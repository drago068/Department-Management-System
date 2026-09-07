import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';
import TopAppBar from '../components/TopAppBar';
import BottomNavBar from '../components/BottomNavBar';

const MarkAttendance = ({ navigation }) => {
  const [selectedDate] = useState('2024-09-06');
  const [selectedPeriod, setSelectedPeriod] = useState('Period 1');

  const students = [
    { id: 'CS2024-001', name: 'Arjun Patel', status: 'present' },
    { id: 'CS2024-002', name: 'Priya Sharma', status: 'present' },
    { id: 'CS2024-003', name: 'Rahul Verma', status: 'absent' },
    { id: 'CS2024-004', name: 'Sneha Gupta', status: 'present' },
    { id: 'CS2024-005', name: 'Vikram Singh', status: 'present' },
    { id: 'CS2024-006', name: 'Ananya Iyer', status: 'od' },
    { id: 'CS2024-007', name: 'Karthik Rajan', status: 'present' },
    { id: 'CS2024-008', name: 'Meera Nair', status: 'present' },
    { id: 'CS2024-009', name: 'Aditya Kumar', status: 'absent' },
    { id: 'CS2024-010', name: 'Divya Menon', status: 'present' },
  ];

  const [studentStates, setStudentStates] = useState(
    students.map((s) => ({ ...s }))
  );

  const toggleStatus = (index, newStatus) => {
    setStudentStates((prev) => {
      const updated = [...prev];
      updated[index] = { ...updated[index], status: newStatus };
      return updated;
    });
  };

  const statusColors = {
    present: { bg: '#dcfce7', text: '#166534', icon: 'check-circle' },
    absent: { bg: '#fee2e2', text: '#b91c1c', icon: 'cancel' },
    od: { bg: '#ffedd5', text: '#c2410c', icon: 'assignment-ind' },
  };

  const presentCount = studentStates.filter((s) => s.status === 'present').length;
  const absentCount = studentStates.filter((s) => s.status === 'absent').length;
  const odCount = studentStates.filter((s) => s.status === 'od').length;

  const bottomNavItems = [
    { key: 'home', label: 'Home', icon: 'dashboard' },
    { key: 'attendance', label: 'Attendance', icon: 'how-to-reg' },
    { key: 'history', label: 'History', icon: 'calendar-month' },
    { key: 'profile', label: 'Profile', icon: 'person' },
  ];

  return (
    <SafeAreaView style={styles.safeArea}>
      <TopAppBar title="Mark Attendance" showMenu onMenuPress={() => navigation.goBack()} />
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.contentInner}>
          {/* Class Info Header */}
          <View style={styles.classInfoCard}>
            <View style={styles.classInfoRow}>
              <View>
                <Text style={styles.className}>CS-101: Data Structures</Text>
                <Text style={styles.classDetail}>B.Tech Semester 3 • Room 402</Text>
              </View>
              <View style={styles.dateBadge}>
                <MaterialIcons name="calendar-today" size={14} color={Colors.primary} />
                <Text style={styles.dateText}>{selectedDate}</Text>
              </View>
            </View>
            {/* Period selector */}
            <View style={styles.periodRow}>
              {['Period 1', 'Period 2', 'Period 3'].map((p) => (
                <TouchableOpacity
                  key={p}
                  style={[styles.periodChip, selectedPeriod === p && styles.periodChipActive]}
                  onPress={() => setSelectedPeriod(p)}
                >
                  <Text style={[styles.periodText, selectedPeriod === p && styles.periodTextActive]}>{p}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Summary Stats */}
          <View style={styles.summaryRow}>
            <View style={[styles.summaryCard, { borderLeftColor: '#22c55e' }]}>
              <Text style={styles.summaryCount}>{presentCount}</Text>
              <Text style={styles.summaryLabel}>Present</Text>
            </View>
            <View style={[styles.summaryCard, { borderLeftColor: '#ef4444' }]}>
              <Text style={styles.summaryCount}>{absentCount}</Text>
              <Text style={styles.summaryLabel}>Absent</Text>
            </View>
            <View style={[styles.summaryCard, { borderLeftColor: '#f97316' }]}>
              <Text style={styles.summaryCount}>{odCount}</Text>
              <Text style={styles.summaryLabel}>OD</Text>
            </View>
          </View>

          {/* Student List */}
          <View style={styles.studentListCard}>
            <View style={styles.studentListHeader}>
              <Text style={styles.sectionTitle}>Student List</Text>
              <Text style={styles.totalCount}>{studentStates.length} students</Text>
            </View>
            {studentStates.map((student, index) => {
              const sc = statusColors[student.status];
              return (
                <View key={student.id} style={styles.studentRow}>
                  <View style={styles.studentInfo}>
                    <View style={styles.studentAvatar}>
                      <Text style={styles.studentAvatarText}>{student.name.charAt(0)}</Text>
                    </View>
                    <View>
                      <Text style={styles.studentName}>{student.name}</Text>
                      <Text style={styles.studentId}>{student.id}</Text>
                    </View>
                  </View>
                  <View style={styles.statusButtons}>
                    <TouchableOpacity
                      style={[styles.statusBtn, student.status === 'present' && { backgroundColor: statusColors.present.bg }]}
                      onPress={() => toggleStatus(index, 'present')}
                    >
                      <MaterialIcons name="check" size={18} color={student.status === 'present' ? statusColors.present.text : Colors.outline} />
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={[styles.statusBtn, student.status === 'absent' && { backgroundColor: statusColors.absent.bg }]}
                      onPress={() => toggleStatus(index, 'absent')}
                    >
                      <MaterialIcons name="close" size={18} color={student.status === 'absent' ? statusColors.absent.text : Colors.outline} />
                    </TouchableOpacity>
                    <TouchableOpacity
                      style={[styles.statusBtn, student.status === 'od' && { backgroundColor: statusColors.od.bg }]}
                      onPress={() => toggleStatus(index, 'od')}
                    >
                      <Text style={[styles.odText, student.status === 'od' && { color: statusColors.od.text }]}>OD</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              );
            })}
          </View>

          {/* Submit Button */}
          <TouchableOpacity style={styles.submitButton} activeOpacity={0.8}>
            <MaterialIcons name="check-circle" size={20} color={Colors.onPrimary} />
            <Text style={styles.submitButtonText}>Submit Attendance</Text>
          </TouchableOpacity>
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
  classInfoCard: {
    backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, padding: 16,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)', gap: 12,
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
  },
  classInfoRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  className: { ...Typography.headlineSm, color: Colors.onSurface, fontSize: 18 },
  classDetail: { ...Typography.bodyMd, color: Colors.onSurfaceVariant, marginTop: 4 },
  dateBadge: {
    flexDirection: 'row', alignItems: 'center', gap: 4,
    backgroundColor: Colors.surfaceContainer, paddingHorizontal: 8, paddingVertical: 4, borderRadius: 8,
  },
  dateText: { ...Typography.labelSm, color: Colors.primary },
  periodRow: { flexDirection: 'row', gap: 8 },
  periodChip: {
    paddingHorizontal: 16, paddingVertical: 8, borderRadius: 8,
    backgroundColor: Colors.surfaceContainerLow, borderWidth: 1, borderColor: Colors.outlineVariant,
  },
  periodChipActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  periodText: { ...Typography.labelSm, color: Colors.onSurfaceVariant },
  periodTextActive: { color: Colors.onPrimary },
  summaryRow: { flexDirection: 'row', gap: 8 },
  summaryCard: {
    flex: 1, backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, padding: 12,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)', borderLeftWidth: 4, alignItems: 'center',
  },
  summaryCount: { ...Typography.headlineMd, color: Colors.onSurface, fontWeight: '700' },
  summaryLabel: { ...Typography.labelSm, color: Colors.onSurfaceVariant, marginTop: 4 },
  studentListCard: {
    backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, overflow: 'hidden',
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)',
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
  },
  studentListHeader: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    padding: 16, borderBottomWidth: 1, borderBottomColor: 'rgba(195,197,215,0.3)',
  },
  sectionTitle: { ...Typography.headlineSm, color: Colors.onSurface },
  totalCount: { ...Typography.labelSm, color: Colors.onSurfaceVariant },
  studentRow: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    paddingHorizontal: 16, paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: 'rgba(195,197,215,0.1)',
  },
  studentInfo: { flexDirection: 'row', alignItems: 'center', gap: 12 },
  studentAvatar: {
    width: 36, height: 36, borderRadius: 18, backgroundColor: Colors.primaryContainer,
    alignItems: 'center', justifyContent: 'center',
  },
  studentAvatarText: { color: Colors.onPrimaryContainer, fontWeight: '700', fontSize: 14 },
  studentName: { ...Typography.labelMd, color: Colors.onSurface },
  studentId: { ...Typography.labelSm, color: Colors.onSurfaceVariant, fontWeight: '400' },
  statusButtons: { flexDirection: 'row', gap: 4 },
  statusBtn: {
    width: 36, height: 36, borderRadius: 8, alignItems: 'center', justifyContent: 'center',
    borderWidth: 1, borderColor: Colors.outlineVariant,
  },
  odText: { ...Typography.labelSm, color: Colors.outline, fontSize: 10 },
  submitButton: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center',
    backgroundColor: Colors.primary, paddingVertical: 14, borderRadius: 12, gap: 8,
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4, elevation: 3,
  },
  submitButtonText: { ...Typography.labelMd, color: Colors.onPrimary, fontSize: 16 },
});

export default MarkAttendance;
