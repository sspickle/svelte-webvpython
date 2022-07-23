import { writable } from 'svelte/store';
import { browser } from '$app/env';

let initialCode = `
from vpython import *
import numpy as np

import sys
print(sys.version)

r = 2 + 3j
s = sphere(pos=vec(r.real,r.imag,0), color=color.blue, make_trail=True)
print("hello" + f"{abs(3 + 4j)}")

while True:
   rate(30)
   r = r*np.exp(1j*0.05)
   s.pos = vec(r.real, r.imag, 0)
`;

const localStorageKey = 'code';
const origLocalStorageCode = browser ? localStorage.getItem(localStorageKey) : null;

export const srcStore = writable(origLocalStorageCode ? origLocalStorageCode : initialCode);

if (browser) {
	srcStore.subscribe((code) => {
		localStorage.setItem(localStorageKey, code);
	});
}
