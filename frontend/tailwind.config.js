module.exports = {
    mode    : 'jit',
    purge   : ['./templates/**/*.html'],
    darkMode: false,
    theme   : {
        extend    : {},
        fontFamily: {
            display: ['"Be Vietnam Pro"', 'system-ui', 'serif'],
            body   : ['"Open Sans"', 'system-ui', 'sans-serif'],
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
                dark: 'var(--c2-dark)'
            }
        }
    },
    variants: {
        extend: {},
    },
    plugins : [],
};
