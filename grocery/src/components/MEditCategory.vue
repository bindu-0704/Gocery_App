<template>
  <div class="page-container">
    <div class="edit-category-form">
      <!-- Red Cross Icon for Close -->
      <button @click="closePage" class="close-btn">
        <i class="fas fa-times"></i>
      </button>
      <h1>Edit Category</h1>
      <form @submit.prevent="submitForm" class="form-container">
        <div class="form-group">
          <label for="newCategoryName">New Name:</label>
          <input type="text" id="newCategoryName" v-model="newName" class="form-control" required />
        </div>
        <button type="submit" class="btn-primary">Submit for Approval</button>
      </form>
      
      <!-- Success and Error Messages -->
      <div v-if="errorMessage" class="mt-3">
        <div class="alert alert-danger" role="alert">
          {{ errorMessage }}
        </div>
      </div>
      <div v-if="successMessage" class="mt-3">
        <div class="alert alert-success" role="alert">
          {{ successMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MEditCategory',
  data() {
    return {
      categoryName: '',  
      newName: '',       
      errorMessage: '',   
      successMessage: '',   
    };
  },
  mounted() {
    const categoryId = this.$route.params.id;
    this.fetchPreviousCategoryInfo(categoryId);
  },
  methods: {
    fetchPreviousCategoryInfo(categoryId) {
      const token = localStorage.getItem('token');
      axios.get(`http://127.0.0.1:5000/manager/categories/${categoryId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          const { name } = response.data;
          this.categoryName = name;
          this.newName = name;  
        })
        .catch(error => {
          this.errorMessage = error.response.data.message;
        });
    },
    submitForm() {
      const formData = new FormData();
      formData.append('name', this.newName);
  
      const token = localStorage.getItem('token');
      const categoryId = this.$route.params.id;
      axios.put(`http://127.0.0.1:5000/manager/edit_category/${categoryId}`, formData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      })
        .then(response => {
          console.log('Response:', response); // Now we are using 'response'
          this.successMessage = 'Changes submitted for approval.';
          this.$router.push('/mcategory');
        })
        .catch(error => {
          this.errorMessage = error.response.data.message;
        });
    },
    closePage() {
      this.$router.push('/mcategory');
    },
  },
};
</script>

<style scoped>
.page-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0.9;
}

.edit-category-form {
  max-width: 500px;
  width: 100%;
  padding: 30px;
  background-color: #f4f4f4;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  position: relative;
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

.alert {
  margin-top: 15px;
}

.alert-success {
  color: #155724;
  background-color: #d4edda;
  border-color: #c3e6cb;
}

.alert-danger {
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
}

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
</style>
