import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { StatusBar } from 'react-native';

import LoginPage from './screens/LoginPage';
import StudentLogin from './screens/StudentLogin';
import StaffLogin from './screens/StaffLogin';
import AdminLogin from './screens/AdminLogin';
import CommonPortal from './screens/CommonPortal';
import StudentDashboard from './screens/StudentDashboard';
import StaffDashboard from './screens/StaffDashboard';
import AdminDashboard from './screens/AdminDashboard';
import MarkAttendance from './screens/MarkAttendance';
import AttendanceReview from './screens/AttendanceReview';
import AttendanceHistory from './screens/AttendanceHistory';
import AdminProfile from './screens/AdminProfile';
import AdminEditProfile from './screens/AdminEditProfile';
import StaffProfile from './screens/StaffProfile';
import StaffEditProfile from './screens/StaffEditProfile';
import StudentProfile from './screens/StudentProfile';
import StudentEditProfile from './screens/StudentEditProfile';
import StudentAttendanceDetail from './screens/StudentAttendanceDetail';
import ReportManagement from './screens/ReportManagement';
import StudyMaterials from './screens/StudyMaterials';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <>
      <StatusBar barStyle="dark-content" backgroundColor="#faf8ff" />
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

          {/* Feature Screens */}
          <Stack.Screen name="MarkAttendance" component={MarkAttendance} />
          <Stack.Screen name="AttendanceReview" component={AttendanceReview} />
          <Stack.Screen name="AttendanceHistory" component={AttendanceHistory} />
          <Stack.Screen name="AdminProfile" component={AdminProfile} />
          <Stack.Screen name="AdminEditProfile" component={AdminEditProfile} />
          <Stack.Screen name="StaffProfile" component={StaffProfile} />
          <Stack.Screen name="StaffEditProfile" component={StaffEditProfile} />
          <Stack.Screen name="StudentProfile" component={StudentProfile} />
          <Stack.Screen name="StudentEditProfile" component={StudentEditProfile} />
          <Stack.Screen name="StudentAttendanceDetail" component={StudentAttendanceDetail} />
          <Stack.Screen name="StudyMaterials" component={StudyMaterials} />
          <Stack.Screen name="ReportManagement" component={ReportManagement} />
        </Stack.Navigator>
      </NavigationContainer>
    </>
  );
}
