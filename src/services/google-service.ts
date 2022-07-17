import { setCurrentUser } from './auth-service';

const SCOPES =
	'https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.metadata https://www.googleapis.com/auth/drive';

export async function googleClient() {
	await gapi.client.init({
		apiKey: import.meta.env.VITE_GOOGLE_API_KEY as string,
		clientId: import.meta.env.VITE_GOOGLE_CLIENT_ID as string,
		scope: SCOPES
	});

	setCurrentUser(gapi.auth2.getAuthInstance().isSignedIn.get());

	// Listen for sign-in state changes.
	gapi.auth2.getAuthInstance().isSignedIn.listen((e) => setCurrentUser(e));
}
