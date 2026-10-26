import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { THEME } from '../theme';
import { Advice } from '../types';
import TechnicianCard from './TechnicianCard';

export default function AdviceCard({ advice }: { advice: Advice }) {
  return (
    <View style={styles.box}>
      <Text style={styles.head}>{advice.headline}</Text>
      <Text style={styles.source}>Advice source: {advice.source}</Text>
      <Text style={styles.text}>{advice.explanation}</Text>
      {advice.actions.map((action, index) => (
        <Text key={index} style={styles.text}>
          {'\u2022'} {action}
        </Text>
      ))}
      {advice.urgency ? <Text style={styles.urgency}>Urgency: {advice.urgency}</Text> : null}
      {advice.technician ? (
        <>
          <Text style={styles.contactLabel}>WHO TO CONTACT</Text>
          <TechnicianCard technician={advice.technician} highlight />
        </>
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  box: { backgroundColor: THEME.panel, borderRadius: 12, borderWidth: 2, borderColor: THEME.accent, padding: 16, marginTop: 16 },
  head: { color: THEME.text, fontSize: 20, fontWeight: 'bold' },
  source: { color: THEME.muted, fontSize: 12, marginBottom: 8 },
  text: { color: '#e6eef5', fontSize: 15, marginBottom: 4 },
  urgency: { color: '#ffd37a', fontWeight: 'bold', marginTop: 6 },
  contactLabel: { color: '#9fb6c9', fontSize: 11, letterSpacing: 1, marginTop: 14 },
});
