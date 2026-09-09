import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, Image, StyleSheet, SafeAreaView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';
import TopAppBar from '../components/TopAppBar';
import BottomNavBar from '../components/BottomNavBar';

const AdminDashboard = ({ navigation }) => {
  const bottomNavItems = [
    { key: 'home', label: 'Home', icon: 'dashboard' },
    { key: 'attendance', label: 'Attendance', icon: 'how-to-reg' },
    { key: 'history', label: 'History', icon: 'calendar-month' },
    { key: 'profile', label: 'Profile', icon: 'person' },
  ];

  const stats = [
    { label: 'Total Students', value: '1,200', icon: 'groups', color: Colors.primary, sub: '+2% from last semester' },
    { label: 'Total Staff', value: '45', icon: 'badge', color: Colors.tertiary, sub: 'Active faculty' },
    { label: "Today's Attendance", value: '94%', icon: 'analytics', color: Colors.primary, sub: '+1.5%', trending: true },
    { label: 'Below Req (75%)', value: '12', icon: 'warning', color: Colors.error, isAlert: true, link: 'Review Students →' },
  ];

  const activities = [
    { course: 'CS101 - Intro to Programming', instructor: 'Dr. Alan Turing', status: 'Submitted (38/40)', statusType: 'success', time: '10:05 AM' },
    { course: 'MA202 - Discrete Math', instructor: 'Prof. Ada Lovelace', status: 'Pending Review', statusType: 'warning', time: '09:45 AM' },
    { course: 'PH301 - Quantum Physics', instructor: 'Dr. Richard Feynman', status: 'Submitted (25/25)', statusType: 'success', time: '09:15 AM' },
  ];

  const quickActions = [
    { label: 'Add Student', icon: 'person-add', color: Colors.primary },
    { label: 'Add Staff', icon: 'badge', color: Colors.tertiary },
    { label: 'Assign Subjects', icon: 'library-books', color: Colors.secondary },
    { label: 'Generate Reports', icon: 'summarize', color: Colors.primary },
  ];

  const barData = [
    { label: 'Mon', height: 80 },
    { label: 'Tue', height: 85 },
    { label: 'Wed', height: 92 },
    { label: 'Thu', height: 90 },
    { label: 'Fri', height: 95 },
  ];

  const statusColor = (type) => {
    if (type === 'success') return { bg: '#dcfce7', text: '#166534' };
    if (type === 'warning') return { bg: '#fef08a', text: '#854d0e' };
    return { bg: Colors.surfaceContainer, text: Colors.onSurface };
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <TopAppBar
        title="Admin Portal"
        showBack
        onBackPress={() => navigation?.navigate('Login')}
        profileImage="https://lh3.googleusercontent.com/aida-public/AB6AXuD1t5z-_oQFWEaabU_WJXKo_VqO91Cj1cerTlzKrkGfjfKSqcYLxb4osCTXeFfFjZjt_RwN3XSs7E1IjqHQ43_S6DeISPQpGZI_lcQ6DCjefn5fA5c6dauILyxqbS3i7H0BtINyQEDLxsbF_xi4onTPB9L_t93ppw-qwRTYb9mtB6ZZQgC6rfLajdkVnLkA96olIVw7dGBlx7YQ2Lb8Yr0yoJg7mPl5YPriyQ0Eed4zO8R7r8JS1wHO"
        onProfilePress={() => navigation?.navigate('AdminProfile')}
      />
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.contentInner}>
          {/* Header */}
          <View>
            <Text style={styles.pageTitle}>Overview</Text>
            <Text style={styles.pageSubtitle}>Real-time attendance metrics across all departments.</Text>
          </View>

          {/* Stat Cards */}
          <View style={styles.statGrid}>
            {stats.map((stat, index) => (
              <View key={index} style={[styles.statCard, stat.isAlert && styles.alertCard]}>
                <View style={styles.statHeader}>
                  <Text style={[styles.statLabel, stat.isAlert && { color: Colors.error }]}>{stat.label}</Text>
                  <MaterialIcons name={stat.icon} size={24} color={stat.color} />
                </View>
                <Text style={[styles.statValue, stat.isAlert && { color: Colors.error }]}>{stat.value}</Text>
                {stat.trending ? (
                  <View style={styles.trendBadge}>
                    <MaterialIcons name="trending-up" size={14} color="#166534" />
                    <Text style={styles.trendText}>{stat.sub}</Text>
                  </View>
                ) : stat.link ? (
                  <TouchableOpacity>
                    <Text style={styles.linkText}>{stat.link}</Text>
                  </TouchableOpacity>
                ) : (
                  <Text style={styles.statSub}>{stat.sub}</Text>
                )}
              </View>
            ))}
          </View>

          {/* Weekly Attendance Trend */}
          <View style={styles.chartCard}>
            <View style={styles.chartHeader}>
              <Text style={styles.sectionTitle}>Weekly Attendance Trend</Text>
              <TouchableOpacity>
                <MaterialIcons name="more-vert" size={24} color={Colors.secondary} />
              </TouchableOpacity>
            </View>
            <View style={styles.barChart}>
              {barData.map((bar, index) => (
                <View key={index} style={styles.barColumn}>
                  <View style={[styles.bar, { height: `${bar.height}%` }]}>
                    <Text style={styles.barTooltip}>{bar.height}%</Text>
                  </View>
                  <Text style={styles.barLabel}>{bar.label}</Text>
                </View>
              ))}
            </View>
          </View>

          {/* Recent Activity Table */}
          <View style={styles.tableCard}>
            <View style={styles.tableHeader}>
              <Text style={styles.sectionTitle}>Recent Activity</Text>
              <TouchableOpacity>
                <Text style={styles.viewLink}>View All</Text>
              </TouchableOpacity>
            </View>
            {/* Table Header Row */}
            <View style={styles.tableRow}>
              <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Course / Section</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1.5 }]}>Instructor</Text>
              <Text style={[styles.tableHeaderCell, { flex: 1.5 }]}>Status</Text>
              <Text style={[styles.tableHeaderCell, { flex: 0.8, textAlign: 'right' }]}>Time</Text>
            </View>
            {activities.map((act, index) => {
              const sc = statusColor(act.statusType);
              return (
                <View key={index} style={styles.tableRow}>
                  <Text style={[styles.tableCell, { flex: 2 }]}>{act.course}</Text>
                  <Text style={[styles.tableCell, { flex: 1.5, color: Colors.onSurfaceVariant }]}>{act.instructor}</Text>
                  <View style={{ flex: 1.5 }}>
                    <View style={[styles.statusBadge, { backgroundColor: sc.bg }]}>
                      <Text style={[styles.statusText, { color: sc.text }]}>{act.status}</Text>
                    </View>
                  </View>
                  <Text style={[styles.tableCell, { flex: 0.8, textAlign: 'right', color: Colors.secondary, fontSize: 12 }]}>{act.time}</Text>
                </View>
              );
            })}
          </View>

          {/* Quick Actions */}
          <View style={styles.quickActionsCard}>
            <Text style={styles.sectionTitle}>Quick Actions</Text>
            <View style={styles.quickActionsGrid}>
              {quickActions.map((action, index) => (
                <TouchableOpacity
                  key={index}
                  style={styles.quickActionItem}
                  activeOpacity={0.7}
                  onPress={() => {
                    if (action.label === 'Generate Reports') navigation?.navigate('ReportManagement');
                    else if (action.label === 'Assign Subjects' || action.label === 'Add Student') navigation?.navigate('ReportManagement');
                  }}
                >
                  <MaterialIcons name={action.icon} size={24} color={action.color} />
                  <Text style={styles.quickActionText}>{action.label}</Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          {/* System Status */}
          <View style={styles.systemStatusCard}>
            <Text style={styles.sectionTitle}>System Status</Text>
            <View style={styles.statusRow}>
              <View style={styles.statusDot}>
                <View style={styles.statusDotInner} />
              </View>
              <Text style={styles.statusLabelText}>All services operational</Text>
            </View>
            <Text style={styles.lastSync}>Last sync: 2 mins ago</Text>
          </View>
        </View>
      </ScrollView>

      <BottomNavBar
        items={bottomNavItems}
        activeItem="home"
        onItemPress={(item) => {
          if (item.key === 'home') navigation?.navigate('AdminDashboard');
          else if (item.key === 'attendance' || item.key === 'reports') navigation?.navigate('ReportManagement');
          else if (item.key === 'history') navigation?.navigate('AttendanceHistory');
          else if (item.key === 'profile') navigation?.navigate('AdminProfile');
        }}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: Colors.background },
  content: { flex: 1 },
  contentInner: { padding: 16, paddingBottom: 80, gap: 16 },
  pageTitle: { ...Typography.headlineLgMobile, color: Colors.onBackground, marginBottom: 4 },
  pageSubtitle: { ...Typography.bodyMd, color: Colors.onSurfaceVariant },
  statGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  statCard: {
    width: '48%', backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12,
    padding: 16, borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)', gap: 8,
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
  },
  alertCard: { backgroundColor: 'rgba(255,218,214,0.2)', borderColor: Colors.errorContainer },
  statHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  statLabel: { ...Typography.labelMd, color: Colors.onSurfaceVariant },
  statValue: { ...Typography.headlineLgMobile, color: Colors.onSurface },
  statSub: { ...Typography.labelSm, color: Colors.secondary },
  trendBadge: {
    flexDirection: 'row', alignItems: 'center', gap: 4,
    backgroundColor: 'rgba(187,247,208,0.3)', paddingHorizontal: 8, paddingVertical: 2, borderRadius: 9999, alignSelf: 'flex-start',
  },
  trendText: { ...Typography.labelSm, color: '#166534' },
  linkText: { ...Typography.labelSm, color: Colors.primary },
  chartCard: {
    backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, padding: 16,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)',
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
  },
  chartHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
  sectionTitle: { ...Typography.headlineSm, color: Colors.onSurface },
  barChart: {
    height: 180, flexDirection: 'row', alignItems: 'flex-end', justifyContent: 'space-between',
    backgroundColor: Colors.surfaceContainerLow, borderRadius: 8, padding: 8, gap: 8,
  },
  barColumn: { flex: 1, alignItems: 'center', height: '100%', justifyContent: 'flex-end' },
  bar: { width: '80%', backgroundColor: Colors.primary, borderTopLeftRadius: 4, borderTopRightRadius: 4, minHeight: 10, justifyContent: 'flex-start', alignItems: 'center' },
  barTooltip: { ...Typography.labelSm, color: Colors.onPrimary, fontSize: 10, marginTop: 4 },
  barLabel: { ...Typography.labelSm, color: Colors.secondary, marginTop: 4 },
  tableCard: {
    backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, overflow: 'hidden',
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)',
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
  },
  tableHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 16 },
  viewLink: { ...Typography.labelSm, color: Colors.primary },
  tableRow: {
    flexDirection: 'row', alignItems: 'center', paddingHorizontal: 16, paddingVertical: 12,
    borderBottomWidth: 1, borderBottomColor: 'rgba(195,197,215,0.2)',
  },
  tableHeaderCell: { ...Typography.labelSm, color: Colors.secondary },
  tableCell: { ...Typography.bodyMd, color: Colors.onSurface },
  statusBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 9999, alignSelf: 'flex-start' },
  statusText: { fontSize: 12, fontWeight: '500' },
  quickActionsCard: {
    backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12, padding: 16,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)',
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
  },
  quickActionsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12, marginTop: 16 },
  quickActionItem: {
    width: '47%', alignItems: 'center', justifyContent: 'center', gap: 8,
    padding: 16, borderRadius: 8, backgroundColor: Colors.surfaceContainerLow,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.2)',
  },
  quickActionText: { ...Typography.labelSm, color: Colors.onSurface, textAlign: 'center' },
  systemStatusCard: {
    backgroundColor: 'rgba(0,63,177,0.05)', borderRadius: 12, padding: 16,
    borderWidth: 1, borderColor: 'rgba(0,63,177,0.2)',
  },
  statusRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 8 },
  statusDot: {
    width: 12, height: 12, borderRadius: 6, backgroundColor: 'rgba(74,222,128,0.3)',
    alignItems: 'center', justifyContent: 'center',
  },
  statusDotInner: { width: 8, height: 8, borderRadius: 4, backgroundColor: '#22c55e' },
  statusLabelText: { ...Typography.labelMd, color: Colors.onSurfaceVariant },
  lastSync: { ...Typography.bodyMd, color: Colors.secondary, fontSize: 12, marginTop: 12 },
});

export default AdminDashboard;
