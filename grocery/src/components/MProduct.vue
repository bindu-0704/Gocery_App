<template>
  <div class="container mt-5">
    <div class="close-btn" @click="closeForm">
      <i class="fas fa-times"></i> <!-- Cross Icon -->
    </div>

    <div class="card">
      <div class="card-header">
        <h1 class="mb-0">Create a New Product</h1>
      </div>
      <div class="card-body">
        <form @submit.prevent="createProduct" class="form-container">
          <div class="form-group">
            <label for="name">Product Name:</label>
            <input type="text" id="name" v-model="product.name" required class="form-control" placeholder="Enter product name" />
          </div>

          <div class="form-group">
            <label for="desc">Description:</label>
            <textarea id="desc" v-model="product.desc" class="form-control" placeholder="Enter description"></textarea>
          </div>

          <div class="form-group">
            <label for="stock">Stock:</label>
            <input type="number" id="stock" v-model="product.stock" required class="form-control" placeholder="Enter stock quantity" />
          </div>
          <div class="form-group">
            <label for="discount">Discount:</label>
            <input type="number" id="discount" v-model="product.discount" required class="form-control" placeholder="Enter discount quantity" />
          </div>

          <div class="form-group">
            <label for="price">Price per Unit:</label>
            <input type="number" id="price" v-model="product.price_per_unit" required class="form-control" placeholder="Enter price" />
          </div>

          <div class="form-group">
            <label for="expiry_date">Expiry Date:</label>
            <input type="date" id="expiry_date" v-model="product.expiry_date" class="form-control" />
          </div>

          <div class="form-group">
            <label for="mfg_date">Manufacturing Date:</label>
            <input type="date" id="mfg_date" v-model="product.mfg_date" class="form-control" />
          </div>

          <div class="form-group">
            <label for="unit_of_measurement">Unit of Measurement:</label>
            <input type="text" id="unit_of_measurement" v-model="product.unit_of_measurement" required class="form-control" placeholder="Enter unit of measurement" />
          </div>

          <div class="form-group">
            <label for="category">Select Category:</label>
            <select id="category" v-model="product.category_id" required class="form-control">
              <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
            </select>
          </div>

          <button type="submit" class="btn btn-primary w-100">Create Product</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MProduct',
  data() {
    return {
      product: {
        name: '',
        desc: '',
        stock: 0,
        price_per_unit: 0,
        expiry_date: '',
        mfg_date: '',
        is_status: '',
        unit_of_measurement: 'Kg',
      },
      categories: [],
    };
  },
  mounted() {
    this.getCategory();
  },
  methods: {
    getCategory() {
      const token = localStorage.getItem('token')
      console.log('Token:', token);

      axios.get('http://localhost:5000/manager/categories', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
        .then((response) => {
          this.categories = response.data;
        })
        .catch((error) => {
          console.error(error);
          alert('An error occurred while fetching categories.');
        });
    },
    createProduct() {
      const confirmationMessage = 'Do you want to create this product?';
      if (window.confirm(confirmationMessage)) {
        const token = localStorage.getItem('token');
        axios.post('http://localhost:5000/manager/product_create', this.product, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(response => {
          console.log('Product created successfully:', response.data);
          this.$router.push('/product');
        })
        .catch(error => {
          if (error.response && error.response.status === 400) {
            alert('Product with the same name already exists!');
          } else {
            console.error('Error creating product:', error);
          }
        });
      } else {
        alert('Product creation canceled by user.');
      }
    },
    closeForm() {
      // Close form logic or redirect to a different page
      this.$router.push('/product');
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 500px;
  margin: 0 auto;
}

.card {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.card-header {
  background-color: #f594c0;
  padding: 20px;
  border-bottom: 1px solid #ddd;
  text-align: center;
}

.card-body {
  padding: 30px;
  background-color: #f4f4f4 !important;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 8px;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
}

.form-group textarea {
  resize: vertical;
  height: 100px;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
  padding: 14px;
  font-size: 18px;
  border-radius: 5px;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.close-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  cursor: pointer;
  font-size: 30px;
  color: red; /* Red Cross */
}

.close-btn:hover {
  color: darkred; /* Darker red on hover */
}
</style>
