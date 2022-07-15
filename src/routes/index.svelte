<script lang="ts">
	import type monaco from 'monaco-editor';
	import { onMount } from 'svelte';
	import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker';
	import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker';
	import cssWorker from 'monaco-editor/esm/vs/language/css/css.worker?worker';
	import htmlWorker from 'monaco-editor/esm/vs/language/html/html.worker?worker';
	import tsWorker from 'monaco-editor/esm/vs/language/typescript/ts.worker?worker';
	import { srcStore } from '../stores/codeSrc.js';
	import { prefsStore } from '../stores/prefs.js';
	import { base } from '$app/paths';

	// @ts-ignore
	let divEl: HTMLDivElement | null = null;
	let editor: monaco.editor.IStandaloneCodeEditor;
	let Monaco;

	let toggleDefaultImports = () => {
		let newUseDefaults = !$prefsStore.add_default_imports;
		prefsStore.set({ add_default_imports: newUseDefaults });
	};

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
			value: $srcStore,
			language: 'python',
			fixedOverflowWidgets: true
		});

		editor.onDidChangeModelContent(() => {
			srcStore.set(editor.getValue());
		});

		return () => {
			editor.dispose();
		};
	});
</script>

<a href="{base}/run">Run this program</a>
<input
	type="checkbox"
	name="default includes"
	checked={$prefsStore.add_default_imports}
	on:change={() => {
		toggleDefaultImports();
	}}
/>
Apply Default Imports
<div class="remainder">
	<div class="editor" id="editor" bind:this={divEl} />
</div>

<style>
	.remainder {
		display: flex;
		flex-direction: column;
		height: 100vh;
		margin: 0;
	}

	.remainder #editor {
		flex-grow: 1;
	}

	.editor {
		overflow: auto;
		max-width: 100%;
		max-height: 100%;
	}
</style>
