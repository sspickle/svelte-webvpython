<script lang="ts">
	import { doAuthorize } from '../utils/doAuthorize.js';
	import { browser } from '$app/env';
	import { cloudDocStore } from '../stores/cloudDocStore';
	import { onDestroy } from 'svelte';

	export let isSignedIn = false;
	export let authCallback: ((signedIn: boolean) => void) | null = null;
	export let SCOPES: string = 'email';

	let auth: any;
	let display_picked: string | null = null;

	const CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
	const APP_ID = import.meta.env.VITE_GOOGLE_APP_ID;
	const DEV_KEY = import.meta.env.VITE_GOOGLE_API_KEY;

	const handleAuthChange = () => {
		isSignedIn = auth.isSignedIn.get();
		if (!isSignedIn) {
			cloudDocStore.setAuthId('');
		}
		if (authCallback) {
			authCallback(isSignedIn);
		}
	};

	function checkAuthAndPick() {
		if ($cloudDocStore.auth_token.length === 0) {
			doAuthorize(SCOPES, (token: string) => {
				cloudDocStore.setAuthId(token);
				createPicker();
			});
		} else {
			createPicker();
		}
	}

	function createPicker() {
		const view = new google.picker.DocsView(google.picker.ViewId.DOCS);
		view.setIncludeFolders(true);
		const picker = new google.picker.PickerBuilder()
			.setDeveloperKey(DEV_KEY)
			.setAppId(APP_ID)
			.setOAuthToken($cloudDocStore.auth_token)
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
			cloudDocStore.setPickedId(data.docs[0].id);
		}
	}

	const loadedAPI = async () => {
		try {
			await new Promise((res, rej) => {
					gapi.load("client:auth2", {callback: res, onerror: rej});
				});
			
			await gapi.client.init({
							clientId: CLIENT_ID,
							scope: SCOPES
						});
			auth = window.gapi.auth2.getAuthInstance();
			handleAuthChange();
			auth.isSignedIn.listen(handleAuthChange);

			gapi.load(
				'picker',
				() => {
					cloudDocStore.setPickerLoaded();
				},
				() => {
					console.log('picker failed to load');
				}
			);

			gapi.client.load(
				'drive',
				'v3', ()=> {
					console.log("drive loaded");
					cloudDocStore.setDriveLoaded()
				}
			);
		} catch (e) {
			console.error(e);
		}
	}

</script>

<svelte:head>
	{#if browser}
	<script defer async
		src="https://apis.google.com/js/api.js"
		on:load={() => {
			loadedAPI();
		}}></script>
	{/if}
</svelte:head>

{#if isSignedIn}
	<button on:click={() => auth.signOut()}>Sign out</button>
	<button on:click={() => checkAuthAndPick()}>Open File</button>
{:else}
	<button on:click={() => auth.signIn()}>Sign in</button>
{/if}

{#if display_picked}
	<p>{display_picked}</p>
{/if}

