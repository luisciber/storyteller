<script lang="ts">
	import { goto } from '$app/navigation';
	import { createStoryEndpointApiStoriesPost } from '$lib/api/services.gen';
	import type { UserPreferences } from '$lib/api/types.gen';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import Modal from '$lib/components/ui/modal.svelte';
	import * as Select from '$lib/components/ui/select';
	import Icon from '@iconify/svelte';
	import type { Selected } from 'bits-ui';
	import { toast } from 'svelte-sonner';

	let userPreferences: UserPreferences = {
		genre: '',
		length: '',
		style: '',
		themes_to_include: [],
		themes_to_avoid: [],
		art_style: ''
	};

	const genres: Selected<string>[] = [
		{ value: 'fantasy', label: 'Fantasía' },
		{ value: 'scifi', label: 'Ciencia Ficción' },
		{ value: 'romance', label: 'Romance' },
		{ value: 'mystery', label: 'Misterio' },
		{ value: 'horror', label: 'Terror' },
		{ value: 'thriller', label: 'Suspense' },
		{ value: 'historical', label: 'Histórica' },
		{ value: 'adventure', label: 'Aventura' },
		{ value: 'comedy', label: 'Comedia' },
		{ value: 'drama', label: 'Drama' },
		{ value: 'dystopian', label: 'Distopía' },
		{ value: 'crime', label: 'Policiaca' },
		{ value: 'western', label: 'Western' },
		{ value: 'literary', label: 'Ficción literaria' }
	];

	let selectedGenre: Selected<string>;

	const lengths: Selected<string>[] = [
		{ value: 'short', label: 'Corta' },
		{ value: 'medium', label: 'Media' },
		{ value: 'long', label: 'Larga' }
	];

	let selectedLength: Selected<string>;

	let themesToInclude = '';
	let themesToAvoid = '';

	let isLoading = false;

	function navigateToRoot() {
		goto(`/`);
	}

	async function handleSubmit() {
		isLoading = true;
		userPreferences.genre = selectedGenre?.label ?? '';
		userPreferences.length = selectedLength?.label ?? '';
		userPreferences.themes_to_include = themesToInclude.split(',').map((theme) => theme.trim());
		userPreferences.themes_to_avoid = themesToAvoid.split(',').map((theme) => theme.trim());

		try {
			await createStoryEndpointApiStoriesPost({ body: userPreferences });
			toast.success('Historia creada correctamente');
			navigateToRoot();
		} catch (error) {
			console.error('Error al crear la historia:', error);
			toast.error('Error al crear la historia');
		} finally {
			isLoading = false;
		}
	}
</script>

<main class="container mx-auto h-full w-full max-w-2xl p-4">
	<h1 class="mb-6 text-center text-3xl font-bold">
		<Icon icon="mdi:book-open-page-variant" class="mr-2 inline-block" />
		Generador de Historias
	</h1>

	<form on:submit|preventDefault={handleSubmit} class="space-y-6 rounded-lg bg-white p-6 shadow-md">
		<div class="flex flex-col gap-2">
			<Label for="genre" class="flex items-center">
				<Icon icon="mdi:genre" class="mr-2" />
				Género
			</Label>
			<Select.Root bind:selected={selectedGenre}>
				<Select.Trigger class="w-full">
					<Select.Value placeholder="Selecciona un género" />
				</Select.Trigger>
				<Select.Content>
					{#each genres as genre}
						<Select.Item value={genre.value}>{genre.label}</Select.Item>
					{/each}
				</Select.Content>
			</Select.Root>
		</div>

		<div class="flex flex-col gap-2">
			<Label for="length" class="flex items-center">
				<Icon icon="mdi:ruler" class="mr-2" />
				Longitud
			</Label>
			<Select.Root bind:selected={selectedLength}>
				<Select.Trigger class="w-full">
					<Select.Value placeholder="Selecciona la longitud" />
				</Select.Trigger>
				<Select.Content>
					{#each lengths as length}
						<Select.Item value={length.value}>{length.label}</Select.Item>
					{/each}
				</Select.Content>
			</Select.Root>
		</div>

		<div class="flex flex-col gap-2">
			<Label for="style" class="flex items-center">
				<Icon icon="mdi:pencil" class="mr-2" />
				Estilo de escritura
			</Label>
			<Input
				type="text"
				id="style"
				bind:value={userPreferences.style}
				placeholder="Descriptivo, Conciso, Poético, Humorístico, Narrativo, Periodístico, Académico, etc."
			/>
		</div>

		<div class="flex flex-col gap-2">
			<Label for="themes_to_include" class="flex items-center">
				<Icon icon="mdi:plus-circle-outline" class="mr-2" />
				Temas a incluir (separados por comas)
			</Label>
			<Input
				type="text"
				id="themes_to_include"
				bind:value={themesToInclude}
				placeholder="Amor, Aventura, Misterio, etc."
			/>
		</div>

		<div class="flex flex-col gap-2">
			<Label for="themes_to_avoid" class="flex items-center">
				<Icon icon="mdi:minus-circle-outline" class="mr-2" />
				Temas a evitar (separados por comas)
			</Label>
			<Input
				type="text"
				id="themes_to_avoid"
				bind:value={themesToAvoid}
				placeholder="Violencia, Guerra, Política, etc."
			/>
		</div>

		<div class="flex flex-col gap-2">
			<Label for="art_style" class="flex items-center">
				<Icon icon="mdi:palette" class="mr-2" />
				Estilo artístico para las imágenes
			</Label>
			<Input
				type="text"
				id="art_style"
				bind:value={userPreferences.art_style}
				placeholder="Futurista, Realista, Cartoon, Acuarela, etc."
			/>
		</div>

		<div class="flex justify-end">
			<Button type="submit" disabled={isLoading} class="w-full sm:w-auto">
				<Icon icon="mdi:magic-wand" class="mr-2" />
				Generar Historia
			</Button>
		</div>
	</form>
</main>

<Modal isOpen={isLoading}>
	<div class="flex flex-col items-center justify-center p-4">
		<div
			class="border-primary mb-4 h-12 w-12 animate-spin rounded-full border-4 border-t-4 border-t-transparent"
		></div>
		<p class="text-lg font-semibold">Generando tu historia...</p>
		<p class="mt-2 text-sm text-gray-500">Por favor, espera un momento.</p>
	</div>
</Modal>
