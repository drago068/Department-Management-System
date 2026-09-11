import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, Image, StyleSheet, SafeAreaView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';
import TopAppBar from '../components/TopAppBar';
import BottomNavBar from '../components/BottomNavBar';

const StaffDashboard = ({ navigation }) => {
  const bottomNavItems = [
    { key: 'home', label: 'Home', icon: 'dashboard' },
    { key: 'attendance', label: 'Attendance', icon: 'how-to-reg' },
    { key: 'notes', label: 'Notes & QP', icon: 'menu-book' },
    { key: 'profile', label: 'Profile', icon: 'person' },
  ];

  const statCards = [
    { label: 'MY CLASSES', value: '4', icon: 'class', iconBg: 'rgba(26, 86, 219, 0.1)', iconColor: Colors.primary },
    { label: "TODAY'S CLASSES", value: '2', icon: 'today', iconBg: 'rgba(26, 219, 103, 0.1)', iconColor: Colors.primary },
    { label: 'ATTENDANCE MARKED', value: '1', subValue: '/ 2', icon: 'fact-check', iconBg: 'rgba(19, 83, 216, 0.1)', iconColor: Colors.surfaceTint, progress: 50 },
    { label: 'SHORTAGE ALERTS', value: '5', icon: 'warning', iconBg: 'rgba(255, 218, 214, 0.3)', iconColor: Colors.error, isError: true },
  ];

  const upcomingClasses = [
    { time: '10:00', period: 'AM', name: 'CS-101: Data Structures', detail: 'B.Tech Semester 3 • Room 402', needsAction: true },
    { time: '08:30', period: 'AM', name: 'CS-305: Algorithms', detail: 'B.Tech Semester 5 • Room 301', completed: true },
  ];

  const recentHistory = [
    { name: 'CS-305: Algorithms', time: 'Today, 09:30 AM', present: '42/45' },
    { name: 'CS-101: Data Structures', time: 'Yesterday, 10:00 AM', present: '38/40' }, 
    { name: 'Lab: Python basics', time: 'Yesterday, 02:00 PM', present: '20/20' },
  ];

  return (
    <SafeAreaView style={styles.safeArea}>
      <TopAppBar
        title="Staff Dashboard"
        showBack
        onBackPress={() => navigation?.navigate('Login')}
        profileImage="https://lh3.googleusercontent.com/aida-public/AB6AXuBs_nuDOZI8b0LXnGPwlVMAVvPv3x7Wwy3GRF14ZCT3QycxHWwSYQml_IqpVh65vsu37hppsz3ERw9tfu6VbVPZebxushWkfgRx4hqCIRt3gulDmO8Ijm8_vybY_AtMzAcA7FHaH964F7nb7xXOOtvkylYcLFkKCKvc5tKwELHDOO-a8DxwkjkdN0KiI8Irb5sH52aXRTSKJDO0qB1QGvUKxwxxNhftj8DZ8aKoy1LhOopLEGncHwIM"
        onProfilePress={() => navigation?.navigate('StaffProfile')}
      />
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.contentInner}>
          {/* Stat Cards Grid */}
          <View style={styles.statGrid}>
            {statCards.map((card, index) => (
              <View key={index} style={styles.statCard}>
                <View style={styles.statCardHeader}>
                  <Text style={[styles.statLabel, card.isError && { color: Colors.error }]}>{card.label}</Text>
                  <View style={[styles.statIconWrap, { backgroundColor: card.iconBg }]}>
                    <MaterialIcons name={card.icon} size={20} color={card.iconColor} />
                  </View>
                </View>
                <View style={styles.statValueRow}>
                  <Text style={[styles.statValue, card.isError && { color: Colors.error }]}>{card.value}</Text>
                  {card.subValue && <Text style={styles.statSubValue}>{card.subValue}</Text>}
                </View>
                {card.progress !== undefined && (
                  <View style={styles.progressBarBg}>
                    <View style={[styles.progressBarFill, { width: `${card.progress}%` }]} />
                  </View>
                )}
              </View>
            ))}
          </View>

          {/* Upcoming Classes */}
          <View style={styles.sectionCard}>
            <View style={styles.sectionCardHeader}>
              <Text style={styles.sectionTitle}>Upcoming Classes</Text>
              <TouchableOpacity>
                <Text style={styles.viewLink}>View Schedule</Text>
              </TouchableOpacity>
            </View>
            <View style={styles.sectionCardBody}>
              {upcomingClasses.map((cls, index) => (
                <View key={index} style={[styles.classItem, cls.completed && { opacity: 0.7 }]}>
                  <View style={styles.classLeft}>
                    <View style={styles.timeBox}>
                      <Text style={styles.timeText}>{cls.time}</Text>
                      <Text style={styles.periodText}>{cls.period}</Text>
                    </View>
                    <View>
                      <Text style={styles.className}>{cls.name}</Text>
                      <Text style={styles.classDetail}>{cls.detail}</Text>
                    </View>
                  </View>
                  {cls.needsAction ? (
                    <TouchableOpacity
                      style={styles.markButton}
                      onPress={() => navigation.navigate('MarkAttendance')}
                      activeOpacity={0.8}
                    >
                      <MaterialIcons name="edit-document" size={16} color={Colors.onPrimary} />
                      <Text style={styles.markButtonText}>Mark Attendance</Text>
                    </TouchableOpacity>
                  ) : (
                    <View style={styles.markedBadge}>
                      <MaterialIcons name="check-circle" size={16} color={Colors.surfaceTint} />
                      <Text style={styles.markedText}>Marked</Text>
                    </View>
                  )}
                </View>
              ))}
            </View>
          </View>

          {/* Recent History */}
          <View style={styles.sectionCard}>
            <View style={styles.sectionCardHeader}>
              <Text style={styles.sectionTitle}>Recent History</Text>
            </View>
            {recentHistory.map((item, index) => (
              <View key={index} style={styles.historyItem}>
                <View>
                  <Text style={styles.historyName}>{item.name}</Text>
                  <Text style={styles.historyTime}>{item.time}</Text>
                </View>
                <View style={styles.historyRight}>
                  <Text style={styles.historyPresent}>{item.present}</Text>
                  <Text style={styles.historyLabel}>Present</Text>
                </View>
              </View>
            ))}
            <View style={styles.viewAllFooter}>
              <TouchableOpacity>
                <Text style={styles.viewLink}>View All History</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </ScrollView>

      <BottomNavBar
        items={bottomNavItems}
        activeItem="home"
        onItemPress={(item) => {
          if (item.key === 'home') navigation?.navigate('StaffDashboard');
          else if (item.key === 'attendance') navigation?.navigate('MarkAttendance');
          else if (item.key === 'notes') navigation?.navigate('StaffNotes');
          else if (item.key === 'profile') navigation?.navigate('StaffProfile');
        }}
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: Colors.background },
  content: { flex: 1 },
  contentInner: { padding: 16, paddingBottom: 80, gap: 16 },
  statGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  statCard: {
    width: '48%', backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12,
    padding: 16, borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)',
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
  },
  statCardHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  statLabel: { ...Typography.labelSm, color: Colors.onSurfaceVariant, letterSpacing: 1, flex: 1 },
  statIconWrap: { padding: 6, borderRadius: 8 },
  statValueRow: { flexDirection: 'row', alignItems: 'baseline', gap: 4, marginTop: 8 },
  statValue: { ...Typography.headlineLg, color: Colors.onSurface },
  statSubValue: { ...Typography.bodyMd, color: Colors.onSurfaceVariant },
  progressBarBg: { width: '100%', height: 6, backgroundColor: Colors.surfaceVariant, borderRadius: 3, marginTop: 8 },
  progressBarFill: { height: 6, borderRadius: 3, backgroundColor: Colors.primary },
  sectionCard: {
    backgroundColor: Colors.surfaceContainerLowest, borderRadius: 12,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)', overflow: 'hidden',
    shadowColor: '#000', shadowOffset: { width: 0, height: 1 }, shadowOpacity: 0.05, shadowRadius: 2, elevation: 1,
  },
  sectionCardHeader: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    padding: 16, borderBottomWidth: 1, borderBottomColor: 'rgba(195,197,215,0.3)',
    backgroundColor: 'rgba(250,248,255,0.5)',
  },
  sectionTitle: { ...Typography.headlineSm, color: Colors.onSurface },
  viewLink: { ...Typography.labelMd, color: Colors.primary },
  sectionCardBody: { padding: 16, gap: 12 },
  classItem: {
    flexDirection: 'column', padding: 16, borderRadius: 8,
    borderWidth: 1, borderColor: 'rgba(195,197,215,0.3)', backgroundColor: Colors.surfaceContainerLow, gap: 12,
  },
  classLeft: { flexDirection: 'row', alignItems: 'center', gap: 16 },
  timeBox: {
    backgroundColor: Colors.surfaceVariant, borderRadius: 8, padding: 12,
    alignItems: 'center', minWidth: 60,
  },
  timeText: { ...Typography.labelSm, color: Colors.onSurfaceVariant },
  periodText: { ...Typography.labelSm, color: Colors.onSurfaceVariant },
  className: { ...Typography.headlineSm, color: Colors.onSurface, fontSize: 16 },
  classDetail: { ...Typography.bodyMd, color: Colors.onSurfaceVariant },
  markButton: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8,
    backgroundColor: Colors.primary, paddingHorizontal: 24, paddingVertical: 10, borderRadius: 8, height: 40,
  },
  markButtonText: { ...Typography.labelMd, color: Colors.onPrimary },
  markedBadge: {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center', gap: 8,
    backgroundColor: 'rgba(19,83,216,0.1)', paddingHorizontal: 16, paddingVertical: 8, borderRadius: 8,
  },
  markedText: { ...Typography.labelMd, color: Colors.surfaceTint },
  historyItem: {
    flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center',
    padding: 16, borderBottomWidth: 1, borderBottomColor: 'rgba(195,197,215,0.3)',
  },
  historyName: { ...Typography.labelMd, color: Colors.onSurface },
  historyTime: { ...Typography.bodyMd, color: Colors.onSurfaceVariant, fontSize: 12, marginTop: 4 },
  historyRight: { alignItems: 'flex-end' },
  historyPresent: { ...Typography.labelMd, color: Colors.onSurface },
  historyLabel: { ...Typography.bodyMd, color: Colors.surfaceTint, fontSize: 12, marginTop: 4 },
  viewAllFooter: {
    padding: 12, borderTopWidth: 1, borderTopColor: 'rgba(195,197,215,0.3)',
    alignItems: 'center', backgroundColor: 'rgba(250,248,255,0.5)',
  },
});

export default StaffDashboard;
