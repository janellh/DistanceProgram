<script lang="ts">
  type Row = {
    id: number;
    source: string;
    destination: string;
    km: number;
    miles?: number | null;
    created_at: string;
  };

  export let items: Row[] = [];
  const fmt = (n?: number | null, s = '') =>
    n == null ? '' : `${Math.round(n * 100) / 100}${s}`;
</script>

<section class="main container">
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
            <th class="num">Distance in Miles</th>
            <th class="num">Distance in Kilometers</th>
          </tr>
        </thead>

        <tbody>
          {#each items as r (r.id ?? r.source + r.destination + r.created_at)}
            <tr>
              <td title={r.source}>{r.source}</td>
              <td title={r.destination}>{r.destination}</td>
              <td class="num">{fmt(r.miles, ' mi')}</td>
              <td class="num">{fmt(r.km, ' km')}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  </div>
</section>

<style>
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