<script lang="ts">
	import { browser } from '$app/env';
	import { cloudDocStore } from '$lib/stores/cloudDocStore';
	import { onMount } from 'svelte';
	import { dev } from "$app/env"

	export let isSignedIn = false;
	export let authCallback: ((signedIn: boolean) => void) | null = null;
	export let SCOPES: string = 'email';
	export let signInPending: boolean = false;

	let auth: any;
	let display_picked: string | null = null;

	async function postData(url = '', data = {}) {
	// Default options are marked with *
		const response = await fetch(url, {
				method: 'POST', // *GET, POST, PUT, DELETE, etc.
				mode: 'cors', // no-cors, *cors, same-origin
				cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
				credentials: 'same-origin', // include, *same-origin, omit
				headers: {
					'Content-Type': 'application/json'
					// 'Content-Type': 'application/x-www-form-urlencoded',
				},
				redirect: 'follow', // manual, *follow, error
				referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
				body: JSON.stringify(data) // body data type must match "Content-Type" header
			});
		return response.json(); // parses JSON response into native JavaScript objects
	}

	let CLIENT_ID:string
	let API_ID:string
	let DEV_KEY:string

	let secsLoaded = false;
	let apiLoaded = false

	const getSecs = async () => {
		const secs = await postData('/api',{sec:import.meta.env.VITE_DUMB_SECRET});
		CLIENT_ID = secs.CLIENT_ID;
		API_ID = secs.APP_ID;
		DEV_KEY = secs.API_KEY;
		console.log('keys set')
		secsLoaded = true;
	}
	
	onMount(()=>{
		getSecs();
	});

	$:{ if (signInPending && auth) {
		auth.signIn();
		signInPending = false;
	}}

	$:{ if (secsLoaded && apiLoaded) {
		loadedAPI()
	}}

	const handleAuthChange = () => {
		isSignedIn = auth.isSignedIn.get();
		if (!isSignedIn) {
			cloudDocStore.setAuthId('');
		}
		if (authCallback) {
			authCallback(isSignedIn);
		}
	};

	export const doAuthorize = (SCOPES, cb) => {
	const handleCB = (authResult) => {
		console.log('in auth result...', JSON.stringify(authResult, null, 2));
		if (authResult && !authResult.error) {
			cloudDocStore.setAuthId(authResult.access_token);
			cb(); // call them back!
		}
	};

	gapi.auth.authorize(
			{
				client_id: CLIENT_ID,
				scope: SCOPES,
				immediate: false
			},
			handleCB
		);
	};

	function checkAuthAndPick() {
		if ($cloudDocStore.auth_token.length === 0) {
			doAuthorize(SCOPES, () => {
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
			.setAppId(API_ID)
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
			apiLoaded=true;
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

