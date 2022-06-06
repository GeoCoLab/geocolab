import { defineConfig } from 'windicss/helpers'

export default defineConfig({
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: {
                    lightest: 'var(--c1-lightest)',
                    light: 'var(--c1-light)',
                    DEFAULT: 'var(--c1)',
                    dark: 'var(--c1-dark)',
                    darkest: 'var(--c1-darkest)'
                },
                secondary: {
                    light: 'var(--c2-light)',
                    DEFAULT: 'var(--c2)',
                    dark: 'var(--c2-dark)',
                    darkest: 'var(--c2-darkest)'
                },
                gray: {
                    100: 'var(--grey-1)',
                    200: 'var(--grey-2)',
                    300: 'var(--grey-3)'
                }
            }
        },
        fontFamily: {
            display: ['"Rubik"', 'sans-serif'],
            body: ['"Karla"', 'sans-serif'],
        },
    }
});
