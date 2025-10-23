<script lang="ts">
  import { page } from '$app/stores';
  import Button from '$lib/components/Button.svelte';

  export let showSwitch = true;

  $: pathname = $page.url.pathname;
  $: onHistory = pathname.startsWith('/history');
  $: switchHref = onHistory ? '/' : '/history';
  $: switchLabel = onHistory ? 'Go to Calculator' : 'View Historical Queries';

  // NEW: toggle icon + colors for history
  $: switchIcon = onHistory ? 'calculator' : 'recently-viewed';
  $: switchBg   = onHistory ? '#FFFFFF' : 'var(--Button-button-secondary, #313030)';
  $: switchFg   = onHistory ? '#222222' : '#FFFFFF';
  $: switchBlend = onHistory ? 'multiply' : 'normal';
</script>

<div class="header-wrap">
  <header class="header container">
    <div class="headline">
      <h1 class="title">Distance Calculator</h1>
      <p class="subtitle">Prototype web application for calculating the distance between addresses.</p>
    </div>

    {#if showSwitch}
      <Button
        text={switchLabel}
        href={switchHref}
        icon={switchIcon}
        width={237}
        height={48}
        padding={3}
        radius={0}
        bg={switchBg}
        fg={switchFg}
        blend={switchBlend}
      />
    {/if}
  </header>
</div>

<style>
  .header-wrap {
    background:#F8F8F6;
  }
  .header {
    display:flex;
    justify-content:space-evenly;
    align-items:center;
    gap:16px;
    min-height:100px;
    padding:16px;
    box-sizing:border-box;
    font-family: Inter, system-ui, Arial, sans-serif;
  }
  .headline {
    display:grid;
    gap:8px;
    max-width:963px;
  }
  .title {
    margin:0;
    font-weight:300;
    font-size:32px;
    line-height:40px;
    color:#222222;
  }
  .subtitle {
    margin:0;
    font-weight:400;
    font-size:14px;
    line-height:20px;
    letter-spacing:.16px;
    color:#4B4949;
  }
</style>