// Configuration file for Tailwind CSS
module.exports = {
  // Specify the paths to all of the template files in the project
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
  // Extend the default theme here (if needed)
    extend: {},
  },
  // Add Flowbite as a plugin
  plugins: [
    require('flowbite/plugin')
  ],
}