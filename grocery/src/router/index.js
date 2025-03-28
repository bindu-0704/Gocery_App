import Vue from 'vue'
import VueRouter from 'vue-router'
import HomePage from '../components/HomePage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import LoginPage from '../components/LoginPage.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import UserDashboard from '../components/UserDashboard.vue';
import UserCart from '../components/UserCart.vue';
import UserOrder from '../components/UserOrder.vue';
import ACategory from '../components/ACategory.vue';
import AProduct from '../components/AProduct.vue';
import MProduct from '../components/MProduct.vue';
import AUpdateCategory from '../components/AUpdateCategory.vue';
import ManagerDashboard from '../components/ManagerDashboard.vue';
import MUpdateProduct from '../components/MUpdateProduct.vue';
import ACreateCategory from '../components/ACreateCategory.vue'
import MCategory from '../components/MCategory.vue';
import MEditCategory from '../components/MEditCategory.vue';
import MAddCategory from '../components/MAddCategory.vue';
import MViewProduct from '../components/MViewProduct.vue';
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage,
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
  },
  {
    path: '/Adashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
  },
  {
    path: '/acreatecategory',
    name: 'ACreateCategory',
    component: ACreateCategory ,
  },
  {
    path: '/user/products',
    name: 'UserDashboard',
    component: UserDashboard,
  },
  {
    path: '/user/cart',
    name: 'UserCart',
    component: UserCart,
  },
  {
    path: '/user/orders',
    name: 'UserOrder',
    component: UserOrder,
  },
  {
    path: '/categories',
    name: 'ACategory',
    component: ACategory,
  },
  {
    path: '/product',
    name: 'ManagerDashboard',
    component: ManagerDashboard,
  },
  {
    path: '/admin/products/:categoryId',
    name: 'AProduct',
    component: AProduct,
  },
  {
    path: '/mproduct',
    name: 'MProduct',
    component: MProduct,
  },
  {
    path: '/mcategory',
    name: 'MCategory',
    component: MCategory,
  },
  {
    path: '/manager/products/:categoryId',
    name: 'MViewProduct',
    component: MViewProduct,
  },
  {
    path: '/manager/add_category',
    name: 'MAddCategorhy',
    component: MAddCategory,
  },
  {
    path: '/manager/edit_category/:id',
    name: 'MEditCategory',
    component: MEditCategory,
  },
  {
    path: '/categories/edit/:id',
    name: 'AUpdateCategory',
    component: AUpdateCategory,
  },
  {
    path: '/manager/edit_products/:id',
    name: 'MUpdateProduct',
    component: MUpdateProduct,
  },

  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
