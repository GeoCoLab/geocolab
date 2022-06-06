import vue from '@vitejs/plugin-vue';
import ssr from 'vite-plugin-ssr/plugin';
import WindiCSS from 'vite-plugin-windicss';

export default {
    plugins: [
        vue(),
        ssr(),
        WindiCSS({
            scan: {
                dirs: ['pages', 'components', 'renderer'],
                fileExtensions: ['vue', 'js']
            }
        })],
    define: {
        __API_HOST__: JSON.stringify(process.env.API_HOST),
        __SECRET__: JSON.stringify(process.env.SECRET)
    }
};
