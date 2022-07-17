import { writable } from 'svelte/store';

export interface User {
	token: string | null;
}

let tokenClient: any;
let accessToken: string | null = null;

const SCOPES =
	'https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.metadata https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.metadata.readonly';

export const currentUser = writable<User>();

export function handleAuthClick() {
	if (!tokenClient) {
		tokenClient = google.accounts.oauth2.initTokenClient({
			client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
			scope: SCOPES,
			callback: async (response) => {
				if (response.error !== undefined) {
					throw response;
				}
				accessToken = response.access_token; // defined later
				setCurrentUser();
			}
		});
	}
	if (accessToken === null) {
		// Prompt the user to select a Google Account and ask for consent to share their data
		// when establishing a new session.
		tokenClient.requestAccessToken({ prompt: 'consent' });
	} else {
		// Skip display of account chooser and consent dialog for an existing session.
		tokenClient.requestAccessToken({ prompt: '' });
	}
}

export function handleSignoutClick() {
	if (accessToken) {
		accessToken = null;
		google.accounts.oauth2.revoke(accessToken);
	}
}

export function setCurrentUser() {
	if (accessToken) {
		currentUser.set({
			token: accessToken
		});
	} else {
		currentUser.set(undefined);
	}
}
