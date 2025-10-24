<script lang="ts">
import { env as publicEnv } from '$env/dynamic/public';
const API_BASE = publicEnv.PUBLIC_API_BASE ?? '';

  type DistanceResponse = {
    km: number;
    mi: number;
    source_norm: string;
    dest_norm: string;
  };

  let origin = '';
  let destination = '';
  let unit: 'miles' | 'kilometers' | 'both' = 'miles';

  let loading = false;
  let error: string | null = null;
  let distanceText = '';

  // Button state/colors (red when both inputs have text)
  $: filled   = origin.trim().length > 0 && destination.trim().length > 0;
  $: btnBg    = filled && !loading ? 'var(--btn-danger, #D73D3D)' : 'var(--Button-button-disabled, #BBBBB9)';
  $: btnFg    = filled && !loading ? '#FFFFFF' : 'var(--Text-text-on-color-disabled, #7D7D7C)';
  $: btnBlend = filled && !loading ? 'normal' : 'multiply';

  const round = (n: number) => Math.round(n * 100) / 100;

  async function submit(): Promise<void> {
  if (!filled || loading) return;

  error = null;
  distanceText = '';
  loading = true;

  try {
    const r = await fetch(`${API_BASE}/distance`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ source: origin, destination })
    });

    if (!r.ok) {
      const msg = (await r.json().catch(() => ({}))) as { detail?: string };
      throw new Error(msg?.detail ?? 'Could not retrieve distance.');
    }

    const result = (await r.json()) as DistanceResponse;
    const km = result.km;
    const mi = result.mi;

    distanceText =
      unit === 'miles' ? `${round(mi)} mi`
      : unit === 'kilometers' ? `${round(km)} km`
      : `${round(mi)} mi / ${round(km)} km`;

  } catch (e) {
    error = e instanceof Error ? e.message : 'Something went wrong.';
  } finally {
    loading = false;
  }
}

</script>

