<script lang="ts">
  import { onMount } from 'svelte';
  import { PUBLIC_API_BASE } from '$env/static/public';

  const API_BASE = (PUBLIC_API_BASE ?? '').replace(/\/+$/, '');

  interface HistoryItem {
    id: number;
    source: string;
    destination: string;
    km: number;
    mi: number;
    created_at: string; // ISO
  }

  let rows: HistoryItem[] = [];
  let loading = true;
  let error: string | null = null;

  async function loadHistory() {
    loading = true;
    error = null;
    try {
      const r = await fetch(`${API_BASE}/history`);
      if (!r.ok) {
        const body = await r.json().catch(() => ({}));
        throw new Error(body?.detail ?? `Failed to load history (${r.status})`);
      }
      const data = (await r.json()) as { items: HistoryItem[] };
      rows = Array.isArray(data?.items) ? data.items : [];
    } catch (e: any) {
      error = e?.message ?? 'Unexpected error loading history';
    } finally {
      loading = false;
    }
  }

  function fmtDate(s: string) {
    const d = new Date(s);
    return isNaN(d.getTime()) ? s : d.toLocaleString();
  }

  onMount(loadHistory);
</script>

<section class="wrap container">
  {#if loading}
    <div class="status">Loading history…</div>
  {:else if error}
    <div class="status error">{error}</div>
  {:else if rows.length === 0}
    <div class="status">No history yet.</div>
  {:else}
    <table class="table">
      <thead>
        <tr>
          <th>When</th>
          <th>Source</th>
          <th>Destination</th>
          <th>KM</th>
          <th>MI</th>
        </tr>
      </thead>
      <tbody>
        {#each rows as r}
          <tr>
            <td>{fmtDate(r.created_at)}</td>
            <td>{r.source}</td>
            <td>{r.destination}</td>
            <td>{r.km.toFixed(3)}</td>
            <td>{r.mi.toFixed(3)}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</section>

<style>
  .wrap { padding: 16px; }
  .status { padding: 12px; }
  .status.error { color: #b00020; }

  .table {
    width: 100%;
    border-collapse: collapse;
    font: 400 14px/20px Inter, system-ui, Arial, sans-serif;
  }
  .table th, .table td {
    border-bottom: 1px solid #e5e7eb;
    text-align: left;
    padding: 10px 8px;
  }
  .table thead th {
    font-weight: 600;
    background: #f8f8f6;
  }

  .main { max-width: 1248px; margin: 0 auto; }
  .card{ background:#FFFFFF; padding:16px; display:grid; gap:8px; box-sizing:border-box; }
  .dt-head{ padding:16px 16px 24px 16px; background:#FFFFFF; }
  .dt-title{ margin:0; font: 400 20px/24px Inter, system-ui, Arial, sans-serif; color: var(--Text-text-primary, #1B1A1A); }
  .dt-desc{ margin:4px 0 0 0; font: 400 14px/18px Inter, system-ui, Arial, sans-serif; letter-spacing:.16px; color: var(--Text-text-secondary, #4B4949); }
  .table-wrap{ overflow-x:auto; }
  .table{ width:1216px; border-collapse:separate; border-spacing:0; background:#FFFFFF; font: 400 14px/20px Inter, system-ui, Arial, sans-serif; color:#1B1A1A; }
  thead tr{ background: var(--Layer-accent-layer-accent-01, #E0E0DE); box-shadow: inset 0 -1px 0 #DCDAD6; }
  thead th{ text-align:left; height:40px; max-height:40px; padding:11px 16px; white-space:nowrap; }
  thead th.num{ text-align:right; }
  tbody tr{ background: var(--Layer-layer-01, #F8F8F6); box-shadow: inset 0 -1px 0 #DCDAD6; height:40px; max-height:40px; }
  tbody td{ padding:11px 16px; vertical-align:middle; }
  tbody td.num{ text-align:right; white-space:nowrap; }
  tbody td{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
</style>


