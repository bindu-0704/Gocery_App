<template>
  <div>
    <h1 class="text-center mt-3">Welcome, Manager</h1>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <router-link to="mproduct" class="navbar-brand">Create Product</router-link>
        <router-link to="mcategory" class="navbar-brand">View Categories</router-link>
        <button class="btn btn-outline-danger my-2 my-sm-0 ml-auto" @click="logout">Logout</button>
      </div>
    </nav>

    <button @click="generateMonthlyReport" class="btn btn-info position-absolute top-0 start-0 m-3">
      Generate Monthly Report
    </button>

    <h1 class="text-center mt-4">PRODUCT LIST</h1>

    <table class="table table-striped table-bordered container my-5">
      <thead class="table-light">
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Description</th>
          <th>Stock</th>
          <th>Price per Unit</th>
          <th>Category ID</th>
          <th>Expiry Date</th>
          <th>Mfg Date</th>
          <th>Discount</th>
          <th>Status</th>
          <th>Unit of Measurement</th>
          <th colspan="2" class="text-center">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id">
          <td>{{ product.id }}</td>
          <td>{{ product.name }}</td>
          <td>{{ product.desc }}</td>
          <td>{{ product.stock }}</td>
          <td>{{ product.price_per_unit }}</td>
          <td>{{ product.category_id }}</td>
          <td>{{ product.expiry_date || 'Not Available' }}</td>
          <td>{{ product.mfg_date || 'Not Available' }}</td>
          <td>{{ product.discount }}</td>
          <td>{{ product.is_status }}</td>
          <td>{{ product.unit_of_measurement }}</td>
          <td>
            <button class="btn btn-primary" @click="editProduct(product)">
              Edit
            </button>
          </td>
          <td>
            <button v-if="product.is_status === 'Active'" class="btn btn-warning" @click="enableDisableProduct(product)">
              Disable
            </button>
            <button v-else class="btn btn-success" @click="enableDisableProduct(product)">
              Enable
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style>

.container {
  max-width: 90%;
}

.text-center {
  text-align: center;
}

.mt-3 {
  margin-top: 1rem;
}

.mt-4 {
  margin-top: 1.5rem;
}

.table-light th {
  background-color: #f594c0 !important; /* Add !important to ensure the style is applied */
  color: #fff; /* Set text color to white to improve readability */
}

.table-light td {
  background-color: #f8f9fa; /* Optional: Adjust table row background color */
}

.position-absolute {
  position: absolute;
}

.top-0 {
  top: 0;
}

.start-0 {
  left: 0;
}

.m-3 {
  margin: 1rem;
}

.my-5 {
  margin-bottom: 3rem;
}
</style>

<script>
import axios from 'axios'
export default {
  name: 'ManagerDashboard',
  data() {
    return {
      products: [],
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      const token = localStorage.getItem('token');
      axios.get('http://localhost:5000/manager/products', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          this.products = response.data;
        })
        .catch((error) => {
          console.error(error);
          alert('An error occurred while fetching products.');
        });
    },
    editProduct(product) {
      alert(`Editing product with ID: ${product.id}`);
      this.$router.push(`/manager/edit_products/${product.id}`);
    },
    enableDisableProduct(product) {
      const token = localStorage.getItem('token');
      const newStatus = product.is_status === 'Active' ? 'Inactive' : 'Active';

      axios.patch(`http://localhost:5000/manager/products/${product.id}`, { action: newStatus }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(() => {
          product.is_status = newStatus;
          alert(`Product ${newStatus === 'Active' ? 'enabled' : 'disabled'} successfully!`);
        })
        .catch((error) => {
          console.error(error);
          alert('An error occurred while updating the product status.');
        });
    },
    generateMonthlyReport() {
      const token = localStorage.getItem('token');
      const apiUrl = 'http://127.0.0.1:5000/manager/generate_monthly_report';

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
    this.successMessage = "CSV downloaded successfully.";
    this.errorMessage = '';
    setTimeout(() => {
      this.successMessage = '';
    }, 1000);
  })
    .catch(error => {
      console.error('Error downloading CSV:', error);
      this.errorMessage = error.response.data.message;
      this.successMessage = '';
      setTimeout(() => {
        this.errorMessage = '';
      }, 1000);
    });
},

logout() {
  const confirmation = window.confirm('Are you sure you want to logout?');
  if (confirmation) {
    // Remove the token from localStorage
    localStorage.removeItem('token');
    
    // Redirect the user to the home page or login page
    this.$router.push('/');
  } else {
    // Optionally, you can add logic to handle the cancel action
    console.log('Logout canceled');
  }
}

  },
};
</script>
