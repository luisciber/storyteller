<script lang="ts">
	import { PUBLIC_API_URL } from '$env/static/public';
	import { client } from '$lib/api';
	import { Toaster } from '$lib/components/ui/sonner';
	import '../app.css';

	client.setConfig({ baseUrl: PUBLIC_API_URL });
	let { children } = $props();
</script>

<nav class="sticky top-0 z-10 bg-gray-800 p-4 shadow-md">
	<div class="container mx-auto flex items-center justify-between">
		<a href="/" class="text-xl font-bold text-white">StoryTeller</a>
		<ul class="flex space-x-4">
			<li><a href="/" class="text-white hover:text-gray-300">Mis Historias</a></li>
			<li><a href="/create-story" class="text-white hover:text-gray-300">Crear Historia</a></li>
		</ul>
	</div>
</nav>

<main class="container mx-auto mt-4">
	{@render children()}
</main>

<Toaster />
