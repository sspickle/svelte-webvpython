import { writable } from 'svelte/store';

export interface ICloudDocStore {
	auth_token: string;
	doc_id: string;
}

const defaultDocStore: ICloudDocStore = {
	auth_token: '',
	doc_id: ''
};

class StoreLogic {
	pickedDoc = ''; // the docId that was picked
	paramDoc = ''; // the docId from the url
	readyDoc = ''; // ready to read the doc
	authToken = ''; // the auth token for reading
	pickLoaded = false; // was the pick lib loaded yet?
	driveLoaded = false; // was the drive lib loaded yet?

	setPicked(doc: string) {
		this.pickedDoc = doc;
		this.checkDocId();
	}

	setParam(doc: string) {
		this.paramDoc = doc;
		this.checkDocId();
	}

	setAuthId(auth_token: string) {
		this.authToken = auth_token;
		update((curr: ICloudDocStore) => ({ ...curr, auth_token: this.authToken })); // update the store
	}

	checkDocId() {
		if (this.paramDoc.length > 0 && this.pickLoaded && this.driveLoaded) {
			// we have a param doc, and everything else is ready, go ahead and set the doc to that
			update((curr: ICloudDocStore) => ({ ...curr, doc_id: this.paramDoc })); // update the store
			this.paramDoc = '';
		} else if (this.pickedDoc.length > 0 && this.pickLoaded && this.driveLoaded) {
			// we have a picked doc, and everything else is ready, go ahead and set the doc to that
			update((curr: ICloudDocStore) => ({ ...curr, doc_id: this.pickedDoc })); // update the store
			this.pickedDoc = '';
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
		setDriveLoaded: () => {
			storeLogic.setDriveLoaded(true);
		},
		setPickerLoaded: () => {
			storeLogic.setPickLoaded(true);
		},
		setAuthId: (auth_token: string) => {
			storeLogic.setAuthId(auth_token);
		}
	};
}

export const cloudDocStore = createStore();
