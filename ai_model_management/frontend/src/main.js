import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';

import 'flowbite';
import './assets/tailwind.css';
import router from './router';

// create the Vue app
const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:8000/';  // the FastAPI backend

app.use(router) // Register the router
app.mount('#app'); // Mount the app to the DOM
