import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { COLORS, THEME } from '../theme';
import { Level } from '../types';

interface Props {
  label: string;
  value: string;
  level: Level;
}

export default function StatusCard({ label, value, level }: Props) {
  return (
    <View style={[styles.card, { borderColor: COLORS[level] }]}>
      <Text style={styles.label}>{label}</Text>
      <Text style={styles.value}>{value}</Text>
      <Text style={[styles.status, { color: COLORS[level] }]}>{level}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    width: '31%',
    minWidth: 100,
    margin: '1%',
    padding: 12,
    borderRadius: 12,
    borderWidth: 3,
    backgroundColor: THEME.panel,
    alignItems: 'center',
  },
  label: { color: '#9fb6c9', fontSize: 11, letterSpacing: 1 },
  value: { color: THEME.text, fontSize: 20, fontWeight: 'bold', marginVertical: 8, textAlign: 'center' },
  status: { fontWeight: 'bold', fontSize: 12 },
});
