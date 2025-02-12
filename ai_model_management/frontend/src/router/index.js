import { createRouter, createWebHistory } from 'vue-router';

import AboutView from '../views/AboutView.vue';
import HomeView from '../views/HomeView.vue';
import SignUpView from '../views/SignUpView.vue';
import LoginView from '../views/LoginView.vue';
import UserView from '../views/UserView.vue';
import DatasetView from '../views/DatasetView.vue';
import DatasetDetailsView from '../views/DatasetDetailsView.vue';
import ModelView from '../views/ModelView.vue';
import ModelDetailsView from '../views/ModelDetailsView.vue';
import TrainingView from '../views/TrainingView.vue';
import TrainingDetailsView from '../views/TrainingDetailsView.vue';
import AdminView from '../views/AdminView.vue';
import AdminUsersView from '../views/AdminUsersView.vue';
import AdminDatasetsView from '../views/AdminDatasetsView.vue';
import AdminDatasetDetailsView from '../views/AdminDatasetDetailsView.vue';
import AdminModelsView from '../views/AdminModelsView.vue';
import AdminModelDetailsView from '../views/AdminModelDetailsView.vue';


const routes = [
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/signin',
    name: 'signup',
    component: SignUpView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: UserView
  },
  {
    path: '/datasets',
    name: 'datasets',
    component: DatasetView
  },
  {
    path: '/datasets/:dataset_id',
    name: 'dataset-details',
    component: DatasetDetailsView
  },
  {
    path: '/models',
    name: 'models',
    component: ModelView
  },
  {
    path: '/models/:model_id',
    name: 'models-details',
    component: ModelDetailsView
  },
  {
    path: '/trainings',
    name: 'trainings',
    component: TrainingView
  },
  {
    path: '/trainings/:training_id',
    name: 'training-details',
    component: TrainingDetailsView
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminView
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: AdminUsersView
  },
  {
    path: '/admin/datasets',
    name: 'admin-datasets',
    component: AdminDatasetsView
  },
  {
    path: '/admin/datasets/:dataset_id',
    name: 'admin-dataset-details',
    component: AdminDatasetDetailsView
  },
  {
    path: '/admin/models',
    name: 'admin-models',
    component: AdminModelsView
  },
  {
    path: '/admin/models/:model_id',
    name: 'admin-model-details',
    component: AdminModelDetailsView
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // Using the base URL for history mode
  routes
});

export default router;
