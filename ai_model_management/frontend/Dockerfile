# Use the official Node.js image for Vue.js
FROM node:20

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the Vue.js app for production
RUN npm run build

# Use a simple web server to serve the built files
RUN npm install -g serve

# Expose the port where the frontend will run
EXPOSE 8080

# Command to serve the built Vue.js
CMD ["npm", "run", "serve"]
