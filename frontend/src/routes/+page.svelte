<script lang="ts">
  import type { DistanceResponse, HistoryItem } from '$lib/types';

  let source = '';
  let destination = '';
  let loading = false;
  let error: string | null = null;
  let result: DistanceResponse | null = null;
  let history: HistoryItem[] = [];

  async function fetchHistory() {
    try {
      const r = await fetch('/history');
      if (!r.ok) throw new Error('Failed to load history');
      const data = (await r.json()) as { items: HistoryItem[] };
      history = data.items;
    } catch (_e: unknown) {
      // non-blocking — just skip if it fails
    }
  }

  async function submit() {
    if (loading) return;
    error = null;
    result = null;
    loading = true;

    try {
      const r = await fetch('/distance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, destination })
      });
      const body = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error((body as any)?.detail ?? 'Could not retrieve distance');
      result = body as DistanceResponse;
      await fetchHistory();
    } catch (e: any) {
      error = e?.message ?? 'Unexpected error';
    } finally {
      loading = false;
    }
  }

  fetchHistory();
</script>

<style>
  .wrap { max-width: 720px; margin: 0 auto; padding: 2rem; font-family: system-ui, sans-serif; }
  .card { border: 1px solid #ddd; border-radius: 12px; padding: 1rem; margin-bottom: 1rem; }
  .row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
  button { padding: 0.6rem 1rem; border-radius: 8px; border: 1px solid #ccc; cursor: pointer; }
  table { width: 100%; border-collapse: collapse; }
  th, td { padding: 0.5rem; border-bottom: 1px solid #eee; text-align: left; }
</style>

<div class="wrap">
  <h1>Distance Calculator</h1>

  <div class="card">
    <div class="row">
      <input placeholder="Source address" bind:value={source} />
      <input placeholder="Destination address" bind:value={destination} />
    </div>
    <div style="margin-top:.75rem; display:flex; gap:.5rem;">
      <button on:click={submit} disabled={loading}>Calculate</button>
      {#if loading}<span>Loading…</span>{/if}
    </div>
    {#if error}<p style="color:#b00020;margin-top:.5rem;">{error}</p>{/if}
    {#if result}
      <p style="margin-top:.5rem;">
        Distance: <strong>{result.km} km</strong> / <strong>{result.mi} mi</strong>
      </p>
    {/if}
  </div>

  <div class="card">
    <h2>Recent Queries</h2>
    {#if history.length === 0}
      <p>No history yet.</p>
    {:else}
      <table>
        <thead><tr><th>When</th><th>From</th><th>To</th><th>KM</th><th>MI</th></tr></thead>
        <tbody>
          {#each history as h}
            <tr>
              <td>{new Date(h.created_at).toLocaleString()}</td>
              <td>{h.source}</td>
              <td>{h.destination}</td>
              <td>{h.km}</td>
              <td>{h.mi}Test</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  </div>
</div>
