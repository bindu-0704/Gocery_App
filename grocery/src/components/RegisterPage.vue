<template>
  
  <div class="page-container">
    <div class="register">
      <!-- Red Cross Icon for Close -->
      <a href="/" class="close-btn"><i class="fas fa-times"></i></a>

      <h1 class="text-center mb-4">Sign Up</h1>
      <form @submit.prevent="register">
        <div class="form-outline mb-4">
          <label for="name" class="form-label">Full Name</label>
          <input type="text" class="form-control" id="name" v-model="name" required placeholder="Enter your name">
        </div>

        <div class="form-outline mb-4">
          <label class="form-label" for="email">Email address</label>
          <input type="email" id="email" class="form-control" v-model="email" required placeholder="Enter your email">
        </div>

        <div class="form-outline mb-4">
          <label class="form-label" for="password">Password</label>
          <input type="password" id="password" v-model="password" class="form-control" required placeholder="Choose a password" />
        </div>

        <div class="form-outline mb-4">
          <label for="role" class="form-label">Role</label>
          <select id="role" v-model="role" required class="form-control">
            <option value="manager">Manager</option>
            <option value="admin">Admin</option>
            <option value="user">User</option>
          </select>
        </div>

        <div class="button-group">
          <button type="submit" class="btn btn-primary">Register</button>
          <router-link to="/login" class="btn btn-link">Already have an account? Login</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "RegisterPage",
  data() {
    return {
      email: '',
      name: '',
      password: '',
      role: 'user',
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://localhost:5000/register', {
          email: this.email,
          name: this.name,
          password: this.password,
          role: this.role,
        });

        console.log(response.data);

        if (this.role === "manager") {
          alert('Registration request has been sent to the admin for approval.');
          this.$router.push("/login");
        } else if (this.role === "admin") {
          this.$router.push("/Adashboard");
        } else {
          this.$router.push("/login");
        }

      } catch (error) {
        if (error.response && (error.response.status === 400 || error.response.data.error === 'name already taken')) {
          alert('name is already taken. Please choose a different name.');
        } else {
          console.error(error.response ? error.response.data.error : error.message);
        }
      }
    }
  }
}
</script>

<style scoped>
/* Background for the entire page */
.page-container {
  height: 100vh;
  background-color: #fff; /* Light background color for the body */
  
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Register Form Styling */
.register {
  max-width: 400px;
  width: 100%;
  padding: 30px;
  background-color: #f4f4f4;  /* White background for the form */
  border-radius: 10px;
  border-color: #021936;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);  /* Add shadow for a pop-up effect */
  z-index: 1000;
  position: relative; /* To position the close button correctly */
}

h1 {
  text-align: center;
  color: #007bff;
  font-size: 2em;
  margin-bottom: 20px;
}

.form-outline {
  margin-bottom: 15px;
}

.form-label {
  font-weight: bold;
}

.form-control {
  border-radius: 5px;
  padding: 10px;
  border: 1px solid #ddd;
}

input, select {
  width: 100%;
}

.button-group {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  border-color: #007bff;
  color: #fff;
  border-radius: 5px;
  margin-bottom: 10px;
  font-weight: bold;
}

.btn-link {
  text-align: center;
  color: #021936;
  text-decoration: underline;
}



input::placeholder, select::placeholder {
  color: #bbb;
}

/* Red Cross (Close) Button */
.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  color: red;
  font-size: 24px;
  cursor: pointer;
}

.close-btn:hover {
  color: darkred;
}

/* Mobile responsiveness */
@media (max-width: 600px) {
  .register {
    margin: 20px;
    padding: 20px;
  }
}
</style>
