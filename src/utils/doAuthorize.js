export const doAuthorize = (cb, SCOPES) => {
	const handleCB = (authResult) => {
		if (authResult && !authResult.error) {
			cb(authResult.access_token);
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
