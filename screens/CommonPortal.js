import React, { useState } from "react";
import {
  SafeAreaView,
  StatusBar,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  Image,
  ScrollView,
  StyleSheet,
  Linking,
  Alert,
} from "react-native";
import { BlurView } from "expo-blur";
import { MaterialIcons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";

export default function CommonPortal({ route, navigation }) {
  const role = route?.params?.role || "student"; // 'student' | 'staff' | 'admin'
  const [searchQuery, setSearchQuery] = useState("");

  const campusServices = [
    {
      title: "Circulars & Official Notices",
      subtitle: "Office of Dean & Controller of Exams",
      icon: "notifications-active",
      type: "circulars",
      new: true,
    },
    {
      title: "Master Timetables",
      subtitle: "Lectures, Lab sessions & Exam Slots",
      icon: "calendar-month",
      type: "timetable",
    },
    {
      title: "Academic Calendar",
      subtitle: "Working days, internal tests & holidays",
      icon: "date-range",
      type: "calendar",
    },
    {
      title: "Q-Fix Redressal System",
      subtitle: "Lab machines, campus Wi-Fi, hostel & infra",
      icon: "support-agent",
      type: "qfix",
    },
  ];

  const filteredServices = campusServices.filter((item) => {
    const query = searchQuery.toLowerCase();

    if (!query) return true;

    return (
      item.title.toLowerCase().includes(query) ||
      item.subtitle.toLowerCase().includes(query)
    );
  });

  const handleNotification = () => {
    Alert.alert("Notifications", "You have no unread circulars.");
  };

  const handleFilter = () => {
    Alert.alert("Filter", "Filter resources by category");
  };

  const handleRaiseTicket = () => {
    Alert.alert("Q-Fix", "Ticket creation portal opened.");
  };

  const handleTrackTicket = () => {
    Alert.alert("Q-Fix", "You have 0 open tickets.");
  };

  const handleDownloadCalendar = () => {
    Alert.alert("Academic Calendar", "Downloading Academic Calendar (PDF)...");
  };

  const openWebsite = () => {
    Linking.openURL("https://suguna.ac.in");
  };

  const callHelpdesk = () => {
    Linking.openURL("tel:+914222629393");
  };

  const emailDean = () => {
    Linking.openURL("mailto:info@suguna.ac.in");
  };

  const navigateToDashboard = () => {
    if (role === "admin") {
      navigation?.navigate("AdminDashboard");
    } else if (role === "staff") {
      navigation?.navigate("StaffDashboard");
    } else {
      navigation?.navigate("StudentDashboard");
    }
  };

  const navigateToAttendance = () => {
    if (role === "admin") {
      navigation?.navigate("AttendanceReview");
    } else if (role === "staff") {
      navigation?.navigate("MarkAttendance");
    } else {
      navigation?.navigate("StudentAttendanceDetail");
    }
  };

  const navigateToReports = () => {
    if (role === "admin") {
      navigation?.navigate("ReportManagement");
    } else if (role === "staff") {
      navigation?.navigate("AttendanceHistory");
    } else {
      navigation?.navigate("AttendanceHistory");
    }
  };

  const navigateToProfile = () => {
    if (role === "admin") {
      navigation?.navigate("AdminProfile");
    } else if (role === "staff") {
      navigation?.navigate("StaffProfile");
    } else {
      navigation?.navigate("StudentProfile");
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar
        barStyle="dark-content"
        backgroundColor="#faf8ff"
      />

      <View style={styles.container}>

        {/* =====================================================
            HEADER
        ===================================================== */}

        <BlurView
          intensity={85}
          tint="light"
          style={styles.header}
        >
          <View style={styles.headerInner}>

            <View style={styles.brandContainer}>

              <Image
                alt="NEXUS Crest"
                source={{
                  uri: "https://lh3.googleusercontent.com/aida/AEtjO1Wvn-7DlspBmymBZsPXM5ofH-gwObYUZX7235q1CvfulTuqnJHFo7-dKK9FtRU_nF9bJmgVlSl3vIe_BLaa3RBjW9icQRFjWupeEupGTt0BOl5iIocHT6vlnlyxA4S2OwCvcTdTEwhoTDbAzsOpRo5PqdfOvY89KN0Ri2ZllbuoLjY-RwWFBXSYB1pBPQBVoQDDG3Q2XjZXSSNyxh92nncG92zKb44jRGkR1tHS9neOiyzZGqYdhtgy71qS3NQuFQJrzqFr3ErYDA",
                }}
                style={styles.crest}
              />

              <View>
                <Text style={styles.nexusText}>
                  NEXUS
                </Text>
              </View>

            </View>

            <View style={styles.headerRightSection}>
              {/* Role badge */}
              <TouchableOpacity
                style={styles.roleBadgeBtn}
                onPress={navigateToDashboard}
                activeOpacity={0.8}
              >
                <MaterialIcons name="dashboard" size={14} color="#003fb1" />
                <Text style={styles.roleBadgeText}>
                  {role === "admin" ? "Admin Portal" : role === "staff" ? "Staff Portal" : "Student Portal"}
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={styles.notificationButton}
                onPress={handleNotification}
                accessibilityLabel="Notifications"
              >
                <MaterialIcons
                  name="notifications"
                  size={24}
                  color="#434654"
                />

                <View style={styles.notificationDot} />
              </TouchableOpacity>
            </View>

          </View>
        </BlurView>


        {/* =====================================================
            MAIN CONTENT
        ===================================================== */}

        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.scrollContent}
          showsVerticalScrollIndicator={false}
        >

          {/* =====================================================
              WELCOME & COLLEGE AFFILIATION
          ===================================================== */}

          <View style={styles.welcomeSection}>

            <View style={styles.welcomeHeader}>

              <View style={styles.collegeContainer}>

                <Image
                  alt="Suguna College of Engineering Emblem"
                  source={{
                    uri: "https://lh3.googleusercontent.com/aida-public/AB6AXuC7zG2t2KFJ1gjxqmVn0-VAIQRgInbAr69Di_NDohbN-gOashwTpBLKhoE-3mGMcGAq0jaZ1woshfFY1-fClci3c-PrLXh4MyH0_8gyyLxBK4f5vJnWCQiVSOF_4IU05k_pAp1PTotEAg6DFsxun5dxTJ_BaLDZezUsBS9ANQJ3UX2vLxAe7ZmXlNgGB7ruJatATtJX65OjVw_EJPTsyM9DLXwMYTNIDty-sequO2uQjeymRNyifQ4lOXV1d3vNvjBP-g",
                  }}
                  style={styles.collegeEmblem}
                />

                <View>
                  <Text style={styles.collegeName}>
                    Suguna College of Engg.
                  </Text>
                </View>

              </View>

              <View style={styles.officialHub}>

                <MaterialIcons
                  name="verified"
                  size={16}
                  color="#003fb1"
                />

                <Text style={styles.officialHubText}>
                  Official Hub
                </Text>

              </View>

            </View>


            {/* =====================================================
                SEARCH
            ===================================================== */}

            <View style={styles.searchContainer}>

              <MaterialIcons
                name="search"
                size={20}
                color="#737686"
                style={styles.searchIcon}
              />

              <TextInput
                value={searchQuery}
                onChangeText={setSearchQuery}
                placeholder="Search circulars, timetables, Q-Fix..."
                placeholderTextColor="#737686"
                style={styles.searchInput}
              />

              <TouchableOpacity
                style={styles.filterButton}
                onPress={handleFilter}
                accessibilityLabel="Filter resources"
              >
                <MaterialIcons
                  name="tune"
                  size={18}
                  color="#434654"
                />
              </TouchableOpacity>

            </View>

          </View>


          {/* =====================================================
              REAL-TIME ALERTS
          ===================================================== */}

          <View style={styles.alertSection} />


          {/* =====================================================
              CAMPUS SERVICES
          ===================================================== */}

          <View style={styles.servicesSection}>

            <View style={styles.sectionHeadingRow}>

              <View style={styles.sectionHeadingLeft}>

                <MaterialIcons
                  name="grid-view"
                  size={20}
                  color="#003fb1"
                />

                <Text style={styles.sectionHeading}>
                  Campus Services
                </Text>

              </View>

              <Text style={styles.modulesText}>
                7 Modules Active
              </Text>

            </View>


            {/* =====================================================
                1. CIRCULARS & OFFICIAL NOTICES
            ===================================================== */}

            {(!searchQuery ||
              filteredServices.some(
                (item) => item.type === "circulars"
              )) && (
              <View style={styles.serviceCard}>

                <View style={styles.serviceTopRow}>

                  <View style={styles.serviceInfoRow}>

                    <View style={styles.primaryIconBox}>
                      <MaterialIcons
                        name="notifications-active"
                        size={24}
                        color="#003fb1"
                      />
                    </View>

                    <View style={styles.serviceTextContainer}>

                      <Text
                        style={styles.serviceTitle}
                        numberOfLines={1}
                      >
                        Circulars & Official Notices
                      </Text>

                      <Text
                        style={styles.serviceSubtitle}
                        numberOfLines={1}
                      >
                        Office of Dean & Controller of Exams
                      </Text>

                    </View>

                  </View>

                  <View style={styles.newBadge}>
                    <Text style={styles.newBadgeText}>
                      New
                    </Text>
                  </View>

                </View>

              </View>
            )}


            {/* =====================================================
                2. TIMETABLE HUB
            ===================================================== */}

            {(!searchQuery ||
              filteredServices.some(
                (item) => item.type === "timetable"
              )) && (
              <View style={styles.serviceCard}>

                <View style={styles.serviceTopRow}>

                  <View style={styles.serviceInfoRow}>

                    <View style={styles.secondaryIconBox}>
                      <MaterialIcons
                        name="calendar-month"
                        size={24}
                        color="#151c27"
                      />
                    </View>

                    <View style={styles.serviceTextContainer}>

                      <Text
                        style={styles.serviceTitle}
                        numberOfLines={1}
                      >
                        Master Timetables
                      </Text>

                      <Text
                        style={styles.serviceSubtitle}
                        numberOfLines={1}
                      >
                        Lectures, Lab sessions & Exam Slots
                      </Text>

                    </View>

                  </View>

                  <MaterialIcons
                    name="chevron-right"
                    size={24}
                    color="#737686"
                  />

                </View>


                {/* Semester Chips */}

                <ScrollView
                  horizontal
                  showsHorizontalScrollIndicator={false}
                  contentContainerStyle={styles.semesterChips}
                >

                  <TouchableOpacity
                    style={styles.currentSemesterChip}
                  >
                    <Text style={styles.currentSemesterText}>
                      Sem VI (Current)
                    </Text>
                  </TouchableOpacity>

                  <TouchableOpacity
                    style={styles.labScheduleChip}
                  >
                    <Text style={styles.labScheduleText}>
                      Lab Schedule
                    </Text>
                  </TouchableOpacity>

                </ScrollView>

              </View>
            )}


            {/* =====================================================
                3. ACADEMIC CALENDAR
            ===================================================== */}

            {(!searchQuery ||
              filteredServices.some(
                (item) => item.type === "calendar"
              )) && (
              <View style={styles.serviceCard}>

                <View style={styles.calendarRow}>

                  <View style={styles.serviceInfoRow}>

                    <View style={styles.tertiaryIconBox}>
                      <MaterialIcons
                        name="date-range"
                        size={24}
                        color="#852b00"
                      />
                    </View>

                    <View style={styles.serviceTextContainer}>

                      <View style={styles.calendarTitleRow}>

                        <Text
                          style={styles.serviceTitle}
                          numberOfLines={1}
                        >
                          Academic Calendar
                        </Text>

                        <View style={styles.yearBadge}>
                          <Text style={styles.yearBadgeText}>
                            2023-24
                          </Text>
                        </View>

                      </View>

                      <Text
                        style={styles.serviceSubtitle}
                        numberOfLines={1}
                      >
                        Working days, internal tests & holidays
                      </Text>

                    </View>

                  </View>

                  <TouchableOpacity
                    style={styles.downloadButton}
                    onPress={handleDownloadCalendar}
                    accessibilityLabel="Download Academic Calendar"
                  >
                    <MaterialIcons
                      name="file-download"
                      size={20}
                      color="#003fb1"
                    />
                  </TouchableOpacity>

                </View>

              </View>
            )}


            {/* =====================================================
                4. Q-FIX
            ===================================================== */}

            {(!searchQuery ||
              filteredServices.some(
                (item) => item.type === "qfix"
              )) && (
              <View style={styles.qfixCard}>

                <View style={styles.qfixHeader}>

                  <View style={styles.serviceInfoRow}>

                    <View style={styles.qfixLogoBox}>

                      <Image
                        source={{
                          uri: "https://lh3.googleusercontent.com/aida-public/AB6AXuBa6V8nS6cVHINLLk2PMToz3m6vvuzmKVCeJoOh7ISXrOhW-QUHrAVzTHuSDVCD6VKkA5z0oJJyhv87p9YK3KOT549O5P023BLsZGe8IXCGK0zymYOkNPt8oul-v_CW_WxwLrpz9seqwKm8OqAicGeoSb3vqMc1Oxgvvoe4KZndkook0s1XjSBe-dlnTrb83ENvMuBJc8-KVJhDnaOwrjGdUNgCH556mtwZK5nGGtSm0GW72lZDPK42QjJRab2mK1O9TA",
                        }}
                        style={styles.qfixLogo}
                      />

                    </View>

                    <View style={styles.serviceTextContainer}>

                      <View style={styles.qfixTitleRow}>

                        <Text
                          style={styles.serviceTitle}
                          numberOfLines={1}
                        >
                          Q-Fix Redressal System
                        </Text>

                        <View style={styles.activeBadge}>
                          <Text style={styles.activeBadgeText}>
                            ACTIVE
                          </Text>
                        </View>

                      </View>

                      <Text
                        style={styles.serviceSubtitle}
                        numberOfLines={1}
                      >
                        Lab machines, campus Wi-Fi, hostel & infra
                      </Text>

                    </View>

                  </View>

                </View>


                {/* Q-Fix Buttons */}

                <View style={styles.qfixButtons}>

                  <TouchableOpacity
                    style={styles.raiseTicketButton}
                    onPress={handleRaiseTicket}
                  >

                    <MaterialIcons
                      name="add-task"
                      size={18}
                      color="#ffffff"
                    />

                    <Text style={styles.raiseTicketText}>
                      Raise Ticket
                    </Text>

                  </TouchableOpacity>

                  <TouchableOpacity
                    style={styles.trackButton}
                    onPress={handleTrackTicket}
                  >

                    <MaterialIcons
                      name="pending-actions"
                      size={18}
                      color="#191b23"
                    />

                    <Text style={styles.trackText}>
                      Track (0 Open)
                    </Text>

                  </TouchableOpacity>

                </View>

              </View>
            )}


            {/* =====================================================
                6. WEB PORTAL
            ===================================================== */}

            <View style={styles.webPortalGrid}>

              <TouchableOpacity
                style={styles.webPortalCard}
                onPress={openWebsite}
              >

                <View style={styles.webPortalTop}>

                  <View style={styles.webIconBox}>

                    <MaterialIcons
                      name="language"
                      size={20}
                      color="#003fb1"
                    />

                  </View>

                  <MaterialIcons
                    name="open-in-new"
                    size={16}
                    color="#737686"
                  />

                </View>

                <View>

                  <Text style={styles.webPortalTitle}>
                    Web Portal
                  </Text>

                  <Text style={styles.webPortalUrl}>
                    suguna.ac.in
                  </Text>

                </View>

              </TouchableOpacity>

            </View>

          </View>


          {/* =====================================================
              CAMPUS FACILITIES
          ===================================================== */}

          <View style={styles.facilitiesSection}>

            <View style={styles.facilitiesHeadingRow}>

              <View style={styles.sectionHeadingLeft}>

                <MaterialIcons
                  name="photo-library"
                  size={20}
                  color="#003fb1"
                />

                <Text style={styles.sectionHeading}>
                  Campus Facilities
                </Text>

              </View>

              <Text style={styles.campusLocation}>
                Kalapatti Campus
              </Text>

            </View>


            {/* Photos */}

            <View style={styles.photoGrid}>

              {/* Engineering Wing */}

              <View style={styles.photoColumn}>

                <View style={styles.photoContainer}>

                  <Image
                    alt="Suguna College Engineering Wing"
                    source={{
                      uri: "https://lh3.googleusercontent.com/aida-public/AB6AXuDxGYcTcULfLOwH--oAEVr8ATG7IDKZIEYFyONK7qXbcaaPdifbVlVP2hnIGeOc2cRURNzi13T0XLfn3qa2Pp_CVmkrKaCTmc82qUetngfHK3xOuaOgNLhm9vmtuY8mv-rEUpDnC38bJvgrk6ZvASBblG_BxfvA03fhKM9qseKColgKo3_ueetrN0d-LgO4hgaOg8ZdUkDF90Q26D8xBEcShKJFtq2TABCuCVxkYdH4YlbvTYZWPR4TKL2WuQkpfPK0ZA",
                    }}
                    style={styles.facilityImage}
                  />

                  <View style={styles.photoLabel}>
                    <Text style={styles.photoLabelText}>
                      Tech Hub
                    </Text>
                  </View>

                </View>

                <Text style={styles.facilityTitle}>
                  Advanced Robotics Lab
                </Text>

              </View>


              {/* Library */}

              <View style={styles.photoColumn}>

                <View style={styles.photoContainer}>

                  <Image
                    source={{
                      uri: "https://lh3.googleusercontent.com/aida-public/AB6AXuDiyMqJfwgoKIrjOg7TVjEkCFk3cwjmUklfzATLBI-4xGcgtXVzQqZvwf8rWJwQHXGHxXuhgz7g3Bt8pdwurMYmIh2VKmR6HSjWP8gHBolsZsBtpyJuJ_5gNj_WHKcbVuco__dTmNXHGwyAcSZ0fPob0V0dI19osdzUZ6d7uK4ws_-La0ghNCzuwdTORlNGjwOsbA8kdQwKTgIOaXXVELzMuGJ08T2GKQ4dkF9Nva4hbL0AMclFxuqW",
                    }}
                    style={styles.facilityImage}
                  />

                  <View style={styles.photoLabel}>
                    <Text style={styles.photoLabelText}>
                      Central Library
                    </Text>
                  </View>

                </View>

                <Text style={styles.facilityTitle}>
                  Digital Knowledge Center
                </Text>

              </View>

            </View>

          </View>


          {/* =====================================================
              UPCOMING MILESTONES
          ===================================================== */}

          <View style={styles.milestonesSection}>

            <View style={styles.milestonesCard}>

              <View style={styles.milestonesHeader}>

                <View style={styles.sectionHeadingLeft}>

                  <MaterialIcons
                    name="event-upcoming"
                    size={20}
                    color="#003fb1"
                  />

                  <Text style={styles.sectionHeading}>
                    Upcoming Milestones
                  </Text>

                </View>

                <Text style={styles.milestoneDate}>
                  Apr – May 2024
                </Text>

              </View>


              <View style={styles.milestoneList}>

                {/* April 22 */}

                <View style={styles.milestoneItem}>

                  <View style={styles.dateBox}>

                    <Text style={styles.aprilText}>
                      Apr
                    </Text>

                    <Text style={styles.dateNumber}>
                      22
                    </Text>

                  </View>

                  <View style={styles.milestoneTextContainer}>

                    <Text
                      style={styles.milestoneTitle}
                      numberOfLines={1}
                    >
                      Model Practical Examinations
                    </Text>

                    <Text
                      style={styles.milestoneSubtitle}
                      numberOfLines={1}
                    >
                      All B.E./B.Tech VI & VIII Semester
                    </Text>

                  </View>

                  <View style={styles.internalBadge}>

                    <Text style={styles.internalBadgeText}>
                      Internal
                    </Text>

                  </View>

                </View>


                {/* May 06 */}

                <View style={styles.milestoneItem}>

                  <View style={styles.dateBox}>

                    <Text style={styles.mayText}>
                      May
                    </Text>

                    <Text style={styles.dateNumber}>
                      06
                    </Text>

                  </View>

                  <View style={styles.milestoneTextContainer}>

                    <Text
                      style={styles.milestoneTitle}
                      numberOfLines={1}
                    >
                      Commencement of Theory Exams
                    </Text>

                    <Text
                      style={styles.milestoneSubtitle}
                      numberOfLines={1}
                    >
                      Autonomous End-Semester Assessments
                    </Text>

                  </View>

                  <View style={styles.finalsBadge}>

                    <Text style={styles.finalsBadgeText}>
                      Finals
                    </Text>

                  </View>

                </View>

              </View>

            </View>

          </View>


          {/* =====================================================
              HELP DESK
          ===================================================== */}

          <View style={styles.helpdeskSection}>

            <View style={styles.helpdeskCard}>

              <View style={styles.helpdeskHeader}>

                <View style={styles.supportIcon}>

                  <MaterialIcons
                    name="support-agent"
                    size={20}
                    color="#ffffff"
                  />

                </View>

                <View style={styles.helpdeskTextContainer}>

                  <Text style={styles.helpdeskTitle}>
                    Campus Helpdesk & Support
                  </Text>

                  <Text style={styles.helpdeskAddress}>
                    Suguna College of Engineering, Kalapatti Road, Coimbatore
                  </Text>

                </View>

              </View>


              {/* Helpdesk Buttons */}

              <View style={styles.helpdeskButtons}>

                <TouchableOpacity
                  style={styles.helpdeskButton}
                  onPress={callHelpdesk}
                >

                  <MaterialIcons
                    name="call"
                    size={16}
                    color="#003fb1"
                  />

                  <Text style={styles.helpdeskButtonText}>
                    +91 422 2629393
                  </Text>

                </TouchableOpacity>

                <TouchableOpacity
                  style={styles.helpdeskButton}
                  onPress={emailDean}
                >

                  <MaterialIcons
                    name="mail"
                    size={16}
                    color="#003fb1"
                  />

                  <Text style={styles.helpdeskButtonText}>
                    Email Dean
                  </Text>

                </TouchableOpacity>

              </View>

            </View>

          </View>


          {/* Bottom Scroll Padding */}

          <View style={{ height: 80 }} />

        </ScrollView>


        {/* =====================================================
            BOTTOM NAVIGATION
        ===================================================== */}

        <BlurView
          intensity={90}
          tint="light"
          style={styles.bottomNavigation}
        >

          <View style={styles.bottomNavInner}>

            {/* HOME */}

            <TouchableOpacity
              style={styles.navItem}
              onPress={() => {}}
            >

              <MaterialIcons
                name="home"
                size={24}
                color="#1a56db"
              />

              <Text style={styles.activeNavText}>
                Hub
              </Text>

            </TouchableOpacity>


            {/* DASHBOARD */}

            <TouchableOpacity
              style={styles.navItem}
              onPress={navigateToDashboard}
            >

              <MaterialIcons
                name="dashboard"
                size={24}
                color="#434654"
              />

              <Text style={styles.navText}>
                Dashboard
              </Text>

            </TouchableOpacity>


            {/* ATTENDANCE */}

            <TouchableOpacity
              style={styles.navItem}
              onPress={navigateToAttendance}
            >

              <MaterialIcons
                name="how-to-reg"
                size={24}
                color="#434654"
              />

              <Text style={styles.navText}>
                Attendance
              </Text>

            </TouchableOpacity>


            {/* PROFILE */}

            <TouchableOpacity
              style={styles.navItem}
              onPress={navigateToProfile}
            >

              <MaterialIcons
                name="person"
                size={24}
                color="#434654"
              />

              <Text style={styles.navText}>
                Profile
              </Text>

            </TouchableOpacity>

          </View>

        </BlurView>

      </View>
    </SafeAreaView>
  );
}


/* =========================================================
   STYLES
========================================================= */

const styles = StyleSheet.create({

  safeArea: {
    flex: 1,
    backgroundColor: "#faf8ff",
  },

  container: {
    flex: 1,
    backgroundColor: "#faf8ff",
  },


  /* ================= HEADER ================= */

  header: {
    position: "absolute",
    top: 0,
    left: 0,
    right: 0,
    height: 64,
    zIndex: 50,
    backgroundColor: "rgba(250,248,255,0.85)",
    borderBottomWidth: 1,
    borderBottomColor: "rgba(0,0,0,0.04)",
  },

  headerInner: {
    height: 64,
    paddingHorizontal: 16,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  brandContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },

  crest: {
    width: 36,
    height: 36,
    borderRadius: 8,
    resizeMode: "contain",
    backgroundColor: "#ffffff",
    padding: 2,
  },

  nexusText: {
    color: "#1a56db",
    fontSize: 20,
    fontWeight: "600",
    letterSpacing: -0.4,
    lineHeight: 22,
  },

  headerRightSection: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },

  roleBadgeBtn: {
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    backgroundColor: "#dbe1ff",
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 16,
  },

  roleBadgeText: {
    fontSize: 11,
    fontWeight: "600",
    color: "#003fb1",
  },

  notificationButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: "center",
    justifyContent: "center",
    position: "relative",
  },

  notificationDot: {
    position: "absolute",
    top: 10,
    right: 10,
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: "#ba1a1a",
    borderWidth: 2,
    borderColor: "#faf8ff",
  },


  /* ================= SCROLL ================= */

  scrollView: {
    flex: 1,
    backgroundColor: "#faf8ff",
  },

  scrollContent: {
    paddingTop: 64,
  },


  /* ================= WELCOME ================= */

  welcomeSection: {
    paddingHorizontal: 16,
    paddingVertical: 16,
    backgroundColor: "#faf8ff",
  },

  welcomeHeader: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  collegeContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    flex: 1,
  },

  collegeEmblem: {
    width: 40,
    height: 40,
    borderRadius: 12,
    resizeMode: "contain",
    backgroundColor: "#ffffff",
    padding: 2,
  },

  collegeName: {
    color: "#003fb1",
    fontSize: 20,
    fontWeight: "600",
    lineHeight: 24,
  },

  officialHub: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 999,
    backgroundColor: "#e7e7f3",
    flexDirection: "row",
    alignItems: "center",
    gap: 4,
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.04,
    shadowRadius: 2,
    elevation: 1,
  },

  officialHubText: {
    color: "#434654",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },


  /* ================= SEARCH ================= */

  searchContainer: {
    width: "100%",
    height: 48,
    marginTop: 8,
    borderRadius: 12,
    backgroundColor: "#ffffff",
    flexDirection: "row",
    alignItems: "center",
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.04,
    shadowRadius: 3,
    elevation: 1,
  },

  searchIcon: {
    marginLeft: 14,
  },

  searchInput: {
    flex: 1,
    height: 48,
    paddingHorizontal: 10,
    color: "#191b23",
    fontSize: 14,
    fontWeight: "400",
  },

  filterButton: {
    width: 28,
    height: 28,
    borderRadius: 8,
    backgroundColor: "#ededf8",
    alignItems: "center",
    justifyContent: "center",
    marginRight: 10,
  },


  /* ================= ALERT ================= */

  alertSection: {
    height: 8,
  },


  /* ================= SERVICES ================= */

  servicesSection: {
    paddingHorizontal: 16,
    marginBottom: 24,
  },

  sectionHeadingRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 8,
  },

  sectionHeadingLeft: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
    flex: 1,
  },

  sectionHeading: {
    color: "#191b23",
    fontSize: 20,
    fontWeight: "600",
    lineHeight: 28,
  },

  modulesText: {
    color: "#003fb1",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },


  /* ================= SERVICE CARD ================= */

  serviceCard: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: "#ffffff",
    marginBottom: 8,
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.04,
    shadowRadius: 5,
    elevation: 2,
  },

  serviceTopRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  serviceInfoRow: {
    flexDirection: "row",
    alignItems: "center",
    flex: 1,
    minWidth: 0,
  },

  serviceTextContainer: {
    flex: 1,
    minWidth: 0,
    marginLeft: 12,
  },

  serviceTitle: {
    color: "#191b23",
    fontSize: 14,
    fontWeight: "600",
    lineHeight: 20,
    flexShrink: 1,
  },

  serviceSubtitle: {
    color: "#434654",
    fontSize: 14,
    fontWeight: "400",
    lineHeight: 20,
    marginTop: 1,
  },


  /* ================= ICON BOXES ================= */

  primaryIconBox: {
    width: 44,
    height: 44,
    borderRadius: 12,
    backgroundColor: "#dbe1ff",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },

  secondaryIconBox: {
    width: 44,
    height: 44,
    borderRadius: 12,
    backgroundColor: "#dce2f3",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },

  tertiaryIconBox: {
    width: 44,
    height: 44,
    borderRadius: 12,
    backgroundColor: "#ffdbcf",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },


  /* ================= NEW BADGE ================= */

  newBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 999,
    backgroundColor: "#ba1a1a",
    marginLeft: 8,
  },

  newBadgeText: {
    color: "#ffffff",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },


  /* ================= SEMESTER ================= */

  semesterChips: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
    paddingTop: 12,
  },

  currentSemesterChip: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    backgroundColor: "#003fb1",
  },

  currentSemesterText: {
    color: "#ffffff",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },

  labScheduleChip: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
    backgroundColor: "#ededf8",
  },

  labScheduleText: {
    color: "#434654",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },


  /* ================= CALENDAR ================= */

  calendarRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  calendarTitleRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },

  yearBadge: {
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
    backgroundColor: "#e7e7f3",
  },

  yearBadgeText: {
    color: "#434654",
    fontSize: 10,
    fontWeight: "600",
    lineHeight: 14,
  },

  downloadButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: "#f3f3fe",
    marginLeft: 8,
  },


  /* ================= Q-FIX ================= */

  qfixCard: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: "#f3f3fe",
    marginBottom: 8,
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.04,
    shadowRadius: 5,
    elevation: 2,
  },

  qfixHeader: {
    flexDirection: "row",
    alignItems: "flex-start",
  },

  qfixLogoBox: {
    width: 44,
    height: 44,
    borderRadius: 12,
    backgroundColor: "#ffffff",
    alignItems: "center",
    justifyContent: "center",
    padding: 6,
    overflow: "hidden",
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.04,
    shadowRadius: 2,
    elevation: 1,
  },

  qfixLogo: {
    width: "100%",
    height: "100%",
    resizeMode: "contain",
  },

  qfixTitleRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 6,
  },

  activeBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 999,
    backgroundColor: "#dbe1ff",
  },

  activeBadgeText: {
    color: "#003fb1",
    fontSize: 11,
    fontWeight: "700",
    lineHeight: 15,
  },

  qfixButtons: {
    flexDirection: "row",
    gap: 8,
    paddingTop: 12,
  },

  raiseTicketButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: "#003fb1",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
  },

  raiseTicketText: {
    color: "#ffffff",
    fontSize: 14,
    fontWeight: "500",
    lineHeight: 20,
  },

  trackButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: "#e7e7f3",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
  },

  trackText: {
    color: "#191b23",
    fontSize: 14,
    fontWeight: "500",
    lineHeight: 20,
  },


  /* ================= WEB PORTAL ================= */

  webPortalGrid: {
    flexDirection: "row",
    gap: 8,
  },

  webPortalCard: {
    flex: 1,
    height: 144,
    padding: 14,
    borderRadius: 12,
    backgroundColor: "#ffffff",
    justifyContent: "space-between",
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.04,
    shadowRadius: 5,
    elevation: 2,
  },

  webPortalTop: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  webIconBox: {
    width: 36,
    height: 36,
    borderRadius: 8,
    backgroundColor: "#dbe1ff",
    alignItems: "center",
    justifyContent: "center",
  },

  webPortalTitle: {
    color: "#191b23",
    fontSize: 14,
    fontWeight: "600",
    lineHeight: 20,
  },

  webPortalUrl: {
    color: "#434654",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },


  /* ================= FACILITIES ================= */

  facilitiesSection: {
    paddingHorizontal: 16,
    marginBottom: 24,
  },

  facilitiesHeadingRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    marginBottom: 8,
  },

  campusLocation: {
    color: "#434654",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },

  photoGrid: {
    flexDirection: "row",
    gap: 8,
  },

  photoColumn: {
    flex: 1,
  },

  photoContainer: {
    width: "100%",
    height: 112,
    borderRadius: 12,
    overflow: "hidden",
    backgroundColor: "#ededf8",
    position: "relative",
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.04,
    shadowRadius: 4,
    elevation: 2,
  },

  facilityImage: {
    width: "100%",
    height: "100%",
    resizeMode: "cover",
  },

  photoLabel: {
    position: "absolute",
    bottom: 8,
    left: 8,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    backgroundColor: "rgba(46,48,57,0.80)",
  },

  photoLabelText: {
    color: "#f0f0fb",
    fontSize: 11,
    fontWeight: "600",
    lineHeight: 15,
  },

  facilityTitle: {
    color: "#191b23",
    fontSize: 12,
    fontWeight: "500",
    lineHeight: 16,
    marginTop: 6,
    paddingHorizontal: 2,
  },


  /* ================= MILESTONES ================= */

  milestonesSection: {
    paddingHorizontal: 16,
    marginBottom: 24,
  },

  milestonesCard: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: "#f3f3fe",
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.04,
    shadowRadius: 5,
    elevation: 2,
  },

  milestonesHeader: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingBottom: 8,
    borderBottomWidth: 1,
    borderBottomColor: "rgba(195,197,215,0.30)",
  },

  milestoneDate: {
    color: "#003fb1",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },

  milestoneList: {
    paddingTop: 4,
    gap: 10,
  },

  milestoneItem: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },

  dateBox: {
    width: 40,
    height: 40,
    borderRadius: 8,
    backgroundColor: "#ffffff",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.04,
    shadowRadius: 2,
    elevation: 1,
  },

  aprilText: {
    color: "#ba1a1a",
    fontSize: 10,
    fontWeight: "700",
    lineHeight: 13,
    textTransform: "uppercase",
  },

  mayText: {
    color: "#003fb1",
    fontSize: 10,
    fontWeight: "700",
    lineHeight: 13,
    textTransform: "uppercase",
  },

  dateNumber: {
    color: "#191b23",
    fontSize: 16,
    fontWeight: "700",
    lineHeight: 18,
  },

  milestoneTextContainer: {
    flex: 1,
    minWidth: 0,
  },

  milestoneTitle: {
    color: "#191b23",
    fontSize: 14,
    fontWeight: "500",
    lineHeight: 20,
  },

  milestoneSubtitle: {
    color: "#434654",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },

  internalBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    backgroundColor: "#e7e7f3",
  },

  internalBadgeText: {
    color: "#434654",
    fontSize: 11,
    fontWeight: "600",
    lineHeight: 15,
  },

  finalsBadge: {
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 4,
    backgroundColor: "#ffdad6",
  },

  finalsBadgeText: {
    color: "#93000a",
    fontSize: 11,
    fontWeight: "600",
    lineHeight: 15,
  },


  /* ================= HELPDESK ================= */

  helpdeskSection: {
    paddingHorizontal: 16,
    paddingBottom: 24,
  },

  helpdeskCard: {
    padding: 16,
    borderRadius: 12,
    backgroundColor: "rgba(226,225,237,0.60)",
    gap: 12,
  },

  helpdeskHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
  },

  supportIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "#003fb1",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.08,
    shadowRadius: 3,
    elevation: 2,
  },

  helpdeskTextContainer: {
    flex: 1,
    minWidth: 0,
  },

  helpdeskTitle: {
    color: "#191b23",
    fontSize: 14,
    fontWeight: "700",
    lineHeight: 20,
  },

  helpdeskAddress: {
    color: "#434654",
    fontSize: 14,
    fontWeight: "400",
    lineHeight: 20,
    marginTop: 1,
  },

  helpdeskButtons: {
    flexDirection: "row",
    gap: 8,
    paddingTop: 4,
  },

  helpdeskButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: "#ffffff",
    alignItems: "center",
    justifyContent: "center",
    flexDirection: "row",
    gap: 4,
    shadowColor: "#000000",
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.04,
    shadowRadius: 2,
    elevation: 1,
  },

  helpdeskButtonText: {
    color: "#003fb1",
    fontSize: 14,
    fontWeight: "600",
    lineHeight: 20,
  },


  /* ================= BOTTOM NAV ================= */

  bottomNavigation: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    height: 64,
    zIndex: 50,
    backgroundColor: "rgba(250,248,255,0.90)",
    borderTopWidth: 1,
    borderTopColor: "rgba(0,0,0,0.05)",
  },

  bottomNavInner: {
    height: 64,
    paddingHorizontal: 8,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-around",
  },

  navItem: {
    width: 64,
    height: 48,
    alignItems: "center",
    justifyContent: "center",
    gap: 2,
  },

  navText: {
    color: "#434654",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },

  activeNavText: {
    color: "#1a56db",
    fontSize: 12,
    fontWeight: "600",
    lineHeight: 16,
  },

});
