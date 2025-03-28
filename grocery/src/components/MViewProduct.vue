<template>
    <div>
      <div class="container mt-4 shadow">
  
        <!-- Header Section -->
        <div class="text-center mb-4">
          <h1>Product Management</h1>
  
          <div class="text-center mb-4">
            <router-link :to="{ name: 'ManagerAddProducts' }">
              <button class="btn btn-primary mx-2">Add Product</button>
            </router-link>
            
          </div>
          <div v-if="errorMessage" class=" mt-3">
            <div class="alert alert-danger" role="alert">
              {{ errorMessage }}
            </div>
          </div>
          <div v-if="successMessage" class=" mt-3">
            <div class="alert alert-success" role="alert">
              {{ successMessage }}
            </div>
          </div>
  
          <!-- Product Cards Section -->
          <div class="row">
            <div v-if="products.length === 0">
              <div>No products available.</div>
            </div>
  
  
            <div v-for="product in products" :key="product.item_id" class="card">
                <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <div class="card-text">{{ product.desc }}</div>
                <div class="card-text"><strong>Stock:</strong> {{ product.stock }}</div>
                <div class="card-text"><strong>Price: </strong>{{ product.price_per_unit }} ₹/{{ product.unit }} </div>
                <div class="card-text"><strong>Category: </strong>{{ product.category }}</div>
                <div class="card-text"><strong>Status:</strong> {{ product.status }}</div>
  
                <div class="btn-group" role="group">
                  <button @click="confirmEdit(product)" class="btn btn-primary">Edit</button>
                  <button @click="confirmAction(product.id, product.is_status)" class="btn btn-warning">
                    {{ actionText(product.is_status) }}
                  </button>
                </div>
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
    name: 'MViewProduct',
    data() {
      return {
        products: [],
        errorMessage: '', 
        successMessage: '',
      };
    },
    created() {
      const categoryId = this.$route.params.categoryId;
      if (categoryId) {
        this.fetchProducts(categoryId);
      } 
    },
    methods: {
      fetchProducts(categoryId) {
        const token = localStorage.getItem('token');
        axios.get(`http://127.0.0.1:5000/manager/products/${categoryId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
          .then(response => {
            this.products = response.data.map(product => ({
              ...product,
              category_name: this.fetchCategoryName(product.category_id),
            }));
          })
          .catch(error => {
            console.error('Error fetching products:', error);
            this.errorMessage = 'Error fetching products. Please try again.';
            this.successMessage = '';
          });
      },
  
      fetchCategoryName(categoryId) {
        if (categoryId === undefined) {
          return 'Unknown Category';
        }
  
        const token = sessionStorage.getItem('access_token');
        return axios
          .get(`http://127.0.0.1:5000/manager/categories/${categoryId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          })
          .then((response) => {
            const categoryDetails = response.data;
            return categoryDetails.name;
          })
          .catch((error) => {
            console.error(`Error fetching category name for ID ${categoryId}:`, error);
            return 'Unknown Category';
          });
      },
  
      actionText(is_status) {
        return is_status === 'Active' ? 'Disable' : 'Enable';
      },
  
      confirmAction(ProductId, currentStatus) {
        const action = this.actionText(currentStatus).toLowerCase();
        const confirmation = confirm(`Are you sure you want to ${action} this product?`);
        if (confirmation) {
          this.performAction(ProductId, currentStatus);
        }
      },
  
      performAction(ProductId, currentStatus) {
        const action = currentStatus === 'Active' ? 'disable' : 'enable';
        axios
          .patch(
            `http://127.0.0.1:5000/manager/update_product/${ProductId}`,
            { action },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
              },
            }
          )
          .then((response) => {
            console.log(response.data.message);
            const updatedProductIndex = this.products.findIndex((product) => product.product_id === ProductId);
            if (updatedProductIndex !== -1) {
              this.products[updatedProductIndex].is_status = response.data.message.includes('enable') ? 'Active' : 'Not Active';
              this.successMessage = `Product ${action}d successfully.`;
              this.errorMessage = '';
            
            }
          })
          .catch((error) => {
            console.error(`Error ${action}ing product:`, error);
            this.errorMessage = `Error ${action}ing product. Please try again.`;
            this.successMessage = '';
             
          });
      },
  
      confirmEdit(product) {
        const confirmationMessage = 'Are you sure you want to edit this product?';
  
        if (confirm(confirmationMessage)) {
          this.$router.push(`/manager/edit_product/${product.product_id}`);
        }
      },
  
      goToAddCategory() {
        this.$router.push('/manager/add_category');
      },
  
      downloadCSV() {
        const token = localStorage.getItem('token');
        const apiUrl = 'http://127.0.0.1:5000/download/products/csv';
  
        axios.get(apiUrl, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          responseType: 'arraybuffer',
        })
          .then(response => {
            const blob = new Blob([response.data], { type: 'text/csv' });
            const link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = 'products.csv';
            document.body.appendChild(link);  
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(link.href);
            this.successMessage = `CSV downloaded successfully.`;
            this.errorMessage = '';
            setTimeout(() => {
              this.successMessage = '';
            
            }, 1000);
            
            
          })
          .catch(error => {
            console.error('Error downloading CSV:', error);
            this.errorMessage = 'Error downloading CSV. Please try again.';
            this.successMessage = '';
            setTimeout(() => {
              this.errorMessage = '';
            
            }, 1000);
          });
      },
  
      
    },
  };
  </script>
    
  <style scoped>
  .container {
    background-color: #f4efef;
    padding: 20px;
    border-radius: 10px;
  }
  
  .card {
    border: 1px solid #ddd;
    border-radius: 10px;
    max-width: 350px;
    margin-left: 20px;
    margin-bottom: 20px;
    text-align: left;
    
  }
  
  .card-img-top {
    max-width: 100%;
    max-height: 300px;
    margin-top: 10px;
    border-radius: 8px;
    image-rendering: -webkit-optimize-contrast;
    object-fit: cover;
  }
  </style>
    