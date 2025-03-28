<template>
  <div class="page-container">
    <div class="update-category-form">
      <button @click="closePage" class="close-btn">
        <i class="fas fa-times"></i>
      </button>
      <h1 class="text-center">UPDATE CATEGORY</h1>
      <form @submit.prevent="confirmAndUpdateCategory" class="form-container">
        <div class="form-group">
          <label for="name">Category Name:</label>
          <input type="text" id="name" v-model="category.name" required />
        </div>
        <button type="submit" class="btn btn-primary">Update Category</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AUpdateCategory',
  data() {
    return {
      category: {
        name: '',
      },
      categoryId: null,
    };
  },
  mounted() {
    const { id } = this.$route.params;

    if (!id) {
      console.error('Category ID not found!');
      return;
    }

    this.categoryId = id;
    this.fetchCategory(id);
  },

  methods: {
    fetchCategory(category_id) {
      const token = localStorage.getItem('token');
      axios.get(`http://localhost:5000/admin/categories/${category_id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          this.category = { ...response.data };
        })
        .catch((error) => {
          console.error(error);
          alert('An error occurred while fetching category data.');
        });
    },

    confirmAndUpdateCategory() {
      if (window.confirm('Are you sure you want to update this category?')) {
        this.updateCategory();
      }
    },

    updateCategory() {
      const token = localStorage.getItem('token');
      axios.put(`http://localhost:5000/admin/categories/${this.categoryId}`, this.category, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(() => {
          alert('Category updated successfully!');
          this.$router.push('/categories');
        })
        .catch((error) => {
          console.error(error);
          alert('An error occurred while updating the category.');
        });
    },

    closePage() {
      this.$router.push('/categories'); // Redirect to home or another page
    },
  },
};
</script>

<style scoped>
/* Full Background */
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

/* Centered Form Styling */
.update-category-form {
  max-width: 400px;
  width: 100%;
  padding: 30px;
  background-color: #f4f4f4;  /* Transparent white background */
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);  /* Add shadow for a pop-up effect */
  position: relative;
}

/* Close Button */
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

/* Heading Styling */
h1 {
  text-align: center;
  color: #343a40; 
}

/* Form Styling */
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

/* Button Styling */
.btn-primary {
  background-color: #28a745;
  color: #fff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 4px;
}

.btn-primary:hover {
  background-color: #218838;
}

/* Error and Success Messages */
.error-message {
  color: #dc3545;
  margin-top: 10px;
}

.success-message {
  color: #28a745;
  margin-top: 10px;
}
</style>
