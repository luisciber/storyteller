<script lang="ts">
	import { page } from '$app/stores';
	import { getStoryByIdApiStoriesStoryIdGet } from '$lib/api/services.gen';
	import type { Story } from '$lib/api/types.gen';
	import { AspectRatio } from '$lib/components/ui/aspect-ratio';
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';

	let story: Story | null = null;

	onMount(async () => {
		const storyId = $page.params.id;
		try {
			const response = await getStoryByIdApiStoriesStoryIdGet({
				path: {
					story_id: storyId
				}
			});
			story = response.data!;
		} catch (error) {
			console.error('Error al obtener la historia:', error);
			toast.error('Error al cargar la historia');
		}
	});
</script>

<main class="container mx-auto p-4">
	{#if story}
		<h1 class="mb-6 text-3xl font-bold">{story.title}</h1>

		<div class="mb-8">
			<AspectRatio ratio={16 / 9} class="bg-muted">
				<img src={story.image_url} alt={story.title} class="rounded-lg object-cover" />
			</AspectRatio>
		</div>

		<div>
			{#each story.chapters as chapter, index}
				<div class="mb-8 border-b pb-8 last:border-b-0">
					<h3 class="mb-4 text-xl font-semibold">{chapter.title}</h3>
					<div class="mb-6">
						<AspectRatio ratio={16 / 9} class="bg-muted">
							<img src={chapter.image_url} alt={chapter.title} class="rounded-lg object-cover" />
						</AspectRatio>
					</div>
					<p>{chapter.content}</p>
				</div>
			{/each}
		</div>
	{:else}
		<p>Cargando historia...</p>
	{/if}
</main>
