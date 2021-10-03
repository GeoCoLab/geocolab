/** @type {import('snowpack').SnowpackUserConfig } */
export default {
    root: './',
    mount: {
        media: { url: '/media', static: true },
        src: { url: '/src' },
        templates: { url: '/templates', static: true },
        style: { url: '/style' }
    },
    devOptions: {
        tailwindConfig: './tailwind.config.js',
    },
    buildOptions: {
        out: 'static'
    },
    env: {
        BASE_URL: '/static'
    },
    plugins: ['@snowpack/plugin-postcss', '@snowpack/plugin-sass'],
};
