<script lang="ts" context="module">
	import { page } from '$app/stores';
</script>

<div>{JSON.stringify($page, null, 2)}</div>
