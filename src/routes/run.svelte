<script lang="ts">
	import { stdoutStore } from '../stores/stdoutSrc';
	import { srcStore } from '../stores/codeSrc';
	import { prefsStore } from '../stores/prefs';
	import { onMount } from 'svelte';
	import { setupGSCanvas, getPyodide } from '../utils/utils';
	import { base } from '$app/paths';

	function redirect_stdout(theText: string) {
		if (mounted) {
			stdoutStore.update((val) => (val += theText + '\n'));
		}
	}

	function redirect_stderr(theText: string) {
		if (mounted) {
			stdoutStore.update((val) => (val += 'stderr:' + theText + '\n'));
		}
	}

	let pyodide: any = null;
	let program: string;
	let stdout: HTMLTextAreaElement;
	let scene: any;
	let mounted: boolean = false;
	let applyDefaultImports: boolean = $prefsStore.add_default_imports;
	let pyodideURL = 'https://cdn.jsdelivr.net/pyodide/v0.21.0a3/full/'; //'https://cdn.jsdelivr.net/pyodide/v0.21.0a3/full/',

	let defaultImportCode = `from math import *
from numpy import arange
from random import random
from vpython import *
`;

	onMount(async () => {
		try {
			scene = await setupGSCanvas();
			pyodide = await getPyodide(redirect_stdout, redirect_stderr, pyodideURL);
		} catch (e) {
			redirect_stderr(JSON.stringify(e));
		}

		if (pyodide) {
			//@ts-ignore
			window.scene = scene;
			//@ts-ignore
			window.__reportScriptError = (err) => {
				try {
					redirect_stderr('__reportScriptError:' + JSON.stringify(err));
				} catch (err) {
					redirect_stderr('__reportScriptError: Not sure! Cannot stringify');
				}
				debugger;
			};
			stdoutStore.set('');
			mounted = true;
			runMe();
			return () => {
				mounted = false;
			};
		} else {
			redirect_stderr('Pyodide not found');
		}
	});

	srcStore.subscribe((src) => {
		program = src;
	});

	stdoutStore.subscribe((text) => {
		if (stdout) {
			if (text.length > 0 && stdout.hasAttribute('hidden')) {
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
				if (applyDefaultImports) {
					await pyodide.loadPackagesFromImports(defaultImportCode);
					var result = await pyodide.runPythonAsync(defaultImportCode);
				}
				let foundTextConstructor = asyncProgram.match(/[^\.\w]text[\ ]*\(/);
				if (foundTextConstructor) {
					//@ts-ignore
					window.fontloading();
					//@ts-ignore
					await window.waitforfonts();
				}
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
