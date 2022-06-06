import { defineStore } from 'pinia/dist/pinia';
import { api, post } from '../utils/api';
import type { Ref } from 'vue';
import { User } from '../types';
import { navigate } from 'vite-plugin-ssr/client/router';

const emptyUser: User = {
    country: null,
    created: null,
    email: null,
    id: null,
    name: null,
    role: null,
    todo: [],
    gravatar: null,
    completion: 0,
    given_name: null,
    family_name: null,
    given_name_first: true
};

export const useAuthStore = defineStore('auth', {
    state: () => ({
        userData: {...emptyUser}
    }),
    getters: {
        loggedIn(): boolean {
            return this.userData.id !== null;
        }
    },
    actions: {
        async login(loginForm: Ref) {
            return post('/login', loginForm.value).then(r => {
                this.userData = r.data;
                return r;
            }).catch(e => {
                return e.response;
            });
        },
        async logout() {
            return api.post('/logout').then(r => {
                this.userData = {...emptyUser};
                navigate('/');
            });
        },
        async loadUser() {
            return api.get('/user').then(r => {
                this.userData = r.data;
            }).catch(e => {
                //
            });
        },
        async register(registerForm: Ref) {
            return post('/register', registerForm.value).then(r => {
                this.userData = r.data;
                return r;
            }).catch(e => {
                return e.response;
            });
        },
    }
});
