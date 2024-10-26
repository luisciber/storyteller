<script lang="ts">
	import { page } from '$app/stores';
	import { getStoryByIdApiStoriesStoryIdGet } from '$lib/api/services.gen';
	import type { Story } from '$lib/api/types.gen';
	import Modal from '$lib/components/ui/modal.svelte';
	import { Loader2 } from 'lucide-svelte';
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { fade, fly } from 'svelte/transition';

	let story: Story | null = null;
	let selectedImage: string | null = null;
	let selectedAudio: string | null | undefined = null;
	let loading = true;

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
		} finally {
			loading = false;
		}
	});

	function openImage(imageUrl: string, audioUrl: string | null | undefined) {
		selectedImage = imageUrl;
		selectedAudio = audioUrl;
	}

	function closeImage() {
		selectedImage = null;
		selectedAudio = null;
	}
</script>

<main class="container mx-auto w-full max-w-5xl p-4">
	{#if loading}
		<div class="flex h-64 items-center justify-center">
			<Loader2 class="text-primary h-16 w-16 animate-spin" />
		</div>
	{:else if story}
		<div class="mb-8 flex w-full items-center justify-between">
			<h1 class="text-paper mb-6 text-center text-4xl font-bold" in:fly={{ y: -20, duration: 500 }}>
				{story.title}
			</h1>

			<button
				class="cursor-pointer border-none bg-transparent p-0"
				on:click={() => openImage(story!.image_url, null)}
			>
				<img
					src={story.image_url}
					alt={story.title}
					class="max-w-[300px] rounded-lg object-cover transition-opacity hover:opacity-90"
				/>
			</button>
		</div>

		{#each story.chapters as chapter, index}
			<section class="mb-12" in:fade={{ duration: 300, delay: index * 100 }}>
				<h2 class="text-paper mb-4 text-2xl font-semibold">{chapter.title}</h2>

				{#if chapter.image_url}
					<div class="clearfix">
						<button
							class="float-left mb-2 mr-4 cursor-pointer border-none bg-transparent p-0"
							on:click={() => openImage(chapter.image_url!, chapter.audio_url)}
						>
							<div class="flex flex-col items-center gap-2">
								<img
									src={chapter.image_url}
									alt={chapter.title}
									class="max-w-[350px] rounded-lg object-cover transition-opacity hover:opacity-90"
								/>
								{#if chapter.audio_url}
									<audio src={chapter.audio_url} controls></audio>
								{/if}
							</div>
						</button>

						<p class="text-paper text-justify leading-relaxed">{chapter.content}</p>
					</div>
				{/if}
			</section>
		{/each}
	{:else}
		<p class="text-paper text-center">No se pudo cargar la historia.</p>
	{/if}
</main>

<Modal on:close={closeImage} isOpen={selectedImage !== null}>
	<div class="flex flex-col items-center gap-4">
		<img src={selectedImage} alt="Imagen ampliada" class="max-h-[90vh] max-w-full object-contain" />
		{#if selectedAudio}
			<audio src={selectedAudio} controls></audio>
		{/if}
	</div>
</Modal>
