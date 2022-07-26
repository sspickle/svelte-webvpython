import type { RequestHandler } from './__types/googleOpen';

// preparing for a Google Drive Integration at some point in the future

export const GET: RequestHandler<string> = async (event) => {
	const result = JSON.stringify(event);

	console.log(result);

	return { status: 200, body: result };
};
