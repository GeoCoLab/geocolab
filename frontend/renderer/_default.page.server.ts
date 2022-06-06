import { renderToNodeStream } from '@vue/server-renderer';
import type { PageContextBuiltIn } from 'vite-plugin-ssr';
import { escapeInject } from 'vite-plugin-ssr';
import { createApp } from './app';
import type { PageContext } from '../types';
import iconUrl from '../assets/apple-touch-icon.png';

export const passToClient = ['pageProps', 'documentProps'];

export async function render(pageContext: PageContextBuiltIn & PageContext) {
    const app = createApp(pageContext);
    const stream = renderToNodeStream(app);

    const title = 'GeoCoLab';
    const desc = 'Matching access to analytical facilities with underserved researchers';

    return escapeInject`<!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="apple-touch-icon" sizes="180x180" href="${ iconUrl }">
        <link rel="shortcut icon" type="image/x-icon" href="${ iconUrl }" />
        <meta name="description" content="${ desc }" />
        <title>${ title }</title>
      </head>
      <body>
        <div id="app">${ stream }</div>
      </body>
    </html>`;
}
