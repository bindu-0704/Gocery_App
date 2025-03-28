<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg" >
      <i class="fa-solid fa-basket-shopping custom-icon"></i>
      <a class="navbar-brand"><em>Grocery Store</em></a>

      <!-- Toggle Button for Mobile View -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navbar Links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <!-- Back Icon with Link at Top Right -->
            <a href="/user/products" class="btn btn-outline-secondary back-arrow">
              <i class="fa fa-arrow-left"></i> 
            </a>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Page Title -->
    <h1 class="text-center mt-4 mb-5">My Orders</h1>

    <!-- Orders Display -->
    <div class="row">
      <div v-for="order in orders" :key="order.id" class="col-md-4 mb-4">
        <div class="order-card shadow">
          <div class="card-body">
            <h5 class="card-title">Order ID: {{ order.id }}</h5>
            <p class="card-text">Order Date: {{ order.order_date }}</p>
            <p class="card-text">Total Amount: ₹{{ order.total_amount }}</p>
            <p class="card-text">Order Status: {{ order.order_is_status }}</p>
            
            <div v-for="orderProduct in order.order_product" :key="orderProduct.id">
              <hr class="my-3">
              <h6 class="card-subtitle mb-2 text-muted">Product Details</h6>
              <p class="card-text">Product: {{ orderProduct.product.name }}</p>
              <p class="card-text">Quantity: {{ orderProduct.quantity }}</p>
              <p class="card-text">Price: ₹{{ orderProduct.price }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Navbar Styling */
.navbar {
  position: relative;
  border-bottom: 1px solid #ddd;
}

.custom-icon {
  color: rgb(130, 87, 7);
  font-size: 40px;
  margin-right: 10px;
}

.navbar-brand {
  color: rgb(206, 91, 8);
  font-size: 36px;
}

.navbar-nav .nav-item a {
  font-size: 18px;
  padding: 10px 15px;
}

.text-center {
  text-align: center;
  font-size: 30px;
  font-weight: bold;
}

/* Back Arrow Styling at Top-Right Corner */
.back-arrow {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  color: rgb(130, 87, 7);
  text-decoration: none;
}

.back-arrow i {
  font-size: 28px;
}

.back-arrow:hover {
  color: rgb(206, 91, 8); /* Change color on hover */
}

/* Order Card Styling */
.order-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 20px;
  font-weight: bold;
}

.card-text {
  font-size: 16px;
  margin-bottom: 10px;
}

.card-subtitle {
  color: #888;
  margin-top: 10px;
}

.card-text p {
  margin: 5px 0;
}

/* Responsive Styling */
@media (max-width: 768px) {
  .navbar-brand {
    font-size: 30px;
  }

  .custom-icon {
    font-size: 35px;
  }
}
</style>

<script>
import axios from 'axios';

export default {
  name: 'UserOrder',
  data() {
    return {
      orders: [],
    };
  },
  mounted() {
    this.fetchOrders();
  },
  methods: {
    fetchOrders() {
      const token = localStorage.getItem('token');
      axios.get('http://localhost:5000/user/orders', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          console.log('Orders:', response.data);
          this.orders = response.data;
        })
        .catch(error => {
          console.error('Error fetching orders:', error);
        });
    },
  },
};
</script>
