<script lang="ts">
	import type monaco from 'monaco-editor';
	import { onMount } from 'svelte';
	import editorWorker from 'monaco-editor/esm/vs/editor/editor.worker?worker';
	import jsonWorker from 'monaco-editor/esm/vs/language/json/json.worker?worker';
	import cssWorker from 'monaco-editor/esm/vs/language/css/css.worker?worker';
	import htmlWorker from 'monaco-editor/esm/vs/language/html/html.worker?worker';
	import tsWorker from 'monaco-editor/esm/vs/language/typescript/ts.worker?worker';
	import { srcStore } from '../stores/codeSrc.js';
	import { base } from '$app/paths';

	// @ts-ignore
	let divEl: HTMLDivElement | null = null;
	let editor: monaco.editor.IStandaloneCodeEditor;
	let Monaco;

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
			language: 'python'
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
<div class="editor" bind:this={divEl} />

<style>
	.editor {
		width: 100vw;
		height: 100vh;
	}
</style>
