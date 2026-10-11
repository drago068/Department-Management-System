import React from 'react';
import { StatusBar } from 'react-native';
import { AppProviders } from './src/app/providers/AppProviders';
import { AppNavigator } from './src/app/navigation/AppNavigator';

export default function App() {
  return (
    <AppProviders>
      <StatusBar barStyle="dark-content" backgroundColor="#faf8ff" />
      <AppNavigator />
    </AppProviders>
  );
}
