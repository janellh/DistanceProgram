// svelte.config.js
import adapter from '@sveltejs/adapter-static';
//import { vitePreprocess } from '@sveltejs/kit/vite';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
  preprocess: vitePreprocess(),
  kit: {
    // Generate an SPA bundle with a 200.html fallback (for client-side routing)
    adapter: adapter({ fallback: '200.html' }),
    // Don’t prerender routes; we’re a pure SPA
    prerender: { entries: [] }
  }
};