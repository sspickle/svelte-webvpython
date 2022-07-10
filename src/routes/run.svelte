<script lang="ts">
	import { stdoutStore } from '../stores/stdoutSrc';
	import { srcStore } from '../stores/codeSrc';
	import { onMount } from 'svelte';
	import { setupGSCanvas, loadPiodide } from '../utils/utils';

	function redirect_stdout(theText: string) {
		stdoutStore.update((val) => (val += theText + '\n'));
	}

	onMount(async () => {
		scene = await setupGSCanvas();
		pyodide = await loadPiodide(redirect_stdout);
		stdoutStore.set('');
		console.log('mounted', scene, pyodide);
		runMe();
	});

	let pyodide: any = null;
	let program: string;
	let stdout: HTMLTextAreaElement;
	let scene: any;

	srcStore.subscribe((src) => {
		program = src;
		console.log('src loaded');
	});

	stdoutStore.subscribe((text) => {
		console.log('stdout:', text);
		if (stdout) {
			stdout.value = text;
		}
	});

	async function runMe() {
		try {
			if (pyodide) {
				let asyncProgram = program.replace('rate(', 'await async_rate(');
				await pyodide.loadPackagesFromImports(asyncProgram);
				var result = await pyodide.runPythonAsync(asyncProgram);
				stdoutStore.update((value) => (value += result));
			}
		} catch (err) {
			console.log('Error:' + err);
			stdoutStore.update((value) => (value += 'Error:' + err + '\n'));
		}
	}
</script>

<a href="/">Edit this code</a>
<h2>Running....</h2>
<div id="glowscript" class="glowscript" />
<div><textarea bind:this={stdout} rows="20" cols="80" /></div>
