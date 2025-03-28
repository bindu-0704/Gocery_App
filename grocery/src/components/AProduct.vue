<template>
  <div class="page-container">
    <a href="/categories" class="back-btn">
      <i class="fas fa-times"></i>
    </a>

    <h1 class="text-center">Products in Category</h1>

    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Description</th>
          <th>Stock</th>
          <th>Price per Unit</th>
          <th>Expiry Date</th>
          <th>Manufacturing Date</th>
          <th>Status</th>
          <th>Discount</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.product_id">
          <td>{{ product.product_id }}</td>
          <td>{{ product.name }}</td>
          <td>{{ product.desc }}</td>
          <td>{{ product.stock }}</td>
          <td>{{ product.price_per_unit }}</td>
          <td>{{ product.exp || 'Not Available' }}</td>
          <td>{{ product.mfg || 'Not Available' }}</td>
          <td>{{ product.is_status }}</td>
          <td>{{ product.discount }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      products: [],
    };
  },
  mounted() {
    this.getProducts()
  },
  methods: {
    getProducts() {
      const categoryId = this.$route.params.categoryId;
      const token = localStorage.getItem('token');
      axios.get(`http://127.0.0.1:5000/admin/products/${categoryId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          this.products = response.data;
        })
        .catch((error) => {
          console.error(error);
          alert('An error occurred while fetching products.');
        });
    }
  }
}
</script>

<style scoped>
/* Container */
.page-container {
  background-color: #aec8ee;
  padding: 20px;
  position: relative;
  
}

/* Back Button */
.back-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  color: red;
  text-decoration: none;
  cursor: pointer;
}

.back-btn:hover {
  color: darkred;
}

/* Table Styling */
table {
  width: 100%;
  margin-top: 30px;
  background-color: #fff;
  border-collapse: collapse;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

th, td {
  padding: 12px;
  text-align: left;
  border: 1px solid #dee2e6;
}

th {
  background-color: #14f15e;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

tr:hover {
  background-color: #f1f1f1;
}

/* Heading Styling */
h1 {
  font-size: 2rem;
  color: #f18f26;
  font-weight: 600;
  margin-top: 20px;
}
</style>
