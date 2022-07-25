import { writable } from 'svelte/store';
import { browser } from '$app/env';

let defaultPrefs = {
	add_default_imports: true,
	saved_doc_id: '',
	saved_doc_name: ''
};

const localStorageKey = 'prefs';
let origLocalStoragePrefs = null;

if (browser) {
	let localStoragePrefsJSON = localStorage.getItem(localStorageKey);
	if (localStoragePrefsJSON) {
		origLocalStoragePrefs = JSON.parse(localStoragePrefsJSON);
	}
}

export const prefsStore = writable(origLocalStoragePrefs ? origLocalStoragePrefs : defaultPrefs);

if (browser) {
	prefsStore.subscribe((prefs) => {
		if (prefs) {
			localStorage.setItem(localStorageKey, JSON.stringify(prefs));
		}
	});
}
