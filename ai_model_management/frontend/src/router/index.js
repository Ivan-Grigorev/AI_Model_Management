import { createRouter, createWebHistory } from 'vue-router';
import AboutView from '../views/AboutView.vue';
import HomeView from '../views/HomeView.vue';
import SignUpView from '../views/SignUpView.vue';
import LoginView from '../views/LoginView.vue';

const routes = [
  {
    path: '/about',  // About route
    name: 'about',
    component: AboutView  // Using AboutView component
  },
  {
    path: '/',
    name: 'home',
    component: HomeView // Using HomeView component
  },
  {
    path: '/signin', // Sign up route
    name: 'signup',
    component: SignUpView // Using SignUpView component
  },
  {
    path: '/login', // Login route
    name: 'login',
    component: LoginView // Using LoginView component
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // Using the base URL for history mode
  routes
});

export default router;
