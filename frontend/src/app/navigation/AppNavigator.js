import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

// Auth Module Screens
import {
  LoginPage,
  StudentLogin,
  StaffLogin,
  AdminLogin,
  CommonPortal,
} from '../../modules/auth';

// Student Module Screens
import {
  StudentDashboard,
  AttendanceHistory,
  StudentAttendanceDetail,
  StudentTimetable,
  StudyMaterials,
  StudentProfile,
  StudentEditProfile,
} from '../../modules/student';

// Staff Module Screens
import {
  StaffDashboard,
  MarkAttendance,
  AttendanceReview,
  StaffTimetable,
  StaffNotes,
  StaffProfile,
  StaffEditProfile,
} from '../../modules/staff';

// Admin Module Screens
import {
  AdminDashboard,
  ReportManagement,
  AdminTimetable,
  AdminStaffOnboardingScreen,
  MentorProctorAllocationScreen,
  EnrollStudent,
  EnrollmentSuccess,
  AdminProfile,
  AdminEditProfile,
} from '../../modules/admin';

const Stack = createNativeStackNavigator();

export function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator
        initialRouteName="Login"
        screenOptions={{
          headerShown: false,
          animation: 'slide_from_right',
          contentStyle: { backgroundColor: '#faf8ff' },
        }}
      >
        {/* Auth Screens */}
        <Stack.Screen name="Login" component={LoginPage} />
        <Stack.Screen name="StudentLogin" component={StudentLogin} />
        <Stack.Screen name="StaffLogin" component={StaffLogin} />
        <Stack.Screen name="AdminLogin" component={AdminLogin} />

        {/* Common Campus Hub */}
        <Stack.Screen name="CommonPortal" component={CommonPortal} />

        {/* Dashboard Screens */}
        <Stack.Screen name="StudentDashboard" component={StudentDashboard} />
        <Stack.Screen name="StaffDashboard" component={StaffDashboard} />
        <Stack.Screen name="AdminDashboard" component={AdminDashboard} />

        {/* Attendance Screens */}
        <Stack.Screen name="MarkAttendance" component={MarkAttendance} />
        <Stack.Screen name="AttendanceReview" component={AttendanceReview} />
        <Stack.Screen name="AttendanceHistory" component={AttendanceHistory} />
        <Stack.Screen name="StudentAttendanceDetail" component={StudentAttendanceDetail} />
        <Stack.Screen name="ReportManagement" component={ReportManagement} />

        {/* Timetable Screens */}
        <Stack.Screen name="StudentTimetable" component={StudentTimetable} />
        <Stack.Screen name="StaffTimetable" component={StaffTimetable} />
        <Stack.Screen name="AdminTimetable" component={AdminTimetable} />

        {/* Profile Screens */}
        <Stack.Screen name="StudentProfile" component={StudentProfile} />
        <Stack.Screen name="StudentEditProfile" component={StudentEditProfile} />
        <Stack.Screen name="StaffProfile" component={StaffProfile} />
        <Stack.Screen name="StaffEditProfile" component={StaffEditProfile} />
        <Stack.Screen name="AdminProfile" component={AdminProfile} />
        <Stack.Screen name="AdminEditProfile" component={AdminEditProfile} />

        {/* Materials Screens */}
        <Stack.Screen name="StudyMaterials" component={StudyMaterials} />
        <Stack.Screen name="StaffNotes" component={StaffNotes} />

        {/* Student Enrollment Screens */}
        <Stack.Screen name="EnrollStudent" component={EnrollStudent} />
        <Stack.Screen name="EnrollmentSuccess" component={EnrollmentSuccess} />

        {/* Faculty Management Screens */}
        <Stack.Screen name="AdminStaffOnboarding" component={AdminStaffOnboardingScreen} />
        <Stack.Screen name="AddStaff" component={AdminStaffOnboardingScreen} />
        <Stack.Screen name="MentorProctorAllocation" component={MentorProctorAllocationScreen} />
        <Stack.Screen name="AssignStudent" component={MentorProctorAllocationScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

export default AppNavigator;
