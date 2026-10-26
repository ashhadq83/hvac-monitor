import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { THEME } from '../theme';

export type Tab = 'dashboard' | 'contacts' | 'settings';

const TABS: { key: Tab; label: string }[] = [
  { key: 'dashboard', label: 'Dashboard' },
  { key: 'contacts', label: 'Contacts' },
  { key: 'settings', label: 'Settings' },
];

interface Props {
  active: Tab;
  onChange: (tab: Tab) => void;
}

export default function TabBar({ active, onChange }: Props) {
  return (
    <View style={styles.bar}>
      {TABS.map(tab => (
        <TouchableOpacity key={tab.key} style={styles.tab} onPress={() => onChange(tab.key)}>
          <Text style={[styles.label, active === tab.key ? styles.active : null]}>{tab.label}</Text>
          {active === tab.key ? <View style={styles.underline} /> : null}
        </TouchableOpacity>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  bar: { flexDirection: 'row', backgroundColor: THEME.panel, paddingBottom: 18, paddingTop: 8 },
  tab: { flex: 1, alignItems: 'center', paddingVertical: 8 },
  label: { color: THEME.muted, fontSize: 15, fontWeight: '600' },
  active: { color: THEME.text },
  underline: { height: 3, width: 28, backgroundColor: THEME.accent, borderRadius: 2, marginTop: 4 },
});
