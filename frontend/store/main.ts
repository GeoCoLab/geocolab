import {defineStore} from 'pinia/dist/pinia';
import {api} from '../utils/api';


export const useStore = defineStore('main', {
    state: () => ({
        countries: []
    }),
    getters: {},
    actions: {
        async init() {
            api.get('/enum/countries').then(r => {
                this.countries = r.data;
            })
        }
    }
})
