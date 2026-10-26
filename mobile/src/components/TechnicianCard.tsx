import React from 'react';
import { Linking, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { THEME } from '../theme';
import { Technician } from '../types';

interface Props {
  technician: Technician;
  highlight?: boolean;
}

export function callNumber(phone: string): void {
  Linking.openURL(`tel:${phone.replace(/[^0-9+]/g, '')}`);
}

export default function TechnicianCard({ technician, highlight }: Props) {
  return (
    <View style={[styles.box, highlight ? styles.highlight : null]}>
      <Text style={styles.name}>{technician.name}</Text>
      <Text style={styles.specialties}>{technician.specialties.join(', ')}</Text>
      {technician.note ? <Text style={styles.note}>{technician.note}</Text> : null}
      <TouchableOpacity style={styles.button} onPress={() => callNumber(technician.phone)}>
        <Text style={styles.buttonText}>Call {technician.phone}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  box: { backgroundColor: THEME.background, borderRadius: 10, padding: 12, marginTop: 10 },
  highlight: { borderWidth: 2, borderColor: THEME.accent },
  name: { color: THEME.text, fontSize: 18, fontWeight: 'bold' },
  specialties: { color: THEME.accent, fontSize: 12, marginTop: 2 },
  note: { color: THEME.muted, fontSize: 12, marginTop: 4 },
  button: { backgroundColor: '#0fa968', borderRadius: 10, padding: 14, marginTop: 10, alignItems: 'center' },
  buttonText: { color: THEME.text, fontSize: 18, fontWeight: 'bold' },
});
