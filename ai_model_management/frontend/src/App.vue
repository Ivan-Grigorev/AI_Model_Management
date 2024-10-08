<template>
  <nav class="flex justify-between items-center">
    <div>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <a @click="handleLogout" class="logout-link">Logout</a>
  </nav>
  <router-view />
</template>

<script>
import AuthService from '@/services/authService'; // Import AuthService

export default {
  mounted() {
    document.title = "AI Model Management";  // Set the title of the page
  },
  methods: {
    handleLogout() {
      AuthService.logout();
      this.$router.push('/'); // Redirect to Home after logout
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #f3f4f6;
  background-size: cover;
  background-position: center;
}

nav {
  padding: 30px;
  position: relative; /* Add relative positioning */
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  cursor: pointer; /* Change cursor to pointer for the logout link */
}

nav a.router-link-exact-active {
  color: #42b983;
}

/* Add styles for the logout link */
.logout-link {
  font-weight: bold;
  color: #e63946; /* Red color for logout link */
}

/* Flexbox styles for positioning */
.flex {
  display: flex;
}

.justify-between {
  justify-content: space-between;
}

.items-center {
  align-items: center;
}
</style>
