FROM node:18

WORKDIR /autoparts

COPY package*.json ./
RUN npm install

COPY . .

CMD ["npm", "run", "dev"]
