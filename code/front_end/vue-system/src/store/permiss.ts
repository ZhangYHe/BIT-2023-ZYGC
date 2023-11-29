import { defineStore } from 'pinia';

interface ObjectList {
	[key: string]: string[];
}

export const usePermissStore = defineStore('permiss', {
	state: () => {
		const keys = localStorage.getItem('ms_keys');
		return {
			key: keys ? JSON.parse(keys) : <string[]>['1'],
			defaultList: <ObjectList>{
				admin:['1','2','7'],
				user:['1','2']
			}
		};
	},
	actions: {
		handleSet(val: string[]) {
			this.key = val;
		}
	}
});
