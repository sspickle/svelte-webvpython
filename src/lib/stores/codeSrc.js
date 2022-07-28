import { writable } from 'svelte/store';
import { browser } from '$app/env';

let initialCode = `
box()
`;

const localStorageKey = 'code';
const origLocalStorageCode = browser ? sessionStorage.getItem(localStorageKey) : null;

export const srcStore = writable(origLocalStorageCode ? origLocalStorageCode : initialCode);

if (browser) {
	srcStore.subscribe((code) => {
		sessionStorage.setItem(localStorageKey, code);
	});
}