<section class="main container">
  <div class="address-section">
    <div class="row">
      <div class="field">
        <div class="label-margin">
          <label for="origin" class="label-text">Source Address</label>
        </div>
        <div class="base">
          <input
            id="origin"
            class="input"
            type="text"
            bind:value={origin}
            placeholder="Input address"
            autocomplete="off"
          />
        </div>
      </div>

      <div class="field">
        <div class="label-margin">
          <label for="destination" class="label-text">Destination Address</label>
        </div>
        <div class="base">
          <input
            id="destination"
            class="input"
            type="text"
            bind:value={destination}
            placeholder="Input address"
            autocomplete="off"
          />
        </div>
      </div>

      <fieldset class="radio-group">
        <legend class="rg-label">Unit</legend>

        <label class="radio">
          <input type="radio" name="unit" value="miles" bind:group={unit} />
          <span class="dot" aria-hidden="true"></span>
          <span class="val">Miles</span>
        </label>

        <label class="radio">
          <input type="radio" name="unit" value="kilometers" bind:group={unit} />
          <span class="dot" aria-hidden="true"></span>
          <span class="val">Kilometers</span>
        </label>

        <label class="radio">
          <input type="radio" name="unit" value="both" bind:group={unit} />
          <span class="dot" aria-hidden="true"></span>
          <span class="val">Both</span>
        </label>
      </fieldset>

      <div class="mini-field">
        <div class="label-margin">
          <label for="distance" class="label-text">Distance</label>
        </div>
        <div class="mini-base">
          <input id="distance" class="mini-input" type="text" value={distanceText} readonly />
        </div>
      </div>
    </div>

    <div class="btn-line">
      <button
        class="calc-btn"
        type="button"
        on:click|preventDefault={submit}
        disabled={!filled || loading}
        aria-disabled={!filled || loading}
        style={`--bg:${btnBg}; --fg:${btnFg}; --blend:${btnBlend};`}
      >
        <span class="content">
          <span class="label">{loading ? 'Calculating…' : 'Calculate Distance'}</span>
          <span class="icon-wrap" aria-hidden="true">
            <svg class="icon" viewBox="0 0 16 16">
              <rect width="16" height="16" fill="#FFFFFF" style="mix-blend-mode:multiply;"></rect>
              <path d="M3 1h10a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1Zm0 3h10V2H3v2Zm2 3H4v2h1V7Zm3 0H6v2h2V7Zm3 0H9v2h2V7ZM5 11H4v2h1v-2Zm3 0H6v2h2v-2Zm3 0H9v2h2v-2Z" transform="translate(2 1)" fill="currentColor"/>
            </svg>
          </span>
        </span>
      </button>
    </div>

    {#if error}
      <div class="error">{error}</div>
    {/if}
  </div>
</section>

<style>
  .main { max-width: 1248px; margin: 0 auto; }

  .address-section{
    background: #FFFFFF;
    padding: 16px;
    display: grid;
    gap: 32px;
    min-height: 212px;
    box-sizing: border-box;
  }

  .row{
    display: grid;
    grid-template-columns:
      minmax(0, 375px)
      minmax(0, 375px)
      101px
      200px;
    gap: 32px;
    min-height: 100px;
  }

  .field{ max-width: 414px; width: 100%; }
  .label-margin{ padding-bottom: 4px; height: 20px; }
  .label-text{
    margin: 0;
    font: 400 12px/16px Inter, system-ui, Arial, sans-serif;
    letter-spacing: 0.32px;
    color: var(--Text-text-secondary, #4B4949);
  }
  .base{
    display: flex; align-items: center;
    height: 40px;
    padding: 11px 16px;
    background: var(--Field-field-01, #F8F8F6);
    border-bottom: 1px solid var(--Border-Border-strong-01, #7D7D7C);
    box-sizing: border-box;
  }
  .input{
    width: 100%; border: 0; outline: 0; background: transparent;
    font: 400 14px/18px Inter, system-ui, Arial, sans-serif;
    letter-spacing: 0.16px; color: var(--text-1, #222222);
  }
  .input::placeholder{ color: var(--Text-text-placeholder, #7D7D7C); }

  .radio-group{
    margin: 0; padding: 0; border: 0; width: 101px;
    display: grid; row-gap: 8px;
  }
  .rg-label{
    margin: 0; padding: 0; display: block;
    font: 400 12px/16px Inter, system-ui, Arial, sans-serif;
    letter-spacing: .32px;
    color: var(--Text-text-secondary, #4B4949);
  }
  .radio{
    display: inline-flex; align-items: center; gap: 8px; height: 20px;
    line-height: 20px; margin: 0; padding: 0; cursor: pointer;
    user-select: none; color: #1B1A1A;
    font: 400 14px/20px Inter, system-ui, Arial, sans-serif;
    position: relative;
  }
  .radio input{
    position: absolute; inline-size: 20px; block-size: 20px;
    opacity: 0; margin: 0; pointer-events: none;
  }
  .dot{
    inline-size: 20px; block-size: 20px; border-radius: 50%;
    border: 1px solid #1B1A1A; box-sizing: border-box;
    display: inline-block; position: relative;
  }
  .radio input:checked + .dot::after{
    content: ''; position: absolute; inset: 3px; border-radius: 50%; background: #1B1A1A;
  }
  .val{ padding-block: 1px; }

  .mini-field{ width: 200px; }
  .mini-base{
    display: flex; align-items: center;
    height: 40px; padding: 11px 0;
    background: #FFFFFF; box-sizing: border-box;
  }
  .mini-input{
    width: 100%; border: 0; outline: 0; background: transparent;
    font: 400 14px/18px Inter, system-ui, Arial, sans-serif;
    letter-spacing: 0.16px; color: #222222;
  }

  .btn-line{ display: inline-flex; }
  .calc-btn{
    width:207px; height:48px; padding:3px; border:0; border-radius:0;
    background: var(--bg, #BBBBB9);
    color: var(--fg, #7D7D7C);
    background-blend-mode: var(--blend, multiply);
    box-shadow: 0 1px 2px rgba(0,0,0,.15);
    cursor: pointer;
  }
  .calc-btn:disabled{ cursor: not-allowed; }
  .calc-btn .content{
    display:inline-flex; align-items:center; justify-content:space-between;
    width:201px; height:42px; padding:12px 13px; gap:32px; box-sizing:border-box;
  }
  .calc-btn .label{ font: 400 14px/18px Inter, system-ui, Arial, sans-serif; letter-spacing:.16px; }
  .icon-wrap{ width:16px; height:16px; display:inline-flex; }
  .icon{ width:16px; height:16px; fill: currentColor; }

  .error { color:#b00020; }

  @media (max-width: 1248px){
    .row{ grid-template-columns: 1fr; align-items: start; }
    .field, .mini-field, .radio-group, .btn-line{ width: 100%; }
  }
</style>