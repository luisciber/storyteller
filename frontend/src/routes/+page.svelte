<script lang="ts">
	import { goto } from '$app/navigation';
	import { listStoriesApiStoriesGet } from '$lib/api/services.gen';
	import type { Story } from '$lib/api/types.gen';
	import { AspectRatio } from '$lib/components/ui/aspect-ratio';
	import { Button } from '$lib/components/ui/button';
	import * as Card from '$lib/components/ui/card';
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';

	let stories: Story[] = [];

	onMount(async () => {
		try {
			const response = await listStoriesApiStoriesGet();
			stories = response.data ?? [];
		} catch (error) {
			console.error('Error al obtener las historias:', error);
			toast.error('Error al obtener las historias');
		}
	});

	function navigateToCreateStory() {
		goto('/create-story');
	}

	function navigateToStory(id: string) {
		goto(`/story/${id}`);
	}
</script>

<main class="container mx-auto p-4">
	<div class="flex items-center justify-between">
		<h1 class="text-paper mb-6 text-3xl font-bold">StoryTeller</h1>

		<div class="mb-4">
			<Button on:click={navigateToCreateStory}>Generar Nueva Historia</Button>
		</div>
	</div>

	<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
		{#each stories as story}
			<Card.Root class="flex flex-col">
				<Card.Header>
					<Card.Title class="text-paper">{story.title}</Card.Title>
					<Card.Description class="flex gap-2">
						<p>Género: {story.preferences.genre}</p>
					</Card.Description>
				</Card.Header>
				<Card.Content class="flex h-full flex-col gap-4">
					<AspectRatio ratio={16 / 9} class="bg-muted">
						<img src={story.image_url} alt={story.title} class="rounded-lg" />
					</AspectRatio>

					<p class="text-paper h-full">{story.premise}</p>
				</Card.Content>
				<Card.Footer class="flex justify-end">
					<Button on:click={() => navigateToStory(story.id!)}>Ver Historia</Button>
				</Card.Footer>
			</Card.Root>
		{/each}
	</div>
</main>
