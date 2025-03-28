<template>
  <div>
    <div class="container">
      <div class="title">
        <!-- Add Category Button at the top left corner -->
        <button @click="goToAddCategory" class="btn-add-category">
          Add Category
        </button>
        <h2 class="text-center">Categories</h2>
        <button @click="closePage" class="close-btn" >
          <i class="fas fa-times" title="BACK TO PREVIOUS PAGE"></i>
        </button>
      </div>
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
      <div class="category-container">
        <div v-for="category in categories" :key="category.cat_id" class="card mb-3 category-card">
          <div class="card-body">
            <h5 class="card-title">{{ category.name }}</h5>
            <div class="btn-group" role="group">
              <button @click="confirmEdit(category)" class="btn btn-primary btn-sm">Edit</button>
              <button @click="confirmEnableDisable(category)" class="btn btn-danger btn-sm">
                {{ category.is_status === 'Active' ? 'Disable' : 'Enable' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MCategory',
  data() {
    return {
      categories: [],
      errorMessage: '',
      successMessage: '',
    };
  },
  mounted() {
    this.fetchCategories();
  },
  methods: {
    fetchCategories() {
      const token = localStorage.getItem('token');
      axios.get('http://127.0.0.1:5000/manager/categories', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          console.log('Categories:', response.data);
          this.categories = response.data;
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
        });
    },
    confirmEnableDisable(category) {
      const confirmationMessage = `Are you sure you want to ${category.is_status === 'Active' ? 'disable' : 'enable'} this category?`;

      if (confirm(confirmationMessage)) {
        this.enableDisableCategory(category.id, category.is_status === 'Active');
      }
    },

    enableDisableCategory(categoryId, enable) {
      const token = localStorage.getItem('token');
      const action = enable ? 'disable' : 'enable';

      axios.patch(`http://127.0.0.1:5000/manager/update_category/${categoryId}`, { action }, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      })
        .then(response => {
          console.log(`Category ${action}d successfully:`, response.data);
          this.successMessage = response.data.message;
          this.errorMessage = '';
          this.fetchCategories();
        })
        .catch(error => {
          console.error(`Error ${action}ing category:`, error);
          this.errorMessage = error.response.data.message;
          this.successMessage = '';
        });
    },

    confirmEdit(category) {
      const confirmationMessage = 'Are you sure you want to edit this category?';

      if (confirm(confirmationMessage)) {
        this.$router.push(`/manager/edit_category/${category.id}`);
      }
    },
    goToAddCategory() {
      this.$router.push('/manager/add_category');
    },
    closePage() {
      this.$router.push('/product');
    }
  },
};
</script>

<style scoped>
.container {
  background-color: #f8f9fa;
  border-radius: 10px;
  margin-top: 20px;
  padding: 20px;
}

.title {
  position: relative;
  padding: 10px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.btn-add-category {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-add-category:hover {
  background-color: #0056b3;
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

.category-container {
  display: flex;
  justify-content: left;
  flex-wrap: wrap;
}

.category-card {
  width: 300px;
  margin: 0 20px 20px 0;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.category-card:hover {
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  transition: box-shadow 0.3s ease-in-out;
}

.btn-primary,
.btn-danger {
  width: 100%;
  margin-top: 10px;
}

.alert {
  border-radius: 10px;
}
</style>
