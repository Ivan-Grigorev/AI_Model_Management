<template>
  <div class="container mx-auto py-6 px-4">
    <h1 class="text-2xl font-bold mb-4">Model Details</h1>

    <div class="border p-4 rounded-lg bg-gray-100">
      <p><strong>ID:</strong> {{ model.id }}</p>
      <p><strong>Name:</strong> {{ model.name }}</p>
      <p><strong>Creation Date:</strong> {{ model.creation_date }}</p>
    </div>

    <button @click="$router.push('/models')" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700">
      Back to All Models
    </button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      model: null,
    };
  },
  methods: {
    fetchModel() {
      const modelId = this.$route.params.model_id; // Ensure this matches the route parameter
      axios.get(`/models/${modelId}`)
        .then(response => {
          this.model = response.data;
        })
        .catch(error => {
          console.error('Model not found', error);
        });
    }
  },
  created() {
    this.fetchModel();
  }
};
</script>
