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
        "cheesy-black": "#0D1627",
        "pepperoni-black": "#172E57",
        "auberside-pink": "#FF8A8F",
        "existential-blurple": "#7364FF"
      },
      fontFamily: {
        "primary": ["'Inter'", "'Helvetica Neue'", "Helvetica", "Arial", "'Lucida Grande'", "sans-serif"]
      }
    },
  },
  plugins: [],
}

