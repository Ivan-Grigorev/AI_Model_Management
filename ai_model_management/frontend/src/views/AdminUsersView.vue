<template>
  <!-- Header -->
  <header class="bg-blue-600 text-white p-4 flex justify-between items-center">
    <router-link to="/admin" class="text-2xl hover:underline">Admin Panel</router-link>
    <h2 class="text-xl font-bold">Users Management</h2>
  </header>

  <div class="container mx-auto mt-8">

    <!-- Table displaying all users -->
    <div class="overflow-x-auto">
      <table class="min-w-full text-sm text-left text-gray-700 bg-white shadow-md rounded-lg overflow-hidden">
        <thead class="bg-gray-200 text-black">
          <tr>
            <th scope="col" class="py-3 px-6">ID</th>
            <th scope="col" class="py-3 px-6">Email</th>
            <th scope="col" class="py-3 px-6">Registration Date</th>
            <th scope="col" class="py-3 px-6">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" class="bg-white border-b hover:bg-gray-100">
            <td class="py-3 px-6">{{ user.id }}</td>
            <td class="py-3 px-6">{{ user.email }}</td>
            <td class="py-3 px-6">{{ user.registration_date }}</td>
            <td class="py-3 px-6">
              <button
                @click="deleteUser(user.email)"
                class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
              >
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      users: [],
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('/admin/users', {
          headers: {
            'Authorization': `Bearer ${this.getToken()}` // Add your token logic if necessary
          }
        });
        this.users = response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    async deleteUser(email) {
      if (confirm(`Are you sure you want to delete ${email}?`)) {
        try {
          const response = await axios.post(`/admin/users/delete/${email}`, null, {
            headers: {
              'Authorization': `Bearer ${this.getToken()}` // Add your token logic if necessary
            }
          });
          if (response.status === 200) { // Check for successful deletion
            alert(`User ${email} has been deleted.`);
            this.fetchUsers(); // Refresh the list after deletion
          } else {
            alert('Failed to delete user.');
          }
        } catch (error) {
          alert(`Error deleting user: ${error.response ? error.response.data : error.message}`);
        }
      }
    },
    logout() {
      // Logic for logging out the admin
      this.$router.push('/login');
    },
    getToken() {
      // Logic for getting the token (if needed)
      return localStorage.getItem('token');
    }
  },
  mounted() {
    this.fetchUsers();
  }
};
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
