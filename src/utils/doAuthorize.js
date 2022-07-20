import { cloudDocStore } from '../stores/cloudDocStore';

export const doAuthorize = (SCOPES) => {
	const handleCB = (authResult) => {
		console.log('in auth result...', JSON.stringify(authResult, null, 2));
		if (authResult && !authResult.error) {
			cloudDocStore.setAuthId(authResult.access_token);
		}
	};

	gapi.auth.authorize(
		{
			client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
			scope: SCOPES,
			immediate: false
		},
		handleCB
	);
};
