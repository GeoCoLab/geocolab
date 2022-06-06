import { defineStore } from 'pinia/dist/pinia';
import { api } from '../utils/api';
import moment from 'moment';
import { canUpdate, expired, sortObjectValues } from '../utils/misc';

export const useEnumStore = defineStore('enums', {
    state: () => ({
        countries: {},
        currencies: {},
        lastCheck: {
            countries: expired(),
            currencies: expired()
        }
    }),
    getters: {},
    actions: {
        async init() {
            if (Object.keys(this.countries).length === 0 && canUpdate(this.lastCheck.countries)) {
                api.get('/enum/countries').then(r => {
                    this.countries = sortObjectValues(r.data);
                    this.lastCheck.countries = moment();
                }).catch(e => {
                    //
                });
            }
            if (Object.keys(this.currencies).length === 0 && canUpdate(this.lastCheck.currencies)) {
                api.get('/enum/currencies').then(r => {
                    this.currencies = sortObjectValues(r.data);
                    this.lastCheck.currencies = moment();
                }).catch(e => {
                    //
                });
            }
        }
    }
});
