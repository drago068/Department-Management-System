import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

const navTabs = [
  { key: 'home', label: 'Home', icon: 'grid-view', screen: 'StudentDashboard' },
  { key: 'attendance', label: 'Attendance', icon: 'how-to-reg', screen: 'StudentAttendanceDetail' },
  { key: 'materials', label: 'Materials', icon: 'menu-book', screen: 'StudyMaterials' },
  { key: 'profile', label: 'Profile', icon: 'person', screen: 'StudentProfile' },
];

const StudentBottomNav = ({ activeTab, navigation }) => {
  return (
    <View style={styles.bottomNavigation}>
      {navTabs.map((tab) => {
        const isActive = activeTab === tab.key;
        if (isActive) {
          return (
            <TouchableOpacity
              key={tab.key}
              activeOpacity={0.9}
              style={styles.activeNavItem}
              onPress={() => {
                if (tab.screen) navigation?.navigate(tab.screen);
              }}
            >
              <MaterialIcons name={tab.icon} size={20} color="#ffffff" />
              <Text style={styles.activeNavText}>{tab.label}</Text>
            </TouchableOpacity>
          );
        }

        return (
          <TouchableOpacity
            key={tab.key}
            activeOpacity={0.7}
            style={styles.navItem}
            onPress={() => {
              if (tab.screen) navigation?.navigate(tab.screen);
            }}
          >
            <MaterialIcons name={tab.icon} size={22} color="#64748b" />
            <Text style={styles.navText}>{tab.label}</Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  bottomNavigation: {
    position: 'absolute',
    left: 0,
    right: 0,
    bottom: 0,
    height: 64,
    backgroundColor: '#ffffff',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingHorizontal: 8,
    borderTopWidth: 1,
    borderTopColor: '#e2e8f0',
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
    width: 64,
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

export default StudentBottomNav;
