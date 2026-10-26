import { useEffect, useState } from 'react';
import { fetchStatus } from '../api';
import { REFRESH_MS } from '../config';
import { Status } from '../types';

export function useStatus(baseUrl: string) {
  const [status, setStatus] = useState<Status | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);

    const load = async () => {
      try {
        const data = await fetchStatus(baseUrl);
        if (!cancelled) {
          setStatus(data);
          setError(null);
        }
      } catch (e) {
        if (!cancelled) {
          setError('Cannot reach the Raspberry Pi backend. Check the address on the Settings page.');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    load();
    const id = setInterval(load, REFRESH_MS);
    return () => {
      cancelled = true;
      clearInterval(id);
    };
  }, [baseUrl]);

  return { status, error, loading };
}
