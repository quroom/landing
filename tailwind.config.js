/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./landing/templates/**/*.html",
    "./landing/forms.py",
    "./landing/views.py",
    "./landing/content.py",
  ],
  theme: {
    extend: {
      colors: {
        navy: "#0F172A",
        sky: "#0EA5E9",
        fog: "#E8EEF5",
        mint: "#4ADE80",
        amber: "#F59E0B",
      },
    },
  },
  plugins: [],
};

