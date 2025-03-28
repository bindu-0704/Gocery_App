<template>
  <div class="admin-dashboard">
    <h1>Welcome, Admin</h1>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand-admin" href="#">ADMIN DASHBOARD</a>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            
            <li class="nav-item">
              <router-link to="/categories"><a class="navbar-brand" href="#">Category Section</a></router-link>
            </li>
          </ul>
        </div>
        <button class="btn btn-outline-danger my-2 my-sm-0 ml-auto" @click="logout">Logout</button>
      </div>
    </nav>

    <section class="request-section">
      <h2>Manager Approval Requests</h2>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="user_request_list.length === 0">
            <td colspan="5" class="text-center">No Requests Found</td>
          </tr>
          <tr v-for="request in user_request_list" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.name }}</td>
            <td>{{ request.email }}</td>
            <td>{{ request.role }}</td>
            <td>
              <button class="btn btn-success" @click="approve(request.id)">Approve</button>
              <button class="btn btn-danger" @click="reject(request.id)">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="user-list-section">
      <h2>User List</h2>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="user_list.length === 0">
            <td colspan="4" class="text-center">No Users Found</td>
          </tr>
          <tr v-for="user in user_list" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "AdminDashboard",
  data() {
    return {
      user_list: [],
      user_request_list: [],
    };
  },
  mounted() {
    this.getUsers();
    this.getRequestUsers();
  },
  methods: {
    getUsers() {
      const token = localStorage.getItem('token');
      axios.get('http://localhost:5000/admin/users', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        this.user_list = response.data;
      })
      .catch((error) => {
        console.error(error);
        alert('An error occurred while fetching users.');
      });
    },
    getRequestUsers() {
      const token = localStorage.getItem('token');
      axios.get('http://localhost:5000/admin/users/request', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((response) => {
        this.user_request_list = response.data;
      })
      .catch((error) => {
        console.error(error);
        alert('An error occurred while fetching user requests.');
      });
    },
    approve(userId) {
      const token = localStorage.getItem('token');
      axios.patch(
        'http://localhost:5000/user/approved',
        { user_id: userId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((response) => {
        console.log(response.data); // If you intend to use the response data
        this.user_list = response.data;
        this.$router.replace('/Adashboard');
      })
      .catch((error) => {
        console.error(error);
        alert('An error occurred while approving the user.');
      });
    },

    reject(userId) {
      const token = localStorage.getItem('token');
      axios.patch(
        'http://localhost:5000/user/reject',
        { user_id: userId },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((response) => {
        console.log(response.data); 
        this.$router.replace('/Adashboard');// If you intend to use the response data
 
      })
      .catch((error) => {
        console.error(error);
        alert('An error occurred while rejecting the user.');
      });
    },

    reloadPage() {
      setTimeout(() => {
        window.location.reload();
      }, 500);
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

<style scoped>
body {
  background-color: #f4f4f4;
}

.admin-dashboard {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
  
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  
}

h1 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #0c1101;
}

h2 {
  font-size: 24px;
  margin-bottom: 15px;
  color: #02080f;
}

.navbar {
  background-color: #343a40;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 20px;
}

.navbar a {
  color: #0f0d0d;
  text-decoration: none;
  margin-right: 15px;
}

.navbar .navbar-brand {
  font-size: 20px;
  text-decoration: underline;
  
  
}
.navbar .navbar-brand-admin {
  color: #d56f0a;
  font-size: 20px;
}

.navbar .btn-outline-danger {
  font-size: 16px;
}

.table {
  width: 100%;
  margin-bottom: 20px;
  border-collapse: collapse;
  background-color: #f8f9fa;
}

.table th,
.table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: left;
}

.table th {
  background-color: #f594c0;
  color: white;
  font-weight: bold;
}

.table td {
  background-color: #ffffff;
}

.table .btn {
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.table .btn-success {
  background-color: #28a745;
  color: white;
}

.table .btn-danger {
  background-color: #dc3545;
  color: white;
}

.table .btn:hover {
  opacity: 0.8;
}

.request-section, .user-list-section {
  margin-top: 30px;
}

.request-section .table {
  margin-bottom: 0;
}

.request-section .table td, .request-section .table th {
  padding: 12px;
}

.success-message {
  color: green;
  margin-top: 10px;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>
