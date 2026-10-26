import React, { useState } from 'react';
import { ScrollView, StyleSheet, Text, TextInput, TouchableOpacity } from 'react-native';
import { fetchStatus } from '../api';
import { DEFAULT_BACKEND_URL } from '../config';
import { THEME } from '../theme';

interface Props {
  baseUrl: string;
  onChange: (url: string) => void;
}

export default function SettingsScreen({ baseUrl, onChange }: Props) {
  const [draft, setDraft] = useState<string>(baseUrl);
  const [message, setMessage] = useState<string>('');

  const clean = (value: string) => value.trim().replace(/\/$/, '');

  const save = async () => {
    const url = clean(draft);
    setMessage('Testing...');
    try {
      await fetchStatus(url);
      onChange(url);
      setMessage('Connected. Address saved for this session.');
    } catch (e) {
      setMessage('Could not connect to that address. Check the Pi IP, the port (5000) and the Wi-Fi.');
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.content}>
      <Text style={styles.title}>Settings</Text>
      <Text style={styles.label}>Backend address (Raspberry Pi)</Text>
      <TextInput
        style={styles.input}
        value={draft}
        onChangeText={setDraft}
        autoCapitalize="none"
        autoCorrect={false}
        keyboardType="url"
        placeholder="http://192.168.1.50:5000"
        placeholderTextColor="#6f879c"
      />
      <TouchableOpacity style={styles.button} onPress={save}>
        <Text style={styles.buttonText}>Test and save</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.secondary} onPress={() => setDraft(DEFAULT_BACKEND_URL)}>
        <Text style={styles.secondaryText}>Use automatic address ({DEFAULT_BACKEND_URL})</Text>
      </TouchableOpacity>
      {message ? <Text style={styles.message}>{message}</Text> : null}
      <Text style={styles.help}>
        Find the Pi address by running "hostname -I" in the Pi terminal. The phone and the Pi must be on the same Wi-Fi.
      </Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: { padding: 16, paddingBottom: 48 },
  title: { color: THEME.text, fontSize: 26, fontWeight: 'bold', textAlign: 'center', marginBottom: 16 },
  label: { color: THEME.muted, marginBottom: 6 },
  input: { backgroundColor: THEME.panel, color: THEME.text, borderRadius: 8, paddingHorizontal: 12, paddingVertical: 12, fontSize: 16 },
  button: { backgroundColor: THEME.accent, borderRadius: 10, padding: 14, marginTop: 12, alignItems: 'center' },
  buttonText: { color: THEME.text, fontSize: 17, fontWeight: 'bold' },
  secondary: { padding: 12, marginTop: 4, alignItems: 'center' },
  secondaryText: { color: THEME.accent, fontSize: 13 },
  message: { color: '#ffd37a', marginTop: 12, textAlign: 'center' },
  help: { color: THEME.muted, marginTop: 24, fontSize: 13, lineHeight: 19 },
});
