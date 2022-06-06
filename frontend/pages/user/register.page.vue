<template>
  <FormKit type="form" id="register" v-model="formData" form-class="mx-auto short-form" @submit="doNothing"
           :errors="errors" :actions="false">
    <FormKit type="text" name="email" label="Email" validation="required" />

    <FormKit type="password" name="password" label="Password" validation="required" />
    <FormKit type="password" name="password_confirm" label="Confirm Password" validation="required|confirm"
             validation-label="Password" />

    <FormKit type="text" name="name" label="Name" validation="required" />

    <CountrySelect name="country" label="Country" v-model="formData.country"/>
    <div class="form-row-custom">
      <div class="form-row-inputs">
        <FormKit type="submit" @click="registerManager">Register as manager</FormKit>
        <FormKit type="submit" @click="registerResearcher">Register as researcher</FormKit>
      </div>
      <help>If you're not sure, register as a researcher.</help>
    </div>
  </FormKit>

  <div class="text-center mt-8">Already have an account? <a href="/user/login">Log in here</a>.</div>
</template>

<script setup>
import { ref } from 'vue';
import { navigate } from 'vite-plugin-ssr/client/router';
import { useEnumStore } from '../../store/enums';
import { useAuthStore } from '../../store/auth';
import CountrySelect from '../../components/CountrySelect.vue'

const enums = useEnumStore();
const auth = useAuthStore();

let errors = ref([]);
const formData = ref({});

function doNothing() {
  // literally do nothing
}

async function submitHandler() {
  return auth.register(formData)
      .then(r => {
        if (r.status >= 400) {
          errors.value = r.data.errors;
          return false;
        } else {
          return true;
        }
      });
}

async function registerResearcher() {
  formData.value['role'] = 'researcher';
  submitHandler().then(success => {
    if (success) {
      navigate('/researcher/register')
    }
  });
}

async function registerManager() {
  formData.value['role'] = 'manager';
  submitHandler().then(success => {
    if (success) {
      navigate('/manager/register')
    }
  });
}

</script>

<style scoped>

</style>
