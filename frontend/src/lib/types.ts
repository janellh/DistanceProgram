export type DistanceResponse = { km: number; mi: number };

export type HistoryItem = {
  id: number;
  source: string;
  destination: string;
  km: number;
  mi: number;
  created_at: string;
};
