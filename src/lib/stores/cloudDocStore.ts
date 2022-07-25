import { writable } from 'svelte/store';

export interface ICloudDocStore {
	auth_token: string;
	doc_id: string;
	signInPending: boolean;
}

const defaultDocStore: ICloudDocStore = {
	auth_token: '',
	doc_id: '',
	signInPending: false
};

class StoreLogic {
	pickedDoc = ''; // the docId that was picked
	paramDoc = ''; // the docId from the url
	lastDocId = ''; // the docId from local storage
	authToken = ''; // the auth token for reading
	pickLoaded = false; // was the pick lib loaded yet?
	driveLoaded = false; // was the drive lib loaded yet?
	signedIn = false;
	signInPending = false;

	setPicked(doc: string) {
		this.pickedDoc = doc;
		this.checkDocId();
	}

	setSignedIn(signedIn: boolean) {
		this.signedIn = signedIn;
		if (signedIn) {
			this.checkDocId();
		} else if (!this.signInPending) {
			this.paramDoc = '';
			this.pickedDoc = '';
		}
	}

	setParam(doc: string) {
		this.paramDoc = doc;
		if (doc.length > 0) {
			this.checkDocId();
		}
	}

	setLocalDocId(docId: string) {
		this.lastDocId = docId;
		if (docId.length > 0) {
			this.checkDocId();
		}
	}

	setAuthId(auth_token: string) {
		this.authToken = auth_token;
		update((curr: ICloudDocStore) => ({ ...curr, auth_token: this.authToken })); // update the store
	}

	checkDocId() {
		if (this.paramDoc.length > 0 && !this.signedIn) {
			console.log('checkDocId: paramDoc but not signed in.. setting signin pending');
			update((curr: ICloudDocStore) => ({ ...curr, signInPending: true }));
			this.signInPending = true;
		}

		if (this.paramDoc.length > 0 && this.pickLoaded && this.driveLoaded && this.signedIn) {
			// we have a param doc, and everything else is ready, go ahead and set the doc to that
			update((curr: ICloudDocStore) => ({ ...curr, doc_id: this.paramDoc, signInPending: false })); // update the store
			this.paramDoc = '';
			this.signInPending = false;
		} else if (this.lastDocId.length > 0 && this.driveLoaded && this.signedIn) {
			// we have a picked doc, and everything else is ready, go ahead and set the doc to that
			update((curr: ICloudDocStore) => ({ ...curr, doc_id: this.lastDocId, signInPending: false })); // update the store
			this.lastDocId = '';
			this.signInPending = false;
		} else if (this.pickedDoc.length > 0 && this.pickLoaded && this.driveLoaded && this.signedIn) {
			// we have a picked doc, and everything else is ready, go ahead and set the doc to that
			update((curr: ICloudDocStore) => ({ ...curr, doc_id: this.pickedDoc, signInPending: false })); // update the store
			this.pickedDoc = '';
			this.signInPending = false;
		}
	}

	setDriveLoaded(loaded: boolean) {
		this.driveLoaded = loaded;
		this.checkDocId();
	}

	setPickLoaded(loaded: boolean) {
		this.pickLoaded = loaded;
		this.checkDocId();
	}
}

const { subscribe, update } = writable<ICloudDocStore>(defaultDocStore);

const storeLogic = new StoreLogic();

function createStore() {
	return {
		subscribe,
		setPickedId: (docid: string) => {
			storeLogic.setPicked(docid);
		},
		setParamId: (docid: string) => {
			storeLogic.setParam(docid);
		},
		setLocalDocId: (docid: string) => {
			storeLogic.setLocalDocId(docid);
		},
		setDriveLoaded: () => {
			storeLogic.setDriveLoaded(true);
		},
		setPickerLoaded: () => {
			storeLogic.setPickLoaded(true);
		},
		setAuthId: (auth_token: string) => {
			storeLogic.setAuthId(auth_token);
		},
		setSignedIn: (signedIn: boolean) => {
			storeLogic.setSignedIn(signedIn);
		}
	};
}

export const cloudDocStore = createStore();
