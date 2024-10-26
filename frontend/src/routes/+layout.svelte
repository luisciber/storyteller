<script lang="ts">
	import { env } from '$env/dynamic/public';
	import { client } from '$lib/api';
	import { Toaster } from '$lib/components/ui/sonner';
	import '../app.css';

	client.setConfig({ baseUrl: env.PUBLIC_API_URL });
	let { children } = $props();
</script>

<nav class="sticky top-0 z-10 bg-gray-800 p-4 shadow-md">
	<div class="container mx-auto flex items-center justify-between">
		<a href="/" class="text-paper text-xl font-bold text-white">StoryTeller</a>
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

<style>
	:global(body) {
		background-color: #f4f4f4;
		color: #333;
	}

	:global(.text-paper) {
		font-family: 'Georgia', serif;
	}

	:global {
		.clearfix::after {
			content: '';
			display: table;
			clear: both;
		}
	}
</style>
