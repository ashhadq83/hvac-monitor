import Constants from 'expo-constants';

/**
 * Where the Python backend runs (port 5000).
 * When the Expo dev server runs on the Raspberry Pi, the phone loads the app from
 * the Pi, so the Pi's address is found automatically from the Expo host address.
 * If it is wrong (for example in tunnel mode), change it on the Settings page.
 */
function detectBackendUrl(): string {
  const hostUri = Constants.expoConfig?.hostUri; // for example "192.168.1.50:8081"
  const host = hostUri ? hostUri.split(':')[0] : 'localhost';
  return `http://${host}:5000`;
}

export const DEFAULT_BACKEND_URL: string = detectBackendUrl();
export const REFRESH_MS = 2000;
