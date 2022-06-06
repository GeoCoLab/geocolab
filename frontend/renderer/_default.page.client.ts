import { createApp } from './app';
import type { PageContextBuiltInClient } from 'vite-plugin-ssr/client/router';
import { useClientRouter } from 'vite-plugin-ssr/client/router';
import type { PageContext } from '../types';

import 'virtual:windi.css';
import '../scss/base.scss';
import '../scss/form.scss';

let app: ReturnType<typeof createApp>;
const {hydrationPromise} = useClientRouter({
    render(pageContext: PageContextBuiltInClient & PageContext) {
        if (!app) {
            app = createApp(pageContext);
            app.mount('#app');
        } else {
            app.changePage(pageContext);
        }
        document.title = 'GeoCoLab';
    },
    // Vue needs the first render to be a hydration
    ensureHydration: true,
    prefetchLinks: true
});

hydrationPromise.then(() => {
    console.log('Hydration finished; page is now interactive.');
});
