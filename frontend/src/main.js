import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/index'
import ElementPlus from 'element-plus'
import VxeUITable from 'vxe-table'
import 'vxe-table/lib/style.css'
// import './assets/materialdesignicons.min.css'
// import './assets/vendor.bundle.base.css'
import './assets/login_style.css'
import "element-plus/dist/index.css";



const app = createApp(App);

app.use(router);
app.use(ElementPlus);
//app.use(Toast, options); // 可以自定义选项
app.use(store);
app.use(VxeUITable);
app.mount("#app");

// createApp(App).use(router).mount('#app')
import axios from 'axios';

// 设置后端服务器的基准 URL
axios.defaults.baseURL = 'http://127.0.0.1:5000';