import React, { useEffect, useState } from 'react';
import { ActivityIndicator, ScrollView, StyleSheet, Text } from 'react-native';
import { fetchTechnicians } from '../api';
import TechnicianCard from '../components/TechnicianCard';
import { THEME } from '../theme';
import { Technician } from '../types';

export default function ContactsScreen({ baseUrl }: { baseUrl: string }) {
  const [list, setList] = useState<Technician[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetchTechnicians(baseUrl)
      .then(data => {
        if (!cancelled) {
          setList(data);
          setError(null);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setError('Cannot load the contact list. Check the address on the Settings page.');
        }
      })
      .finally(() => {
        if (!cancelled) {
          setLoading(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, [baseUrl]);

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={styles.title}>HVAC technicians</Text>
      <Text style={styles.subtitle}>Edit this list in backend/technicians.json on the Pi</Text>
      {loading ? <ActivityIndicator size="large" color="#7fdce6" /> : null}
      {error ? <Text style={styles.error}>{error}</Text> : null}
      {list.map(t => (
        <TechnicianCard key={t.id} technician={t} />
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: { padding: 16, paddingBottom: 48 },
  title: { color: THEME.text, fontSize: 26, fontWeight: 'bold', textAlign: 'center' },
  subtitle: { color: THEME.muted, textAlign: 'center', marginBottom: 12 },
  error: { color: '#ffb3b3', backgroundColor: '#2e0b0b', padding: 12, borderRadius: 8 },
});
