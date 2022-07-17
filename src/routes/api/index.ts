import type { RequestHandler } from './__types/index';

type OutputType = { message: string; rtype: string };

export const get: RequestHandler<OutputType> = async ({ request }) => {
	return { body: { message: 'Hello World', rtype: request.method } };
};
