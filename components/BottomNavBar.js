import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import Colors from '../constants/colors';
import Typography from '../constants/typography';

const BottomNavBar = ({ items, activeItem, onItemPress }) => {
  return (
    <View style={styles.container}>
      {items.map((item, index) => {
        const isActive = activeItem === item.key;
        return (
          <TouchableOpacity
            key={item.key || index}
            style={[styles.navItem, isActive && styles.navItemActive]}
            onPress={() => onItemPress && onItemPress(item)}
            activeOpacity={0.7}
          >
            <MaterialIcons
              name={item.icon}
              size={24}
              color={isActive ? Colors.onPrimaryContainer : Colors.onSurfaceVariant}
            />
            <Text style={[styles.navItemText, isActive && styles.navItemTextActive]}>
              {item.label}
            </Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    height: 64,
    paddingHorizontal: 16,
    backgroundColor: Colors.surfaceContainerLowest,
    borderTopWidth: 1,
    borderTopColor: Colors.outlineVariant,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 8,
  },
  navItem: {
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 16,
    paddingVertical: 4,
    borderRadius: 9999,
  },
  navItemActive: {
    backgroundColor: Colors.primaryContainer,
    paddingHorizontal: 16,
    paddingVertical: 4,
  },
  navItemText: {
    ...Typography.labelSm,
    color: Colors.onSurfaceVariant,
    marginTop: 2,
  },
  navItemTextActive: {
    color: Colors.onPrimaryContainer,
  },
});

export default BottomNavBar;
