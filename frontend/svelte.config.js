//import adapter from '@sveltejs/adapter-static';
//import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
/*
export default {
  preprocess: vitePreprocess(),
  kit: {
    // SvelteKit will emit 200.html (SPA fallback)
    adapter: adapter({ fallback: '200.html' })
  }
};*/
import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter(),
    // If you need client-side routing fallback:
    prerender: { handleHttpError: 'warn' }
  }
};

export default config;