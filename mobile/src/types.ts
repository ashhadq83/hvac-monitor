export type Level = 'NORMAL' | 'WARNING' | 'CRITICAL';

export interface Technician {
  id: string;
  name: string;
  phone: string;
  specialties: string[];
  note?: string;
}

export interface Advice {
  source: string;
  headline: string;
  explanation: string;
  actions: string[];
  urgency: string;
  technician: Technician | null;
}

export interface Status {
  temp_c: number | null;
  pressure_pa: number | null;
  vib_events: number;
  temp_status: Level;
  pressure_status: Level;
  vib_status: Level;
  overall: Level;
  alerts: string[];
  advice: Advice;
}
