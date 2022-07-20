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
	import { cloudDocStore, type ICloudDocStore } from '../stores/cloudDocStore';
	import { onDestroy } from 'svelte';
	import GoogleButton from '../components/GoogleButton.svelte';

	const SCOPES =
		'https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.metadata https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.metadata.readonly';

	let docMeta: any = null; // metadata for the docid we're editing
	const driveUploadPath = 'https://www.googleapis.com/upload/drive/v3/files';

	let isSignedIn: boolean = false;

	let divEl: HTMLDivElement | null = null;
	let editor: monaco.editor.IStandaloneCodeEditor;
	let Monaco;
	let runLink: HTMLAnchorElement | null = null;
	let loaded_doc = '';

	let savedComment = '';

	let unsubscribe = cloudDocStore.subscribe((currDocStore: ICloudDocStore) => {
		if (currDocStore.doc_id != loaded_doc) {
			loadFileIntoSrcStore(currDocStore.doc_id);
		}
	});

	onDestroy(unsubscribe);

	const loadFileIntoSrcStore = async (docid: string) => {
		savedComment = 'loading file...';
		try {
			await readFile(docid, (body: string) => {
				srcStore.set(body);
				editor.setValue(body);
				loaded_doc = docid;
				savedComment = '';
			});
		} catch (e) {
			console.log('error reading file', e);
			savedComment = 'Error reading file, maybe log in?';
		}
	};

	const saveFile = () => {
		savedComment = '(saving....)';
		updateFile(loaded_doc);
	};

	async function readFile(fileId: string, callback: (body: string) => void) {
		let request = gapi.client.drive.files.get({
			fileId: fileId,
			alt: 'media'
		});
		request.then(
			function (response) {
				if (typeof callback === 'function') callback(response.body);
			},
			function (error) {
				console.log(error);
			}
		);
		request = gapi.client.drive.files.get({
			fileId: fileId,
			fields: '*'
		});
		request.then(function (response) {
			docMeta = response.result;
		});
	}

	function updateFile(driveId: string) {
		return new Promise((resolve, reject) => {
			gapi.client
				.request({
					path: driveUploadPath + '/' + driveId,
					method: 'PATCH',
					params: { uploadType: 'media' },
					headers: {
						'Content-Type': 'text/plain'
					},
					body: $srcStore
				})
				.then((response) => {
					savedComment = '(saved!)';
				})
				.catch((error) => {
					reject(console.log(error));
					savedComment = '(error!)';
				});
		});
	}

	let toggleDefaultImports = () => {
		let newUseDefaults = !$prefsStore.add_default_imports;
		prefsStore.set({ ...$prefsStore, add_default_imports: newUseDefaults });
	};

	onMount(async () => {
		// @ts-ignore
		document.addEventListener('visibilitychange', (event) => {
			// when tab becomes active, set focus on the editor
			if (document.visibilityState == 'visible') {
				editor.focus();
			}
		});

		document.onkeydown = (e) => {
			if (e.key === 'm' && e.ctrlKey) {
				e.preventDefault();
				if (runLink) {
					runLink.click();
				}
			}
		};

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

		const params = new URLSearchParams(window.location.search);
		if (params.has('docid')) {
			cloudDocStore.setParamId(<string>params.get('docid'));
		}

		Monaco = await import('monaco-editor');

		editor = Monaco.editor.create(<HTMLElement>divEl, {
			value: $srcStore,
			language: 'python',
			fixedOverflowWidgets: true
		});

		editor.onDidChangeModelContent(() => {
			savedComment = '(unsaved)';
			srcStore.set(editor.getValue());
		});

		return () => {
			editor.dispose();
		};
	});
</script>

<a bind:this={runLink} href="{base}/run" target="_blank">Run this program</a>
<input
	type="checkbox"
	name="default includes"
	checked={$prefsStore.add_default_imports}
	on:change={() => {
		toggleDefaultImports();
	}}
/>
Apply Default Imports

{#if loaded_doc.length > 0}
	<button on:click={saveFile}>Save</button>
	<span
		>(Currently viewing: file:
		{#if docMeta}
			{docMeta.name}
		{:else}
			{loaded_doc}
		{/if})
	</span>
	<span>{savedComment}</span>
{/if}

<GoogleButton {SCOPES} bind:isSignedIn />

<div class="remainder">
	<div class="editor" id="editor" bind:this={divEl} />
</div>

<svelte:head>
	<script async defer src="https://apis.google.com/js/api.js"></script>
	<!--	<script async defer src="https://accounts.google.com/gsi/client"></script> -->
</svelte:head>

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
