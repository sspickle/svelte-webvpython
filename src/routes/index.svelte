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
	import GoogleButton from '../components/googleButton.svelte';
	import { doAuthorize } from '../utils/doAuthorize.js';
	const SCOPES =
		'https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.metadata https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.metadata.readonly';

	let docid = '';
	let docMeta = null;
	const driveUploadPath = 'https://www.googleapis.com/upload/drive/v3/files';

	let auth_token: string = '';
	let isSignedIn: boolean = false;

	let divEl: HTMLDivElement | null = null;
	let editor: monaco.editor.IStandaloneCodeEditor;
	let Monaco;
	let mounted = false;
	let idloaded = '';
	let driveLoaded = false;
	let pickLoaded = false;
	let runLink: HTMLAnchorElement | null = null;
	let savedComment = '';

	$: {
		console.log('checking all three', driveLoaded, pickLoaded, docid.length);
		if (driveLoaded && pickLoaded && docid.length > 0 && isSignedIn && idloaded !== docid) {
			if (!auth_token) {
				doAuthorize((token: string) => {
					auth_token = token;
					loadFileIntoSrcStore(docid);
				}, SCOPES);
			} else {
				loadFileIntoSrcStore(docid);
			}
		}
	}

	function authChanged(isSignedIn: boolean) {
		console.log('authChanged', isSignedIn);
		if (!isSignedIn) {
			auth_token = '';
		}
	}

	const notifyMeFilePicked = (dinfo: any) => {
		docid = dinfo[0].id;
	};

	prefsStore.subscribe((prefs) => {
		console.log('checking prefs', prefs, 'docid', docid, 'prefsDocID', prefs.last_doc_id);
		if (prefs.last_doc_id.length > 0 && prefs.last_doc_id !== docid) {
			docid = prefs.last_doc_id;
		}
	});

	const loadFileIntoSrcStore = async (docid: string) => {
		console.log('in reading file into editor', docid);
		savedComment = 'loading file...';
		try {
			await readFile(docid, (body) => {
				srcStore.set(body);
				editor.setValue(body);
				idloaded = docid;
				savedComment = '';
			});
		} catch (e) {
			console.log('error reading file', e);
			savedComment = 'Error reading file, maybe log in?';
		}
	};

	const saveFile = () => {
		savedComment = '(saving....)';
		console.log('in save', docid, $srcStore);
		updateFile(docid, $srcStore);
	};

	async function readFile(fileId, callback) {
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

	function handleClientLoad() {
		console.log('lib loading');
		gapi.load('client', function () {
			console.log('client loaded, loading drive');
			gapi.client.load(
				'drive',
				'v3',
				function () {
					console.log('drive loaded');
					driveLoaded = true;
				},
				function () {
					console.log('drive load failed');
				}
			);
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

	let toggleDefaultImports = () => {
		let newUseDefaults = !$prefsStore.add_default_imports;
		prefsStore.set({ ...$prefsStore, add_default_imports: newUseDefaults });
	};

	onMount(async () => {
		// @ts-ignore
		console.log('mounting...');
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

		handleClientLoad();

		const params = new URLSearchParams(window.location.search);

		if (params.get('docid')) {
			const paramDocid = params.get('docid') as string;
			console.log('paramDocId', paramDocid);
			if (paramDocid !== docid) {
				console.log('setting perfStore docid', paramDocid);
				prefsStore.set({ ...$prefsStore, last_doc_id: paramDocid });
			}
		} else if ($prefsStore.last_doc_id?.length > 0) {
			docid = $prefsStore.last_doc_id;
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

<!-- {@debug docid, mounted, driveLoaded, pickLoaded} -->

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

{#if docid.length > 0}
	<button on:click={saveFile}>Save</button>
	{#if docid === idloaded}
		<span
			>(Currently viewing: file:
			{#if docMeta}
				{docMeta.name}
			{:else}
				{docid}
			{/if})
		</span>
	{:else}
		<span>wait for file to load</span>
	{/if}
	<span>{savedComment}</span>
{/if}

<GoogleButton
	notifyMe={notifyMeFilePicked}
	bind:auth_token
	bind:isSignedIn
	authCallback={authChanged}
	{SCOPES}
/>

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
