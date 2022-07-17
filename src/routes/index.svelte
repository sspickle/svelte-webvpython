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
	import { googleClient } from '../services/google-service';
	import { currentUser, handelAuthIn, handleSignOut } from '../services/auth-service';

	let gapiCalled = false;
	let fileRead = false;
	let docid = '';
	const driveUploadPath = 'https://www.googleapis.com/upload/drive/v3/files';
	// @ts-ignore
	let divEl: HTMLDivElement | null = null;
	let editor: monaco.editor.IStandaloneCodeEditor;
	let Monaco;
	let mounted = false;
	let savedComment = '';

	currentUser.subscribe((user) => {
		if (user) {
			if (gapiCalled && docid && !fileRead) {
				readFileIntoEditor();
			}
		}
	});

	const readFileIntoEditor = () => {
		console.log('in reading file into editor', docid);
		readFile(docid, (body) => {
			srcStore.set(body);
		});
	};

	const saveFile = () => {
		savedComment = '(saving....)';
		console.log('in save', docid, $srcStore);
		updateFile(docid, $srcStore);
	};

	function readFile(fileId, callback) {
		var request = gapi.client.drive.files.get({
			fileId: fileId,
			alt: 'media'
		});
		request.then(
			function (response) {
				console.log(response); //response.body contains the string value of the file
				if (typeof callback === 'function') callback(response.body);
			},
			function (error) {
				console.log(error);
			}
		);
		return request;
	}

	function updateFile(driveId, newData) {
		return new Promise((resolve, reject) => {
			gapi.client
				.request({
					path: driveUploadPath + '/' + driveId,
					method: 'PATCH',
					params: { uploadType: 'media' },
					body: $srcStore
				})
				.then((response) => {
					resolve(console.log(response));
					savedComment = '(saved!)';
				})
				.catch((error) => {
					reject(console.log(error));
					savedComment = '(error!)';
				});
		});
	}

	function handleClientLoad() {
		if (!gapiCalled) {
			console.log('lib loaded');
			gapi.load('client:auth2', googleClient);
			gapi.load('client', function () {
				gapi.client.load('drive', 'v2', function () {
					console.log('drive loaded');
					gapiCalled = true;
					if (gapiCalled && docid && !fileRead) {
						foo();
					} else {
						console.log('gapi is ready but docid is not ready');
					}
				});
			});
		}
	}

	let toggleDefaultImports = () => {
		let newUseDefaults = !$prefsStore.add_default_imports;
		prefsStore.set({ ...$prefsStore, add_default_imports: newUseDefaults });
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
			savedComment = '(unsaved)';
			srcStore.set(editor.getValue());
		});

		mounted = true;
		console.log('Mounted!');

		if (!gapiCalled) {
			handleClientLoad();
		}

		const params = new URLSearchParams(window.location.search);
		console.log(params.get('docid'));
		if (params.get('docid')) {
			docid = params.get('docid');
			prefsStore.set({ ...$prefsStore, last_doc_id: docid });
			if (gapiCalled && docid && !fileRead) {
				readFileIntoEditor();
			} else {
				console.log('docid is ready, but gapi is not ready');
			}
		} else if ($prefsStore.last_doc_id.length > 0) {
			docid = $prefsStore.last_doc_id;
			if (gapiCalled && docid && !fileRead) {
				readFileIntoEditor();
			} else {
				console.log('docid is ready, but gapi is not ready');
			}
		}

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

{#if docid.length > 0 && $currentUser}
	<button on:click={saveFile}>Save</button>

	<span>Currently editing: gid: {docid} </span>

	<span>{savedComment}</span>
{/if}

{#if $currentUser}
	<div>
		<h4>Logged in as: {$currentUser.name}</h4>
		<button on:click={handleSignOut}>Logout</button>
	</div>
{:else}
	<span>No user</span>
	<button on:click={handelAuthIn}>Login</button>
{/if}

<div class="remainder">
	<div class="editor" id="editor" bind:this={divEl} />
</div>

<svelte:head>
	<script async defer src="https://apis.google.com/js/api.js"></script>
</svelte:head>

<style>
	.remainder {
		display: flex;
		flex-direction: column;
		height: 80vh;
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
