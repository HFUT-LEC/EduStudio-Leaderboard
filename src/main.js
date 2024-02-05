import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap';
import 'mdb-vue-ui-kit/css/mdb.min.css';

createApp(App).use(router).use(store).mount('#app')

