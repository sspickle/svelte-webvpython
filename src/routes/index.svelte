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
	import { currentUser, handleAuthClick, handleSignoutClick } from '../services/auth-service';

	let gapiCalled = false;
	let fileRead = false;
	let docid = '';
	let driveLoaded = false;
	let pickLoaded = false;
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

	prefsStore.subscribe((prefs) => {
		if (mounted && prefs.last_doc_id.length > 0 && prefs.last_doc_id !== docid) {
			docid = prefs.last_doc_id;
			loadFileIntoSrcStore(docid);
		}
	});

	const loadFileIntoSrcStore = async (docid: string) => {
		console.log('in reading file into editor', docid);
		if (driveLoaded) {
			await readFile(docid, (body) => {
				srcStore.set(body);
				editor.setValue(body);
				savedComment = '';
			});
		} else {
			console.log('drive not loaded, cannot read file');
		}
	};

	const saveFile = () => {
		savedComment = '(saving....)';
		console.log('in save', docid, $srcStore);
		updateFile(docid, $srcStore);
	};

	async function readFile(fileId, callback) {
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
					headers: {
						'Content-Type': 'text/plain'
					},
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

	function createPicker() {
		editor.setValue('');
		const view = new google.picker.DocsView(google.picker.ViewId.DOCS);
		//view.setMimeTypes('text/plain');
		view.setIncludeFolders(true);
		view.setQuery('*.py');
		const picker = new google.picker.PickerBuilder()
			.setDeveloperKey(import.meta.env.VITE_GOOGLE_API_KEY)
			.setAppId(import.meta.env.VITE_GOOGLE_APP_ID)
			.setOAuthToken($currentUser.token)
			.addView(view)
			.setCallback(pickerCallback)
			.build();
		picker.setVisible(true);
	}

	/**
	 * Displays the file details of the user's selection.
	 * @param {object} data - Containers the user selection from the picker
	 */
	function pickerCallback(data) {
		if (data.action === google.picker.Action.PICKED) {
			prefsStore.set({ ...$prefsStore, last_doc_id: data.docs[0].id });
		}
	}

	function handleClientLoad() {
		if (!gapiCalled) {
			console.log('lib loading');
			gapi.load('client', function () {
				console.log('client loaded, loading drive');
				gapi.client.load('drive', 'v3', function () {
					console.log('drive loaded');
					driveLoaded = true;
				});
				console.log('loading picker');
				gapi.load(
					'picker',
					() => {
						console.log('picker loaded');
						pickLoaded = true;
					},
					() => {
						console.log('picker failed to load');
					}
				);
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

		if (!gapiCalled) {
			await handleClientLoad();
		}

		const params = new URLSearchParams(window.location.search);
		console.log(params.get('docid'));

		if (params.get('docid')) {
			const paramDocid = params.get('docid') as string;
			if (paramDocid !== docid) {
				prefsStore.set({ ...$prefsStore, last_doc_id: paramDocid });
			}
		} else if ($prefsStore.last_doc_id?.length > 0) {
			docid = $prefsStore.last_doc_id;
			loadFileIntoSrcStore(docid);
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

		mounted = true;
		console.log('Mounted!');

		return () => {
			editor.dispose();
		};
	});
</script>

<a href="{base}/run" target="_blank">Run this program</a>
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
		<h4>Logged in</h4>
		<button on:click={handleSignoutClick}>Logout</button>
		<button on:click={createPicker}>Open File</button>
	</div>
{:else}
	<span>No user</span>
	<button on:click={() => handleAuthClick()}>Login</button>
{/if}

<div class="remainder">
	<div class="editor" id="editor" bind:this={divEl} />
</div>

<svelte:head>
	<script async defer src="https://apis.google.com/js/api.js"></script>
	<script async defer src="https://accounts.google.com/gsi/client"></script>
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
