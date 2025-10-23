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
    created_at: string;
  }

  let rows: HistoryItem[] = [];
  let loading = true;
  let error: string | null = null;

  function num(x: unknown): number | null {
    const v = Number(x);
    return Number.isFinite(v) ? v : null;
  }
  function fmtNum(x: unknown): string {
    const v = num(x);
    return v === null ? '—' : v.toFixed(3);
  }
  function fmtDate(s: string) {
    const d = new Date(s);
    return isNaN(d.getTime()) ? s : d.toLocaleString();
  }

  async function loadHistory() {
    console.log("loadHistory Here");
    loading = true;
    error = null;
    try {
      const r = await fetch(`${API_BASE}/history`, { headers: { accept: 'application/json' } });
      console.log("r", r);
      if (!r.ok) {
        console.log("r", r);
        const text = await r.text();
        throw new Error(`Failed to load history (${r.status}). ${text.slice(0,200)}`);
      }
      const data = await r.json();
      console.log("data", data);
      rows = Array.isArray(data?.items) ? (data.items as HistoryItem[]) : [];
    } catch (e: any) {
      error = e?.message ?? 'Unexpected error loading history';
      rows = [];
    } finally {
      loading = false;
    }
  }

  onMount(loadHistory);
</script>

<section class="main container">
  {#if loading}
    <div class="status">Loading history…</div>
  {:else if error}
    <div class="status error">{error}</div>
  {:else if rows.length === 0}
    <div class="status">No history yet.</div>
  {:else}
    <div class="card">
      <header class="dt-head">
        <h3 class="dt-title">Historical Queries</h3>
        <p class="dt-desc">History of the user’s queries.</p>
      </header>
      <div class="table-wrap">
        <table class="table" role="grid" aria-label="Historical Queries">
          <colgroup>
            <col style="width:304px" />
            <col style="width:304px" />
            <col style="width:304px" />
            <col style="width:304px" />
          </colgroup>
          <thead>
            <tr>
              <th>Source Address</th>
              <th>Destination Address</th>
              <th>Distance in Miles</th>
              <th>Distance in Kilometers</th>
            </tr>
          </thead>
          <tbody>
            {#each rows as r}
              <tr>
                <td title="{r.source}">{r.source}</td>
                <td title="{r.destination}">{r.destination}</td>
                <td class="num">{fmtNum(r.mi)}</td>
                <td class="num">{fmtNum(r.km)}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  {/if}
</section>

<style>
  .main {
    max-width: 1248px;
    margin: 0 auto;
  }
  .card{
    background:#FFFFFF;
    padding:16px;
    display:grid;
    gap: 8px;
    box-sizing: border-box;
  }
  .dt-head {
    padding: 16px 16px 24px 16px;
    background: #FFFFFF;
  }
  .dt-title {
    margin: 0;
    font: 400 20px/24px Inter, system-ui, Arial, sans-serif;
    color: var(--Text-text-primary, #1B1A1A);
  }
  .dt-desc{
    margin:4px 0 0 0;
    font: 400 14px/18px Inter, system-ui, Arial, sans-serif;
    letter-spacing:.16px;
    color: var(--Text-text-secondary, #4B4949);
  }
  .table-wrap{
    overflow-x:auto;
  }
  .table{
    width:1216px;
    border-collapse:separate;
    border-spacing:0;
    background:#FFFFFF;
    font: 400 14px/20px Inter, system-ui, Arial, sans-serif;
    color:#1B1A1A;
  }
  thead tr{
    background: var(--Layer-accent-layer-accent-01, #E0E0DE);
    box-shadow: inset 0 -1px 0 #DCDAD6;
  }
  thead th{
    text-align:left;
    height:40px;
    max-height:40px;
    padding:11px 16px;
    white-space:nowrap;
  }
  thead th.num{
    text-align:left;
  }
  tbody tr{
    background: var(--Layer-layer-01, #F8F8F6);
    box-shadow: inset 0 -1px 0 #DCDAD6;
    height:40px;
    max-height:40px;
  }
  tbody td{
    padding:11px 16px;
    vertical-align:middle;
  }
  tbody td.num{
    text-align:right;
    white-space:nowrap;
  }
  tbody td{
    overflow:hidden;
    text-overflow:ellipsis;
    white-space:nowrap;
  }
</style>


