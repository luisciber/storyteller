<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import { client } from '$lib/api';
	import { Toaster } from '$lib/components/ui/sonner';
	import '../app.css';

	client.setConfig({ baseUrl: PUBLIC_API_URL });
	let { children } = $props();
</script>

<Toaster />

{@render children()}
