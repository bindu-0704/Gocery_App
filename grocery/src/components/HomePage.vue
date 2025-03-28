<template>
    <div >
      <div class="top d-flex justify-content-between align-items-center">
  <div class="brand d-flex align-items-center">
    <div class="basket-icon">
      <i class="fa-solid fa-basket-shopping custom-icon"></i>
    </div>
    <h2 class="heading ms-2">Grocery Store</h2>
  </div>
  <div class="search">
    <form class="d-flex flex-grow " @submit.prevent="searchProducts">
      <input class="form-control flex-grow" type="search" placeholder="Fruits, Vegetables, Snacks..." aria-label="Search" v-model="searchTerm">
      <button class="btn btn-outline-success" type="submit">Search</button>
    </form>
  </div>
  <div class="user d-flex align-items-center">
    <i class="fa-solid fa-user" @click="register"></i>
    <h3 @click="register" class="ms-2">Account</h3>
  </div>
</div>

<!-- Navbar Section -->
<nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <!-- Navbar Toggler -->
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Navbar Brand -->
        

        <!-- Collapsible Navbar Content -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <div class="dropdown">
              <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                Dropdown button
              </button>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#">Action</a></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li><a class="dropdown-item" href="#">Something else here</a></li>
              </ul>
            </div>

            <!-- Regular Nav Item -->
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Home</a>
            </li>

            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Offer</a>
            </li>
            
            

            <!-- Another Nav Item -->
            <li class="nav-item">
              <a class="nav-link" href="#">Deals</a>
            </li>
          </ul>

          <!-- Offcanvas Trigger Button -->
          <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample" aria-controls="offcanvasExample">
            My Cart
          </button>
        </div>
      </div>
    </nav>


<!-- Offcanvas Section -->
<div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasExampleLabel">Offcanvas Right</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    <p>
      Some text as placeholder. In real life, you can have <a href="#" class="btn btn-primary">links</a> here.
    </p>
  </div>
</div>




    

        
    <!-- Hero Section 
    <div class="hero-section text-center text-white">
      <h1>Fresh Groceries Delivered to Your Doorstep</h1>
      <p>Explore our wide range of fresh fruits, vegetables, and daily essentials.</p>
      <button class="btn btn-primary mt-3 " v-on:click="shopnow">Shop Now</button>
    </div>-->
    <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="carousel">
  <div class="carousel-indicators">
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="2" aria-label="Slide 3"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="@/assets/carousel3.jpg" class="d-block " alt="...">
    </div>
    <div class="carousel-item">
      <img src="@/assets/carousel1.jpg" class="d-block " alt="...">
    </div>
    <div class="carousel-item">
      <img src="@/assets/carousel2.jpg" class="d-block " alt="...">
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>
   
    <!-- Featured Categories -->
    
    <div class="container-category product-section" ref="productSection">
    <h2 class="text-center my-5">Shop by Products</h2>
    <div class="category-column">
      <div class="row">
        <div v-for="product in products" :key="product.id" class="col-md-4 mb-4">
          <div class="card">
            <div v-if="product.stock > 0" class="card">
              <div class="card-body">
                <h3 class="card-title">Name: {{ product.name }}</h3>
                <p class="card-text">Price: {{ product.price_per_unit }}/{{ product.unit_of_measurement }}</p>

                <form @submit.prevent="addToCart(product)">
                  <div class="input">
                    <input v-model="product.quantity" type="number" min="0" :max="product.stock" required class="quantity" placeholder="Quantity" />
                  </div>
                  <button class="btn btn-success">Add to Cart</button>
                </form>
              </div>
            </div>
            <div v-else class="disabled-card" style="cursor: not-allowed;">
              <div class="card-body">
                <h3 class="card-title">Name: {{ product.name }}</h3>
                <p class="card-text" style="color: red;">Out of Stock</p>
              </div>
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
  name: 'HomePage',
  data() {
    return {
      products: [],
      searchTerm:'',
      category:'',
    };
  },
  mounted() {
    this.thefetchproducts()
  },
  methods: {
    thefetchproducts() {
      const token = localStorage.getItem('token');
      console.log(token);
      axios.get('http://localhost:5000/user/products')
      .then(response => {
        console.log('Response Data:', response.data);
        this.products = response.data;
      })
      .catch(error => {
        console.error('Error fetching products:', error);
      });

    },
    addToCart() {
      const token = localStorage.getItem('token');
      if (!token) {
        alert("Please log in to add items to the cart.");
        this.$router.push('login');
      }

      
    },
    register() {
      this.$router.push('/register'); // Redirect to home or another page
    },
    shopnow() {
      
      // Close the login form or redirect to another page
      this.$router.push('/register'); // Redirect to home or another page
      alert("Please register first");
    },
    async searchProducts() {
      const token = localStorage.getItem('token');
      console.log('token:', token);
      if(!this.searchTerm){
          this.thefetchproducts();
          this.$refs.productSection.scrollIntoView({behaviour : 'smooth' , block: 'start'})
      }else{
        axios.post('http://localhost:5000/user/search_products', {
          searchterm: this.searchTerm,
        }, { headers: { Authorization: `Bearer ${token}` } })
        .then(response => {
          console.log(response.data);
          this.products = response.data.result;
          if (this.$refs.productSection){
            this.$refs.productSection.scrollIntoView({behaviour : 'smooth' , block: 'start'})
          }
        })
        .catch(error => {
          console.error('Error fetching products:', error);
        });
      }
    }
  }
}
</script>

