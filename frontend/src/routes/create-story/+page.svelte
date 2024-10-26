<script lang="ts">
	import { createStoryEndpointApiStoriesPost } from '$lib/api/services.gen';
	import type { UserPreferences } from '$lib/api/types.gen';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as Select from '$lib/components/ui/select';
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
		{ value: 'mystery', label: 'Misterio' }
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

	async function handleSubmit() {
		userPreferences.genre = selectedGenre.label!;
		userPreferences.length = selectedLength.label!;
		userPreferences.themes_to_include = themesToInclude.split(',').map((theme) => theme.trim());
		userPreferences.themes_to_avoid = themesToAvoid.split(',').map((theme) => theme.trim());

		try {
			const response = await createStoryEndpointApiStoriesPost({ body: userPreferences });
			console.log('Historia creada:', response.data);
			toast.success('Historia creada correctamente');
		} catch (error) {
			console.error('Error al crear la historia:', error);
			toast.error('Error al crear la historia');
		}
	}
</script>

<main class="container mx-auto p-4">
	<h1 class="mb-6 text-3xl font-bold">Generador de Historias</h1>

	<form on:submit|preventDefault={handleSubmit} class="space-y-4">
		<div>
			<Label for="genre">Género</Label>
			<Select.Root bind:selected={selectedGenre}>
				<Select.Trigger>
					<Select.Value placeholder="Selecciona un género" />
				</Select.Trigger>
				<Select.Content>
					{#each genres as genre}
						<Select.Item value={genre.value}>{genre.label}</Select.Item>
					{/each}
				</Select.Content>
			</Select.Root>
		</div>

		<div>
			<Label for="length">Longitud</Label>
			<Select.Root bind:selected={selectedLength}>
				<Select.Trigger>
					<Select.Value placeholder="Selecciona la longitud" />
				</Select.Trigger>
				<Select.Content>
					{#each lengths as length}
						<Select.Item value={length.value}>{length.label}</Select.Item>
					{/each}
				</Select.Content>
			</Select.Root>
		</div>

		<div>
			<Label for="style">Estilo de escritura</Label>
			<Input
				type="text"
				id="style"
				bind:value={userPreferences.style}
				placeholder="Descriptivo, Conciso, Poético, etc."
			/>
		</div>

		<div class="flex flex-col gap-2">
			<Label for="themes_to_include">Temas a incluir (separados por comas)</Label>
			<Input
				type="text"
				id="themes_to_include"
				bind:value={themesToInclude}
				placeholder="Amor, Aventura, Misterio"
			/>
		</div>

		<div class="flex flex-col gap-2">
			<Label for="themes_to_avoid">Temas a evitar (separados por comas)</Label>
			<Input
				type="text"
				id="themes_to_avoid"
				bind:value={themesToAvoid}
				placeholder="Violencia, Guerra, Política"
			/>
		</div>

		<div class="flex flex-col gap-2">
			<Label for="art_style">Estilo artístico para las imágenes</Label>
			<Input
				type="text"
				id="art_style"
				bind:value={userPreferences.art_style}
				placeholder="Realista, Cartoon, Acuarela, etc."
			/>
		</div>

		<div class="flex justify-end">
			<Button type="submit">Generar Historia</Button>
		</div>
	</form>
</main>
