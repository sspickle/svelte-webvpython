<script lang="ts">
	import { stdoutStore } from '../stores/stdoutSrc';
	import { srcStore } from '../stores/codeSrc';
	import { onMount } from 'svelte';
	import { setupGSCanvas, loadPiodide } from '../utils/utils';
	import { base } from '$app/paths';

	function redirect_stdout(theText: string) {
		if (mounted) {
			stdoutStore.update((val) => (val += theText + '\n'));
		}
	}

	let pyodide: any = null;
	let program: string;
	let stdout: HTMLTextAreaElement;
	let scene: any;
	let mounted: boolean = false;

	onMount(async () => {
		scene = await setupGSCanvas();
		pyodide = await loadPiodide(redirect_stdout);

		//@ts-ignore
		window.scene = scene;
		//@ts-ignore
		window.__reportScriptError = (err) => {
			redirect_stdout('REPORT ERROR:' + JSON.stringify(err));
		};
		stdoutStore.set('');
		mounted = true;
		runMe();
		return () => {
			mounted = false;
		};
	});

	srcStore.subscribe((src) => {
		program = src;
	});

	stdoutStore.subscribe((text) => {
		if (stdout) {
			if (text.length > 0) {
				console.log('in stdout update:', text);
				stdout.removeAttribute('hidden');
			}
			stdout.value = text;
			stdout.scrollTop = stdout.scrollHeight;
		}
	});

	async function runMe() {
		try {
			if (pyodide) {
				let asyncProgram = program.replace(/[^\.\w\n]rate[\ ]*\(/g, ' await rate('); // replace ` rate(` with `async async_rate(`
				asyncProgram = asyncProgram.replace(/\n]rate[\ ]*\(/g, '\n await rate('); // replace '\nrate(` with `\nasync async_rate(`
				asyncProgram = asyncProgram.replace(/[^\.\w]text[\ ]*\(/g, 'await text('); // replace `text(` with `async text(`
				await pyodide.loadPackagesFromImports(asyncProgram);
				var result = await pyodide.runPythonAsync(asyncProgram);
				if (result) {
					stdoutStore.update((value) => (value += result));
				}
			}
		} catch (err) {
			console.log('Error:' + err);
			stdoutStore.update((value) => (value += 'Error:' + err + '\n'));
		}
	}
</script>

<a href="{base}/" target="_self">Edit this code</a>
<h2>Running....</h2>
<div id="glowscript" class="glowscript" />
<div><textarea bind:this={stdout} rows="10" cols="80" hidden /></div>
