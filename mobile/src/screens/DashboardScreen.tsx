import React from 'react';
import { ActivityIndicator, ScrollView, StyleSheet, Text, View } from 'react-native';
import AdviceCard from '../components/AdviceCard';
import StatusCard from '../components/StatusCard';
import { useStatus } from '../hooks/useStatus';
import { COLORS, THEME } from '../theme';

export default function DashboardScreen({ baseUrl }: { baseUrl: string }) {
  const { status, error, loading } = useStatus(baseUrl);
  const showAdvice = status !== null && status.overall !== 'NORMAL' && status.advice.headline !== '';

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={styles.title}>HVAC Health Monitor</Text>
      <Text style={styles.subtitle}>Live status from your Raspberry Pi</Text>

      {loading && !status ? <ActivityIndicator size="large" color="#7fdce6" style={styles.spinner} /> : null}
      {error ? <Text style={styles.error}>{error}</Text> : null}

      {status ? (
        <>
          <View style={styles.cards}>
            <StatusCard
              label="AIRFLOW"
              value={status.pressure_pa === null ? '--' : `${status.pressure_pa.toFixed(0)} Pa`}
              level={status.pressure_status}
            />
            <StatusCard
              label="TEMPERATURE"
              value={status.temp_c === null ? '--' : `${status.temp_c.toFixed(1)} °C`}
              level={status.temp_status}
            />
            <StatusCard label="VIBRATION" value={`${status.vib_events} pulses`} level={status.vib_status} />
          </View>

          <View style={[styles.banner, { backgroundColor: COLORS[status.overall] }]}>
            <Text style={styles.bannerText}>
              {status.alerts.length > 0 ? status.alerts.join('\n') : 'System healthy. No alerts.'}
            </Text>
          </View>

          {showAdvice ? <AdviceCard advice={status.advice} /> : null}
        </>
      ) : null}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: { padding: 16, paddingBottom: 48 },
  title: { color: THEME.text, fontSize: 28, fontWeight: 'bold', textAlign: 'center' },
  subtitle: { color: THEME.muted, textAlign: 'center', marginBottom: 16 },
  spinner: { marginVertical: 24 },
  error: { color: '#ffb3b3', backgroundColor: '#2e0b0b', padding: 12, borderRadius: 8, marginBottom: 12 },
  cards: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'center' },
  banner: { borderRadius: 10, padding: 14, marginTop: 12 },
  bannerText: { color: THEME.text, fontSize: 16, textAlign: 'center' },
});
