FROM node:13.5-stretch

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY package.json /app/package.json
RUN npm install --silent --only=production
RUN npm install react-scripts -g --silent

CMD ["npm", "start"]
