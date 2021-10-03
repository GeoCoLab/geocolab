module.exports = {
    mode    : 'jit',
    purge   : ['./templates/**/*.html'],
    darkMode: false,
    theme   : {
        extend    : {},
        fontFamily: {
            display: ['"Roboto"', 'sans-serif'],
            body   : ['"Rubik"', 'sans-serif'],
        },
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
            }
        }
    },
    variants: {
        extend: {},
    },
    plugins : [],
};
