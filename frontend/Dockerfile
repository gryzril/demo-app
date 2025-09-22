FROM node:16

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
EXPOSE 5173
# CMD ["npm","run","dev"]

CMD ["sh", "-c", "npm run dev && tail -f /dev/null"]