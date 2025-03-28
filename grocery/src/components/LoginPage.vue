<template>
  <div class="page-container">
    <div class="login">
      <!-- Red Cross Icon for Close -->
      <a href="/" class="close-btn"><i class="fas fa-times"></i></a>

      <h1 class="text-center mb-4">Login</h1>
      <form @submit.prevent="loginUser">
        <div class="form-outline mb-4">
          <label for="name" class="form-label">Full Name</label>
          <input type="text" class="form-control" id="name" v-model="name" required placeholder="Enter your name">
        </div>

        <div class="form-outline mb-4">
          <label class="form-label" for="password">Password</label>
          <input type="password" id="password" class="form-control" v-model="password" required placeholder="Enter your password" />
        </div>

        <div class="button-group">
          <button type="submit" class="btn btn-primary">Login</button>
          <router-link to="/register" class="btn btn-link">Don't have an account? Register</router-link>
        </div>
      </form>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    </div>
  </div>
</template>

<style scoped>
/* Background for the entire page */
.page-container {
  height: 100vh;
  background-color: #fff;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Login Form Styling */
.login {
  max-width: 400px;
  width: 100%;
  padding: 30px;
  background-color: #f4f4f4;
  border-radius: 10px;
  border-color: #021936;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  position: relative;
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

input::placeholder {
  color: #bbb;
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

/* Error Message Styling */
.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 10px;
}

.success-message {
  color: #28a745;
  text-align: center;
  margin-top: 10px;
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
  .login {
    margin: 20px;
    padding: 20px;
  }
}
</style>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      name: "",
      password: "",
      errorMessage: "",
      successMessage: "",
    };
  },
  methods: {
    async loginUser() {
      try {
        const confirmationMessage = "Do you want to log in?";
        if (window.confirm(confirmationMessage)) {
          const response = await axios.post("http://localhost:5000/login", {
            name: this.name,
            password: this.password,
          });

          const { access_token, name, role } = response.data;
          localStorage.setItem("token", access_token);
          this.successMessage = `Welcome, ${name}! You are logged in as ${role}.`;

          if (role === "manager") {
            this.$router.push("/product");
          } else if (role === "admin") {
            this.$router.push("/Adashboard");
          } else {
            this.$router.push("/user/products");
          }
        } else {
          this.errorMessage = "Login canceled by user.";
        }
      } catch (error) {
        this.errorMessage = "Invalid credentials or user is not active.";
      }
    },
  },
};
</script>
