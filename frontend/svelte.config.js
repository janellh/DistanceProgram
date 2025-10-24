import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

export default {
  preprocess: vitePreprocess(),
  kit: {
    // SvelteKit will emit 200.html (SPA fallback)
    adapter: adapter({ fallback: '200.html' })
  }
};
