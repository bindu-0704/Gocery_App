<template>
  <div>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-light">
      <i class="fa-solid fa-basket-shopping custom-icon"></i>
      <a class="navbar-brand"><em>Grocery Store</em></a>

      <!-- Toggle Button for Mobile View -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          <li class="nav-item active">
            <router-link to="/user/orders" class="nav-link" title="Go to Order Page">My Orders</router-link>
          </li>
        </ul>
      </div>
      <!-- Icon on the Right Corner -->
      <div class="nav-item active">
        <router-link to="/user/products" class="nav-link back-arrow" title="Back to User Dashboard" >
          <i class="fa fa-arrow-left"></i> <!-- Icon for Back -->
        </router-link>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="card-container">
      <h1 class="heading">Your Shopping Cart</h1>

      <div v-if="loading" class="spinner-container">
        <i class="fa fa-spinner fa-spin"></i> Loading...
      </div>

      <div class="row">
        <div v-for="item in cartItems" :key="item.id" class="col-md-4 mb-4">
          <div class="card shadow-sm rounded">
            <div class="card-body">
              <h3>{{ item.product.name }}</h3>
              <p v-if="item.product.stock >= item.quantity">Quantity: {{ item.quantity }}</p>
              <p v-else class="out-of-stock">Out of stock. Remove this product from cart.</p>
              <p>Total Amount: ₹ {{ item.total_amount }}</p>
              <div class="button-container">
                <button @click="buyConfirmation(item.product)" :disabled="item.product.stock < item.quantity" class="btn btn-success">
                  Buy
                </button>
                <button @click="removeFromCartConfirmation(item.product)" class="btn btn-danger">Remove</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- "Buy All" Button only visible if there are items in the cart -->
      <button v-if="cartItems.length > 0" @click="buyAllConfirmation" :disabled="isAnyItemOutOfStock" class="btn btn-primary buy-all-button">
        Buy All
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Navigation Bar Styles */
.navbar {
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.custom-icon {
  color: rgb(130, 87, 7);
  font-size: 40px;
  margin-right: 10px;
}

.navbar-brand {
  color: rgb(206, 91, 8);
  font-size: 28px;
  font-weight: bold;
}

/* Align the "Back" Icon to the Right */
.navbar-nav {
  margin-right: auto; /* Ensure the other items are pushed to the left */
}

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


.navbar .back-icon:hover {
  color: rgb(206, 91, 8); /* Change color on hover */
}

/* Card Container Styles */
.card-container {
  margin: 30px;
}

.heading {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

/* Card Styles */
.card {
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.card-body h3 {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 10px;
}

.out-of-stock {
  color: red;
  font-weight: bold;
}

.button-container {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.button-container button {
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  width: 45%;
  transition: background-color 0.3s ease;
}

.card-body button:disabled {
  background-color: #d6d6d6;
  cursor: not-allowed;
}

/* Buy All Button Styles */
.buy-all-button {
  background-color: #28a745;
  color: #fff;
  padding: 12px 20px;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  width: auto;
  margin-top: 20px;
  transition: background-color 0.3s ease;
}

.buy-all-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* Spinner Styles */
.spinner-container {
  text-align: center;
  font-size: 18px;
  margin-top: 20px;
  color: #007bff;
}

/* Button Hover Effects */
.btn:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

/* Additional Styles for Buttons */
.btn {
  border-radius: 6px;
  padding: 12px 25px;
  font-size: 14px;
}

.btn-success {
  background-color: #28a745;
  color: white;
  transition: background-color 0.3s ease;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  transition: background-color 0.3s ease;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-danger:hover {
  background-color: #c82333;
}
</style>

<script>
import axios from 'axios';

export default {
  name: 'UserCart',
  data() {
    return {
      cartItems: [],
      loading: false,  // Loading state
    };
  },
  mounted() {
    this.fetchCartItems();
  },
  methods: {
    fetchCartItems() {
      this.loading = true;
      const token = localStorage.getItem('token');
      axios.get('http://localhost:5000/user/cart', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then(response => {
        this.cartItems = response.data;
      })
      .catch(error => {
        console.error('Error fetching cart items:', error);
      })
      .finally(() => {
        this.loading = false;  // End loading state
      });
    },
    buyConfirmation(product) {
      const confirmationMessage = `Do you want to buy ${product.name}?`;
      if (window.confirm(confirmationMessage)) {
        this.buy(product);
      }
    },
    buy(product) {
      const token = localStorage.getItem('token');
      const data = {
        product_id: product.id,
      };

      axios.post('http://localhost:5000/user/buy', data, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        console.log(response.data.message);
        this.reloadPage();
      })
      .catch(error => {
        console.error('Error buying item:', error);
      });
    },
    removeFromCartConfirmation(product) {
      const confirmationMessage = `Do you want to remove ${product.name} from the cart?`;
      if (window.confirm(confirmationMessage)) {
        this.removeFromCart(product);
      }
    },
    removeFromCart(product) {
      const token = localStorage.getItem('token');
      const productId = product.id;

      axios.delete('http://localhost:5000/user/remove', {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        data: { product_id: productId }
      })
      .then(response => {
        console.log(response.data.message);
        this.fetchCartItems();
      })
      .catch(error => {
        console.error('Error removing item from cart:', error);
      });
    },
    buyAllConfirmation() {
      const confirmationMessage = 'Do you want to buy all items in the cart?';
      if (window.confirm(confirmationMessage)) {
        this.buyAll();
      }
    },
    buyAll() {
      const token = localStorage.getItem('token');
      const data = {
        cartItems: this.cartItems.map(item => item.product.id),
      };

      axios.post('http://localhost:5000/user/buy_all', data, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      .then(response => {
        console.log(response.data.message);
        this.reloadPage();
      })
      .catch(error => {
        console.error('Error buying all items:', error);
      });
    },
    reloadPage() {
      location.reload();
    },
  },
  computed: {
    isAnyItemOutOfStock() {
      return this.cartItems.some(item => item.product.stock < item.quantity);
    }
  },
};
</script>
