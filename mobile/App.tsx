import React, { useState } from 'react';
import { Platform, StatusBar, StyleSheet, View } from 'react-native';
import TabBar, { Tab } from './src/components/TabBar';
import { DEFAULT_BACKEND_URL } from './src/config';
import ContactsScreen from './src/screens/ContactsScreen';
import DashboardScreen from './src/screens/DashboardScreen';
import SettingsScreen from './src/screens/SettingsScreen';
import { THEME } from './src/theme';

export default function App() {
  const [tab, setTab] = useState<Tab>('dashboard');
  const [baseUrl, setBaseUrl] = useState<string>(DEFAULT_BACKEND_URL);

  return (
    <View style={styles.screen}>
      <StatusBar barStyle="light-content" />
      <View style={styles.body}>
        {tab === 'dashboard' ? <DashboardScreen baseUrl={baseUrl} /> : null}
        {tab === 'contacts' ? <ContactsScreen baseUrl={baseUrl} /> : null}
        {tab === 'settings' ? <SettingsScreen baseUrl={baseUrl} onChange={setBaseUrl} /> : null}
      </View>
      <TabBar active={tab} onChange={setTab} />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: THEME.background,
    paddingTop: Platform.OS === 'ios' ? 56 : (StatusBar.currentHeight ?? 24) + 12,
  },
  body: { flex: 1 },
});
