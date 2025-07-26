export function filterSearchesFuzzy(text: string, array: string[]): string[] {
	text = text?.trim?.() || '';
	if (!text) {
		return array;
	}
	const escaped = text.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
	const regexPattern = '.*' + escaped.replace(/\s+/g, '.*') + '.*';
	const regex = new RegExp(regexPattern, 'i');
	return array.filter((elem) => regex.test(elem));
}

export async function customFetch(
	input: RequestInfo | URL,
	init: RequestInit = {}
): Promise<Response> {
	return fetch(input, {
		...init,
		headers: {
			...(init.headers || {}),
			...{}, // Your custom headers here
		}
	});
}