<style scoped>
/* Navbar Styles */



.top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e0e0e0;
}

.brand {
  display: flex;
  align-items: center;
}

.basket-icon {
  margin-right: 2px;
  font-size: 4px;  
}

.custom-icon {
  color: rgb(130, 87, 7);
  font-size: 4px; 
}

.heading {
  font-size: 24px; 
  font-weight: bold;
  color: rgb(206, 91, 8); 
}

.search {
  flex-grow: 1;
  margin: 0 20px;
  margin-left: 180px;
  border-radius: 2%;
}

.search .form-control {
  border-radius: 30px;
  height: 40px;
  align-items: center;
  max-width: 500px;
}

.search .btn {
  margin-left: 10px;
  background-color: #4CAF50;
  color: #fff;
  border-radius: 20px;
  padding: 8px 16px;
}

.user {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.user i {
  font-size: 20px;
  margin-right: 8px;
  color: #333;
}

.user h3 {
  font-size: 1rem;
  margin: 0;
  color: #333;
}

.carousel-control-prev-icon {
  background-color: #333;
}

.carousel-control-next-icon {
  background-color: #333;
}
.carousel-item img{
  width: 1500px;
  height: 500px;
  border-radius: 50px;
}

.custom-navbar {
  
  top: 0;
  width: 100%;
  z-index: 1000;
  background-color: rgb(251, 250, 251) !important;
  height: 80px !important;
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

/* Hero Section */
.hero-section {
  /*background: url('@/assets/grocery.jpg') no-repeat center center/cover;*/
  padding: 100px 20px;
  height: 500px
}

.hero-section h1 {
  font-size: 3rem;
  color: rgb(206, 91, 8);
}

.hero-section p {
  font-size: 1.2rem;
  margin-top: 10px;
  color: rgb(245, 244, 241);
}

.hero-section .btn {
  margin-top: 20px;
}

/* Categories Section */
.categories-section {
  padding: 50px 0;
}

.category-img {
  width: 100%;
  height: 200px; /* Set a fixed height for consistency */
  object-fit: cover; /* Ensures the images cover the space without distortion */
  border-radius: 10px;
  margin-bottom: 10px;
}

h4 {
  margin-top: 10px;
  color: #333;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2rem;
  }

  .hero-section p {
    font-size: 1rem;
  }
  
  .category-img {
    border-radius: 5px;
    height: 150px; /* Adjust height for mobile */
  }
}
</style>
