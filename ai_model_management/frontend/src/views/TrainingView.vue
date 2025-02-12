<template>
  <!-- Header -->
  <header class="bg-green-600 text-white p-4 flex justify-between items-center">
    <router-link to="/dashboard" class="text-2xl hover:underline">User Dashboard</router-link>
    <h2 class="text-xl font-bold">Trainings Management</h2>
  </header>

  <div class="container mx-auto p-4">
    <!-- Add Training Form -->
    <div class="bg-white shadow-md rounded-lg p-6 mb-6">
      <h2 class="text-lg font-bold mb-4">Add New Training</h2>
      <form @submit.prevent="addTraining">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="trainingName">
              Training Name
            </label>
            <input
              v-model="newTraining.training_name"
              id="trainingName"
              type="text"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Enter training name"
              required
            />
          </div>

          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="modelId">
              Model ID
            </label>
            <input
              v-model="newTraining.model_id"
              id="modelId"
              type="text"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Enter model ID"
              required
            />
          </div>

          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="datasetId">
              Dataset ID
            </label>
            <input
              v-model="newTraining.dataset_id"
              id="datasetId"
              type="text"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Enter dataset ID"
              required
            />
          </div>
        </div>

        <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Add Training
        </button>
      </form>

      <!-- Display error message if Model ID or Dataset ID does not exist -->
      <div v-if="errorMessage" class="mt-4 text-red-500 font-bold">
        {{ errorMessage }}
      </div>
    </div>

    <!-- Search Training Form -->
    <div class="bg-white shadow-md rounded-lg p-6 mb-6" style="min-height: 150px;">
      <h2 class="text-lg font-bold mb-4">Search Training</h2>
      <form @submit.prevent="searchTraining">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="searchQuery">
            Search by ID or Training Name
          </label>
          <input
            v-model="searchQuery"
            id="searchQuery"
            type="text"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            placeholder="Enter training ID or training name"
            required
          />
        </div>
        <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Search
        </button>
      </form>

      <!-- Display success message if training is found -->
      <div v-if="foundTrainingId" class="mt-4 text-green-500 font-bold">
        <a :href="`/trainings/${foundTrainingId}`"
        class="text-green-500 hover:text-green-700"
        style="text-decoration:none; color:green">
        Training Found. View training details.</a>
      </div>

      <!-- Display error message if training not found -->
      <div v-if="searchError" class="mt-4 text-red-500 font-bold">
        Training not found. Please try again.
      </div>
    </div>

    <!-- Trainings Table -->
    <div class="bg-white shadow-md rounded-lg p-6">
      <h2 class="text-lg font-bold mb-4">Recorded Trainings</h2>
      <table class="min-w-full table-auto">
        <thead>
          <tr class="bg-gray-200">
            <th class="px-4 py-2">Training ID</th>
            <th class="px-4 py-2">Training Name</th>
            <th class="px-4 py-2">Model ID</th>
            <th class="px-4 py-2">Dataset ID</th>
            <th class="px-4 py-2">Precision</th>
            <th class="px-4 py-2">Recall</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="training in trainings" :key="training.id" class="border-b">
            <td class="px-4 py-2">
              <a :href="`/trainings/${training.id}`" class="text-blue-500 underline hover:text-blue-700">
                {{ training.id }}
              </a>
            </td>
            <td class="px-4 py-2">{{ training.training_name }}</td>
            <td class="px-4 py-2">{{ training.model_id }}</td>
            <td class="px-4 py-2">{{ training.dataset_id }}</td>
            <td class="px-4 py-2">{{ (training.precision * 100).toFixed(2) }}%</td>
            <td class="px-4 py-2">{{ (training.recall * 100).toFixed(2) }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/apiService'; // Import the centralized API service

export default {
  data() {
    return {
      trainings: [],  // Store all trainings
      searchQuery: '',  // For the search functionality
      searchError: false,  // To handle search errors
      foundTrainingId: null,  // To store found training ID
      newTraining: {  // For the add training form
        training_name: '',
        model_id: '',
        dataset_id: '',
      },
      errorMessage: '',  // To display error if Model ID or Dataset ID not found
    };
  },
  methods: {
    async fetchTrainings() {
      // API call to fetch trainings
      try {
        const response = await apiClient.get('/trainings');
        this.trainings = response.data;
      } catch (error) {
        console.error('Error fetching trainings:', error);
      }
    },
    async addTraining() {
      // API call to add a new training
      try {
        this.errorMessage = '';  // Reset the error message

        const response = await apiClient.post('/trainings', this.newTraining);
        this.trainings.push(response.data);

        // Reset the form after successful submission
        this.newTraining.training_name = '';
        this.newTraining.model_id = '';
        this.newTraining.dataset_id = '';
      } catch (error) {
        // Check for a 404 error and display the message from the backend
        if (error.response && error.response.status === 404) {
          this.errorMessage = error.response.data.detail;
        } else {
          this.errorMessage = 'An error occurred. Please try again.';
        }
      }
    },
    async searchTraining() {
      // Search for a training by ID or training name
      const query = this.searchQuery.trim();
      this.searchError = false;
      this.foundTrainingId = null; // Reset the found training ID

      if (query) {
        try {
          // Try searching by ID first
          const trainingId = parseInt(query);
          if (!isNaN(trainingId)) {
            await apiClient.get(`/trainings/${trainingId}`);
            this.foundTrainingId = trainingId;
          } else {
            // If not a valid ID, search by training name
            const response = await apiClient.get(`/trainings`);
            const training = response.data.find(t => t.training_name.toLowerCase() === query.toLowerCase());
            if (training) {
              this.foundTrainingId = training.id;
            } else {
              this.searchError = true; // Training not found
            }
          }
        } catch (error) {
          this.searchError = true; // Handle search error
        }
      }
    }
  },
  mounted() {
    this.fetchTrainings();
  }
};
</script>
