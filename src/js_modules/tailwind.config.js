/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./../templates/**/*.html"],
  theme: {
    extend: {},
    colors:{
      darkGlass:{
        50:"rgba(15,15,15,0.2)",
        100:"rgba(15,15,15,0.4)",
        200:"rgba(15,15,15,0.6)",
        300:"rgba(15,15,15,0.8)"
      },
      lightGlass:{
        50:"rgba(255, 255, 255, 0.2)",
        100:"rgba(255, 255, 255, 0.4)",
        200:"rgba(255, 255, 255, 0.6)",
        300:"rgba(255, 255, 255, 0.8)",
        400:"rgba(255, 255, 255, 0.10)",
        500:"rgba(255, 255, 255, 0.12)"
      }
    }
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
}

