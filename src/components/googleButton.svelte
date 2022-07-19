<script lang="ts">
	import { onMount } from 'svelte';
	import { doAuthorize } from '../utils/doAuthorize.js';
	export let isSignedIn = false;
	let auth: any;
	export let auth_token: string | null = null;
	let display_picked: string | null = null;
	export let authCallback: ((signedIn: boolean) => void) | null = null;
	export let SCOPES: string = 'email';
	export let notifyMe: (dinfo: any) => void;

	const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
	const APP_ID = import.meta.env.VITE_GOOGLE_APP_ID;
	const DEV_KEY = import.meta.env.VITE_GOOGLE_API_KEY;

	const handleAuthChange = () => {
		isSignedIn = auth.isSignedIn.get();
		console.log('isSignedIn', isSignedIn);
		if (!isSignedIn) {
			auth_token = null;
		}
		if (authCallback) {
			authCallback(isSignedIn);
		}
	};

	function checkAuthAndPick() {
		if (!auth_token) {
			doAuthorize((token: string) => {
				auth_token = token;
				createPicker();
			});
		} else {
			createPicker();
		}
	}

	onMount(() => {
		gapi.load('client:auth2', () => {
			gapi.client
				.init({
					clientId: CLIENT_ID,
					scope: SCOPES
				})
				.then(() => {
					auth = window.gapi.auth2.getAuthInstance();
					console.log('we have auth now');
					handleAuthChange();
					auth.isSignedIn.listen(handleAuthChange);
				})
				.catch((err) => {
					console.log('error', err);
				});
			gapi.client.load(
				'drive',
				'v3',
				function () {
					console.log('drive loaded');
				},
				function () {
					console.log('drive load failed');
				}
			);
		});
		gapi.load(
			'picker',
			() => {
				console.log('picker loaded');
			},
			() => {
				console.log('picker failed to load');
			}
		);
	});

	function createPicker() {
		const view = new google.picker.DocsView(google.picker.ViewId.DOCS);
		//view.setMimeTypes('text/plain');
		view.setIncludeFolders(true);
		view.setQuery('*.py');
		const picker = new google.picker.PickerBuilder()
			.setDeveloperKey(DEV_KEY)
			.setAppId(APP_ID)
			.setOAuthToken(auth_token)
			.addView(view)
			.setCallback(pickerCallback)
			.setMaxItems(1)
			.build();
		picker.setVisible(true);
	}

	/**
	 * Displays the file details of the user's selection.
	 * @param {object} data - Containers the user selection from the picker
	 */
	function pickerCallback(data) {
		if (data.action === google.picker.Action.PICKED) {
			notifyMe(data.docs);
		}
	}
</script>

{#if isSignedIn}
	<button on:click={() => auth.signOut()}>Sign out</button>
	<button on:click={() => checkAuthAndPick()}>Open File</button>
{:else}
	<button on:click={() => auth.signIn()}>Sign in</button>
{/if}

{#if display_picked}
	<p>{display_picked}</p>
{/if}
