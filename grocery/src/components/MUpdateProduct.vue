<template>
  <div>
    <h1 class="text-center mt-5">UPDATE PRODUCT DETAILS</h1>
    <br />
    <div class="position-relative">
      <div class="container">
        <form @submit.prevent="updateProduct" class="p-4 bg-light rounded">
          <div class="mb-3">
            <label for="product-name" class="form-label">Name:</label>
            <input type="text" v-model="product.name" id="product-name" class="form-control" required placeholder="Enter product name" />
          </div>
          <div class="mb-3">
            <label for="product-desc" class="form-label">Description:</label>
            <textarea v-model="product.desc" id="product-desc" class="form-control" rows="3" placeholder="Enter product description"></textarea>
          </div>
          <div class="mb-3">
            <label for="product-stock" class="form-label">Stock:</label>
            <input type="number" v-model.number="product.stock" id="product-stock" class="form-control" required placeholder="Enter stock quantity" />
          </div>
          <div class="mb-3">
            <label for="product-discount" class="form-label">Discount:</label>
            <input type="number" v-model.number="product.discount" id="product-discount" class="form-control" required placeholder="Enter discount quantity" />
          </div>
          <div class="mb-3">
            <label for="product-price" class="form-label">Price per Unit:</label>
            <input type="number" v-model.number="product.price_per_unit" id="product-price" class="form-control" required placeholder="Enter price per unit" />
          </div>
          <div class="mb-3">
            <label for="product-category" class="form-label">Category:</label>
            <select v-model="product.category_id" id="product-category" class="form-control">
              <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">Update Product</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MUpdateProduct',
  data() {
    return {
      product: {
        name: '',
        desc: '',
        stock: 0,
        price_per_unit: 0,
        category_id: 0,
      },
      categories: [],
    };
  },
  mounted() {
    const { id } = this.$route.params;

    if (!id) {
      console.error('Product ID not found!');
      return;
    }

    this.fetchProduct(id);
  },
  methods: {
    fetchProduct(product_id) {

      const token = localStorage.getItem('token');
      this.fetchCategories()
      axios.get(`http://localhost:5000/manager/products/${product_id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          this.product = response.data;
        })
        .catch((error) => {
          console.error(error);
          alert('An error occurred while fetching product data.');
        });
    },
    fetchCategories(){
      const token = localStorage.getItem('token');
      axios.get(`http://localhost:5000/manager/categories`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
          this.categories = response.data
      })
      .catch((error=>{
        console.error(error);
        alert('An error occurred while fetching categories data.');
      }))
    },
    updateProduct() {
      const token = localStorage.getItem('token');
      const { id } = this.$route.params;

      axios.put(
        `http://localhost:5000/manager/edit_products/${id}`,
        this.product,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      )
        .then(() => {
          alert('Product updated successfully!');
          this.$router.push('/product')
        })
        .catch((error) => {
          console.error(error);
          alert('An error occurred while updating the product.');
        });
    },
  },
};
</script>

