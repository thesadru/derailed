/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "silver-gray": "#818181",
        "cheesy-black": "#161618",
        "pepperoni-black": "#212124",
        "auberside-pink": "#FF8A8F"
      },
      fontFamily: {
        "primary": ["'Roboto Flex'", "'Helvetica Neue'", "Helvetica", "Arial", "'Lucida Grande'", "sans-serif"]
      }
    },
  },
  plugins: [],
}

