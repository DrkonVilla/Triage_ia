FROM node:20-alpine

WORKDIR /app

# Copiar package files
COPY package*.json ./
RUN if [ -s package-lock.json ]; then npm ci; else npm install; fi

# Copiar código
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]