/** @type {import('tailwindcss').Config} */
import daisyui from "daisyui";

export default {
  content: [
    "./webAMG/templates/**/*.html",
    "./templates/**/*.html",
    "./webAMG/**/*.py",
    "./config/**/*.py",
    "./**/*.py",
    "./static/**/*.js",
  ],
  theme: {
    extend: {
      svg: {
        DEFAULT: 'currentColor',
      },
    },
  },
  plugins: [daisyui],
};
