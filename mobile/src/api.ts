import { Status, Technician } from './types';

async function getJson<T>(url: string, timeoutMs = 4000): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) {
      throw new Error(`Server answered ${response.status}`);
    }
    return (await response.json()) as T;
  } finally {
    clearTimeout(timer);
  }
}

export function fetchStatus(baseUrl: string): Promise<Status> {
  return getJson<Status>(`${baseUrl}/api/status`);
}

export function fetchTechnicians(baseUrl: string): Promise<Technician[]> {
  return getJson<Technician[]>(`${baseUrl}/api/technicians`);
}
