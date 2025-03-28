<template>
  <div class="page-container">
    <div class="create-category-form">
      <!-- Red Cross Icon for Close -->
      <button @click="closePage" class="close-btn">
        <i class="fas fa-times"></i>
      </button>
      <h1>Create a New Category</h1>
      <form @submit.prevent="confirmAndCreateCategory" class="form-container">
        <div class="form-group">
          <label for="name">Category Name:</label>
          <input type="text" id="name" v-model="category.name" required />
        </div>
        <button type="submit" class="btn-primary">Create Category</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ACreateCategory',
  data() {
    return {
      category: {
        name: '',
      },
    };
  },

  methods: {
    confirmAndCreateCategory() {
      if (window.confirm('Are you sure you want to create this category?')) {
        this.createCategory();
      }
    },

    createCategory() {
      const token = localStorage.getItem('token');
      axios.post('http://localhost:5000/admin/category', this.category, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          console.log('Category created successfully:', response.data);
          alert('Category created successfully');
          this.$router.push('/categories');
        })
        .catch(error => {
          console.error('Error creating category:', error.response.data.error);
          alert(error.response ? error.response.data.error : 'An error occurred while creating the category.');
        });
    },

    closePage() {
      this.$router.push('/categories'); // Redirect to the home page or previous page
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
  opacity: 0.8; /* Adjust opacity for the entire container */
}


/* Centered Form Styling */
.create-category-form {
  max-width: 400px;
  width: 100%;
  padding: 30px;
  background-color: #f4f4f4;  /* White background for the form */
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);  /* Add shadow for a pop-up effect */
  position: relative;  /* Make sure the cross button is positioned relative to the form */
}

h1 {
  text-align: center;
  color: #343a40; 
  font-size: 24px;
}

form {
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
