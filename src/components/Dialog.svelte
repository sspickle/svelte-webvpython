<script lang="ts">
	import { getContext } from 'svelte';
	export let message: string;
	export let onCancel = () => {};
	export let onOkay = () => {};

	function _onCancel() {
		onCancel();
	}

	function _onOkay() {
		onOkay();
	}
</script>

<h2>{message}</h2>

<div class="buttons">
	<button on:click={_onCancel}> No Thanks </button>
	<button on:click={_onOkay}> Yes, Please </button>
</div>

<style>
	h2 {
		font-size: 2rem;
		text-align: center;
	}

	.buttons {
		display: flex;
		justify-content: space-between;
	}
</style>
