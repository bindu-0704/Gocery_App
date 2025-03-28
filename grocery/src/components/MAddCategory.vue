<template>
  <div class="page-container">
    <div class="create-category-form">
      <button @click="closePage" class="close-btn">
        <i class="fas fa-times"></i>
      </button>
      <h1>Create a New Category</h1>
      <form @submit.prevent="submitForm" class="form-container">
        <div class="form-group">
          <label for="newCategoryName">Category Name:</label>
          <input type="text" id="newCategoryName" v-model="newCategoryName" class="form-control" required>
        </div>
        <button type="submit" class="btn-primary">Create Category</button>
      </form>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MAddCategory',
  data() {
    return {
      newCategoryName: '',
      errorMessage: '',
      successMessage: '',
    };
  },
  methods: {
    submitForm() {
      const data = new FormData();
      data.append('name', this.newCategoryName);

      const token = localStorage.getItem('token');
      this.errorMessage = '';
      this.successMessage = '';

      axios.post('http://127.0.0.1:5000/manager/add_category', data, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          this.successMessage = response.data.message;
          alert(response.data.message);
          this.$router.push('/mcategory');
        })
        .catch(error => {
          this.errorMessage = error.response.data.message;
        });
    },
    
    closePage() {
      this.$router.push('/mcategory'); // Redirect to the categories page
    },
  },
};
</script>

<style scoped>
/* Full Background */
.page-container {
  height: 100vh;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0.8;
}

/* Centered Form Styling */
.create-category-form {
  max-width: 400px;
  width: 100%;
  padding: 30px;
  background-color: #f4f4f4;  /* White background for the form */
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);  /* Add shadow for a pop-up effect */
  position: relative;  /* Ensure the close button is positioned correctly */
}

h1 {
  text-align: center;
  color: #343a40; 
  font-size: 24px;
}

.form-container {
  margin-top: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  color: #495057; 
}

input {
  width: 100%;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ced4da; 
  border-radius: 4px;
}

.btn-primary {
  background-color: #28a745; 
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
  width: 100%;
}

.btn-primary:hover {
  background-color: #218838; 
}

.error-message {
  color: #dc3545; 
  margin-top: 10px;
}

.success-message {
  color: #28a745; 
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

.close-btn i {
  font-size: 24px;
}
</style>
