<script lang="ts">
  import { goto } from '$app/navigation';

  export let text = 'View Historical Queries';
  export let href: string | null = null;
  export let icon: 'recently-viewed' | 'calculator' | null = 'recently-viewed';

  export let width = 237;
  export let height = 48;
  export let padding = 3;
  export let radius = 0;

  export let bg = 'var(--Button-button-secondary, #313030)';
  export let fg = '#FFFFFF';
  export let blend: CSSStyleDeclaration['backgroundBlendMode'] | string = 'normal';

  export let disabled = false;

  function handleClick(e: MouseEvent) {
    if (disabled) { e.preventDefault(); return; }
    if (href) { e.preventDefault(); goto(href); }
  }
</script>

<a
  class="btn"
  href={href ?? '#'}
  aria-disabled={disabled}
  on:click={href ? handleClick : undefined}
  style={`--w:${width}px; --h:${height}px; --pad:${padding}px; --radius:${radius}px; --bg:${bg}; --fg:${fg}; --blend:${blend}; --border:${bg};`}
>
    <span class="label">{text}</span>
  {#if icon === 'recently-viewed'}
    <svg class="icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M13 3a9 9 0 1 0 8.66 6.5h-2.1a7 7 0 1 1-3.2-4.58l-1.96 1.96H21V2.82l-2.02 2.02A8.98 8.98 0 0 0 13 3Zm-1 4h2v6h-5v-2h3V7Z"/>
    </svg>
  {:else if icon === 'calculator'}
    <svg class="icon" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 3h10a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2zm0 4h10V5H7v2zm2 4H8v2h1v-2zm3 0h-2v2h2v-2zm3 0h-2v2h2v-2zM9 15H8v2h1v-2zm3 0h-2v2h2v-2zm3 0h-2v2h2v-2z"/>
    </svg>
  {/if}
</a>

<style>
  .btn{
    display:inline-flex; align-items:center; justify-content:center; gap:8px;
    width: var(--w); height: var(--h);
    padding: var(--pad);
    border-radius: var(--radius);
    text-decoration: none; user-select: none;
    background: var(--bg);
    background-blend-mode: var(--blend);
    color: var(--fg);
    border: 1px solid var(--border);
    box-shadow: 0 1px 2px rgba(0,0,0,.15);
    transition: filter .12s ease, transform .06s ease;
  }
  .btn:hover { filter: brightness(1.05); }
  .btn:active { transform: translateY(1px); }
  .btn[aria-disabled="true"]{ opacity:.6; pointer-events:none; }

  .icon { width: 18px; height: 18px; fill: currentColor; flex: 0 0 auto; }
  .label { font: 400 14px/20px Inter, system-ui, Arial, sans-serif; letter-spacing: .16px; }
</style>