import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, StyleSheet, SafeAreaView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';
import TopAppBar from '../components/TopAppBar';
import BottomNavBar from '../components/BottomNavBar';

const ReportManagement = ({ navigation }) => {
  const [selectedReportType, setSelectedReportType] = useState('attendance');

  const reportTypes = [
    { key: 'attendance', label: 'Attendance', icon: 'how-to-reg' },
    { key: 'student', label: 'Student', icon: 'school' },
    { key: 'staff', label: 'Staff', icon: 'badge' },
    { key: 'department', label: 'Department', icon: 'business' },
  ];

  const recentReports = [
    { name: 'Monthly Attendance Report - August 2024', type: 'Attendance', date: 'Sep 1, 2024', format: 'Excel', size: '2.3 MB', status: 'ready' },
    { name: 'Student Shortage List - Semester 3', type: 'Student', date: 'Aug 30, 2024', format: 'PDF', size: '1.1 MB', status: 'ready' },
    { name: 'Staff Teaching Load Report', type: 'Staff', date: 'Aug 28, 2024', format: 'Excel', size: '856 KB', status: 'ready' },
    { name: 'Department Performance Summary', type: 'Department', date: 'Aug 25, 2024', format: 'PDF', size: '3.4 MB', status: 'generating' },
  ];

  const quickReports = [
    { label: 'Today\'s Attendance', icon: 'today', description: 'Generate attendance for all classes today' },
    { label: 'Shortage List', icon: 'warning', description: 'Students below 75% attendance' },
    { label: 'Monthly Summary', icon: 'calendar-month', description: 'Complete monthly attendance summary' },
    { label: 'Staff Report', icon: 'badge', description: 'Staff-wise attendance marking report' },
  ];

  const bottomNavItems = [
    { key: 'home', label: 'Home', icon: 'dashboard' },
    { key: 'attendance', label: 'Attendance', icon: 'how-to-reg' },
    { key: 'history', label: 'History', icon: 'calendar-month' },
    { key: 'profile', label: 'Profile', icon: 'person' },
  ];

  return (
    <SafeAreaView style={styles.safeArea}>
      <TopAppBar title="Reports" />
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.contentInner}>
          {/* Page Header */}
          <View>
            <Text style={styles.pageTitle}>Reports & Excel Management</Text>
            <Text style={styles.pageSubtitle}>Generate, download, and manage attendance reports.</Text>
          </View>

          {/* Quick Generate */}
          <View style={styles.sectionCard}>
            <Text style={styles.sectionTitle}>Quick Generate</Text>
            <View style={styles.quickGrid}>
              {quickReports.map((qr, index) => (
                <TouchableOpacity key={index} style={styles.quickItem} activeOpacity={0.7}>
                  <View style={styles.quickIconWrap}>
                    <MaterialIcons name={qr.icon} size={24} color={Colors.primary} />
                  </View>
                  <Text style={styles.quickLabel}>{qr.label}</Text>
                  <Text style={styles.quickDesc}>{qr.description}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* Report Type Filter */}
          <View style={styles.filterRow}>
            {reportTypes.map((rt) => (
              <TouchableOpacity
                key={rt.key}
                style={[styles.filterChip, selectedReportType === rt.key && styles.filterChipActive]}
                onPress={() => setSelectedReportType(rt.key)}
              >
                <MaterialIcons
                  name={rt.icon}
                  size={16}
                  color={selectedReportType === rt.key ? Colors.onPrimary : Colors.onSurfaceVariant}
                />
                <Text style={[styles.filterText, selectedReportType === rt.key && styles.filterTextActive]}>
                  {rt.label}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          {/* Recent Reports */}
          <View style={styles.sectionCard}>
            <View style={styles.sectionHeader}>
              <Text style={styles.sectionTitle}>Recent Reports</Text>
              <TouchableOpacity>
                <Text style={styles.viewAll}>View All</Text>
              </TouchableOpacity>
            </View>
            {recentReports.map((report, index) => (
              <View key={index} style={styles.reportItem}>
                <View style={styles.reportIconWrap}>
                  <MaterialIcons
                    name={report.format === 'Excel' ? 'table-chart' : 'picture-as-pdf'}
                    size={24}
                    color={report.format === 'Excel' ? '#16a34a' : Colors.error}
                  />
                </View>
                <View style={styles.reportInfo}>
                  <Text style={styles.reportName}>{report.name}</Text>
                  <Text style={styles.reportMeta}>{report.date} • {report.size}</Text>
                </View>
                <View style={styles.reportActions}>
                  {report.status === 'ready' ? (
                    <TouchableOpacity style={styles.downloadBtn}>
                      <MaterialIcons name="download" size={20} color={Colors.primary} />
                    </TouchableOpacity>
                  ) : (
                    <View style={styles.generatingBadge}>
                      <MaterialIcons name="hourglass-top" size={14} color={Colors.secondary} />
                      <Text style={styles.generatingText}>Generating</Text>
                    </View>
                  )}
                </View>
              </View>
            ))}
          </View>

          {/* Custom Report Generator */}
          <View style={styles.customReportCard}>
            <View style={styles.customReportHeader}>
              <MaterialIcons name="auto-awesome" size={24} color={Colors.primary} />
              <Text style={styles.sectionTitle}>Custom Report</Text>
            </View>
            <Text style={styles.customReportDesc}>
              Generate a custom report by selecting date range, subjects, and format.
            </Text>
            <TouchableOpacity style={styles.generateButton} activeOpacity={0.8}>
              <MaterialIcons name="add-chart" size={20} color={Colors.onPrimary} />
              <Text style={styles.generateButtonText}>Create Custom Report</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
      <BottomNavBar items={bottomNavItems} activeItem="home" />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: Colors.background },
  content: { flex: 1 },
  contentInner: { padding: 16, paddingBottom: 80, gap: 16 },
  pageTitle: { ...Typography.headlineLgMobile, color: Colors.onBackground },
  pageSubtitle: { ...Typography.bodyMd, color: Colors.onSurfaceVariant, marginTop: 4 },
  sectionCard: {
    backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, padding: 16,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)', gap: 12,
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
  },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  sectionTitle: { ...Typography.headlineSm, color: Colors.onSurface },
  viewAll: { ...Typography.labelSm, color: Colors.primary },
  quickGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  quickItem: {
    width: '48%', backgroundColor: Colors.surfaceContainerLow, borderRadius: 12, padding: 16,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.2)', gap: 8,
  },
  quickIconWrap: {
    width: 44, height: 44, borderRadius: 12, backgroundColor: 'rgba(0,63,177,0.1)',
    alignItems: 'center', justifyContent: 'center',
  },
  quickLabel: { ...Typography.labelMd, color: Colors.onSurface, fontWeight: '600' },
  quickDesc: { ...Typography.bodyMd, color: Colors.onSurfaceVariant, fontSize: 12 },
  filterRow: { flexDirection: 'row', gap: 8, flexWrap: 'wrap' },
  filterChip: {
    flexDirection: 'row', alignItems: 'center', gap: 4,
    paddingHorizontal: 12, paddingVertical: 6, borderRadius: 9999,
    backgroundColor: Colors.surfaceContainerLow, borderWidth: 1, borderColor: Colors.outlineVariant,
  },
  filterChipActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  filterText: { ...Typography.labelSm, color: Colors.onSurfaceVariant },
  filterTextActive: { color: Colors.onPrimary },
  reportItem: {
    flexDirection: 'row', alignItems: 'center', gap: 12,
    paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: 'rgba(195,197,215,0.2)',
  },
  reportIconWrap: {
    width: 44, height: 44, borderRadius: 8, backgroundColor: Colors.surfaceContainerLow,
    alignItems: 'center', justifyContent: 'center',
  },
  reportInfo: { flex: 1 },
  reportName: { ...Typography.labelMd, color: Colors.onSurface },
  reportMeta: { ...Typography.bodyMd, color: Colors.onSurfaceVariant, fontSize: 12, marginTop: 2 },
  reportActions: {},
  downloadBtn: {
    width: 40, height: 40, borderRadius: 20, backgroundColor: Colors.surfaceContainerLow,
    alignItems: 'center', justifyContent: 'center',
  },
  generatingBadge: {
    flexDirection: 'row', alignItems: 'center', gap: 4,
    backgroundColor: Colors.surfaceContainerLow, paddingHorizontal: 8, paddingVertical: 4, borderRadius: 8,
  },
  generatingText: { ...Typography.labelSm, color: Colors.secondary, fontWeight: '400' },
  customReportCard: {
    backgroundColor: 'rgba(0,63,177,0.05)', borderRadius: 12, padding: 20,
    borderWidth: 1, borderColor: 'rgba(0,63,177,0.15)', gap: 12,
  },
  customReportHeader: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  customReportDesc: { ...Typography.bodyMd, color: Colors.onSurfaceVariant },
  generateButton: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8,
    backgroundColor: Colors.primary, paddingVertical: 12, borderRadius: 8,
  },
  generateButtonText: { ...Typography.labelMd, color: Colors.onPrimary },
});

export default ReportManagement;
