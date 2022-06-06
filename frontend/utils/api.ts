import axios from 'axios';


let API_HOST;
try {
    API_HOST = __API_HOST__;
} catch (e) {
    API_HOST = 'http://10.0.12.12';
}

const BASE_URL = API_HOST + '/api';

export const api = axios.create({
    baseURL: BASE_URL,
    timeout: 20000,
    headers: {
        'Content-Type': 'application/json'
    },
    xsrfCookieName: 'csrf_access_token',
    xsrfHeaderName: 'X-CSRF-TOKEN'
});

export async function post(endpoint: string, formData: Object) {
    // I'm not sure if this is required and/or even does anything anymore, but I'm gonna leave it for now
    return api.get('/csrf')
        .then(() => api.post(endpoint, formData));
}

api.interceptors.response.use(
    function (response) {
        return response;
    },
    async function (error) {
        let originalRequest = error.config;
        if (error.response.data.msg === 'Token has expired') {
            try {
                await api.post('/refresh', {}, {xsrfCookieName: 'csrf_refresh_token'});
                return api(originalRequest);
            } catch (e) {
                // they're just gonna have to log in again
            }
        }
        return Promise.reject(error);
    }
);
