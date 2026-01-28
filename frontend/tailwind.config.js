/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'valorant-red': '#ff4655',
                'valorant-black': '#0f1923',
                'valorant-white': '#ece8e1',
                'valorant-gray': '#8b9bb4',
            },
            fontFamily: {
                sans: ['Overpass', 'sans-serif'],
                mono: ['monospace'],
            },
            animation: {
                'spin-slow': 'spin 3s linear infinite',
            }
        },
    },
    plugins: [],
}
