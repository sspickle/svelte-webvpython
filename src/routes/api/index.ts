import type { RequestHandler } from './__types/index';
import { SecretManagerServiceClient } from '@google-cloud/secret-manager';

const getName = (name: string): string => {
	return `projects/glowscript-py38/secrets/${name}/versions/latest`;
};

// Instantiates a client
const client = new SecretManagerServiceClient();

async function accessSecretVersion(name: string) {
	const [version] = await client.accessSecretVersion({
		name: getName(name)
	});

	// Extract the payload as a string.
	const payload = version!.payload!.data!.toString();

	// WARNING: Do not print the secret in a production environment - this
	// snippet is showing how to access the secret material.
	return payload;
}

interface GetResult {
	CLIENT_ID: string;
	API_KEY: string;
	APP_ID: string;
	EXT: string;
}

const defaultResult: GetResult = {
	CLIENT_ID: '',
	API_KEY: '',
	APP_ID: '',
	EXT: ''
};

export const POST: RequestHandler<GetResult | string> = async ({ request }) => {
	const incoming = await request.json();
	if (!incoming['sec'] || incoming['sec'] !== import.meta.env.VITE_DUMB_SECRET) {
		return {
			status: 401,
			body: 'Unauthorized'
		};
	}

	let result = defaultResult;
	result = {
		...result,
		CLIENT_ID: await accessSecretVersion('CLIENT_ID'),
		API_KEY: await accessSecretVersion('API_KEY'),
		APP_ID: await accessSecretVersion('APP_ID'),
		EXT: 'done!'
	};
	return { status: 200, body: result };
};
