import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config';
import Material from '@primeuix/themes/material';

import App from './App.vue'
import router from './router/index'

// Components
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import InputNumber from 'primevue/inputnumber';
import Password from 'primevue/password';
import Dropdown from 'primevue/dropdown';
import MultiSelect from 'primevue/multiselect';
import Checkbox from 'primevue/checkbox';
import RadioButton from 'primevue/radiobutton';
import InputSwitch from 'primevue/inputswitch';
import Calendar from 'primevue/calendar';
import Dialog from 'primevue/dialog';
import Sidebar from 'primevue/sidebar';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Tooltip from 'primevue/tooltip';
import ToastService from 'primevue/toastservice';
import ConfirmationService from 'primevue/confirmationservice';

const app = createApp(App)

app.component('Textarea', Textarea);
app.component('Button', Button);
app.component('InputText', InputText);
app.component('Textarea', Textarea);
app.component('InputNumber', InputNumber);
app.component('Password', Password);
app.component('Dropdown', Dropdown);
app.component('MultiSelect', MultiSelect);
app.component('Checkbox', Checkbox);
app.component('RadioButton', RadioButton);
app.component('InputSwitch', InputSwitch);
app.component('Calendar', Calendar);
app.component('Dialog', Dialog);
app.component('Sidebar', Sidebar);
app.component('Toast', Toast);
app.component('ConfirmDialog', ConfirmDialog);
app.component('DataTable', DataTable);
app.component('Column', Column);

app.directive('tooltip', Tooltip);


app.use(createPinia());
app.use(PrimeVue, { theme: { preset: Material } });
app.use(ToastService);
app.use(ConfirmationService);
app.use(router)

app.mount('#app')
