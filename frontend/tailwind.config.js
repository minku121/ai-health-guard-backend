const { nextui } = require("@nextui-org/react");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {},
  },
  darkMode: "class",
  plugins: [nextui({
    themes: {
      light: {
        colors: {
          primary: "#0072f5",
          secondary: "#7828c8",
          success: "#17c964",
          warning: "#f5a524",
          danger: "#f31260",
        }
      },
      dark: {
        colors: {
          primary: "#0072f5",
          secondary: "#9353d3",
          success: "#17c964",
          warning: "#f5a524",
          danger: "#f31260",
        }
      }
    }
  })],
}
