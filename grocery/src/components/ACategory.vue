<template>
  <div class="container-fluid">
    
    <button @click="closePage" class="close-btn">
        <i class="fas fa-times" href="/"></i>
      </button>
    <div class="row">
      <!-- Left Half for Category List -->
      <div class="col-6 left-half">
        <div class="header">
          <h1 class="text-left">Category List</h1>
          
        </div>
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="category in categories" :key="category.id">
              <td>{{ category.id }}</td>
              <td>{{ category.name }}</td>
              <td>
                <button class="btn btn-primary" @click="editCategory(category)">Edit</button>
                <button @click="confirmEnableDisable(category)" class="btn btn-warning">
                  {{ category.is_status === 'Active' ? 'Disable' : 'Enable' }}
                </button>
                <button @click="viewProducts(category.id)" class="btn btn-secondary">View Products</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Right Half for Category Approval Requests -->
      <div class="col-6 right-half">
        <div class="header">
          <h1 class="text-right">Category Approval Requests</h1>
        </div>
        <table class="table table-striped table-bordered">
          <thead>
            <tr>
              <th>ID</th>
              <th>Category Name</th>
              <th>Action</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in approvalRequests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.new_name }}</td>
              <td>{{ request.action }}</td>
              <td>{{ request.is_approved }}</td>
              <td>
                <button @click="approveRequest(request.id)" class="btn btn-success"
                  :disabled="request.is_approved !== 'Pending'">Approve</button>
                <button @click="rejectRequest(request.id)" class="btn btn-danger"
                  :disabled="request.is_approved !== 'Pending'">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  

  <!-- Fixed Add Category Button -->
    <div class="fixed-bottom">
      <div class="d-grid gap-2 d-md-flex justify-content-md-end">
        <router-link to="/acreatecategory">
          <button class="btn btn-primary me-md-2 btn-lg" type="button">Add Category</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style>
.container-fluid {
  display: flex;
  justify-content: space-between;
}

.row {
  width: 100%;
  display: flex;
}

.left-half, .right-half {
  padding: 20px;
  height: 100vh;
  overflow-y: auto;
}

.left-half {
  background-color: #f4f4f4;
}

.right-half {
  background-color: #ffffff;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  font-size: 1.5rem;
  font-weight: bold;
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

.close-btn i {
  font-size: 24px;
}

.table {
  margin-top: 1rem;
}

.fixed-bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #f4f4f4;
  border-top: 1px solid #ddd;
  padding: 1rem;
}

.btn-lg {
  font-size: 1.25rem;
}

.btn-primary,
.btn-warning,
.btn-secondary,
.btn-success,
.btn-danger {
  margin-right: 0.5rem;
}

.btn-primary:hover {
  background-color: #6d3205;
  border-color: #b35100;
}

.btn-warning:hover {
  background-color: #e0a800;
  border-color: #e0a800;
}

.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #5a6268;
}

.btn-success:hover {
  background-color: #218838;
  border-color: #218838;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #c82333;
}
</style>

<script>
import axios from 'axios';

export default {
  name: 'ACategory',
  data() {
    return {
      categories: [],
      approvalRequests: [],
    };
  },
  mounted() {
    this.getCategory();
    this.getApprovalRequests();
  },
  methods: {
    getCategory() {
      const token = localStorage.getItem('token');
      console.log(localStorage.getItem('token'));

      axios.get('http://localhost:5000/admin/categories', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          
          this.categories = response.data;
        })
        .catch((error) => {
          console.error(error);
          alert('An error occurred while fetching categories.');
        });
    },
    editCategory(category) {
      this.$router.push(`/categories/edit/${category.id}`);
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

      axios.patch(`http://127.0.0.1:5000/admin/categories/${categoryId}`, { action }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then(response => {
          console.log(`Category ${action}d successfully:`, response.data);
          this.displaySuccess(`Category ${action}d successfully`);
          this.getCategory();

        })
        .catch(error => {
          console.error(`Error ${action}ing category:`, error.response);
          this.displayError(`Failed to ${action} category. Please try again.`);
        });
    },
    viewProducts(categoryId) {
      this.$router.push(`/admin/products/${categoryId}`);
    },
    displaySuccess(message) {
      console.log(message);
    },
    displayError(message) {
      console.error(message);
    },
    getApprovalRequests() {
      const token = localStorage.getItem('token');
      axios.get('http://localhost:5000/admin/approval-requests', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
        .then((response) => {
          this.approvalRequests = response.data.filter(request => request.is_approved === 'Pending');
        })
        .catch((error) => {
          console.error(error);
          alert('An error occurred while fetching approval requests.');
        });
    },

    approveRequest(requestId) {
      const token = localStorage.getItem('token');

      if (window.confirm('Are you sure you want to approve this request?')) {
        axios.patch(`http://localhost:5000/admin/accept_approval/${requestId}`, {}, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
          .then((response) => {
            console.log('Approval successful:', response.data);
            this.displaySuccess('Approval successful');
            this.getApprovalRequests();
            this.getCategory();
          })
          .catch((error) => {
            console.error('Error approving request:', error.response);
            this.displayError('Failed to approve request. Please try again.');
          });
      }
    },

    rejectRequest(requestId) {
      const token = localStorage.getItem('token');
      const confirmationMessage = 'Are you sure you want to reject this request?';

      if (window.confirm(confirmationMessage)) {
        axios.delete(`http://localhost:5000/admin/reject_approval/${requestId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
          .then(response => {
            console.log('Rejection successful:', response.data);
            this.getApprovalRequests();
          })
          .catch(error => {
            console.error('Error rejecting request:', error.response);
          });
      }
    },

    

    closePage() {
      this.$router.push('/Adashboard'); // Redirect to the home page or previous page
    },
  },
};
</script>
