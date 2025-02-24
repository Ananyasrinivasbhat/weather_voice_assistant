# Use an official Node.js runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port your Vite app runs on (default is 5173)
EXPOSE 5173

# Command to run your Vite app in development mode
CMD ["npm", "run", "dev"]