<script lang="ts">
	let initialCode = `
from vpython import *
import numpy as np

import sys
print(sys.version)

r = 2 + 3j
s = sphere(pos=vec(r.real,r.imag,0), color=color.blue, make_trail=True)
print("hello" + f"{abs(3 + 4j)}")

while True:
   rate(30)
   r = r*np.exp(1j*0.05)
   s.pos = vec(r.real, r.imag, 0)
`;
	import type monaco from 'monaco-editor';
	import { onMount } from 'svelte';
	import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker';
	import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker';
	import cssWorker from 'monaco-editor/esm/vs/language/css/css.worker?worker';
	import htmlWorker from 'monaco-editor/esm/vs/language/html/html.worker?worker';
	import tsWorker from 'monaco-editor/esm/vs/language/typescript/ts.worker?worker';
	import { prepGSEnvironment } from '../utils/utils.js';

	// @ts-ignore
	let divEl: HTMLDivElement | null = null;
	let editor: monaco.editor.IStandaloneCodeEditor;
	let Monaco;
	let runButton: HTMLButtonElement | null = null;
	let stdout: HTMLTextAreaElement;

	// @ts-ignore
	let pyodide: any;

	onMount(async () => {
		// @ts-ignore
		self.MonacoEnvironment = {
			getWorker: function (_moduleId: any, label: string) {
				if (label === 'json') {
					return new jsonWorker();
				}
				if (label === 'css' || label === 'scss' || label === 'less') {
					return new cssWorker();
				}
				if (label === 'html' || label === 'handlebars' || label === 'razor') {
					return new htmlWorker();
				}
				if (label === 'typescript' || label === 'javascript') {
					return new tsWorker();
				}
				return new editorWorker();
			}
		};

		Monaco = await import('monaco-editor');
		editor = Monaco.editor.create(<HTMLElement>divEl, {
			value: initialCode,
			language: 'python'
		});

		pyodide = await prepGSEnvironment(redirect_stdout);
		if (runButton) {
			runButton.disabled = false;
		}

		return () => {
			editor.dispose();
		};
	});

	async function runMe() {
		if (runButton) {
			runButton.disabled = true;
			runButton.innerText = 'Running...';
		}
		var program = editor.getValue().split('rate(').join('await async_rate(');
		try {
			await pyodide.loadPackagesFromImports(program);
			var result = await pyodide.runPythonAsync(program);
		} catch (err) {
			console.log('Error:' + err);
		}
	}

	function redirect_stdout(theText: string) {
		stdout.value += theText + '\n';
	}
</script>

<div class="container">
	<div class="buttonCol">
		<button
			bind:this={runButton}
			disabled={true}
			on:click={() => {
				runMe();
			}}>Run</button
		>
	</div>
	<div class="explainRow">
		<p>This is a very crude attempt to demo WebVPython using Pyodide.</p>
		<p>So far we have sphere, cone, box, arrow, helix, rate, and vector.</p>
	</div>
	<div id="glowscript" class="glowscript glowCol">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<script
			type="text/javascript"
			src="https://www.glowscript.org/lib/jquery/2.1/jquery.min.js"></script>
		<script
			type="text/javascript"
			src="https://www.glowscript.org/lib/jquery/2.1/jquery-ui.custom.min.js"></script>
		<script
			type="text/javascript"
			src="https://www.glowscript.org/package/glow.3.2.min.js"></script>
	</div>
	<div class="editCol" bind:this={divEl} />
	<div class="stdoutRow">
		<textarea bind:this={stdout} rows="20" cols="80" />
	</div>
</div>

<style>
	.container {
		display: grid;
		grid-template-columns: 1fr 4fr 4fr;
		grid-template-rows: 1fr 4fr 3fr;
		height: 100vh;
	}

	.explainRow {
		grid-column: 1 / -1;
		grid-row: 1;
		text-align: center;
	}

	.buttonCol {
		grid-column: 1;
		grid-row: 2;
		justify-self: center;
		align-self: center;
	}

	.editCol {
		grid-column: 2;
		grid-row: 2;
		height: 50vh;
		border: 1px solid black;
	}

	.stdoutRow {
		grid-column: 2/4;
		grid-row: 3;
		justify-self: center;
		align-self: center;
	}

	.glowCol {
		grid-column: 3;
		grid-row: 2;
		height: 50vh;
		border: 1px solid black;
	}
</style>
