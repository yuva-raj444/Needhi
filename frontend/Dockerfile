FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source
COPY public/ ./public/
COPY src/ ./src/

# Build React app
RUN npm run build

# Use nginx to serve
FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=0 /app/build ./build

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]
