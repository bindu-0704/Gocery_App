<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light" >
      <i class="fa-solid fa-basket-shopping custom-icon"></i>
      <a class="navbar-brand"><em>Grocery Store</em></a>

      <!-- Toggle Button for Mobile View -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a class="nav-link" href="/user/cart">Cart</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/user/orders">My Orders</a>
          </li>
        </ul>
        <form class="d-flex flex-grow-1 mx-3" @submit.prevent="searchProducts">
          <input class="form-control me-2" type="search" placeholder="Search for products..." aria-label="Search" v-model="searchTerm">
          <button class="btn btn-outline-light custom-search-btn" type="submit">Search</button>
          <button class="btn btn-outline-secondary mx-2" @click="thefetchproducts">Reset</button>
        </form>
        <button class="btn btn-outline-danger my-2 my-sm-0 ml-auto" @click="logout">Logout</button>
      </div>
    </nav>

    <div class="container product-section my-5" ref="productSection">
      <h2 class="text-center mb-5">Shop by Products</h2>
      <div class="category-column">
        <div class="row">
          <div v-for="product in products" :key="product.id" class="col-md-4 mb-4">
            <div :class="['card', { 'out-of-stock': product.stock === 0 }]">
              <div class="card-body">
                <h3 class="card-title">{{ product.name }}</h3>
                <p class="card-text">Category: {{ product.category }}</p>
                <p class="card-text">{{ product.desc }}</p>
                <p class="card-text">Price: {{ product.price_per_unit }}/{{ product.unit_of_measurement }}</p>
                <p class="card-text" v-if="product.stock === 0" style="color: red;">Out of Stock</p>
                
                <form @submit.prevent="addToCart(product)" v-if="product.stock > 0">
                  <div class="input">
                    <input v-model="product.quantity" type="number" min="1" :max="product.stock" required class="quantity" placeholder="Quantity" />
                  </div>
                  <button class="btn btn-success">Add to Cart</button>
                </form>
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
  name: 'UserDashboard',
  data() {
    return {
      products: [],
      searchTerm: '',
    };
  },
  mounted() {
    this.thefetchproducts();
  },
  methods: {
    thefetchproducts() {
      const token = localStorage.getItem('token');
      axios.get('http://localhost:5000/user/products', {
        headers: { Authorization: `Bearer ${token}` },
      })
        .then(response => {
          this.products = response.data;
        })
        .catch(error => {
          console.error('Error fetching products:', error);
        });
    },
    addToCart(product) {
      const token = localStorage.getItem('token');
      const data = { product_id: product.product_id, quantity: product.quantity };
      
      if (window.confirm(`Do you want to add ${product.quantity} ${product.name}(s) to the cart?`)) {
        axios.post('http://localhost:5000/user/add_to_cart', data, {
          headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }
        })
        .then(() => {
          alert('Product added to cart');
          this.thefetchproducts();
        })
        .catch(error => {
          console.error('Error adding item to cart:', error);
        });
      }
    },
    logout() {
      if (window.confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('token');
        this.$router.push('/');
      }
    },
    searchProducts() {
      const searchTermLower = this.searchTerm.toLowerCase();
      const filteredProducts = this.products.filter(product => 
        (product.name.toLowerCase().includes(searchTermLower) || 
        product.category.toLowerCase().includes(searchTermLower)) && 
        product.is_status === 'Active'); // Filter only active products during search
      this.products = filteredProducts;

      // Scroll to the "Shop by Products" section
      this.$nextTick(() => {
        const section = this.$refs.productSection;
        if (section) {
          section.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    }
  }
};
</script>

<style scoped>
/* Main styling for navbar */
.navbar {
  background-color: #f7fbf8 !important;
}

.custom-icon {
  color: rgb(130, 87, 7);
  font-size: 40px;
  margin-right: 10px;
}
.navbar-brand {
  color: rgb(206, 91, 8);
  font-size: 40px;
}

.navbar-nav .nav-item {
  margin-right: 20px;
}

.navbar-collapse {
  justify-content: flex-end;
}

.form-control {
  border-radius: 30px;
  height: 40px;
}

.btn {
  border-radius: 20px;
}

.btn-outline-light, .btn-outline-secondary {
  border-radius: 20px;
}

/* Custom styles for search button */
.custom-search-btn {
  background-color: #28a745;
  color: white;
  border-color: #28a745;
}

.product-section {
  padding-top: 0px; /* Reduced gap between navbar and products */
}

/* Styling for products */
.card {
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 15px;
  text-align: center;
}

.card-title {
  font-size: 20px;
  font-weight: bold;
}

.card-text {
  font-size: 14px;
}

.quantity {
  width: 80px;
  margin-right: 10px;
}

.input {
  display: flex;
  justify-content: center;
  margin-bottom: 15px;
}

.out-of-stock .card-body {
  background-color: #f8d7da;
  color: #721c24;
}

.out-of-stock .card-body p {
  color: #721c24;
}

.category-column {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
}

.col-md-4 {
  flex: 0 0 30%;
  margin-bottom: 20px;
}

.container {
  margin-top: 20px;
}

/* Ensure responsive layout */
@media (max-width: 768px) {
  .col-md-4 {
    flex: 0 0 45%;
  }
}

@media (max-width: 576px) {
  .col-md-4 {
    flex: 0 0 100%;
  }
}
</style>
