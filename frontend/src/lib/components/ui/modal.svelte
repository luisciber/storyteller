<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	export let isOpen = false;

	const dispatch = createEventDispatcher();

	function closeModal() {
		dispatch('close');
	}
</script>

{#if isOpen}
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<div
		class="fixed inset-0 z-50 flex items-center justify-center overflow-y-auto overflow-x-hidden outline-none focus:outline-none"
		on:click|self={closeModal}
		transition:fade
		role="dialog"
		tabindex="-1"
	>
		<div class="relative mx-auto my-6 w-auto max-w-full">
			<div
				class="relative flex w-full flex-col rounded-lg border-0 bg-white shadow-lg outline-none focus:outline-none"
			>
				<div class="flex-auto p-6">
					<slot />
				</div>
			</div>
		</div>
	</div>
	<div class="fixed inset-0 z-40 bg-black opacity-25" transition:fade></div>
{/if}
