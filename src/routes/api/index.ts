import type { RequestHandler } from './__types/index';

interface GetResult {
	CLIENT_ID: string;
	API_KEY: string;
}

const defaultResult: GetResult = {
	CLIENT_ID: '',
	API_KEY: ''
};

export const GET: RequestHandler<GetResult> = async ({ request }) => {
	let result = defaultResult;
	result = { ...result, CLIENT_ID: JSON.stringify(Object.keys(process.env)) };
	return { body: result };
};
